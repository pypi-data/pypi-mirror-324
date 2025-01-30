import json
from typing import List, NamedTuple

from transformers import (
    AutoModelForSeq2SeqLM,
    DataCollatorForSeq2Seq,
    AutoConfig,
    AutoTokenizer,
)

from quotect.common.arguments import QuotectArguments
from quotect.data.data import QuoteDataset
from quotect.data.preprocess_data import get_quote_document
from quotect.model.trainer import QuoteTrainer
from quotect.data.convert_quotes import convert_to_quote_json

max_len = 4096


def _text2doc(inp, filename, text):
    sent_map = {s: i for i, s in enumerate(inp.sents)}
    doc = {"annotations": [], "documentName": filename, "originalText": text}
    doc["sentences"] = [
        {
            "begin": s.start,
            "charBegin": s.start_char,
            "charEnd": s.end_char,
            "end": s.end,
            "id": i,
            "text": s.text,
            "tokenIds": [t.i for t in s],
            "tokens": [t.text for t in s],
        }
        for i, s in enumerate(inp.sents)
    ]
    doc["tokens"] = [
        {
            "charBegin": t.idx,
            "charEnd": t.idx + len(t),
            "id": t.i,
            "sentence": sent_map[t.sent],
            "text": t.text,
            "word": t.i - t.sent.start,
        }
        for t in inp
    ]
    return doc


class Token(NamedTuple):
    start: int
    end: int
    sent: int
    text: str


class Span(NamedTuple):
    start: int
    end: int
    text: str


class QuoteInput(NamedTuple):
    name: str
    tokens: List[Token]
    sentences: List[Span]
    text: str


class Quotect:
    def __init__(self, trainer_args: QuotectArguments):
        self.trainer_args = trainer_args
        self.tokenizer = self._get_tokenizer(trainer_args.model_name_or_path)
        self.model = self._get_model(trainer_args.model_name_or_path)
        self.collator = DataCollatorForSeq2Seq(self.tokenizer, model=self.model)
        self.trainer = QuoteTrainer(
            tokenizer=self.tokenizer,
            model=self.model,
            args=trainer_args,
            data_collator=self.collator,
        )
        self.nlp = None

    def predict(self, input: QuoteInput):
        if (
            len(input.sentences) == 0 or len(input.tokens) == 0
        ) and input.text is not None:
            if self.nlp is None:
                import spacy

                try:
                    self.nlp = spacy.load("de_dep_news_trf")
                except OSError:
                    print('Downloading language model for spacy')
                    from spacy.cli import download
                    download('de_dep_news_trf')
                    self.nlp = spacy.load("de_dep_news_trf")
            doc = _text2doc(self.nlp(input.text), input.name, input.text)
        else:
            doc = {
                "documentName": input.name,
                "annotations": [],
            }
            doc["sentences"] = [
                {
                    "begin": s.start,
                    "charBegin": input.tokens[s.start].start,
                    "charEnd": input.tokens[s.end - 1].end,
                    "end": s.end,
                    "id": i,
                    "text": s.text,
                    "tokenIds": list(range(s.start, s.end)),
                    "tokens": [t.text for t in s],
                }
                for i, s in enumerate(input.sentences)
            ]
            doc["tokens"] = [
                {
                    "charBegin": t.start,
                    "charEnd": t.end,
                    "id": i,
                    "sentence": t.sent,
                    "text": t.text,
                    "word": i - input.sentences[t.sent].start,
                }
                for i, t in enumerate(input.tokens)
            ]

        input_docs = get_quote_document(
            doc,
            self.tokenizer,
            segment_len=max_len,
            stride=0,
            is_train=False,
            mark_sentence=True,
        )

        dataset = QuoteDataset(self.tokenizer, input_docs)
        prediction = self.trainer.predict(
            dataset,
            max_length=max_len,
            num_beams=self.trainer_args.generation_num_beams,
        )
        clusters = prediction.metrics[f"test_{input.name}"]

        outputs = convert_to_quote_json(
            [doc], {input.name: clusters}, mark_sentence=True
        )

        return outputs[0]

    def _get_tokenizer(self, model_name_or_path: str):
        tok = AutoTokenizer.from_pretrained(
            model_name_or_path, model_max_length=max_len
        )
        return tok

    def _get_model(self, model_name_or_path: str):
        config = AutoConfig.from_pretrained(model_name_or_path)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name_or_path, config=config)
        return model


if __name__ == "__main__":
    args = QuotectArguments(
        model_name_or_path="fynnos/quotect-mt5-base",
        output_dir="/tmp",
        predict_with_generate=True,
        generation_max_length=max_len,
        generation_num_beams=1,
    )
    q = Quotect(args)
    input = QuoteInput(
        name="test",
        tokens=[],
        sentences=[],
        text="Sie sagte gestern: 'Morgen scheint die Sonne!' Jemand anderes erwiderte, dass es bestimmt regnen wird.",
    )
    print(json.dumps(q.predict(input)))
