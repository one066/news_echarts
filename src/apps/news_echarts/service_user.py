from flask import Blueprint

from apps.news_echarts.models.user import User
from apps.news_echarts.models.verification_code import VerificationCode
from apps.news_echarts.validator import (
    EmailLoginValidated,
    EmailValidated,
    LoginValidated,
    ModifyInformationValidated,
    ProfileSerialize,
    UserTokenSerialize,
)
from extension.flask.api import class_route, login_require
from extension.flask.views import GetView, PatchView, PostView
from extension.models.token import Token
from SDK.qq_email import OneEmail
from utils.utils import save_photo

user_services_api = Blueprint('user', __name__, url_prefix='/v1/service/user')


@class_route(user_services_api, 'send_verification_code')
class SendVerificationCodeService(PostView):
    """
    注册验证码
    """
    validated_class = EmailValidated

    def action(self):
        email = self.validated_data["email"]

        verification_code_db = VerificationCode()
        _verification_code = verification_code_db.create(email)

        # 发送验证码
        one_email = OneEmail()
        one_email.add_message(
            subject="验证码",
            recipients=[email],
            body=f'你的验证码为：{_verification_code}'
        )
        one_email.send()


@class_route(user_services_api, 'login')
class UserLoginService(PostView):
    """
    登录
    """
    validated_class = LoginValidated
    serialize_class = UserTokenSerialize

    def action(self):
        nick_name_or_email = self.validated_data["nick_name_or_email"]
        password = self.validated_data["password"]

        user_db = User()
        user_id, nick_name = user_db.login_check(nick_name_or_email, password)

        token_db = Token()
        return {
            "token": token_db.get(user_id),
            "user_id": user_id,
            "nick_name": nick_name
        }


@class_route(user_services_api, 'email_login')
class UserEmailLoginService(PostView):
    """
    邮箱登录
    """
    validated_class = EmailLoginValidated
    serialize_class = UserTokenSerialize

    def action(self):
        email = self.validated_data["email"]
        verification_code = self.validated_data["verification_code"]

        user_db = User()

        # 没有注册则注册一个账号
        if not user_db.email_is_exist(email):
            user_id, nick_name = user_db.create(email)
        else:
            user_id, nick_name = user_db.get_user_id_and_name_by_email(email)

        # 检查 验证码
        verification_code_db = VerificationCode()
        verification_code_db.check(email, verification_code)

        token_db = Token()
        return {
            "token": token_db.get(user_id),
            "user_id": user_id,
            "nick_name": nick_name
        }


@class_route(user_services_api, 'modify_information')
@login_require
class ModifyInformationService(PatchView):
    """
    修改资料
    """
    decorators = [login_require]
    validated_class = ModifyInformationValidated
    serialize_class = UserTokenSerialize

    def action(self):
        user_id = self.get_user_id()

        user_db = User()
        photo_base64 = self.validated_data.get("photo_base64")
        nick_name = self.validated_data.get("nick_name")

        if photo_base64:
            save_photo(photo_base64, user_id)
            # TODO 暂时不保存进数据库
            self.validated_data.pop("photo_base64")

        if nick_name:
            # 检查 nickname 是否存在
            user_db.nick_name_check(nick_name)
        if not self.validated_data:
            return

        user_db.update(user_id, **self.validated_data)


@class_route(user_services_api, 'profile')
@login_require
class UserProfileService(GetView):
    """
    得到用户的资料
    """
    decorators = [login_require]
    serialize_class = ProfileSerialize

    def action(self):
        user_id = self.get_user_id()

        user_db = User()
        profile = user_db.get(user_id)
        return profile
