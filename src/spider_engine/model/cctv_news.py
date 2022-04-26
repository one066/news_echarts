import json
from datetime import datetime

from spider_engine.model.news_base import NewsBase


class CctvNews(NewsBase):
    """
    央视新闻
    """
    CCTV_NEWS_URL = "http://news.cctv.com/2019/07/gaiban/cmsdatainterface/page/news_{page}.jsonp?cb=news"

    def __init__(self):
        super().__init__()

        self.app_name = "cctv_news"
        self.app_chinese_name = "央视新闻"

    def _get_page_news(self, page: int) -> list[dict]:
        """ 得到当前页新闻的信息
        """
        _response = self.get(self.CCTV_NEWS_URL.format(page=page))

        # response format is `news({...})`
        _response = _response.text[5:-1]
        contents = json.loads(_response)
        return contents["data"]["list"]

    def get_news_header(self) -> None:
        for page in range(1, 100):
            news = self._get_page_news(page)

            for a_news in news:

                upload_date = datetime.strptime(
                    a_news["focus_date"], "%Y-%m-%d %H:%M:%S"
                )
                url = a_news["url"].replace("https", "http")
                if not self.add_news(
                    app_name=self.app_name,
                    app_chinese_name=self.app_chinese_name,
                    url=url,
                    title=a_news["title"],
                    upload_date=upload_date,
                    tags=a_news["keywords"]
                ):
                    return

    def get_news_content(self, url: str) -> str:
        element_path = "//div[@id='content_area' or @id='text_area' or id='wrapperbox']/p"
        return self.get_div_all_content(url=url, element_path=element_path)
