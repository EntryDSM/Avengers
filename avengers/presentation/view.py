from sanic.request import Request
from sanic.views import HTTPMethodView

from avengers.presentation.blueprint import bp


class SignUp(HTTPMethodView):
    async def post(self, request: Request):
        ...


class SignUpVerify(HTTPMethodView):
    async def get(self, request: Request):
        ...


class UserAuth(HTTPMethodView):
    async def post(self, request: Request):
        ...

    async def patch(self, request: Request):
        ...

    async def delete(self, request: Request):
        ...


bp.add_route(SignUp.as_view(), "/signup")
bp.add_route(SignUpVerify.as_view(), "/signup/verify")
bp.add_route(UserAuth.as_view(), "/auth")
