from sanic.request import Request
from sanic.views import HTTPMethodView
from sanic.response import HTTPResponse

from avengers.data.repositories.unauthorized_user import UnauthorizedUserRepository
from avengers.presentation.blueprint import bp
from avengers.services.auth import AuthService
from avengers.data.repositories.user import UserRepository


class SignUp(HTTPMethodView):
    service = AuthService(
        user_repository=UserRepository(),
        unauthorized_user_repository=UnauthorizedUserRepository()
    )

    async def post(self, request: Request) -> HTTPResponse:
        response = await self.service.sign_up(
            email=request.json.get("email"),
            password=request.json.get("password")
        )

        return response


class SignUpVerify(HTTPMethodView):
    service = AuthService(
        user_repository=UserRepository(),
        unauthorized_user_repository=UnauthorizedUserRepository()
    )

    async def get(self, request: Request) -> HTTPResponse:
        verify_key: str = request.args.get("key")
        response = await self.service.verify_key(verify_key)

        return response


class UserAuth(HTTPMethodView):
    service = AuthService(
        user_repository=UserRepository(),
        unauthorized_user_repository=UnauthorizedUserRepository()
    )

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
