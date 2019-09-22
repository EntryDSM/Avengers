from asyncio import AbstractEventLoop

from sanic import Sanic, response

from avengers import __version__
from avengers.config import Configuration
from avengers.presentation.routes import endpoints


def create_app(config: Configuration):
    app = Sanic(__name__)

    @app.listener('before_server_start')
    async def init(
        _: Sanic, __: AbstractEventLoop
    ):  # pylint: disable=unused-variable
        pass

    @app.listener('after_server_stop')
    async def close(
        _: Sanic, __: AbstractEventLoop
    ):  # pylint: disable=unused-variable
        pass

    @app.route('/')
    async def index(_):  # pylint: disable=unused-variable
        return response.json({'version': __version__, 'configs': config})

    app.blueprint(endpoints)

    return app
