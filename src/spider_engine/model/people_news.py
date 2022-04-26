import time
from datetime import datetime

from spider_engine.model.news_base import NewsBase


class PeopleNews(NewsBase):
    """
    人民网滚动新闻
    """
    PEOPLE_NEWS_URL = "http://news.people.com.cn/210801/211150/index.js?_={now_timestamp}"

    def __init__(self):
        super().__init__()

        self.app_name = "people_news"
        self.app_chinese_name = "人民网"

    def _get_now_news(self) -> list[dict]:
        """ 得到当前页新闻的信息
        """
        _response = self.get(
            self.PEOPLE_NEWS_URL.format(now_timestamp=time.time())
        )
        contents = _response.json()
        return contents["items"]

    def get_news_header(self) -> None:
        news = self._get_now_news()

        for a_news in news:

            upload_date = datetime.strptime(a_news["date"], "%Y-%m-%d %H:%M:%S")
            if not self.add_news(
                app_name=self.app_name,
                app_chinese_name=self.app_chinese_name,
                url=a_news["url"],
                title=a_news["title"],
                upload_date=upload_date,
                tags=""
            ):
                return

    def get_news_content(self, url: str) -> str:
        element_path = "//div[@class='rm_txt_con cf' or @class='text_c' or " \
                       "@class='artDet' or @class='content clear clearfix']/p"
        return self.get_div_all_content(
            url=url, element_path=element_path, encoding="gbk"
        )
