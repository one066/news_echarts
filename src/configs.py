import os

from extension.base_config import BaseConfig


class Development(BaseConfig):
    DEBUG = True
    STAGE = 'development'

    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{os.environ.get("MYSQL_USER")}:{os.environ.get("MYSQL_PASSWORD")}' \
                              f'@{os.environ.get("MYSQL_HOST")}:3306/news_echarts?charset=utf8'

    REDIS_HOST = os.environ.get("REDIS_HOST")
    REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD")


class Testing(BaseConfig):
    DEBUG = True
    STAGE = 'testing'

    TESTING = True


class Production(BaseConfig):
    STAGE = 'production'
