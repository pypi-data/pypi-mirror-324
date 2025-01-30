from torch.utils.data import Dataset
from collections import defaultdict
import re
import torch
from dataclasses import dataclass
from typing import Any, Optional, Union
from transformers.tokenization_utils_base import PreTrainedTokenizerBase
from transformers.utils import PaddingStrategy

from quotect.utils.alignment import global_align, affine_global_align
from quotect.utils.helper import split_list


class QuoteDataset(Dataset):
    def __init__(self, tokenizer, input_documents, split="predict"):
        self.tokenizer = tokenizer
        self.split = split
        # convert tokens to ids for each sample
        self.samples, self.doc_labels = self.load_dataset(input_documents)

    def __len__(self):
        return len(self.samples)

    def load_dataset(self, input_documents):
        samples = []
        doc_labels = {}
        for item in input_documents:
            target_sent = self.tokenizer.convert_tokens_to_ids(item["target_sentence"])
            target_seq = self.tokenizer.convert_tokens_to_ids(
                item["target_short_sentence"]
            )
            sample = {
                "sentence": self.tokenizer.convert_tokens_to_ids(item["sentence"]),
                "target_sentence": target_sent,
                "target_seq": target_seq,
                "subtoken_map": item["subtoken_map"],
                "seg_clusters": [[tuple(m) for m in c] for c in item["seg_clusters"]],
                "offset": item["offset"],
                "doc_key": item["doc_key"],
            }
            doc_id = re.sub(r"_\d+$", "", item["doc_key"])
            doc_labels[doc_id] = [[tuple(m) for m in c] for c in item["gold_clusters"]]
            samples.append(sample)
        return samples, doc_labels

    def __getitem__(self, index):
        sample = self.samples[index]
        input_ids = torch.tensor(sample["sentence"], dtype=torch.long)
        label_ids = torch.tensor(sample["target_seq"], dtype=torch.long)
        attention_mask = torch.ones((len(input_ids)), dtype=torch.long)
        src_encoding = {
            "input_ids": input_ids,
            "attention_mask": attention_mask,
            "labels": label_ids,
        }
        return src_encoding


def parse_int_output_tokens(
    input_ids, output_ids, special_ids, subtoken_map, tokenizer
):
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
    rec_ids, new_id = [], -1
    ment_start_stack = []
    unmatched_clusters = defaultdict(list)
    new_output_ids = []

    new_input_ids = [t for t in input_ids if t != tokenizer.pad_token_id]
    token_mentions = []
    pred_tokens = tokenizer.convert_ids_to_tokens(output_ids)
    global wrong_matches
    global correct_matches

    for i in range(len(output_ids)):
        if output_ids[i] == tokenizer.pad_token_id:
            break
        if output_ids[i] in special_starts:
            index = special_starts.index(output_ids[i])
            new_id += 1
            ment_start_stack.append([new_id, "name", [], index, pred_tokens[i]])
        elif output_ids[i] in special_ends:
            index = special_ends.index(output_ids[i])
            new_id += 0
            if len(ment_start_stack) > 0:
                item = ment_start_stack.pop()
                if index != item[3]:
                    wrong_matches += 1
                if item[1] == "ent" and index == item[3]:
                    correct_matches += 1
                    unmatched_clusters[tuple(item[2])].append((item[0], new_id, index))
        else:
            # a normal token
            # if output_ids[i] == special_ids['sep']:
            #     status = "ent"
            if len(ment_start_stack) > 0:
                # inside some entities
                if output_ids[i] == special_ids["sep"]:
                    ment_start_stack[-1][1] = "ent"
                else:
                    if ment_start_stack[-1][1] == "ent":
                        ment_start_stack[-1][2].append(output_ids[i])
                    elif ment_start_stack[-1][1] == "name":
                        new_id += 1
                        rec_ids.append(output_ids[i])
                    else:
                        raise ValueError("wrong status")
            else:
                # outside
                new_id += 1
                rec_ids.append(output_ids[i])
        if output_ids[i] in special_starts:
            new_id -= 1
    # Needleman-Wunsch text alignment algorithm
    wrong_reconstruction = rec_ids != new_input_ids
    if wrong_reconstruction:
        print("wrong reconstruction! please debug parse_int_output_tokens")
        matching = global_align(new_input_ids, rec_ids)

        # update predicted entities with the positions in the original sentence
        clusters = defaultdict(list)

        for ent_id, ments in unmatched_clusters.items():
            for start, end, part in ments:
                new_start = None  # start in the original sequence
                new_end = None  # end in the original sequence

                for j in range(start, end + 1):
                    if j in matching:
                        if new_start is None:
                            new_start = matching[j]

                        new_end = matching[j]

                if new_start is not None:
                    # predict entity
                    clusters[ent_id].append(
                        (subtoken_map[new_start], subtoken_map[new_end], part)
                    )
                    token_mentions.append((new_start, new_end, part))
        token_mentions = list(set(token_mentions))
    else:
        clusters = [
            [(subtoken_map[m[0]], subtoken_map[m[1]], m[2]) for m in v]
            for v in unmatched_clusters.values()
        ]

        token_mentions = [
            (m[0], m[1], m[2]) for v in unmatched_clusters.values() for m in v
        ]
        token_mentions = list(set(token_mentions))
    new_output_ids = output_ids
    predict_clusters = [list(set(v)) for k, v in clusters.items()]
    return predict_clusters, token_mentions, new_output_ids


