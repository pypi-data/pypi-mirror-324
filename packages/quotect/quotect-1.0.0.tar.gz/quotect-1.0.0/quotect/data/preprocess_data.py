from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import sys
import json
import copy
import collections
import logging
from typing import Tuple, Dict, List
from collections import defaultdict
import numpy as np
from argparse_dataclass import dataclass


import quotect.utils.helper as helper
from quotect.common.constants import (
    QUOTE_TYPE_NAMES,
    SEP_TOKEN,
    COPY,
    SENTENCE_START,
    SENTENCE_END,
    REQUIRED_PARTS_START,
    REQUIRED_PARTS_END,
    GROUP_PART_NAMES,
    IS_QUOTE_TYPE,
    int_tokenizer,
)

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S",
    level=logging.INFO,
)
logger = logging.getLogger(__file__)


def is_punctuation(c):
    if c in {
        ".",
        ",",
        "?",
        "!",
        ";",
        ":",
        "'s",
        "'m",
        "'ve",
        "n't",
        "'ll",
        ")",
        "]",
        "}",
        "-",
    }:
        return True
    return False


class QuoteDocState:
    def __init__(self, key):
        self.doc_key = key
        self.sentence_end = []
        self.token_end = []
        self.tokens = []
        self.subtokens = []
        self.info = []
        self.segments = []
        self.subtoken_map = []
        self.segment_subtoken_map = []
        self.sentence_map = []
        self.segment_sentence_map = []
        self.clusters = collections.defaultdict(list)
        self.word_clusters = collections.defaultdict(list)
        self.mention_to_seg_id = collections.defaultdict(list)
        self.word_mention_to_seg_id = collections.defaultdict(list)
        self.segment_info = []
        self.offsets = []

    def finalize(self, mark_sentence):
        all_seg_clusters = get_seg_clusters(
            self.clusters, self.mention_to_seg_id, len(self.segments)
        )
        all_word_seg_clusters = get_seg_clusters(
            self.word_clusters, self.word_mention_to_seg_id, len(self.segments)
        )
        cluster_indices = get_mention_to_cid(all_seg_clusters)
        docs = []
        num_words = len(helper.flat_lists(self.segments))
        num_segments = len(self.segments)

        subtoken_map = self.segment_subtoken_map
        assert num_words == len(helper.flat_lists(self.segment_subtoken_map))

        sentence_map = self.segment_sentence_map
        assert num_words == len(helper.flat_lists(sentence_map))

        all_mentions = list(self.mention_to_seg_id.keys())
        sentences = self.segments

        # inserting <m> and </m> into target sequences for all mentions
        target_sentences = m_star_target_sequences(
            all_mentions,
            self.segments,
            SEP_TOKEN,
            self.mention_to_seg_id,
            cluster_indices,
            self.offsets,
        )
        target_short_seqs = []
        target_texts = []
        for target_seq in target_sentences:
            target_short = trim_target_sequence(target_seq, mark_sentence)
            target_short_seqs.append(target_short)
            target_text = int_tokenizer.convert_tokens_to_string(target_short)
            target_texts.append(target_text)

        target_maps = get_target_map(
            target_sentences, REQUIRED_PARTS_END, int_tokenizer.tokenize(SEP_TOKEN)[0]
        )
        target_int_tags = get_target_int_tags(
            target_sentences,
            target_maps,
            REQUIRED_PARTS_START,
            int_tokenizer.tokenize(SEP_TOKEN)[0],
            COPY,
        )
        # add gold clusters info into docs
        for i in range(num_segments):
            docs.append(
                {
                    "doc_key": f"{self.doc_key}_{i}",
                    "offset": self.offsets[i],
                    "sentence": sentences[i],
                    "target_sentence": target_sentences[i],
                    "target_short_sentence": target_short_seqs[i],
                    "target_text": target_texts[i],
                    "target_action": target_int_tags[i],
                    "sentence_map": sentence_map[i],
                    "subtoken_map": subtoken_map[i],
                    "gold_clusters": self.word_clusters,
                    "seg_clusters": all_word_seg_clusters[i],
                    "gold_token_clusters": self.clusters,
                }
            )

        return docs


