import random

import ujson

from apps.news_echarts.exception import (
    VerificationCodeExpired,
    WrongVerificationCode,
)
from extension.redis_client import redis_client


def generate_verification_code() -> str:
    return str(random.randint(0, 999999)).rjust(6, '0')


class VerificationCode:
    """
    用户登录验证码
    """
    USER_VERIFICATION_CODE_KEY = "news_echarts:email:{email_id}:verification_code"
    # 保存 60 s
    TTL = 60

    def create(self, email_id: str) -> str:
        _verification_code = generate_verification_code()
        redis_client.set(
            self.USER_VERIFICATION_CODE_KEY.format(email_id=email_id),
            _verification_code
        )
        redis_client.expire(
            self.USER_VERIFICATION_CODE_KEY.format(email_id=email_id), self.TTL
        )
        return _verification_code

    def check(self, email_id: str, verification_code: str) -> None:
        _verification_code = redis_client.get(
            self.USER_VERIFICATION_CODE_KEY.format(email_id=email_id)
        )

        if not _verification_code:
            raise VerificationCodeExpired

        _verification_code = ujson.loads(_verification_code)
        if _verification_code != verification_code:
            raise WrongVerificationCode
