from datetime import datetime

from lxml import etree

from spider_engine.model.news_base import NewsBase


class ChinaNews(NewsBase):
    """
    中国新闻网滚动新闻
    """
    CHINA_NEWS_URL = "http://www.chinanews.com.cn/scroll-news/news{page}.html"

    def __init__(self):
        super().__init__()

        self.app_name = "china_news"
        self.app_chinese_name = "中国新闻网"

    def _get_page_news(self, page: int) -> tuple:
        _response = self.get(self.CHINA_NEWS_URL.format(page=page))
        html = etree.HTML(_response.text)

        tags = html.xpath('//div[@class="dd_lm"]/a/text()')
        titles = html.xpath('//div[@class="dd_bt"]/a/text()')
        urls = html.xpath('//div[@class="dd_bt"]/a/@href')
        update_times = html.xpath('//div[@class="dd_time"]/text()')

        return tags, titles, urls, update_times

    @staticmethod
    def _refactoring_update_time(update_time: str) -> datetime:
        """重构 update_time | `2-15 15:38` update to `2022-02-15 15:38:30`
        """
        now_year: int = datetime.now().year

        # update_time format is `2-15 15:38`
        return datetime.strptime(
            f"{now_year}-{update_time}:30", "%Y-%m-%d %H:%M:%S"
        )

    def get_news_header(self) -> None:
        for page in range(1, 100):

            now_page_news = self._get_page_news(page)

            for tag, title, url, update_time in zip(*now_page_news):

                upload_date = self._refactoring_update_time(update_time)
                if not self.add_news(
                    app_name=self.app_name,
                    app_chinese_name=self.app_chinese_name,
                    url="http://www.chinanews.com.cn" + url,
                    title=title,
                    upload_date=upload_date,
                    tags=tag
                ):
                    return

    def get_news_content(self, url: str) -> str:
        element_path = "//div[@class='left_zw' or @class='content_desc']/p"
        return self.get_div_all_content(url=url, element_path=element_path)
