from sanic import Blueprint

from avengers.presentation import view

bp = Blueprint(__name__.split(".")[0], url_prefix="/api/v1")
