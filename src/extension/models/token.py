import random

from extension.redis_client import redis_client


def generate_token() -> str:
    _string = 'ABCDEFGHIJKLMNOPQUVWXYZ' \
              'abcdefghijklmnopquvwxyz' \
              '0123456789'
    return "".join([random.choice(_string) for _ in range(20)])


class Token:
    """
    用户 token
    """
    USER_TOKEN_KEY = "news_echarts:user:{user_id}:token"
    # 保存 7 天
    TTL = 60 * 60 * 12 * 7

    def get(self, user_id: str) -> str:
        """ 得到token
        """
        _token = redis_client.get(self.USER_TOKEN_KEY.format(user_id=user_id))

        # 如果没有新建一个
        if not _token:
            _token = generate_token()
            redis_client.set(
                self.USER_TOKEN_KEY.format(user_id=user_id), _token
            )
            redis_client.expire(
                self.USER_TOKEN_KEY.format(user_id=user_id), self.TTL
            )
        return _token

    def check(self, user_id: str, token: str) -> bool:
        _token = redis_client.get(self.USER_TOKEN_KEY.format(user_id=user_id))
        if not _token:
            return False

        return _token.decode() == token
