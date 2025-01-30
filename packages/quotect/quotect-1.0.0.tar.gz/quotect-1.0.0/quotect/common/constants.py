from transformers import MT5Tokenizer, T5Tokenizer
from copy import deepcopy

IS_MULTILINGUAL = True  # use mT5
IS_QUOTE_TYPE = True  # distinguish between different quotation types (direct, indirect, reported, ...)

Tokenizer = MT5Tokenizer if IS_MULTILINGUAL else T5Tokenizer
pretrained_tokenizer = "google/mt5-small" if IS_MULTILINGUAL else "google-t5/t5-small"

int_tokenizer = Tokenizer.from_pretrained(pretrained_tokenizer, model_max_length=4096)

CUE_START = "<cue>"
CUE_END = "</cue>"
QUOTE_START = "<quote>"
QUOTE_END = "</quote>"
QUOTE_DIRECT_START = "<direct>"
QUOTE_DIRECT_END = "</direct>"
QUOTE_INDIRECT_START = "<indirect>"
QUOTE_INDIRECT_END = "</indirect>"
QUOTE_FRIN_START = "<frin>"
QUOTE_FRIN_END = "</frin>"
QUOTE_INFRIN_START = "<infrin>"
QUOTE_INFRIN_END = "</infrin>"
QUOTE_REPORTED_START = "<reported>"
QUOTE_REPORTED_END = "</reported>"
FRAME_START = "<frame>"
FRAME_END = "</frame>"
ADDR_START = "<addr>"
ADDR_END = "</addr>"
SPEAKER_START = "<speaker>"
SPEAKER_END = "</speaker>"
MENTION_START = "<m>"
MENTION_END = "</m>"
SEP_TOKEN = "|"
COPY = "<copy>"
REQUIRED_PARTS = [
    CUE_START,
    CUE_END,
    QUOTE_START,
    QUOTE_END,
    FRAME_START,
    FRAME_END,
    ADDR_START,
    ADDR_END,
    SPEAKER_START,
    SPEAKER_END,
    MENTION_START,
    MENTION_END,
]

QUOTE_TYPES = [
    QUOTE_DIRECT_START,
    QUOTE_DIRECT_END,
    QUOTE_INDIRECT_START,
    QUOTE_INDIRECT_END,
    QUOTE_FRIN_START,
    QUOTE_FRIN_END,
    QUOTE_INFRIN_START,
    QUOTE_INFRIN_END,
    QUOTE_REPORTED_START,
    QUOTE_REPORTED_END,
]
if IS_QUOTE_TYPE:
    REQUIRED_PARTS.extend(QUOTE_TYPES)

REQUIRED_PARTS_START = REQUIRED_PARTS[::2]
REQUIRED_PARTS_END = REQUIRED_PARTS[1::2]
GROUP_PART_NAMES = ("cue", "quote", "frame", "addressee", "speaker")
QUOTE_TYPE_NAMES = (
    "Direct",
    "Indirect",
    "FreeIndirect",
    "IndirectFreeIndirect",
    "Reported",
)

int_tokenizer.add_tokens(REQUIRED_PARTS + [COPY])
SPECIAL_IDS = {
    "cue_start": int_tokenizer.encode(CUE_START, add_special_tokens=False)[0],
    "cue_end": int_tokenizer.encode(CUE_END, add_special_tokens=False)[0],
    "quote_start": int_tokenizer.encode(QUOTE_START, add_special_tokens=False)[0],
    "quote_end": int_tokenizer.encode(QUOTE_END, add_special_tokens=False)[0],
    "frame_start": int_tokenizer.encode(FRAME_START, add_special_tokens=False)[0],
    "frame_end": int_tokenizer.encode(FRAME_END, add_special_tokens=False)[0],
    "addr_start": int_tokenizer.encode(ADDR_START, add_special_tokens=False)[0],
    "addr_end": int_tokenizer.encode(ADDR_END, add_special_tokens=False)[0],
    "speaker_start": int_tokenizer.encode(SPEAKER_START, add_special_tokens=False)[0],
    "speaker_end": int_tokenizer.encode(SPEAKER_END, add_special_tokens=False)[0],
    "mention_start": int_tokenizer.encode(MENTION_START, add_special_tokens=False)[0],
    "mention_end": int_tokenizer.encode(MENTION_END, add_special_tokens=False)[0],
    "sep": int_tokenizer.encode(SEP_TOKEN, add_special_tokens=False)[0],
    "copy": int_tokenizer.encode(COPY, add_special_tokens=False)[0],
    "eos": int_tokenizer.eos_token_id,
}
if IS_QUOTE_TYPE:
    SPECIAL_IDS["direct_start"] = int_tokenizer.encode(
        QUOTE_DIRECT_START, add_special_tokens=False
    )[0]
    SPECIAL_IDS["direct_end"] = int_tokenizer.encode(
        QUOTE_DIRECT_END, add_special_tokens=False
    )[0]
    SPECIAL_IDS["indirect_start"] = int_tokenizer.encode(
        QUOTE_INDIRECT_START, add_special_tokens=False
    )[0]
    SPECIAL_IDS["indirect_end"] = int_tokenizer.encode(
        QUOTE_INDIRECT_END, add_special_tokens=False
    )[0]
    SPECIAL_IDS["frin_start"] = int_tokenizer.encode(
        QUOTE_FRIN_START, add_special_tokens=False
    )[0]
    SPECIAL_IDS["frin_end"] = int_tokenizer.encode(
        QUOTE_FRIN_END, add_special_tokens=False
    )[0]
    SPECIAL_IDS["infrin_start"] = int_tokenizer.encode(
        QUOTE_INFRIN_START, add_special_tokens=False
    )[0]
    SPECIAL_IDS["infrin_end"] = int_tokenizer.encode(
        QUOTE_INFRIN_END, add_special_tokens=False
    )[0]
    SPECIAL_IDS["reported_start"] = int_tokenizer.encode(
        QUOTE_REPORTED_START, add_special_tokens=False
    )[0]
    SPECIAL_IDS["reported_end"] = int_tokenizer.encode(
        QUOTE_REPORTED_END, add_special_tokens=False
    )[0]
integers = []
for i in range(500):
    cid = int_tokenizer.encode(str(i), add_special_tokens=False)
    integers.extend(cid)
integers = list(set(integers))
SPECIAL_IDS["integers"] = integers

mark_sent_tokenizer = Tokenizer.from_pretrained(
    pretrained_tokenizer, model_max_length=4096
)

SENTENCE_START = "<sentence>"
SENTENCE_END = "</sentence>"

mark_sent_tokenizer.add_tokens(REQUIRED_PARTS + [COPY, SENTENCE_START, SENTENCE_END])
MARK_SPECIAL_IDS = deepcopy(SPECIAL_IDS)
MARK_SPECIAL_IDS["sentence_start"] = mark_sent_tokenizer.encode(
    SENTENCE_START, add_special_tokens=False
)[0]
MARK_SPECIAL_IDS["sentence_end"] = mark_sent_tokenizer.encode(
    SENTENCE_END, add_special_tokens=False
)[0]
