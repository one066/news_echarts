import random
import uuid

from apps.news_echarts.exception import UserNickNameAlreadyExist, WrongPassword
from extension.mysql_client import db


def generate_user_id() -> str:
    return uuid.uuid4().hex


def generate_nick_name() -> str:
    _letters_string = "".join([
        random.choice('ABCDEFGHIJKLMNOPQUVWXYZabcdefghijklmnopquvwxyz')
        for _ in range(5)
    ])
    _int_string = "".join([random.choice('0123456789') for _ in range(12)])
    return f"{_letters_string}-{_int_string}"


class User(db.Model):
    """
    用户
    """
    __tablename__ = 'user'
    user_id = db.Column(db.String(32), nullable=True, primary_key=True)
    email = db.Column(db.String(30), nullable=True)
    nick_name = db.Column(db.String(30), nullable=True)
    password = db.Column(db.String(30))
    phone_number = db.Column(db.String(30))
    introduction = db.Column(db.TEXT)  # 简介
    photo_base64 = db.Column(db.TEXT)  # 头像的 base64 编码

    @classmethod
    def email_is_exist(cls, email: str) -> bool:
        """ 检查 email 是否已经存在
        """
        email = db.session.query(cls.email).filter(cls.email == email).first()
        return bool(email)

    @classmethod
    def get_user_id_and_name_by_email(cls, email: str) -> tuple:
        """ 通过 user_id 得到 email
        """
        _user = db.session.query(cls.user_id,
                                 cls.nick_name).filter(cls.email == email
                                                      ).first()
        return _user.user_id, _user.nick_name

    @classmethod
    def nick_name_check(cls, nick_name: str) -> None:
        """ 检查 nick_name 是否已经存在
        """
        if db.session.query(cls.nick_name).filter(cls.nick_name == nick_name
                                                 ).first():
            raise UserNickNameAlreadyExist

    @classmethod
    def login_check(cls, nick_name_or_email: str, password: str) -> tuple:
        """ 登录检查
        """
        # 尝试 nick_name 登录
        result = db.session.query(cls.user_id, cls.password, cls.nick_name)\
            .filter(cls.nick_name == nick_name_or_email)\
            .first()

        if not result:
            # 尝试 email 登录
            result = db.session.query(cls.user_id, cls.password, cls.nick_name)\
                .filter(cls.email == nick_name_or_email)\
                .first()

        if password != result["password"]:
            raise WrongPassword

        return result["user_id"], result["nick_name"]

    @classmethod
    def create(cls, email: str) -> tuple:
        user_id = generate_user_id()
        nick_name = generate_nick_name()
        db.session.add(
            User(
                user_id=user_id,
                email=email,
                nick_name=nick_name,
            )
        )

        db.session.commit()
        return user_id, nick_name

    @classmethod
    def update(cls, user_id: str, **information) -> None:
        db.session.query(cls).filter(cls.user_id == user_id).update(information)
        db.session.commit()

    @classmethod
    def get(cls, user_id: str) -> dict:
        _user = db.session.query(
            cls.user_id, cls.email, cls.phone_number, cls.introduction,
            cls.nick_name
        ).filter(cls.user_id == user_id).first()
        return dict(_user)

    @classmethod
    def get_photo(cls, user_id: str) -> dict:
        _user = db.session.query(cls.photo_base64
                                ).filter(cls.user_id == user_id).first()
        return dict(_user)
