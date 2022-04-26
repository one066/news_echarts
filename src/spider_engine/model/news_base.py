from datetime import datetime
from typing import Optional

import requests
from lxml import etree
from requests import Response
from urllib3.exceptions import ReadTimeoutError

from utils.head import random_head


class NewsBase:
    """
    新闻 基类
    """

    def __init__(self):
        self.news: list = []
        self.last_title: Optional[str] = None

    def set_last_title(self, last_title: str) -> None:
        self.last_title = last_title

    def get(self,
            url: str,
            time_out: int = 5,
            encoding: str = "utf-8") -> Optional[Response]:
        # TODO 有需求则添加 ip 代理
        try:
            _response = requests.get(
                url, timeout=time_out, headers={"User-Agent": random_head()}
            )
        except ReadTimeoutError:
            print(url, '     failed')
            return

        _response.encoding = encoding
        return _response

    def get_div_all_content(
        self,
        url: str,
        element_path: str,
        encoding: str = "utf-8"
    ) -> Optional[str]:
        """ 得到 div 下所有文字
        """
        _response = self.get(url, encoding=encoding)
        html = etree.HTML(_response.text)

        # 去除 js 代码
        for _element in html.xpath('//script'):
            _element.getparent().remove(_element)

        elements = html.xpath(element_path)
        if not elements:
            return

        return "\n".join([
            element.xpath('string(.)').strip() for element in elements
        ])

    def get_news_header(self):
        """ 得到新闻 header 信息 如: urls、titles、upload_dates、tags
        """
        raise NotImplementedError

    def get_news_content(self, url: str) -> str:
        """得到正文
        """
        raise NotImplementedError

    def add_news(
        self, app_name: str, app_chinese_name: str, url: str, title: str,
        upload_date: datetime, tags: str
    ) -> bool:
        # 如果已经存在
        if title == self.last_title:
            return False

        # 如果已经不是今天的新闻
        if datetime.now().date() != upload_date.date():
            return False

        self.news.append({
            "app_name": app_name,
            "app_chinese_name": app_chinese_name,
            "url": url,
            "title": title,
            "upload_date": upload_date,
            "tags": tags
        })
        return True
