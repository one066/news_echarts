from flask import Blueprint

from apps.news_echarts.models.news import News, NewsExtension
from apps.news_echarts.models.simple import Simple
from apps.news_echarts.models.user_view_history import UserViewHistory
from apps.news_echarts.validator import (
    AnalysisResultServiceSerialize,
    ClickServiceSerialize,
    DataSerialize,
    GetNewsServiceSerialize,
    HotSearchSerialize,
    NewsIdServiceValidated,
    RecommendedNewsSerialize,
    TopWordsSerialize,
    UpdateNewsValidated,
)
from extension.flask.api import cache, class_route, login_require
from extension.flask.views import GetView, PatchView, PostView
from news_analysis_engine.controller.recommended_news_controller import (
    RecommendedNewsController,
)
from spider_engine.controller.get_hot_search_controller import (
    GetHotSearchController,
)
from utils.utils import read_cut_news

news_services_api = Blueprint('news', __name__, url_prefix='/v1/service/news')


@class_route(news_services_api, 'header')
@login_require
class GetNewHeaderService(GetView):
    """
    得到 new id、app_chinese_name、title、url、upload_date
    """
    serialize_class = GetNewsServiceSerialize

    def action(self):
        news_db = News()
        news = news_db.get_news_by_desc_time()
        return {"news": news}


@class_route(news_services_api, 'analysis_result')
@login_require
class GetNewAnalysisResultService(PostView):
    """
    得到 news 分析结果
    """
    validated_class = NewsIdServiceValidated
    serialize_class = AnalysisResultServiceSerialize

    def action(self):
        news_id = self.validated_data["news_id"]

        news_extension_db = NewsExtension()
        analysis_result = news_extension_db.get_news_analysis_result_by_id(
            news_id
        )

        return {"analysis_result": analysis_result}


@class_route(news_services_api, 'click')
@login_require
class ClickNewsService(PostView):
    """
    点击 news
    """
    validated_class = NewsIdServiceValidated
    serialize_class = ClickServiceSerialize

    def action(self):
        news_id = self.validated_data["news_id"]
        user_id = self.get_user_id()

        news_db = News()
        news = news_db.get_news_by_news_id(news_id)

        # 加到 观看历史
        user_view_history_db = UserViewHistory()
        user_view_history_db.add(user_id, news.title, news.url)

        # 新闻点击次数 +1
        news_extension_db = NewsExtension()
        news_extension_db.click(news_id)
        return news


@class_route(news_services_api, 'view_history')
@login_require
@cache(ttl=60 * 10, only=True)
class ViewHistoryNewsService(GetView):
    """
    得到玩家 观看历史
    """
    serialize_class = GetNewsServiceSerialize

    def action(self):
        user_id = self.get_user_id()
        # 加到 观看历史
        user_view_history_db = UserViewHistory()
        news = user_view_history_db.get(user_id)

        return {"news": news}


@class_route(news_services_api, 'recommended')
@login_require
@cache(only=True)
class RecommendedNewsService(GetView):
    """
    根据观看历史、推荐10篇新闻
    """
    serialize_class = RecommendedNewsSerialize

    def action(self):
        user_id = self.get_user_id()

        user_view_history_db = UserViewHistory()
        user_view_history = user_view_history_db.get(user_id)

        news_words = read_cut_news()

        recommended_news_controller = RecommendedNewsController()
        recommended_news_controller.set_key_words(user_view_history)
        recommended_news_controller.set_news_words(news_words)
        top_ten_news_ids = recommended_news_controller.run()

        news_db = News()
        top_ten_news = news_db.get_news_by_news_ids(top_ten_news_ids)

        return {"top_ten_news": top_ten_news}


@class_route(news_services_api, 'news_num_by_app')
@login_require
@cache()
class NewsNumService(GetView):
    """
    得到每个平台 新闻数量
    """
    serialize_class = DataSerialize

    def action(self):
        news_db = News()
        data = news_db.get_news_num_by_app()
        return {"data": data}


@class_route(news_services_api, 'emotional_total')
@login_require
@cache()
class EmotionalTotalService(GetView):
    """
    情感统计
    """
    serialize_class = DataSerialize

    def action(self):
        news_extension_db = NewsExtension()
        data = news_extension_db.get_emotional_total()
        return {"data": data}


@class_route(news_services_api, 'news_num_by_provinces')
@login_require
@cache()
class NewsNumByProvincesService(GetView):
    """
    得到每个省份新闻数量
    """
    serialize_class = DataSerialize

    def action(self):
        news_extension_db = NewsExtension()
        data = news_extension_db.get_news_num_by_provinces()
        return {"data": data}


@class_route(news_services_api, 'news_top_click_by_app')
@login_require
@cache()
class NewsTopClickByAppService(GetView):
    """
    得到各个新闻平台点击量前10的新闻
    """
    serialize_class = DataSerialize

    def action(self):
        news_extension_db = NewsExtension()
        data = news_extension_db.get_news_top_click_by_app()
        return {"data": data}


@class_route(news_services_api, 'top_words')
@login_require
class TopWordsService(GetView):
    """
    得到所有新闻热词前10
    """
    serialize_class = TopWordsSerialize

    def action(self):
        simple_db = Simple("top_words")
        return simple_db.get()


@class_route(news_services_api, 'hot_search')
@login_require
@cache(ttl=60 * 10)
class HotSearchService(GetView):
    """
    微博、bili bili、百度、知乎 热搜前十
    """
    serialize_class = HotSearchSerialize

    def action(self):
        get_hot_search_controller = GetHotSearchController()
        hot_search = get_hot_search_controller.run()
        return {"hot_search": hot_search}


@class_route(news_services_api, '')
@login_require
class UpdateNewsService(PatchView):
    """
    更新新闻
    """
    validated_class = UpdateNewsValidated

    def action(self):
        news_extension_db = NewsExtension()
        news_extension_db.update(**self.validated_data)
