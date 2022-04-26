import ujson
from flask import Blueprint
from flask_socketio import emit

from apps.news_echarts.models.chat import Chat
from apps.news_echarts.validator import GetMessageSerialize
from extension.flask.api import class_route, login_require
from extension.flask.views import GetView
from extension.socketio import socket_io

chat_services_api = Blueprint('chat', __name__, url_prefix='/v1/service/chat')


@class_route(chat_services_api, '')
@login_require
class GetMessageService(GetView):
    """
    得到消息
    """
    serialize_class = GetMessageSerialize

    def action(self):
        chat_db = Chat()
        messages = chat_db.get()
        return {"messages": messages}


@socket_io.on('echo', namespace='/echo')
def echo(message):

    chat_db = Chat()

    result = ujson.loads(message)
    chat_db.add(
        user_id=result["user_id"],
        content=result["content"],
        name=result["name"]
    )

    emit('echo', message, broadcast=True)
