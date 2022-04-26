from flask import Blueprint

from apps.news_echarts.models.news import News, NewsExtension
from apps.news_echarts.models.simple import Simple
from apps.news_echarts.validator import (
    TopWordsSerialize,
    UpdateNewestNewsServiceSerialize,
)
from extension.flask.api import class_route
from extension.flask.views import GetView, PostView
from extension.mysql_client import db
from news_analysis_engine.controller.all_news_top_word_controller import (
    AllNewsTopWordController,
)
from news_analysis_engine.controller.news_analysis_controller import (
    NewsAnalysisController,
)
from news_analysis_engine.controller.recommended_news_controller import (
    RecommendedNewsController,
)
from spider_engine.controller.add_news_content_controller import (
    AddNewsContentController,
)
from spider_engine.controller.get_newest_news_header_controller import (
    GetNewestNewsHeaderController,
)
from utils.utils import save_cut_news

task_services_api = Blueprint('task', __name__, url_prefix='/v1/service/task')


@class_route(task_services_api, 'update_news')
class UpdateNewestNewsService(PostView):
    """
    news 爬虫
    """
    serialize_class = UpdateNewestNewsServiceSerialize

    def action(self):
        news_db = News()
        # 得到所有新闻平台最后一个 title
        all_app_last_title = news_db.get_all_app_last_title()

        # 获取 news header
        print("获取 news header")
        get_newest_news_header_controller = GetNewestNewsHeaderController()
        get_newest_news_header_controller.set_all_app_last_title(
            all_app_last_title
        )
        news_headers = get_newest_news_header_controller.run()

        # 获取 news content
        print("获取 news content")
        add_news_content_controller = AddNewsContentController()
        add_news_content_controller.set_news(news_headers)
        all_app_news = add_news_content_controller.run()

        # 批量添加到数据库
        db.session.bulk_insert_mappings(
            News, [
                dict(
                    app_name=a_news["app_name"],
                    app_chinese_name=a_news["app_chinese_name"],
                    title=a_news["title"],
                    url=a_news["url"],
                    upload_date=a_news["upload_date"],
                    content=a_news["content"],
                ) for a_news in all_app_news
            ]
        )
        db.session.commit()
        db.session.remove()

        return {"total": len(all_app_news), "news": all_app_news}


@class_route(task_services_api, 'analysis_news')
class AnalysisNewsService(PostView):
    """
    分析 news
    """

    def action(self):
        news_extension_db = NewsExtension()
        not_analysis_news = news_extension_db.get_not_analysis_news()

        # 进行分析
        news_analysis_controller = NewsAnalysisController()
        news_analysis_controller.set_news(not_analysis_news)
        news = news_analysis_controller.run()

        # 批量添加到数据库
        db.session.bulk_insert_mappings(
            NewsExtension, [
                dict(
                    news_id=a_news["news_id"],
                    words_count=a_news["words_count"],
                    keywords=a_news["keywords"],
                    abstract=a_news["abstract"],
                    positive=a_news["positive"],
                    provinces=a_news["provinces"],
                    number_of_clicks=10,
                ) for a_news in news
            ]
        )
        db.session.commit()
        db.session.remove()


@class_route(task_services_api, 'count_top_words')
class TopWordsTaskService(GetView):
    """
    计算得到所有新闻热词前 10
    """
    serialize_class = TopWordsSerialize

    def action(self):
        news_db = News()
        contents = news_db.get_news_content()

        all_news_top_word_controller = AllNewsTopWordController()
        all_news_top_word_controller.set_contents(contents)
        words = all_news_top_word_controller.run()

        simple_db = Simple("top_words")
        simple_db.add({"words": words})
        return {"words": words}


@class_route(task_services_api, 'cut_news')
class CutNewsTaskService(GetView):
    """
    新闻分词  主要是提前分词好，加快用户推荐速度
    """

    def action(self):
        news_db = News()
        news = news_db.get_news_content()

        recommended_news_controller = RecommendedNewsController()
        cut_news = recommended_news_controller.cut(news)

        # TODO 暂时直接保存在本地
        save_cut_news(cut_news)


@class_route(task_services_api, 'clear_news')
class ClearNewsService(PostView):
    """
    清空 表格
    """

    def action(self):
        db.session.query(NewsExtension).delete()
        db.session.query(News).delete()
        db.session.commit()
