from sanic.request import Request
from sanic.response import json
from sanic.views import HTTPMethodView

from avengers.services.school_search import SchoolSearchService


class SchoolSearchView(HTTPMethodView):
    service = SchoolSearchService()

    async def get(self, request: Request):
        key = request.args.get("query")

        result = await self.service.search(key)
        return json(result, status=200)

