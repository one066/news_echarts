import os


class BaseConfig:
    # flask
    SECRET_KEY = os.urandom(24)
    KEY = "x9uo3L1xDDcF58Pt"

    # 定时任务配置
    SCHEDULER_API_ENABLED = True
    SCHEDULER_TIMEZONE = 'Asia/Shanghai'
    JOBS = [
        {
            'id': 'No1',
            'func': 'tasks.spider_task:update_news',
            'args': '',
            'trigger': {
                'type': 'cron',
                'day': '25',
                'hour': '7,12,15',
                'minute': '20',
                'second': '1'
            }
        },
        {
            'id': 'No2',
            'func': 'tasks.spider_task:clear_news',
            'args': '',
            'trigger': {
                'type': 'cron',
                'day': '25',
                'hour': '7',
                'minute': '1',
                'second': '1'
            }
        },
    ]

    # mysql
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@msyql:3306/news_echarts?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_POOL_SIZE = 10
    SQLALCHEMY_POOL_RECYCLE = 30
    SQLALCHEMY_POOL_TIMEOUT = 25
    SQLALCHEMY_PRE_PING = True
    SQLALCHEMY_TIME_OUT = 86400

    # redis
    REDIS_HOST = 'redis'
    REDIS_PASSWORD = ''

    # email
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_DEBUG = True
    MAIL_USERNAME = '2531210067@qq.com'
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_ASCII_ATTACHMENTS = True