def parse_short_target_tokens(
    input_ids,
    output_ids,
    special_ids,
    subtoken_map,
    tokenizer,
    align_mode,
    split_sentence,
):
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
    rec_ids, new_id = [], -1
    ment_start_stack = []
    unmatched_clusters = defaultdict(list)
    new_input_ids = [t for t in input_ids if t != tokenizer.pad_token_id]
    for i in range(len(output_ids)):
        if output_ids[i] == tokenizer.pad_token_id:
            break
        if output_ids[i] in special_starts:
            index = special_starts.index(output_ids[i])
            ment_start_stack.append([new_id + 1, "name", [], index])
        elif output_ids[i] in special_ends:
            index = special_ends.index(output_ids[i])
            if len(ment_start_stack) > 0:
                item = ment_start_stack.pop()
                if item[1] == "ent" and index == item[3]:
                    unmatched_clusters[tuple(item[2])].append((item[0], new_id, index))
        else:
            # a normal token
            if len(ment_start_stack) > 0:
                # inside some entities
                if output_ids[i] == special_ids["sep"]:
                    ment_start_stack[-1][1] = "ent"
                else:
                    if ment_start_stack[-1][1] == "ent":
                        ment_start_stack[-1][2].append(output_ids[i])
                    elif ment_start_stack[-1][1] == "name":
                        new_id += 1
                        rec_ids.append(output_ids[i])
                    else:
                        raise ValueError("wrong status")

            else:
                # outside
                new_id += 1
                rec_ids.append(output_ids[i])
    # Affine global text alignment algorithm
    if split_sentence:
        input_sents = split_list(new_input_ids, special_ids["sentence_start"], True)
        out_sents = split_list(rec_ids, special_ids["sentence_start"], True)
        try:
            assert len(input_sents) == len(out_sents)
            aligned_input_ids, aligned_rec_ids, matching = [], [], {}
            input_offset, out_offset = 0, 0
            for input_sent, out_sent in zip(input_sents, out_sents):
                aligned_input_sent, aligned_out_sent, sent_match = affine_global_align(
                    input_sent, out_sent, special_ids["copy"], align_mode
                )
                aligned_input_ids.extend(aligned_input_sent)
                aligned_rec_ids.extend(aligned_out_sent)
                matching.update(
                    {k + out_offset: v + input_offset for k, v in sent_match.items()}
                )
                input_offset += len(input_sent)
                out_offset += len(out_sent)
        except AssertionError:
            print(
                f"input sents and out sents different length "
                f"{len(input_sents)} vs {len(out_sents)}, have to use "
                f"global alignment"
            )
            aligned_input_ids, aligned_rec_ids, matching = affine_global_align(
                new_input_ids, rec_ids, special_ids["copy"], align_mode
            )
    else:
        aligned_input_ids, aligned_rec_ids, matching = affine_global_align(
            new_input_ids, rec_ids, special_ids["copy"], align_mode
        )
    # update predicted entities with the positions in the original sentence
    clusters = defaultdict(list)

    for ent_id, ments in unmatched_clusters.items():
        for start, end, part in ments:
            new_start = None  # start in the original sequence
            new_end = None  # end in the original sequence

            for j in range(start, end + 1):
                if j in matching:
                    if new_start is None:
                        new_start = matching[j]

                    new_end = matching[j]

            if new_start is not None:
                # predict entity
                clusters[ent_id].append(
                    (subtoken_map[new_start], subtoken_map[new_end], part)
                )
    predict_clusters = [list(set(v)) for k, v in clusters.items()]
    return predict_clusters, aligned_input_ids, aligned_rec_ids


