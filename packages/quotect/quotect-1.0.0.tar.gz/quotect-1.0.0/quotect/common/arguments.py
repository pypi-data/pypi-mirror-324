from dataclasses import dataclass, field
from typing import Optional, Union
from transformers import Seq2SeqTrainingArguments
from transformers.trainer import OptimizerNames


@dataclass
class DataArguments:
    original_input_dir: str = field()

    predict_only: bool = field(default=False)

    data_dir: Optional[str] = field(
        default=None, metadata={"help": "Path to data directory"}
    )
    max_eval_len: Optional[int] = field(
        default=1536,
        metadata={"help": "maximum dev/test source input length"},
    )
    max_eval_len_out: Optional[int] = field(
        default=2048,
        metadata={"help": "maximum dev/test target decode length"},
    )
    language: Optional[str] = field(
        default="german", metadata={"help": "text language"}
    )


@dataclass
class QuotectArguments(Seq2SeqTrainingArguments):
    model_name_or_path: str = field(default="fynnos/quotect-mt5-base")

    do_train: bool = field(default=False, metadata={"help": "Whether to run training."})
    save_dir: Optional[str] = field(
        default=None, metadata={"help": "Path to save predicts directory"}
    )
    save_predicts: Optional[bool] = field(
        default=True, metadata={"help": "whether to save predictions"}
    )
    mark_sentence: Optional[bool] = field(
        default=True, metadata={"help": "mark sentence end for short target?"}
    )
    align_mode: Optional[str] = field(
        default="l", metadata={"help": "alignment mode: highroad (h) or lowroad (l) "}
    )
    optim: Union[OptimizerNames, str] = field(
        default="adamw_apex_fused",
        metadata={"help": "The optimizer to use."},
    )
    parallelize_model: Optional[bool] = field(
        default=False, metadata={"help": "whether to enable naive model parallel"}
    )
    seq2seq_type: Optional[str] = field(
        default="short_seq", metadata={"help": "seq2seq type: action, short_seq"}
    )
