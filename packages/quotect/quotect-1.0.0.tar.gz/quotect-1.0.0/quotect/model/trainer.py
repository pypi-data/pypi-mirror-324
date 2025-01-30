from transformers import Seq2SeqTrainer
import os
import json
import re
import torch.nn as nn
from collections import defaultdict
from typing import Dict, Union, Any, Optional, Tuple, List
import torch
from torch.utils.data import DataLoader
from transformers.trainer_utils import EvalLoopOutput
from quotect.data.data import parse_int_output_tokens, parse_short_target_tokens
from quotect.common.constants import SPECIAL_IDS, MARK_SPECIAL_IDS
from quotect.data.eval_quotes import evaluate
from quotect.data.convert_quotes import convert_to_quote_json

from transformers.utils import logging


from transformers import LogitsProcessorList
from quotect.model import ShortSeqProcessor, IntProcessor
from transformers.trainer_seq2seq import is_deepspeed_zero3_enabled

logger = logging.get_logger(__name__)
TRAINING_ARGS_NAME = "training_args.bin"
TRAINER_STATE_NAME = "trainer_state.json"
OPTIMIZER_NAME = "optimizer.pt"
SCHEDULER_NAME = "scheduler.pt"
SCALER_NAME = "scaler.pt"


class QuoteTrainer(Seq2SeqTrainer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, compute_metrics=self.compute_metrics)

    def compute_metrics(self, pred: Any) -> Dict:
        tok = self.processing_class if hasattr(self, "processing_class") else self.tokenizer
        predicts = pred.predictions
        doc_labels, samples, split = self.eval_info
        del self.eval_info
        documents_to_chunk_data = defaultdict(list)
        documents_to_chunk_gold = defaultdict(list)
        predictions = {}
        golds = {}
        assert len(samples) <= len(
            predicts
        )  # with batching and multi-GPU predicts may be longer
        out_sents = []
        last_doc_id = re.sub(r"_\d+$", "", samples[0]["doc_key"])
        for sample, predict in zip(samples, predicts):
            doc_key = sample["doc_key"]
            doc_id = re.sub(r"_\d+$", "", doc_key)
            # require convert to ids first
            input_ids = sample["sentence"]
            subtoken_map = sample["subtoken_map"]
            offset = sample["offset"]
            # remove bos
            predict_ids = predict[1:].tolist()
            gold_data = sample["seg_clusters"]
            if self.args.seq2seq_type == "short_seq":
                special_ids = (
                    MARK_SPECIAL_IDS if self.args.mark_sentence else SPECIAL_IDS
                )
                pred_data, aligned_input_ids, aligned_pred_ids = (
                    parse_short_target_tokens(
                        input_ids,
                        predict_ids,
                        special_ids,
                        subtoken_map,
                        tok,
                        self.args.align_mode,
                        self.args.mark_sentence,
                    )
                )
                predict_ids = [
                    t for t in predict_ids if t != tok.pad_token_id
                ]
                pred_tokens = tok.convert_ids_to_tokens(predict_ids)
                out_predict = {
                    "doc_key": doc_key,
                    "pred_tokens": pred_tokens,
                    "pred_text": tok.convert_tokens_to_string(pred_tokens),
                    "pred_aligned_text": tok.convert_ids_to_tokens(
                        aligned_pred_ids
                    ),
                    "predict_clusters": pred_data,
                    "gold_clusters": gold_data,
                    "input_aligned_text": tok.convert_ids_to_tokens(
                        aligned_input_ids
                    ),
                }
            else:
                pred_data, pred_token_mentions, predict_ids = parse_int_output_tokens(
                    input_ids, predict_ids, SPECIAL_IDS, subtoken_map, tok
                )
                pred_token_mentions = [
                    (m[0] + offset, m[1] + offset) for m in pred_token_mentions
                ]
                predict_ids = [
                    t for t in predict_ids if t != tok.pad_token_id
                ]
                pred_tokens = tok.convert_ids_to_tokens(predict_ids)
                out_predict = {
                    "doc_key": doc_key,
                    "pred_tokens": pred_tokens,
                    "pred_text": tok.convert_tokens_to_string(pred_tokens),
                    "predict_clusters": pred_data,
                    "gold_clusters": gold_data,
                    "predict_token_mentions": pred_token_mentions,
                }
            # list of (m1,m2)

            documents_to_chunk_data[doc_id].extend(pred_data)
            documents_to_chunk_gold[doc_id].extend(gold_data)

            out_sents.append(out_predict)
            if doc_id != last_doc_id:
                predictions[last_doc_id] = documents_to_chunk_data[last_doc_id]
                golds[last_doc_id] = documents_to_chunk_gold[last_doc_id]
            last_doc_id = doc_id
        # final one
        predictions[last_doc_id] = documents_to_chunk_data[last_doc_id]

        golds[last_doc_id] = documents_to_chunk_gold[last_doc_id]

        predictions_list = []
        labels_list = []
        golds_list = []

        for document_id, doc_label in doc_labels.items():
            predictions_list.append(predictions[document_id])
            labels_list.append(doc_label)
            golds_list.append(golds[document_id])
        if self.eval_dataset is None:
            return predictions

        quote_gold_path = (
            f"{self.eval_dataset.data_args.original_input_dir}/{split}.jsonlines"
        )
        quote_predictions = convert_to_quote_json(
            quote_gold_path,
            predictions,
            self.args.seq2seq_type == "short_seq" and self.args.mark_sentence,
        )

        quote_metrics = evaluate(quote_predictions, quote_gold_path)
        quote_results = {f"quote_{k}": v for k, v in quote_metrics.items()}

        results = {**quote_results}
        if self.is_world_process_zero() and self.args.save_predicts:
            os.makedirs(self.args.save_dir, exist_ok=True)
            save_path = os.path.join(self.args.save_dir, f"{split}-predicts.jsonlines")
            results_path = os.path.join(self.args.save_dir, f"{split}-results.json")
            quote_path = os.path.join(self.args.save_dir, f"{split}-quote.jsonlines")
            with open(save_path, "w", encoding="utf-8") as f:
                for p in out_sents:
                    json.dump(p, f, ensure_ascii=False)
                    # f.write(json.dumps(p, ensure_ascii=False))
                    f.write("\n")
            with open(results_path, "w") as f:
                json.dump(results, f, ensure_ascii=False)
            with open(quote_path, "w") as f:
                for quote in quote_predictions:
                    json.dump(quote, f, ensure_ascii=False)
                    f.write("\n")
        return results

    def evaluation_loop(
        self,
        dataloader: DataLoader,
        description: str,
        prediction_loss_only: Optional[bool] = False,
        ignore_keys: Optional[List[str]] = None,
        metric_key_prefix: str = "eval",
    ) -> EvalLoopOutput:
        eval_dataset = getattr(dataloader, "dataset", None)
        if hasattr(self, "eval_info"):
            raise ValueError("eval_info must not be present!")
        self.eval_info = (
            eval_dataset.doc_labels,
            eval_dataset.samples,
            eval_dataset.split,
        )

        return super().evaluation_loop(
            dataloader,
            description,
            prediction_loss_only,
            ignore_keys,
            metric_key_prefix,
        )

    def prediction_step(
        self,
        model: nn.Module,
        inputs: Dict[str, Union[torch.Tensor, Any]],
        prediction_loss_only: bool,
        ignore_keys: Optional[List[str]] = None,
    ) -> Tuple[Optional[float], Optional[torch.Tensor], Optional[torch.Tensor]]:
        """
        Perform an evaluation step on `model` using `inputs`.

        Subclass and override to inject custom behavior.

        Args:
            model (`nn.Module`):
                The model to evaluate.
            inputs (`Dict[str, Union[torch.Tensor, Any]]`):
                The inputs and targets of the model.

                The dictionary will be unpacked before being fed to the model. Most models expect the targets under the
                argument `labels`. Check your model's documentation for all accepted arguments.
            prediction_loss_only (`bool`):
                Whether or not to return the loss only.
            ignore_keys:
                list of ignore keys

        Return:
            Tuple[Optional[float], Optional[torch.Tensor], Optional[torch.Tensor]]: A tuple with the loss, logits and
            labels (each being optional).
        """

        if not self.args.predict_with_generate or prediction_loss_only:
            return super().prediction_step(
                model,
                inputs,
                prediction_loss_only=prediction_loss_only,
                ignore_keys=ignore_keys,
            )
        has_labels = "labels" in inputs
        inputs = self._prepare_inputs(inputs)

        # XXX: adapt synced_gpus for fairscale as well
        gen_kwargs = self._gen_kwargs.copy()
        gen_kwargs["max_length"] = (
            gen_kwargs["max_length"]
            if gen_kwargs.get("max_length") is not None
            else self.model.config.max_length
        )
        gen_kwargs["num_beams"] = (
            gen_kwargs["num_beams"]
            if gen_kwargs.get("num_beams") is not None
            else self.model.config.num_beams
        )
        default_synced_gpus = True if is_deepspeed_zero3_enabled() else False
        gen_kwargs["synced_gpus"] = (
            gen_kwargs["synced_gpus"]
            if gen_kwargs.get("synced_gpus") is not None
            else default_synced_gpus
        )

        if "attention_mask" in inputs:
            gen_kwargs["attention_mask"] = inputs.get("attention_mask", None)
        if "global_attention_mask" in inputs:
            gen_kwargs["global_attention_mask"] = inputs.get(
                "global_attention_mask", None
            )

        # prepare generation inputs
        # some encoder-decoder models can have varying encoder's and thus
        # varying model input names
        if (
            hasattr(self.model, "encoder")
            and self.model.encoder.main_input_name != self.model.main_input_name
        ):
            generation_inputs = inputs[self.model.encoder.main_input_name]
        else:
            generation_inputs = inputs[self.model.main_input_name]
        #  add our logits_processor here
        if self.args.seq2seq_type != "short_seq":
            gen_kwargs["logits_processor"] = LogitsProcessorList(
                [IntProcessor(generation_inputs, SPECIAL_IDS, self.args.seq2seq_type)]
            )
        elif self.args.mark_sentence:
            gen_kwargs["logits_processor"] = LogitsProcessorList(
                [ShortSeqProcessor(generation_inputs, MARK_SPECIAL_IDS)]
            )

        generated_tokens = self.model.generate(
            generation_inputs,
            **gen_kwargs,
        )
        # in case the batch is shorter than max length, the output should be padded
        if generated_tokens.shape[-1] < gen_kwargs["max_length"]:
            generated_tokens = self._pad_tensors_to_max_len(
                generated_tokens, gen_kwargs["max_length"]
            )

        with torch.no_grad():
            with self.compute_loss_context_manager():
                outputs = model(**inputs)
            if has_labels:
                if self.label_smoother is not None:
                    loss = (
                        self.label_smoother(outputs, inputs["labels"]).mean().detach()
                    )
                else:
                    loss = (
                        (outputs["loss"] if isinstance(outputs, dict) else outputs[0])
                        .mean()
                        .detach()
                    )
            else:
                loss = None

        if self.args.prediction_loss_only:
            return (loss, None, None)

        if has_labels:
            labels = inputs["labels"]
            if labels.shape[-1] < gen_kwargs["max_length"]:
                labels = self._pad_tensors_to_max_len(labels, gen_kwargs["max_length"])
        else:
            labels = None

        return (loss, generated_tokens, labels)
