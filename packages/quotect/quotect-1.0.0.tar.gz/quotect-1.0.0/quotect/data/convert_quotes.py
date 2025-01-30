import json
import sys
from collections import defaultdict

from quotect.common.constants import (
    GROUP_PART_NAMES,
    IS_QUOTE_TYPE,
    QUOTE_TYPE_NAMES,
)


def output_quote_json(input_file, output_file, predictions, mark_sentence):
    outputs = []
    for line in input_file:
        input = json.loads(line) if isinstance(line, str) else line
        documentName = input["documentName"]
        del input["annotations"]
        pred_clusters = predictions[documentName]
        annotations = []
        gold_tokens = input["tokens"]
        originalText = input["originalText"]
        if mark_sentence:
            tokens = [None]
            lastSent = gold_tokens[0]["sentence"]
            for t in gold_tokens:
                s = t["sentence"]
                if lastSent != s:
                    tokens.append(None)
                    tokens.append(None)
                tokens.append(t)
                lastSent = s
        else:
            tokens = gold_tokens

        for cluster in pred_clusters:
            parts = defaultdict(list)
            cluster.sort()
            for span_start, span_end, part in cluster:
                start_token, end_token = tokens[span_start], tokens[span_end]
                i = 1
                while start_token is None:
                    print("error start_token is none", file=sys.stderr)
                    start_token = tokens[span_start + i]
                    i += 1
                i = 1
                while end_token is None:
                    print("error end_token is none", file=sys.stderr)
                    end_token = tokens[span_end - i]
                    i -= 1
                parts[part].append(
                    {
                        "charBegin": start_token["charBegin"],
                        "charEnd": end_token["charEnd"],
                        "begin": start_token["id"],
                        "end": end_token["id"] + 1,
                    }
                )
            a = {}
            for part, spans in parts.items():
                tokenIds = [x for s in spans for x in range(s["begin"], s["end"])]
                tokenIds.sort()
                text = " ".join(
                    [originalText[s["charBegin"] : s["charEnd"]] for s in spans]
                )
                a[GROUP_PART_NAMES[part if part < len(GROUP_PART_NAMES) else 1]] = {
                    "spans": spans,
                    "text": text,
                    "tokenIds": tokenIds,
                }
                if part >= len(GROUP_PART_NAMES) or part == 1:
                    a["type"] = (
                        QUOTE_TYPE_NAMES[part - (len(GROUP_PART_NAMES) + 1)]
                        if IS_QUOTE_TYPE and part > len(GROUP_PART_NAMES)
                        else "Indirect"
                    )
                    a["medium"] = "Speech"
            if a.get("quote", None) is not None:
                annotations.append(a)
        input["annotations"] = annotations
        outputs.append(input)
        if output_file is not None:
            json.dump(input, output_file, ensure_ascii=False)
            output_file.write("\n")
    return outputs


def convert_to_quote_json(
    quote_gold, predict_clusters_or_json_path, mark_sentence, out_file=None
):
    if isinstance(predict_clusters_or_json_path, str):
        predictions = {}
        with open(predict_clusters_or_json_path, "r") as json_pred_file:
            for line in json_pred_file:
                doc = json.loads(line)
                predictions[doc["doc_key"][:-2]] = doc["predict_clusters"]
    else:
        predictions = predict_clusters_or_json_path

    if isinstance(quote_gold, str):
        with open(quote_gold, "r") as gold_file:
            return output_quote_json(gold_file, out_file, predictions, mark_sentence)
    else:
        return output_quote_json(quote_gold, out_file, predictions, mark_sentence)


if __name__ == "__main__":
    convert_to_quote_json(sys.argv[1], sys.argv[2], sys.argv[3] == "True", sys.stdout)
