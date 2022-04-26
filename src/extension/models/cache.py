from typing import Optional

import ujson

from extension.redis_client import redis_client


# TODO flask_cache 长期不维护，有问题 暂未找到替代品， 自己写了个
class Cache:
    """
    主页缓存
    """
    CACHE_KEY = "news_echarts:{api_name}"

    def __init__(self, api_name: str):

        self.api_name: str = api_name

        # 默认保存 1 h
        self.ttl = 60 * 60

    def update_ttl(self, ttl: int):
        self.ttl = ttl

    def save(self, data: dict) -> None:
        redis_client.set(
            self.CACHE_KEY.format(api_name=self.api_name), ujson.dumps(data)
        )
        redis_client.expire(
            self.CACHE_KEY.format(api_name=self.api_name), self.ttl
        )

    def get(self) -> Optional[dict]:
        data = redis_client.get(self.CACHE_KEY.format(api_name=self.api_name))
        if data:
            return ujson.loads(data)

        return
