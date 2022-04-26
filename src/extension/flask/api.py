from functools import wraps

from flask import Blueprint, jsonify, redirect, request, url_for
from flask.views import MethodView, MethodViewType
from marshmallow import ValidationError

from extension.flask.exceptions import TokenFailed
from extension.models.cache import Cache
from extension.models.token import Token


def ok_response(result):
    body = {'ok': True, 'result': result}
    return jsonify(body)


def failed_response(error_type, error_message):
    body = {
        'ok': False,
        'error_type': error_type,
        'error_message': error_message,
    }
    return jsonify(body)


def class_route(blueprint: Blueprint, rule, **options):
    """class view 的路由
    """

    def decorator(view):
        if isinstance(view, MethodViewType):
            view_func = view.as_view(view.__name__)
        else:
            view_func = view

        blueprint.add_url_rule(
            rule, view.__name__, view_func=view_func, **options
        )
        return view

    return decorator


def handle_exception(view_name, exception, **kwargs):
    """处理异常
    APIException: 返回适当的错误信息
    else: 重新抛出异常
    """
    if isinstance(exception, ValidationError):
        return failed_response(
            error_type='ValidationError',
            error_message=exception.messages,
        )
    elif hasattr(exception,
                 'error_type') and hasattr(exception, 'error_message'):
        return failed_response(
            error_type=exception.error_type,
            error_message=exception.error_message,
        )
    else:
        raise exception


class APIBaseView(MethodView):
    """扩展 class based view, 增加异常处理
    """

    @property
    def user_id(self):
        return request.headers.get('x-authenticated-userid', None)

    @classmethod
    def parse_json(cls):
        """解析 request body 为 json
        """
        return request.json or {}

    @classmethod
    def get_user_id(cls):
        user_id = request.cookies.get('user_id')
        if not user_id:
            raise TokenFailed
        return user_id

    def dispatch_request(self, *args, **kwargs):
        try:
            return super().dispatch_request(*args, **kwargs)
        except Exception as exception:
            return handle_exception(
                self.__class__.__name__, exception, **kwargs
            )


def token_check():
    cookie = request.cookies

    token = cookie.get('token')
    user_id = cookie.get('user_id')

    if not token or not user_id:
        return False

    token_db = Token()
    return token_db.check(user_id, token)


def login_require(view):
    """
    登录检查
    """

    @wraps(view)
    def decorator(*args, **kwargs):

        token = token_check()
        if not token and isinstance(view, MethodViewType):
            return failed_response(
                error_type="Token failed", error_message="Token failed"
            )
        if not token:
            return redirect(url_for('front_end_views.login'))

        if isinstance(view, MethodViewType):
            return view.as_view(view.__name__)()

        return view(*args, **kwargs)

    return decorator


def cache(name=None, ttl=60 * 60 * 2, only=False):
    """缓存装饰器"""

    def inter(view):

        @wraps(view)
        def wrapper(*args, **kwargs):

            _name = name

            # 没有传name就使用 request.path
            if not _name:
                _name = request.path.split('/')[-1]

            # 如果针对用户 key 添加 user_id
            if only:
                _name += f":{request.cookies.get('user_id')}"

            _cache = Cache(_name)

            # 有数据直接返回
            data = _cache.get()

            if data:
                return data

            else:
                if isinstance(view, MethodViewType):
                    _result = view.as_view(view.__name__)()
                else:
                    _result = view(*args, **kwargs)

                _cache.update_ttl(ttl)
                _cache.save(_result)
                return _result

        return wrapper

    return inter
