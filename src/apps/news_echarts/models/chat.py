import datetime

import ujson

from apps.news_echarts.exception import NotMessage
from extension.redis_client import redis_client


class Chat:
    """
    用户 chat
    """
    CHAT_KEY = "news_echarts:chat"
    # 最大保存
    MAXIMUM_CAPACITY = 100

    def get(self) -> list:
        """得到聊天记录
        """
        messages = redis_client.lrange(self.CHAT_KEY, 0, -1)
        if not messages:
            raise NotMessage

        return [ujson.loads(message) for message in messages][::-1]

    def _ensure_volume(self) -> None:
        """保证容量不超过最大容量"""
        history_length = redis_client.llen(self.CHAT_KEY)

        # 超出容量删除一个
        if self.MAXIMUM_CAPACITY < history_length:
            redis_client.rpop(self.CHAT_KEY)

    def add(self, user_id: str, content: str, name: str) -> None:
        """增加消息"""
        self._ensure_volume()
        redis_client.lpush(
            self.CHAT_KEY,
            ujson.dumps({
                "user_id": user_id,
                "content": content,
                "name": name,
                "at": datetime.datetime.now().astimezone().isoformat()
            })
        )
