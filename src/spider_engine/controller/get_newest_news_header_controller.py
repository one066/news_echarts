import threading

from spider_engine.model.cctv_news import CctvNews
from spider_engine.model.china_news import ChinaNews
from spider_engine.model.people_news import PeopleNews
from spider_engine.model.sina_news import SinaNews


class GetNewestNewsHeaderController:
    """
    得到最新的新闻 header
    """

    def __init__(self):
        self.sina_news = SinaNews()
        self.china_news = ChinaNews()
        self.people_news = PeopleNews()
        self.cctv_news = CctvNews()

    def set_all_app_last_title(self, all_app_last_title: dict) -> None:
        for app_name, last_title in all_app_last_title.items():
            eval(f"self.{app_name}.set_last_title")(last_title)

    def run(self) -> list:
        threads = [
            threading.Thread(target=self.sina_news.get_news_header),
            threading.Thread(target=self.china_news.get_news_header),
            threading.Thread(target=self.people_news.get_news_header),
            threading.Thread(target=self.cctv_news.get_news_header),
        ]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        return self.sina_news.news + self.china_news.news + self.people_news.news + self.cctv_news.news
