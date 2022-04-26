from sqlalchemy.engine import Row

from apps.news_echarts.models.news import NewsByDescTimeResult
from news_analysis_engine.model.recommended_news import RecommendedNews


class RecommendedNewsController:
    """
    新闻推荐
    """

    def __init__(self):
        self.recommended_news = RecommendedNews()

    def set_news_words(self, news_words: list) -> None:
        self.recommended_news.set_news_words(news_words)

    def cut(self, news: list[Row]) -> list:
        return self.recommended_news.cut(news)

    def set_key_words(self, user_view_history: NewsByDescTimeResult) -> None:
        self.recommended_news.set_key_words([
            _new["title"] for _new in user_view_history
        ])

    def run(self) -> list[str]:
        top_ten_new_ids = self.recommended_news.top_ten_new_ids()
        return top_ten_new_ids