def get_quote_document(js, tokenizer, segment_len, stride, is_train, mark_sentence):
    document_state = QuoteDocState(js["documentName"])
    doc_word_idx = -1
    sent_word_map = {}
    for sentence in js["sentences"]:
        sent_idx = sentence["id"]
        sent_word_map[sent_idx] = {}
        if mark_sentence:
            doc_word_idx += 1
            document_state.token_end.append(True)
            document_state.subtokens.append(SENTENCE_START)
            document_state.sentence_end.append(False)
            document_state.subtoken_map.append(doc_word_idx)
        for word_idx, word in enumerate(sentence["tokens"]):
            doc_word_idx += 1
            sent_word_map[sent_idx][word_idx] = [len(document_state.subtokens)]
            word = normalize_word(word)
            if is_punctuation(word):
                subtokens = tokenizer.tokenize(word)[1:]  # skipping '_'
            else:
                subtokens = tokenizer.tokenize(word)
            document_state.tokens.append(word)
            if len(subtokens) > 0:
                document_state.token_end += [False] * (len(subtokens) - 1) + [True]
            for sidx, subtoken in enumerate(subtokens):
                document_state.subtokens.append(subtoken)
                document_state.sentence_end.append(False)
                document_state.subtoken_map.append(doc_word_idx)
            sent_word_map[sent_idx][word_idx].append(len(document_state.subtokens))
        if len(document_state.sentence_end) > 0:
            if mark_sentence:
                doc_word_idx += 1
                document_state.token_end.append(True)
                document_state.subtokens.append(SENTENCE_END)
                document_state.sentence_end.append(True)
                document_state.subtoken_map.append(doc_word_idx)
            else:
                document_state.sentence_end[-1] = True
    constraints1 = document_state.sentence_end

    assert len(document_state.sentence_end) == len(document_state.token_end)
    document_state.sentence_map = get_doc_sentence_map(document_state.sentence_end)
    mapped_clusters = []
    word_clusters = []
    tokens = js["tokens"]
    for group in js["annotations"]:
        cur_cluster = []
        word_cluster = []
        for part_id, part_name in enumerate(GROUP_PART_NAMES):
            part = group[part_name]
            id = (
                part_id
                if IS_QUOTE_TYPE and part_id != 1
                else 6 + QUOTE_TYPE_NAMES.index(group["type"])
            )
            for span in part["spans"]:
                start = span["begin"]
                end = span["end"]
                start_token = tokens[start]
                end_token = tokens[end - 1]
                start_sid = start_token["sentence"]
                end_sid = end_token["sentence"]
                word_start = start_token["word"]
                word_end = end_token["word"]
                span_start = sent_word_map[start_sid][word_start][0]
                span_end = sent_word_map[end_sid][word_end][1] - 1
                word_span_start = document_state.subtoken_map[span_start]
                word_span_end = document_state.subtoken_map[span_end]
                cur_cluster.append((span_start, span_end, id))
                word_cluster.append((word_span_start, word_span_end, id))

        mapped_clusters.append(sorted(cur_cluster, key=lambda x: x[0]))
        word_clusters.append(sorted(word_cluster, key=lambda x: x[0]))
    document_state.clusters = mapped_clusters
    document_state.word_clusters = word_clusters
    split_into_segments(
        document_state,
        segment_len,
        stride,
        constraints1,
        document_state.token_end,
        is_train,
        True,
    )
    document = document_state.finalize(mark_sentence)
    return document


def get_seg_clusters(merged_clusters, mention_to_seg_id, num_segs):
    all_seg_clusters = []
    for seg_id in range(num_segs):
        seg_clusters = []
        for c in merged_clusters:
            seg_cluster = []
            for m in c:
                m_sids = mention_to_seg_id[tuple(m)]
                if seg_id in m_sids:
                    seg_cluster.append(m)
            if len(seg_cluster) >= 1:
                seg_clusters.append(seg_cluster)
        all_seg_clusters.append(seg_clusters)
    return all_seg_clusters


