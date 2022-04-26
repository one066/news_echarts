import json
import re
import urllib.parse
from typing import Optional

import requests
from requests import Response

from utils.head import random_head


class TopSearch:
    """
    微博、bili bili、百度、知乎 热搜前十
    """
    BILI_BILI_HOT_URL = 'http://api.bilibili.com/x/web-interface/search/square?limit=10'
    WEI_BO_HOT_URL = "http://weibo.com/ajax/side/hotSearch"
    BAI_DU_HOT_URL = "http://www.baidu.com/s?wd=%E8%99%9A%E5%B9%BBblog&rsv_spt=1&" \
                     "rsv_iqid=0x8424c7bd00024a91&issp=1&f=8&rsv_bp=1&rsv_idx=2&ie=utf-8&tn=baiduhome_pg&" \
                     "rsv_dl=ib&rsv_enter=0&rsv_sug3=11&rsv_sug1=10&rsv_sug7=100&rsv_btype=i&" \
                     "inputT=8722&rsv_sug4=8722 "
    ZHI_HU_HOT_URL = "http://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=50&desktop=true"

    def __init__(self):
        self.top_num: int = 10

    def _get(self, url: str) -> Optional[Response]:
        _response = requests.get(
            url, timeout=5, headers={"User-Agent": random_head()}
        )
        return _response

    def bili_bili_top(self) -> list[dict]:
        """ bili_bili 热搜前十"""
        _response = self._get(self.BILI_BILI_HOT_URL)

        _result = json.loads(_response.text)["data"]["trending"]["list"]
        return [{
            _result[_index]["show_name"]:
                f"https://search.bilibili.com/all?keyword={urllib.parse.quote(_result[_index]['keyword'])}"
        } for _index in range(self.top_num)]

    def bai_du_top(self) -> list[dict]:
        """ baidu 热搜前十"""
        _response = self._get(self.BAI_DU_HOT_URL)

        _result = re.findall(
            'pmd"><!--s-data:(.*)--', _response.content.decode()
        )

        _result = json.loads(_result[0])["bdlistGroup"][0]
        return [{
            _result[_index]["link"]:
                "https://www.baidu.com/" + _result[_index]["leftUrl"]
        } for _index in range(self.top_num)]

    def zhi_hu_top(self) -> list[dict]:
        """ zhi hu 热搜前十"""
        _response = self._get(self.ZHI_HU_HOT_URL)

        _result = json.loads(_response.text)["data"]
        return [{
            _result[_index]["target"]["title"]:
                f'https://www.zhihu.com/question/{_result[_index]["target"]["id"]}'
        } for _index in range(self.top_num)]

    def wei_bo_top(self) -> list[dict]:
        """ 微博 热搜前十"""
        _response = self._get(self.WEI_BO_HOT_URL)

        _result = json.loads(_response.text)["data"]["realtime"]
        return [{
            _result[_index]["word"]:
                f"https://s.weibo.com/weibo?q=%23{urllib.parse.quote(_result[_index]['word'])}%23&Refer=top"
        } for _index in range(self.top_num)]
