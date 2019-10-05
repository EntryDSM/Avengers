import os
from datetime import timedelta

from entry_logger_sanic import set_logger
from sanic import Sanic, response
from sanic_jwt_extended import JWTManager

from avengers import __version__
from avengers.config import LOGO, RUN_ENV, SERVICE_NAME, settings
from avengers.presentation.blueprint import bp
from avengers.presentation.handler import add_error_handlers
from avengers.presentation.listener import initialize, release


def create_app():
    app = Sanic(SERVICE_NAME)
    app.config.LOGO = LOGO

    if RUN_ENV == "prod":
        app.config["SLACK_WEBHOOK_URL"] = settings.SLACK_WEBHOOK_URL
        app.config["SLACK_MAINTAINER_ID"] = settings.SLACK_MAINTAINER_ID

    log_path = os.path.dirname(__file__).replace("/avengers", "")

    set_logger(app, log_path)

    app.register_listener(initialize, "before_server_start")
    app.register_listener(release, "after_server_stop")

    add_error_handlers(app)

    app.config["JWT_SECRET_KEY"] = settings.JWT_SECRET_KEY
    app.config["JWT_ACCESS_EXPIRES"] = timedelta(seconds=settings.JWT_ACCESS_EXPIRES)
    app.config["JWT_REFRESH_EXPIRES"] = timedelta(seconds=settings.JWT_REFRESH_EXPIRES)
    JWTManager(app)

    @app.route("/")
    async def index(_):  # pylint: disable=unused-variable
        return response.json({"version": __version__})

    app.blueprint(bp)

    return app
