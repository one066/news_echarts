from typing import Dict, List, Optional

import ujson

from extension.redis_client import redis_client

UserViewHistoryResult = Optional[List[Dict]]


class UserViewHistory:
    """
    用户观看历史
    """
    USER_VIEW_HISTORY_KEY = "news_echarts:user:{user_id}:view_history"
    # 最大保存
    MAXIMUM_CAPACITY = 100

    def _keep_capacity(self, user_id):
        """ 保持不超过容量
        """
        history_length = redis_client.llen(
            self.USER_VIEW_HISTORY_KEY.format(user_id=user_id)
        )
        if self.MAXIMUM_CAPACITY < history_length:
            redis_client.rpop(
                self.USER_VIEW_HISTORY_KEY.format(user_id=user_id)
            )

    def add(self, user_id: str, title: str, url: str) -> None:
        redis_client.lrem(
            name=self.USER_VIEW_HISTORY_KEY.format(user_id=user_id),
            value=ujson.dumps({
                "title": title,
                "url": url
            }),
            count=0
        )
        redis_client.lpush(
            self.USER_VIEW_HISTORY_KEY.format(user_id=user_id),
            ujson.dumps({
                "title": title,
                "url": url
            })
        )

    def get(self, user_id) -> UserViewHistoryResult:
        history = redis_client.lrange(
            self.USER_VIEW_HISTORY_KEY.format(user_id=user_id), 0, -1
        )
        history = [ujson.loads(_history) for _history in history]
        return history
