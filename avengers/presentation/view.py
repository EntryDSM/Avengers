from sanic.request import Request
from sanic.views import HTTPMethodView
from sanic.response import HTTPResponse

from avengers.presentation.blueprint import bp
from avengers.services.auth import AuthService
from avengers.data.repositories.user import UserRepository


class SignUp(HTTPMethodView):
    repository = UserRepository()
    service = AuthService(repository)

    async def post(self, request: Request) -> HTTPResponse:
        response = await self.service.sign_up(
            email=request.json.get("email"),
            password=request.json.get("password")
        )

        return response


class SignUpVerify(HTTPMethodView):
    repository = UserRepository()
    service = AuthService(repository)

    async def get(self, request: Request) -> HTTPResponse:
        response = await self.service.verify_key(request)

        return response


class UserAuth(HTTPMethodView):
    repository = UserRepository()
    service = AuthService(repository)

    async def post(self, request: Request) -> HTTPResponse:
        response = await self.service.login(request)

        return response

    async def patch(self, request: Request) -> HTTPResponse:
        response = await self.service.refresh_token(request)

        return response

    async def delete(self, request: Request) -> HTTPResponse:
        response = await self.service.logout(request)

        return response


bp.add_route(SignUp.as_view(), "/signup")
bp.add_route(SignUpVerify.as_view(), "/signup/verify")
bp.add_route(UserAuth.as_view(), "/auth")
