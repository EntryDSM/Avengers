from sanic.exceptions import NotFound
from sanic.request import Request
from sanic.response import json
from sanic.views import HTTPMethodView

from avengers.data.exc import DataNotFoundError
from avengers.services.mypage import MyPageService
from avengers.services.school_search import SchoolSearchService


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
