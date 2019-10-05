from marshmallow import ValidationError
from sanic.exceptions import NotFound
from sanic.request import Request
from sanic.response import json
from sanic.views import HTTPMethodView
from sanic_jwt_extended import create_access_token, create_refresh_token, jwt_refresh_token_required
from sanic_jwt_extended.tokens import Token

from avengers.data.exc import DataNotFoundError
from avengers.data.models.user import PreUserModel
from avengers.presentation.exceptions import InvalidSignupInfo, InvalidVerificationKey, UserNotFound, TokenError
from avengers.services.auth import AuthService
from avengers.services.mypage import MyPageService
from avengers.services.school_search import SchoolSearchService
from avengers.presentation.schema.auth import SignUpRequestSchema, LoginRequestSchema


class SchoolSearchView(HTTPMethodView):
    service = SchoolSearchService()

    async def get(self, request: Request):
        key = request.args.get("query")

        result = await self.service.search(key)
        return json(result, status=200)


class MyPageView(HTTPMethodView):
    service = MyPageService()

    # @jwt_required
    async def get(self, request: Request):
        _ = "kshr2d2@gmail.com"  # FIXME

        try:
            result = await self.service.retrieve_status(_)
            return json(body=result, status=200)
        except DataNotFoundError:
            raise NotFound("User not found")


class SignUpView(HTTPMethodView):
    service = AuthService()
    signup_schema = SignUpRequestSchema()

    async def post(self, request: Request):
        if not request.json:
            print(1)
            raise InvalidSignupInfo

        try:
            pre_user = self.signup_schema.load(request.json)
        except ValidationError:
            raise InvalidSignupInfo

        pre_user = PreUserModel(**pre_user)

        await self.service.signup(pre_user)

        return json({}, status=204)


class SignUpVerifyView(HTTPMethodView):
    service = AuthService()

    async def get(self, request: Request):
        if not request.args:
            raise InvalidVerificationKey

        key = request.args.get("key")

        if not key:
            raise InvalidVerificationKey

        await self.service.confirm(key)

        return json({}, status=204)


class AuthView(HTTPMethodView):
    service = AuthService()
    login_schema = LoginRequestSchema()

    async def post(self, request: Request):
        if not request.json:
            raise UserNotFound

        try:
            login = self.login_schema.load(request.json)
        except ValidationError:
            raise UserNotFound

        access_token, refresh_token = await self.service.login(**login, app=request.app)

        return json({'access': access_token, 'refresh': refresh_token}, 201)

    async def patch(self, request: Request):
        try:
            token = request.headers.get("X-Refresh-Token").split("Bearer ")[1]
        except (IndexError, AttributeError):
            raise TokenError

        access_token = await self.service.refresh(token, request.app)

        return json({'access': access_token}, 201)

    async def delete(self, request: Request):
        try:
            token = request.headers.get("X-Refresh-Token").split("Bearer ")[1]
        except (IndexError, AttributeError):
            raise TokenError

        await self.service.logout(token)

        return json({}, status=204)

