from sqlalchemy import desc
from sqlalchemy.engine import Row

from extension.mysql_client import db
from utils.utils import news_update_time_to_str

NewsByDescTimeResult = list[dict]


class News(db.Model):
    """
    新闻
    """
    __tablename__ = 'news'
    news_id = db.Column(
        db.Integer, autoincrement=True, nullable=False, primary_key=True
    )
    app_name = db.Column(db.String(20), nullable=True)
    app_chinese_name = db.Column(db.String(20), nullable=True)
    title = db.Column(db.String(150), nullable=True)
    url = db.Column(db.String(150), nullable=True)
    upload_date = db.Column(db.DateTime, nullable=True)
    content = db.Column(db.TEXT)

    @classmethod
    def get_all_app_last_title(cls) -> dict:
        """ 得到所有新闻平台最后一个 title
        """
        results = db.session.query(cls.title, cls.app_name).group_by(
            cls.app_name
        ).order_by(desc(cls.upload_date)).all()

        db.session.remove()
        return {_result.app_name: _result.title for _result in results}

    @classmethod
    def get_apps_chinese_name(cls) -> list:
        """ 得到 apps_chinese_name
        """
        news = db.session.query(cls.app_chinese_name
                               ).group_by(cls.app_chinese_name).all()

        return [a_news.app_chinese_name for a_news in news]

    @classmethod
    def get_news_by_news_id(cls, news_id) -> Row:
        """ 通过 news_id 得到 title、url
        """
        news = db.session.query(
            cls.news_id, cls.app_chinese_name, cls.title, cls.url,
            cls.upload_date
        ).filter(cls.news_id == news_id).first()
        return news

    @classmethod
    def get_news_by_news_ids(cls, news_ids: list) -> list:
        """ 通过 news_ids 得到 title、url
        """
        news = db.session.query(
            cls.news_id, cls.app_chinese_name, cls.title, cls.url,
            cls.upload_date
        ).filter(cls.news_id.in_(news_ids)).all()

        news = [a_news._asdict() for a_news in news]
        return [news_update_time_to_str(a_news) for a_news in news]

    @classmethod
    def get_news_content(cls) -> list[Row]:
        """ 通过 news_id 得到 title、url
        """
        return db.session.query(cls.news_id, cls.content).all()

    @classmethod
    def get_news_num_by_app(cls) -> dict:
        """  得到每个平台 新闻数量
        """
        news = db.session.query(
            cls.app_chinese_name,
            db.func.count('*').label("count")
        ).group_by(cls.app_chinese_name).all()

        return dict(news)

    @classmethod
    def get_news_by_desc_time(cls) -> NewsByDescTimeResult:
        """ 得到新闻通过时间降序
        """
        news = db.session.query(
            cls.news_id, cls.app_chinese_name, cls.title, cls.url,
            cls.upload_date
        ).join(
            NewsExtension, cls.news_id == NewsExtension.news_id, isouter=True
        ).order_by(desc(cls.upload_date)
                  ).filter(NewsExtension.news_id.isnot(None)).all()

        news = [a_news._asdict() for a_news in news]
        return [news_update_time_to_str(a_news) for a_news in news]


class NewsExtension(db.Model):
    """
    新闻扩展
    分开主要是为了增加功能避免破坏原始数据
    """
    __tablename__ = 'news_extension'
    news_id = db.Column(db.Integer, nullable=False, primary_key=True)
    words_count = db.Column(db.TEXT, nullable=True)
    keywords = db.Column(db.TEXT, nullable=True)
    abstract = db.Column(db.TEXT, nullable=True)
    positive = db.Column(db.String(50), nullable=True)
    provinces = db.Column(db.String(50))
    number_of_clicks = db.Column(db.Integer, nullable=True)

    @classmethod
    def get_not_analysis_news(cls) -> list[Row]:
        """ 得到没有分析处理过的新闻
        """
        news = db.session.query(News.news_id, News.title, News.content).join(
            cls, cls.news_id == News.news_id, isouter=True
        ).filter(cls.news_id.is_(None)).all()

        db.session.remove()
        return [a_news._asdict() for a_news in news]

    @classmethod
    def get_news_analysis_result_by_id(cls, news_id: int) -> list:
        """ 得到 news 分析结果
        """
        analysis_result = db.session.query(
            cls.news_id, cls.words_count, cls.keywords, cls.abstract,
            cls.positive, News.url, News.title, cls.number_of_clicks
        ).join(cls, cls.news_id == News.news_id,
               isouter=True).filter(cls.news_id == news_id).first()
        return analysis_result._asdict()

    @classmethod
    def get_news_analysis_result(cls) -> list:
        """ 得到 news 分析结果
        """
        analysis_result = db.session.query(
            cls.news_id, cls.keywords, cls.abstract, cls.positive, News.url,
            News.title, News.app_chinese_name, cls.number_of_clicks
        ).join(cls, cls.news_id == News.news_id, isouter=True).all()

        return [
            a_analysis_result._asdict() for a_analysis_result in analysis_result
        ]

    @classmethod
    def click(cls, news_id: int) -> None:
        """ click: number_of_clicks + 1
        """
        number_of_clicks = db.session.query(cls.number_of_clicks
                                           ).filter(cls.news_id == news_id
                                                   ).first().number_of_clicks
        db.session.query(cls).filter(cls.news_id == news_id).update({
            "number_of_clicks": number_of_clicks + 1
        })

        db.session.commit()

    @classmethod
    def get_emotional_total(cls) -> dict:
        """  情感统计
        """
        news = db.session.query(
            cls.positive,
            db.func.count('*').label("count")
        ).group_by(cls.positive).all()
        return dict(news)

    @classmethod
    def get_news_num_by_provinces(cls) -> dict:
        """  各省新闻统计
        """
        news = db.session.query(
            cls.provinces,
            db.func.count('*').label("count")
        ).group_by(cls.provinces).filter(cls.provinces.isnot(None)).all()
        return dict(news)

    @classmethod
    def get_news_top_click_by_app(cls) -> dict:
        """  得到各个新闻平台点击量前10的新闻
        """
        apps_name = News.get_apps_chinese_name()
        apps_top_news = {}
        for app_name in apps_name:

            # 得到当前 app_name 点击降序的前 10
            app_top_news = db.session.query(
                News.news_id, News.title, News.url, News.app_chinese_name,
                cls.number_of_clicks
            ).join(cls, cls.news_id == News.news_id, isouter=True).order_by(
                desc(cls.number_of_clicks)
            ).filter(News.app_chinese_name == app_name).limit(10).all()

            # 将 每个 新闻内容转为 字典
            apps_top_news[app_name] = [
                a_news._asdict() for a_news in app_top_news
            ]
        return apps_top_news

    @classmethod
    def update(cls, **news_information) -> None:
        """ 更新 news 内容
        """
        db.session.query(cls).filter(
            cls.news_id == news_information["news_id"]
        ).update(news_information)

        db.session.commit()
