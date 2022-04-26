from apps.news_echarts.admin import admin
from apps.news_echarts.service_chat import chat_services_api
from apps.news_echarts.service_news import news_services_api
from apps.news_echarts.service_task import task_services_api
from apps.news_echarts.service_user import user_services_api

blueprints = [
    task_services_api, news_services_api, user_services_api, chat_services_api,
    admin
]

__all__ = ['blueprints']