def get_mention_to_cid(all_seg_clusters):
    # k: old group idx  v: sorted group idx

    def get_seg_mention_to_gid(groups):
        mention_to_gid = defaultdict(list)
        first_mentions = [min(g, key=lambda m: (m[1], -m[0])) for g in groups]
        assert len(first_mentions) == len(groups)
        sorted_ids = sorted(
            list(range(len(first_mentions))),
            key=lambda k: (first_mentions[k][1], -first_mentions[k][0]),
        )
        gid_map = {j: i for i, j in enumerate(sorted_ids)}
        for i, g in enumerate(groups):
            gid = gid_map[i]
            for m in g:
                mention_to_gid[tuple(m)].append(gid)
        return mention_to_gid

    all_seg_ment2cid = []
    for seg_clusters in all_seg_clusters:
        ment2cid = get_seg_mention_to_gid(seg_clusters)
        all_seg_ment2cid.append(ment2cid)
    return all_seg_ment2cid


def m_star_target_sequences(
    mentions: List[Tuple[int, int]],
    sequences: List[List[str]],
    m_sep: str,
    mention_to_seg_id: Dict[tuple, list],
    cluster_indices: List[Dict],
    offsets: List,
):
    """
    Get a sequence of target sentences with <m> and <\m> inserted.
    mentions: list of mentions, e.g. [(0, 0), (2, 3), (4, 4)] format: [start, end] (inclusive)
    sequences: list of sequences, e.g. [['I', 'have', 'a', 'cat'], ['I', 'have', 'a', 'dog']]
    m_special_start: special token for starting bracket
    m_special_end: special token for ending bracket
    mention_to_seg_id: dict, mapping mention to its segment id
    """
    m_startings, m_endings, m_parts = (
        zip(*mentions) if len(mentions) > 0 else ([], [], [])
    )
    all_m_cids = []
    all_m_sids = []
    for m in mentions:
        m_sids = mention_to_seg_id[tuple(m)]
        m_seg_cids = [cluster_indices[m_sid] for m_sid in m_sids]
        prev_cid = None
        i = 0
        m_cids = []  # [m_seg_cid[tuple(m)] for m_seg_cid in m_seg_cids]
        for m_seg_cid in m_seg_cids:
            if prev_cid is m_seg_cid:
                i += 1
            else:
                i = 0
                prev_cid = m_seg_cid
            m_cids.append(m_seg_cid[tuple(m)][i])
        all_m_cids.append(m_cids)
        all_m_sids.append(m_sids)
    # later segment comes first
    end_pos = [
        (m_sid, x + 1, -1, -m_startings[i], m_cid, part)
        for i, (x, part) in enumerate(zip(m_endings, m_parts))
        for m_sid, m_cid in zip(all_m_sids[i], all_m_cids[i])
    ]
    start_pos = [
        (m_sid, x, 1, -m_endings[i], m_cid, part)
        for i, (x, part) in enumerate(zip(m_startings, m_parts))
        for m_sid, m_cid in zip(all_m_sids[i], all_m_cids[i])
    ]
    # insert from right to left, so that the calculated positions are not changed
    sorted_pos = sorted(end_pos + start_pos, reverse=True)
    target_sequences = copy.deepcopy(sequences)
    # offset of each segment
    # prev_loc, prev_token, prev_seg_idx = -1, None, -1
    for x in sorted_pos:
        seg_idx = x[0]
        offset = offsets[seg_idx]
        if x[2] > 0:
            # start
            assert x[2] == 1
            start_label = REQUIRED_PARTS_START[x[5]]  #  f"<{x[5]}>"
            target_sequences[seg_idx].insert(x[1] - offset, start_label)
        else:
            # end
            end_label = REQUIRED_PARTS_END[x[5]]  # f"</{x[5]}>"
            end_inserts = (
                int_tokenizer.tokenize(m_sep)
                + int_tokenizer.tokenize(str(x[-2]))
                + [end_label]
            )
            for e in reversed(end_inserts):
                target_sequences[seg_idx].insert(x[1] - offset, e)
    return target_sequences


