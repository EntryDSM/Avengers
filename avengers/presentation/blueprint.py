from sanic import Blueprint

from avengers.presentation import view

bp = Blueprint(__name__.split(".")[0], url_prefix="/api/v1")

bp.add_route(view.SchoolSearchView.as_view(), "/school/search")
bp.add_route(view.MyPageView.as_view(), "/self/status")
bp.add_route(view.SignUpView.as_view(), "/signup")
bp.add_route(view.SignUpVerifyView.as_view(), "/signup/verify")
bp.add_route(view.AuthView.as_view(), "/auth")
bp.add_route(view.PhotoView.as_view(), "/self/photo")
