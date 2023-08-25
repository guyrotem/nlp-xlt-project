import json
from dataclasses import dataclass


class Gsm8kParser:
    def __init__(self):
        with open('data/GSM8K_100.json') as gsm8k_file:
            contents = json.load(gsm8k_file)
            rows = contents['rows']
            self._qa = list(map(_row_mapper, rows))

    def get_items(self):
        return self._qa


def _row_mapper(item):
    index = item['row_idx']
    row = item['row']
    q = row['question']
    a = row['answer']
    gold = int(a.split("#### ")[1])
    return QA(index, q, gold)


@dataclass
class QA:
    index: int
    question: str
    gold_answer: int
