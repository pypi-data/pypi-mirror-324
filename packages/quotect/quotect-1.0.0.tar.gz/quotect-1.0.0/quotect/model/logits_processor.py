from transformers import LogitsProcessor
import torch


class ShortSeqProcessor(LogitsProcessor):
    def __init__(self, orig_inputs: torch.Tensor, special_ids):
        self.orig_inputs = orig_inputs
        special_starts = [
            v
            for k, v in special_ids.items()
            if k.endswith("_start") and not k.startswith("sentence")
        ]
        special_ends = [
            v
            for k, v in special_ids.items()
            if k.endswith("_end") and not k.startswith("sentence")
        ]
        self.special_starts = torch.tensor(special_starts, device=orig_inputs.device)
        self.special_ends = torch.tensor(special_ends, device=orig_inputs.device)
        self.sentence_start = special_ids["sentence_start"]
        self.sentence_end = special_ids["sentence_end"]
        self.sep = special_ids["sep"]
        ent_ids = special_ids["integers"]
        self.ent_ids = torch.tensor(ent_ids, device=orig_inputs.device)
        self.eos_id = special_ids["eos"]
        self.sentence_mask = self.get_sentence_mask(orig_inputs)

    def get_sentence_mask(self, orig_inputs: torch.Tensor):
        # index from 1 instead of 0
        return (orig_inputs == self.sentence_start).cumsum(-1)

    def __call__(
        self, input_ids: torch.LongTensor, scores: torch.FloatTensor
    ) -> torch.FloatTensor:
        is_sent_start = input_ids == self.sentence_start
        is_sent_end = input_ids == self.sentence_end
        sent_idx = is_sent_start.sum(-1, keepdim=True)
        unclose_sent = (sent_idx.sum(-1) - is_sent_end.sum(-1)) > 0
        close_sent = ~unclose_sent
        is_sep = input_ids == self.sep
        is_end = torch.isin(input_ids, self.special_ends)
        is_start = torch.isin(input_ids, self.special_starts)
        is_ent = (is_sep.cumsum(-1) - is_end.cumsum(-1)).bool()
        unclose_ent = is_ent[:, -1] & unclose_sent
        unclose_ment = (is_start.sum(-1) - is_sep.sum(-1)) > 0
        close_ent = ~unclose_ent
        unclose_ment = close_ent & unclose_ment & unclose_sent
        masks = torch.ones_like(scores, dtype=torch.bool)
        masks[unclose_sent, self.sentence_end] = False
        masks[close_sent, self.sentence_start] = False
        assert scores.size(0) % self.orig_inputs.size(0) == 0
        num_beams = scores.size(0) // self.orig_inputs.size(0)
        # repeat over beams
        orig_ids = self.orig_inputs.repeat_interleave(num_beams, 0)
        sent_mask = self.sentence_mask.repeat_interleave(num_beams, 0)
        cur_sent_mask = sent_mask != sent_idx
        sent_ids = orig_ids.masked_fill(cur_sent_mask, self.sentence_end)
        masks[unclose_sent] = masks[unclose_sent].scatter(
            1, sent_ids[unclose_sent], False
        )
        masks[unclose_sent, self.sentence_start] = True
        masks[unclose_ent, self.ent_ids.unsqueeze(1)] = False

        if input_ids.shape[1] > 1:
            specials = (
                input_ids.unsqueeze(1) == self.special_starts.unsqueeze(1)
            ).cumsum(-1) - (
                input_ids.unsqueeze(1) == self.special_ends.unsqueeze(1)
            ).cumsum(-1)
            m = specials > specials[:, :, -1].unsqueeze(-1)
            replacement = (
                specials[:, :, -1]
                .unsqueeze(-1)
                .expand(
                    input_ids.shape[0], self.special_ends.shape[0], input_ids.shape[1]
                )
            )
            specials[m] = replacement[m]

            specials_diff = (specials[:, :, 1:] - specials[:, :, :-1]) * torch.arange(
                2, input_ids.shape[1] + 1, device=specials.device
            )
            specials_diff[specials[:, :, -1] == 0, :] = 0
            candidates = specials_diff.max(dim=2).values.argmax(dim=1)
            masks[
                torch.arange(scores.size(0), device=candidates.device)[unclose_ent],
                self.special_ends[candidates[unclose_ent]],
            ] = False

        masks[close_ent, self.special_starts.unsqueeze(1)] = False
        masks[unclose_ment, self.sep] = False
        is_eos = close_sent & (sent_idx.sum(-1) == sent_mask[:, -1])
        masks[is_eos] = True
        masks[is_eos, self.eos_id] = False
        scores.masked_fill_(masks, -float("inf"))
        return scores


