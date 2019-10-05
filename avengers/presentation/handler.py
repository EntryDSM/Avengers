from sanic import Sanic
from sanic.exceptions import SanicException
from sanic.request import Request
from sanic.response import json

from avengers.presentation.exceptions import AvengersException


async def base_handler(request: Request, exception: SanicException):
    # pylint: disable=unused-argument

    status = getattr(exception, "status_code", AvengersException.status_code)

    return json(
        body={
            "error_code": getattr(
                exception, "error_code", AvengersException.error_code
            ),
            "description": getattr(
                exception,
                "description",
                AvengersException.description
                if status // 500
                else exception.args[0],
            ),
        },
        status=status,
    )


def add_error_handlers(app: Sanic):
    app.error_handler.add(SanicException, base_handler)
