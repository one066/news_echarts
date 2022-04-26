from collections import Counter

import jieba
import ujson

from utils.utils import get_stop_word


class WordsCount:
    """
    词云
    """

    def __init__(self):
        self.stop_words = get_stop_word()

    def remove_stop_word(self, words: list[str]) -> list[str]:
        return [_word for _word in words if _word not in self.stop_words]

    def start(self, content: str) -> str:
        words = jieba.lcut(content)
        words = self.remove_stop_word(words)
        counter = Counter(words)

        return ujson.dumps([{
            "name": name,
            "value": value
        } for name, value in counter.most_common(30)])
