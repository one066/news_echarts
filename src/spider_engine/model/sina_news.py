from datetime import datetime

from spider_engine.model.news_base import NewsBase


class SinaNews(NewsBase):
    """
    新浪滚动新闻
    """
    SINA_NEWS_URL = "http://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2509&k=&num=50&page={page}"

    def __init__(self):
        super().__init__()

        self.app_name = "sina_news"
        self.app_chinese_name = "新浪新闻"

    def _get_page_news(self, page: int) -> list[dict]:
        """ 得到当前页新闻的信息
        """
        _response = self.get(self.SINA_NEWS_URL.format(page=page))
        contents = _response.json()
        return contents["result"]["data"]

    def get_news_header(self) -> None:
        for page in range(1, 100):
            news = self._get_page_news(page)

            for a_news in news:

                upload_date = datetime.fromtimestamp(int(a_news["intime"]))
                url = a_news["url"].replace("https", "http")
                if not self.add_news(
                    app_name=self.app_name,
                    app_chinese_name=self.app_chinese_name,
                    url=url,
                    title=a_news["title"],
                    upload_date=upload_date,
                    tags=""
                ):
                    return

    def get_news_content(self, url: str) -> str:
        element_path = "//div[@id='artibody' or @id='article']/p"
        return self.get_div_all_content(url=url, element_path=element_path)
