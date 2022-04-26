from collections import Counter
from typing import Optional

import jieba
from sqlalchemy.engine import Row

from utils.utils import get_stop_word


class AllNewsTopWordController:
    """
    所有新闻 热词 top 10
    """

    def __init__(self):
        self.contents: Optional[str] = None

        self.stop_words = get_stop_word()

    def remove_stop_word(self, words: list[str]) -> list[str]:
        return [
            _word for _word in words
            if _word not in self.stop_words and 1 < len(_word)
        ]

    def set_contents(self, news: list[Row]) -> None:
        self.contents = " ".join([a_news.content for a_news in news])

    def run(self) -> list:
        words = jieba.lcut(self.contents)
        words = self.remove_stop_word(words)
        counter = Counter(words)
        return counter.most_common(10)
