from apps.news_echarts.exception import WrongPassword
from extension.mysql_client import db


class Admin(db.Model):
    """
    管理员
    """
    __tablename__ = 'admin'
    user_id = db.Column(db.String(32), nullable=True, primary_key=True)
    nick_name = db.Column(db.String(30), nullable=True)
    password = db.Column(db.String(30))

    @classmethod
    def login_check(cls, nickname: str, password: str):
        """登录检查
        """
        result = db.session.query(cls.user_id, cls.password, cls.nick_name) \
            .filter(cls.nick_name == nickname) \
            .first()

        if password != result["password"]:
            raise WrongPassword

        return result["user_id"], result["nick_name"]

    # TODO 展示就不做添加的接口了、手动添加账号就足够了
