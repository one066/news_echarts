import random
import threading
import time

from tqdm import tqdm

from spider_engine.model.cctv_news import CctvNews
from spider_engine.model.china_news import ChinaNews
from spider_engine.model.people_news import PeopleNews
from spider_engine.model.sina_news import SinaNews


class AddNewsContentController:
    """
    得到新闻的 content
    """

    def __init__(self):
        self.sina_news = SinaNews()
        self.china_news = ChinaNews()
        self.people_news = PeopleNews()
        self.cctv_news = CctvNews()

        self.news_headers: list[dict] = []
        self.news: list[dict] = []

        # 每次运行线程数量
        self.each_run_threading_num = 4

    def set_news(self, news_headers: list):
        # 打乱一下 news 避免多个线程一直跑同个新闻平台的爬虫
        random.shuffle(news_headers)
        self.news_headers = news_headers

    def news_add_content(self, **a_news) -> None:
        """news 获取 正文"""
        # 随机暂停零点几秒 避免多进程同时发起请求
        time.sleep(random.random())

        a_news["content"] = eval(f"self.{a_news['app_name']}.get_news_content")(
            a_news["url"]
        )
        print(a_news["url"], "success")
        self.news.append(a_news)

    def run(self) -> list:
        threads = [
            threading.Thread(target=self.news_add_content, kwargs=news_header)
            for news_header in self.news_headers
        ]

        for index, thread in tqdm(enumerate(threads)):
            thread.start()

            # 执行完一轮 停留几秒
            if (index % self.each_run_threading_num) == 0:
                time.sleep(random.uniform(3, 3.2))

        for thread in threads:
            thread.join()

        # 删除 content 为 None 的新闻
        return [a_news for a_news in self.news if a_news["content"]]
