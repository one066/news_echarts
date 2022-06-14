import os

from flask import Blueprint, render_template

from extension.flask.api import login_require

front_end_views = Blueprint(
    'front_end_views',
    __name__,
    url_prefix='/echarts_news',
    template_folder='template',
    static_url_path='',
    static_folder='static'
)

record_number = os.environ.get("RECORD_NUMBER")


@front_end_views.route('/home', methods=['GET'])
@login_require
def home():

    return render_template('home.html', record_number=record_number)


@front_end_views.route('/news', methods=['GET'])
@login_require
def news():

    return render_template('news.html', record_number=record_number)


@front_end_views.route('/chat', methods=['GET'])
@login_require
def chat():

    return render_template('chat.html', record_number=record_number)


@front_end_views.route('/profile', methods=['GET'])
@login_require
def profile():

    return render_template('profile.html', record_number=record_number)


@front_end_views.route('/show', methods=['GET'])
@login_require
def show():

    return render_template('show.html', record_number=record_number)


@front_end_views.route('/login', methods=['GET'])
def login():

    return render_template('login.html', record_number=record_number)


@front_end_views.route('/admin_login', methods=['GET'])
def admin_login():

    return render_template('admin_login.html', record_number=record_number)


@front_end_views.route('/update_news', methods=['GET'])
@login_require
def update_news():

    return render_template('update_news.html', record_number=record_number)
