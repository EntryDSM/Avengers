from marshmallow import ValidationError
from sanic.exceptions import NotFound
from sanic.request import Request
from sanic.response import json
from sanic.views import HTTPMethodView

from avengers.data.exc import DataNotFoundError
from avengers.data.models.user import PreUserModel
from avengers.presentation.exceptions import InvalidSignupInfo, InvalidVerificationKey
from avengers.services.auth import AuthService
from avengers.services.mypage import MyPageService
from avengers.services.school_search import SchoolSearchService
from avengers.presentation.schema.auth import SignUpRequestSchema


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
            print(2)
            print(request.json)
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
