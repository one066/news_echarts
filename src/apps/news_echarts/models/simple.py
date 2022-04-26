from typing import Union

import ujson

from extension.redis_client import redis_client


class Simple:
    """
    只做保持、读取的 redis
    """
    SIMPLE_KEY = "news_echarts:{name}"

    def __init__(self, name):
        self.key = self.SIMPLE_KEY.format(name=name)

    def add(self, data: Union[dict, list, str]) -> None:
        redis_client.set(self.key, ujson.dumps(data))

    def get(self) -> Union[dict, list, str]:
        return ujson.loads(redis_client.get(self.key))
