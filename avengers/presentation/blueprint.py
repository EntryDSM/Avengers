from sanic import Blueprint

from avengers.presentation.view import SignUp, SignUpVerify, UserAuth

bp = Blueprint(__name__.split(".")[0], url_prefix="/api/v1")

bp.add_route(SignUp.as_view(), "/signup")
bp.add_route(SignUpVerify.as_view(), "/signup/verify")
bp.add_route(UserAuth.as_view(), "/auth")
