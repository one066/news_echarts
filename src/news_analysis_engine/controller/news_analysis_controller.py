import random
import threading
import time
from typing import Optional

import cpca
from tqdm import tqdm

from news_analysis_engine.model.extract_topic import ExtractTopic
from news_analysis_engine.model.sentiment_analysis import SentimentAnalysis
from news_analysis_engine.model.words_count import WordsCount


class NewsAnalysisController:
    """
    新闻分析
    """

    def __init__(self):
        self.words_count = WordsCount()
        self.extract_topic = ExtractTopic()
        self.sentiment_analysis = SentimentAnalysis()

        self.news: list = []
        self.news_after_analysis = []
        self.each_run_threading_num = 5

    def set_news(self, news: list) -> None:
        self.news = news

    @staticmethod
    def get_provinces(content: str) -> Optional[str]:
        return cpca.transform([content])["省"][0]

    def news_analysis(self, **a_news) -> None:
        a_news["words_count"] = self.words_count.start(a_news["content"])
        a_news["positive"] = self.sentiment_analysis.get_sentiment(
            a_news["content"]
        )
        keywords, abstract = self.extract_topic.text_rank(a_news["content"])
        a_news["keywords"] = " ".join(keywords)
        a_news["abstract"] = " ".join(abstract)
        a_news["provinces"] = self.get_provinces(a_news["content"])
        print(f"{time.time()} {a_news['news_id']} success", flush=True)
        a_news.pop("content")
        self.news_after_analysis.append(a_news)

    def run(self) -> list[dict]:
        print(f"join threading {time.time()}", flush=True)
        threads = [
            threading.Thread(target=self.news_analysis, kwargs=a_news)
            for a_news in self.news
        ]

        for start_index in range(0, len(threads), self.each_run_threading_num):

            for thread in threads[start_index:start_index + self.each_run_threading_num]:
                thread.start()
            for thread in threads[start_index:start_index + self.each_run_threading_num]:
                thread.join()

        return self.news_after_analysis
