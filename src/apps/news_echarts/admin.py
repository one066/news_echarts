from flask import Blueprint

from apps.news_echarts.models.admin import Admin
from apps.news_echarts.models.news import NewsExtension
from apps.news_echarts.validator import (
    AnalysisResultServiceSerialize,
    LoginValidated,
    UserTokenSerialize,
)
from extension.flask.api import class_route
from extension.flask.views import GetView, PostView
from extension.models.token import Token

admin = Blueprint('admin', __name__, url_prefix='/admin')


@class_route(admin, 'admin_login')
class AdminLoginService(PostView):
    """
    登录
    """
    validated_class = LoginValidated
    serialize_class = UserTokenSerialize

    def action(self):
        nick_name = self.validated_data["nick_name_or_email"]
        password = self.validated_data["password"]

        _admin = Admin()
        user_id, nick_name = _admin.login_check(nick_name, password)

        token_db = Token()
        return {
            "token": token_db.get(user_id),
            "user_id": user_id,
            "nick_name": nick_name
        }


@class_route(admin, '/news')
class GetAllNewAnalysisResultService(GetView):
    """
    得到 news
    """
    serialize_class = AnalysisResultServiceSerialize

    def action(self):

        news_extension_db = NewsExtension()
        analysis_result = news_extension_db.get_news_analysis_result()
        return {"analysis_result": analysis_result}