def trim_target_sequence(target_seq, mark_sentence=False):
    out_seq = []
    ment_stack = []
    # use sentence map to add periods
    for idx, s in enumerate(target_seq):
        if s in REQUIRED_PARTS_START:
            out_seq.append(s)
            ment_stack.append(idx)
        elif len(ment_stack) > 0:
            out_seq.append(s)
            if s in REQUIRED_PARTS_END:
                ment_stack.pop()
        elif mark_sentence and (s == SENTENCE_START or s == SENTENCE_END):
            out_seq.append(s)
    out_seq.append("</s>")
    return out_seq


def get_target_int_tags(target_sequences, target_maps, m_special_start, m_sep, m_copy):
    # 1 for inside entity 0 for outside entity
    target_tags = []
    for target_sequence, target_map in zip(target_sequences, target_maps):
        target_tag = np.array(target_sequence)
        tgt_map = np.array(target_map, dtype=bool)
        tag_map = (
            (~np.isin(target_tag, m_special_start)) & (target_tag != m_sep) & (~tgt_map)
        )
        target_tag[tag_map] = m_copy
        target_tags.append(target_tag.tolist())
    return target_tags


def get_target_map(target_sequences, m_special_end, m_sep):
    # 1 for inside entity 0 for outside entity
    target_maps = []
    for target_sequence in target_sequences:
        target_map = []
        status = "o"
        for t in target_sequence:
            if status == "o":
                target_map.append(0)
            else:
                target_map.append(1)
            if t == m_sep:
                status = "i"
            elif t in m_special_end:
                status = "o"
        assert len(target_map) == len(target_sequence)
        target_maps.append(target_map)
    return target_maps


def normalize_word(word):
    if word == "''" or word == "``":  # <unk> otherwise
        return '"'
    elif word == "`":  # <unk> otherwise
        return "'"
    else:
        return word


# first try to satisfy constraints1, and if not possible, constraints2.
def split_into_segments(
    document_state,
    max_segment_len,
    stride,
    constraints1,
    constraints2,
    is_train,
    include_mention_to_seg,
):
    current = 0
    offsets = []
    if not is_train and len(document_state.subtokens) < max_segment_len:
        stride = len(document_state.subtokens)
    if include_mention_to_seg:
        all_mentions = helper.flat_lists(document_state.clusters)
    seg_idx = 0
    while current < len(document_state.subtokens):
        offsets.append(current)
        end = min(current + max_segment_len - 1 - 1, len(document_state.subtokens) - 1)

        while end >= current and not constraints1[end]:
            end -= 1

        if end < current:
            end = min(
                current + max_segment_len - 1 - 1, len(document_state.subtokens) - 1
            )
            while end >= current and not constraints2[end]:
                end -= 1
            if end < current:
                raise Exception("Can't find valid segment")

        document_state.segments.append(
            document_state.subtokens[current : end + 1] + ["</s>"]
        )
        if include_mention_to_seg:
            for m in all_mentions:
                if current <= m[0] <= m[1] <= end:
                    document_state.mention_to_seg_id[tuple(m)].append(seg_idx)
                    document_state.word_mention_to_seg_id[
                        (
                            document_state.subtoken_map[m[0]],
                            document_state.subtoken_map[m[1]],
                            m[2],
                        )
                    ].append(seg_idx)
        sent_map = document_state.sentence_map[current : end + 1]
        document_state.segment_sentence_map.append(sent_map + [sent_map[-1]])
        subtoken_map = document_state.subtoken_map[current : end + 1]
        document_state.segment_subtoken_map.append(subtoken_map + [subtoken_map[-1]])
        seg_idx += 1
        if not include_mention_to_seg:
            document_state.segment_info.append(
                document_state.info[current : end + 1] + [None]
            )
        # current = end + 1
        next_cur = min(current + stride, len(document_state.subtokens))
        while next_cur > current and not constraints1[next_cur - 1]:
            next_cur -= 1
        if next_cur < current + 1:
            next_cur = min(current + stride, len(document_state.subtokens))
            while next_cur > current and not constraints2[next_cur - 1]:
                next_cur -= 1
            if next_cur < current + 1:
                raise Exception("Can't find valid stride")
        current = next_cur
    document_state.offsets = offsets
    return


