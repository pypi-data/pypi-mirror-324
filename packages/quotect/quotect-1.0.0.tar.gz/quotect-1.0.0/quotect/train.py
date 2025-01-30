import logging
import os
import sys
from transformers import HfArgumentParser, set_seed
from transformers import (
    AutoModelForSeq2SeqLM,
    DataCollatorForSeq2Seq,
    AutoConfig,
    AutoTokenizer,
)
from transformers.integrations import TensorBoardCallback
from quotect.common.arguments import DataArguments, QuotectArguments as TrainingArguments
from quotect.common.constants import (
    COPY,
    SENTENCE_START,
    SENTENCE_END,
    SPECIAL_IDS,
    REQUIRED_PARTS,
)
from quotect.model.trainer import QuoteTrainer
from quotect.data.data import ConstrainedDataCollator, QuoteDataset
from quotect.model import ConstrainedT5

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stderr))


def main(args=None):
    parser = HfArgumentParser((DataArguments, TrainingArguments))

    if len(sys.argv) == 2 and sys.argv[1].endswith(".json"):
        data_args, training_args = parser.parse_json_file(
            json_file=os.path.abspath(sys.argv[1])
        )
    elif args is not None:
        data_args, training_args = parser.parse_dict(args)
    else:
        data_args, training_args = parser.parse_args_into_dataclasses()
        data_args: DataArguments
        training_args: TrainingArguments

    if (
        os.path.exists(training_args.output_dir)
        and os.listdir(training_args.output_dir)
        and training_args.do_train
        and not training_args.overwrite_output_dir
    ):
        raise ValueError(
            f"Output directory ({training_args.output_dir}) already exists and is not empty. Use --overwrite_output_dir to overcome."
        )

    # Setup logging
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(name)s -   %(message)s",
        datefmt="%m/%d/%Y %H:%M:%S",
        level=logging.INFO if training_args.local_rank in [-1, 0] else logging.WARN,
    )
    logger.warning(
        "Process rank: %s, device: %s, n_gpu: %s, distributed training: %s, fp16 training: %s, bf16 training: %s",
        training_args.local_rank,
        training_args.device,
        training_args.n_gpu,
        bool(training_args.local_rank != -1),
        training_args.fp16,
        training_args.bf16,
    )
    logger.info("Training/evaluation parameters %s", training_args)
    logger.info("Data arguments %s", data_args)

    set_seed(training_args.seed)
    tokenizer = AutoTokenizer.from_pretrained(
        training_args.model_name_or_path, model_max_length=4096
    )
    num_new_tokens = tokenizer.add_tokens(REQUIRED_PARTS + [COPY])
    if training_args.seq2seq_type == "short_seq" and training_args.mark_sentence:
        num_new_tokens += tokenizer.add_tokens([SENTENCE_START, SENTENCE_END])
    # we  need to resize model token embeddings
    config = AutoConfig.from_pretrained(training_args.model_name_or_path)
    if training_args.gradient_checkpointing:
        # use_cache is False for training, True for evaluation
        config.use_cache = False
    if training_args.seq2seq_type == "action":
        special_ids = SPECIAL_IDS
        model = ConstrainedT5.from_pretrained(
            training_args.model_name_or_path,
            config=config,
            special_ids=special_ids,
            seq2seq_type=training_args.seq2seq_type,
        )
    else:
        model = AutoModelForSeq2SeqLM.from_pretrained(
            training_args.model_name_or_path, config=config
        )

    if len(model.get_input_embeddings().weight) < len(tokenizer):
        logger.info("resize model input embeddings")
        model.resize_token_embeddings(len(tokenizer))

    if training_args.seq2seq_type == "action":
        collator = ConstrainedDataCollator(tokenizer, model=model)
    else:
        collator = DataCollatorForSeq2Seq(tokenizer, model=model)
    # model.resize_token_embeddings(len(tokenizer))
    if data_args.predict_only:
        predict_set = QuoteDataset(tokenizer, data_args, training_args, "predict")
        train_set = None
        dev_set = predict_set
        test_set = predict_set
        tb_callback = None
    else:
        train_set = QuoteDataset(tokenizer, data_args, training_args, "train")
        dev_set = QuoteDataset(tokenizer, data_args, training_args, "dev")
        test_set = QuoteDataset(tokenizer, data_args, training_args, "test")
        tb_callback = TensorBoardCallback()
    if training_args.parallelize_model:
        model.parallelize()
    trainer = QuoteTrainer(
        tokenizer=tokenizer,
        model=model,
        args=training_args,
        train_dataset=train_set,
        eval_dataset=dev_set,
        data_collator=collator,
        callbacks=[] if tb_callback is None else [tb_callback],
    )
    if training_args.do_train:
        if (
            training_args.resume_from_checkpoint is not None
            and training_args.resume_from_checkpoint is not False
            and training_args.resume_from_checkpoint != "False"
        ):
            trainer.train(resume_from_checkpoint=training_args.resume_from_checkpoint)
        else:
            trainer.train()
        if trainer.is_world_process_zero():
            trainer.save_model()
            tokenizer.save_pretrained(training_args.output_dir)

    if training_args.do_predict:
        test_results = trainer.evaluate(
            test_set,
            max_length=data_args.max_eval_len_out,
            num_beams=training_args.generation_num_beams,
        )
        logger.info(f"test results: {test_results}")
        dev_results = trainer.evaluate(
            dev_set,
            max_length=data_args.max_eval_len_out,
            num_beams=training_args.generation_num_beams,
        )
        logger.info(f"dev results: {dev_results}")
    if data_args.predict_only:
        trainer.predict(
            predict_set,
            max_length=data_args.max_eval_len_out,
            num_beams=training_args.generation_num_beams,
        )


if __name__ == "__main__":
    main()