@dataclass
class ConstrainedDataCollator:
    """
    Data collator that will dynamically pad the inputs received, as well as the labels.

    Args:
        tokenizer ([`PreTrainedTokenizer`] or [`PreTrainedTokenizerFast`]):
            The tokenizer used for encoding the data.
        model ([`PreTrainedModel`]):
            The model that is being trained. If set and has the *prepare_decoder_input_ids_from_labels*, use it to
            prepare the *decoder_input_ids*

            This is useful when using *label_smoothing* to avoid calculating loss twice.
        padding (`bool`, `str` or [`~utils.PaddingStrategy`], *optional*, defaults to `True`):
            Select a strategy to pad the returned sequences (according to the model's padding side and padding index)
            among:

            - `True` or `'longest'`: Pad to the longest sequence in the batch (or no padding if only a single sequence
              is provided).
            - `'max_length'`: Pad to a maximum length specified with the argument `max_length` or to the maximum
              acceptable input length for the model if that argument is not provided.
            - `False` or `'do_not_pad'` (default): No padding (i.e., can output a batch with sequences of different
              lengths).
        max_length (`int`, *optional*):
            Maximum length of the returned list and optionally padding length (see above).
        pad_to_multiple_of (`int`, *optional*):
            If set will pad the sequence to a multiple of the provided value.

            This is especially useful to enable the use of Tensor Cores on NVIDIA hardware with compute capability >=
            7.5 (Volta).
        label_pad_token_id (`int`, *optional*, defaults to -100):
            The id to use when padding the labels (-100 will be automatically ignored by PyTorch loss functions).
        return_tensors (`str`):
            The type of Tensor to return. Allowable values are "np", "pt" and "tf".
    """

    tokenizer: PreTrainedTokenizerBase
    model: Optional[Any] = None
    padding: Union[bool, str, PaddingStrategy] = True
    max_length: Optional[int] = None
    pad_to_multiple_of: Optional[int] = None
    label_pad_token_id: int = -100
    return_tensors: str = "pt"

    def __call__(self, features, return_tensors=None):
        import numpy as np

        if return_tensors is None:
            return_tensors = self.return_tensors
        labels = (
            [feature["labels"] for feature in features]
            if "labels" in features[0].keys()
            else None
        )
        decoder_labels = (
            [feature["decoder_labels"] for feature in features]
            if "decoder_labels" in features[0].keys()
            else None
        )
        # We have to pad the labels before calling `tokenizer.pad` as this method won't pad them and needs them of the
        # same length to return tensors.
        if labels is not None:
            assert decoder_labels is not None
            max_label_length = max(len(label) for label in labels)
            if self.pad_to_multiple_of is not None:
                max_label_length = (
                    (max_label_length + self.pad_to_multiple_of - 1)
                    // self.pad_to_multiple_of
                    * self.pad_to_multiple_of
                )

            padding_side = self.tokenizer.padding_side
            for feature in features:
                remainder = [self.label_pad_token_id] * (
                    max_label_length - len(feature["labels"])
                )
                if isinstance(feature["labels"], list):
                    feature["labels"] = (
                        feature["labels"] + remainder
                        if padding_side == "right"
                        else remainder + feature["labels"]
                    )
                    feature["decoder_labels"] = (
                        feature["decoder_labels"] + remainder
                        if padding_side == "right"
                        else remainder + feature["decoder_labels"]
                    )
                elif padding_side == "right":
                    feature["labels"] = np.concatenate(
                        [feature["labels"], remainder]
                    ).astype(np.int64)
                    feature["decoder_labels"] = np.concatenate(
                        [feature["decoder_labels"], remainder]
                    ).astype(np.int64)
                else:
                    feature["labels"] = np.concatenate(
                        [remainder, feature["labels"]]
                    ).astype(np.int64)
                    feature["decoder_labels"] = np.concatenate(
                        [remainder, feature["decoder_labels"]]
                    ).astype(np.int64)

        features = self.tokenizer.pad(
            features,
            padding=self.padding,
            max_length=self.max_length,
            pad_to_multiple_of=self.pad_to_multiple_of,
            return_tensors=return_tensors,
        )

        # prepare decoder_input_ids
        if (
            labels is not None
            and self.model is not None
            and hasattr(self.model, "prepare_decoder_input_ids_from_labels")
        ):
            decoder_input_ids = self.model.prepare_decoder_input_ids_from_labels(
                labels=features["decoder_labels"]
            )
            features["decoder_input_ids"] = decoder_input_ids
        del features["decoder_labels"]
        return features