def get_doc_sentence_map(sentence_end):
    current = 0
    sent_map = []
    for i, s in enumerate(sentence_end):
        sent_map.append(current)
        current += int(s)
    return sent_map


def minimize_quote_split(
    split,
    tokenizer,
    seg_len,
    stride,
    input_dir,
    output_dir,
    mark_sentence,
    language,
):
    is_train = split == "train"
    input_path = os.path.join(input_dir, f"{split}.jsonlines")
    output_path = os.path.join(
        output_dir, f"{split}.t5-small.{language}.{seg_len}.jsonlines"
    )
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    count = 0
    logger.info("Minimizing {}".format(input_path))
    datasets, max_target_len, max_target_short_len = [], 0, 0
    max_input_len = 0
    max_num_clusters = 0
    max_seg_clusters = 0
    with open(input_path, "r") as input_file:
        for line in input_file.readlines():
            instance = json.loads(line)
            document = get_quote_document(
                instance, tokenizer, seg_len, stride, is_train, mark_sentence
            )
            for doc in document:
                max_input_len = max([max_input_len] + [len(doc["sentence"])])
                max_target_len = max([max_target_len] + [len(doc["target_sentence"])])
                max_target_short_len = max(
                    max_target_short_len, len(doc["target_short_sentence"])
                )
                max_num_clusters = max([max_num_clusters] + [len(doc["gold_clusters"])])
                max_seg_clusters = max([max_num_clusters] + [len(doc["seg_clusters"])])
                datasets.append(doc)
                count += 1

    with open(output_path, "w") as f:
        for d in datasets:
            f.write("%s\n" % json.dumps(d, ensure_ascii=False))
    logger.info(
        f"Maximum input sequence length: {max_input_len}, Maximum target sequence length: {max_target_len}, Maximum target short sequence length: {max_target_short_len}"
    )
    logger.info(f"Maximum num gold clusters: {max_num_clusters}")
    logger.info(f"Maximum num segment clusters: {max_seg_clusters}")
    logger.info("Wrote {} documents to {}".format(count, output_path))


def minimize_data(
    data_name,
    language,
    seg_len,
    stride,
    input_dir,
    output_dir,
    tokenizer,
    mark_sentence,
    splits,
):
    if data_name == "quote":
        for split in splits:
            minimize_quote_split(
                split,
                tokenizer,
                seg_len,
                stride,
                input_dir,
                output_dir,
                mark_sentence,
                language,
            )
    else:
        raise ValueError(f"Unsupported dataset {data_name}")


@dataclass
class PreprocessingOptions:
    input_dir: str = "quoteinputs"
    output_dir: str = "inputs"
    dataset_name: str = "quote"
    language: str = "german"
    seg_lens: str = "2048,4096"
    mark_sentence: bool = True
    splits: str = "train,dev,test"


def main(args: PreprocessingOptions):
    if not os.path.isdir(args.output_dir):
        os.mkdir(args.output_dir)
    input_dir = args.input_dir
    output_dir = args.output_dir
    tokenizer = int_tokenizer

    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)
    seg_lens = [int(s) for s in args.seg_lens.split(",")]
    for seg_len in seg_lens:
        stride = seg_len // 2
        minimize_data(
            args.dataset_name,
            args.language,
            seg_len,
            stride,
            input_dir,
            output_dir,
            tokenizer,
            args.mark_sentence,
            args.splits.split(","),
        )


if __name__ == "__main__":
    args = PreprocessingOptions.parse_args(sys.argv[1:])
    main(args)
