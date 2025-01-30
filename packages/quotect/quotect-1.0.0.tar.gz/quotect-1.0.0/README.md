# quotect

Python package to perform quotation detection on German texts.

## Installation

From PYPI: `pip install quotect`

From reposiory: `pip install -e .`

## Usage

```python
import json
from quotect import Quotect
args = QuotectArguments(
    model_name_or_path="fynnos/quotect-mt5-base",
    output_dir="/tmp",
    predict_with_generate=True,
    generation_max_length=max_len,
    generation_num_beams=1,
)
q = Quotect(args)
input = QuoteInput(
    name="example",
    tokens=[],
    sentences=[],
    text="Sie sagte gestern: 'Morgen scheint die Sonne!' Jemand anderes erwiderte, dass es bestimmt regnen wird.",
)
print(json.dumps(q.predict(input)))
```

## Citation

Based on the publication [Fine-grained quotation detection and attribution in German news articles](https://aclanthology.org/2024.konvens-main.22/)
