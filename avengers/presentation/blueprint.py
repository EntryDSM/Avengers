from sanic import Blueprint

bp = Blueprint(__name__.split(".")[0], url_prefix="/api/v1")