class IntProcessor(LogitsProcessor):
    def __init__(self, orig_inputs, special_ids, seq2seq_type):
        """

        :param orig_inputs: original input_ids
        :param special_ids: dict with keys:[special_starts, special_ends, sep,
        integers]
        """
        self.orig_inputs = orig_inputs
        self.seq2seq_type = seq2seq_type
        self.special_ids = special_ids
        special_starts = [
            v
            for k, v in special_ids.items()
            if k.endswith("_start") and not k.startswith("sentence")
        ]
        special_ends = [
            v
            for k, v in special_ids.items()
            if k.endswith("_end") and not k.startswith("sentence")
        ]
        self.special_starts = torch.tensor(special_starts, device=orig_inputs.device)
        self.special_ends = torch.tensor(special_ends, device=orig_inputs.device)
        self.sep = special_ids["sep"]
        ent_ids = special_ids["integers"]
        self.ent_ids = torch.tensor(ent_ids, device=orig_inputs.device)
        specials = special_starts + [self.sep] + ent_ids + special_ends
        if self.seq2seq_type == "action":
            self.copy_id = special_ids["copy"]
            specials.append(self.copy_id)
        self.specials = torch.tensor(specials, device=orig_inputs.device)
        self.eos_id = special_ids["eos"]

    def __call__(
        self, input_ids: torch.LongTensor, scores: torch.FloatTensor
    ) -> torch.FloatTensor:
        """

        :param input_ids: BC x l
        :param scores:  BC x V
        :return:
        """
        # input_ids : B x L
        is_sep = input_ids == self.sep
        is_end = torch.isin(input_ids, self.special_ends)
        is_start = torch.isin(input_ids, self.special_starts)
        is_ent = (is_sep.cumsum(-1) - is_end.cumsum(-1)).bool()
        is_copy = (~is_start) & (~is_ent) & (~is_end)
        unclose_ent = is_ent[:, -1]
        unclose_ment = (is_start.sum(-1) - is_sep.sum(-1)) > 0
        unclose_ment = (~unclose_ent) & unclose_ment
        # -1 for <pad> at begining
        num_copied = is_copy.sum(-1) - 1
        masks = torch.ones_like(scores, dtype=torch.bool)
        close_ent = ~unclose_ent
        num_copied = num_copied.clamp(max=self.orig_inputs.size(1) - 1)
        # unclosed ent allows to generate cluster ids
        masks[unclose_ent, self.ent_ids.unsqueeze(1)] = False

        if input_ids.shape[1] > 1:
            specials = (
                input_ids.unsqueeze(1) == self.special_starts.unsqueeze(1)
            ).cumsum(-1) - (
                input_ids.unsqueeze(1) == self.special_ends.unsqueeze(1)
            ).cumsum(-1)
            m = specials > specials[:, :, -1].unsqueeze(-1)
            replacement = (
                specials[:, :, -1]
                .unsqueeze(-1)
                .expand(
                    input_ids.shape[0], self.special_ends.shape[0], input_ids.shape[1]
                )
            )
            specials[m] = replacement[m]

            specials_diff = (specials[:, :, 1:] - specials[:, :, :-1]) * torch.arange(
                2, input_ids.shape[1] + 1, device=specials.device
            )
            specials_diff[specials[:, :, -1] == 0, :] = 0
            candidates = specials_diff.max(dim=2).values.argmax(dim=1)
            masks[
                torch.arange(scores.size(0), device=candidates.device)[unclose_ent],
                self.special_ends[candidates[unclose_ent]],
            ] = False

        masks[close_ent, self.special_starts.unsqueeze(1)] = False
        masks[unclose_ment, self.sep] = False
        # get next copy id
        assert scores.size(0) % self.orig_inputs.size(0) == 0
        num_beams = scores.size(0) // self.orig_inputs.size(0)
        # repeat over beams
        orig_ids = self.orig_inputs.repeat_interleave(num_beams, 0)
        next_ids = orig_ids[torch.arange(scores.size(0)), num_copied]
        if self.seq2seq_type == "action":
            scores[close_ent, next_ids[close_ent]] = scores[close_ent, self.copy_id]
        masks[close_ent, next_ids[close_ent]] = False
        is_eos = close_ent & (next_ids == self.eos_id)
        masks[is_eos, self.specials.unsqueeze(1)] = True
        masks[is_eos, self.eos_id] = False

        scores.masked_fill_(masks, -float("inf"))
        return scores
