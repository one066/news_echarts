import gevent.monkey

gevent.monkey.patch_all()
import click  # noqa: E402

from apps.base import create_app  # noqa: E402
from extension.mysql_client import db  # noqa: E402
from extension.socketio import socket_io  # noqa: E402

app = create_app(config_name="development")


@click.group()
def cli():
    pass


@cli.command('create_db')
def create_db():
    click.echo('----->    start get mysql db     <-----')
    with app.app_context():
        db.create_all()
    click.echo('----->    get mysql db success    <-----')


if __name__ == '__main__':
    socket_io.run(app)
