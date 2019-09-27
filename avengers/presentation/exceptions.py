from sanic.exceptions import SanicException, add_status_code

from avengers.presentation.errors import descriptions, error_codes


@add_status_code(503)
class AvengersException(SanicException):
    error_code = error_codes.unknown_internal_server_error
    description = descriptions.ERR_SERVER


@add_status_code(503)
class RedisOperationError(AvengersException):
    error_code = error_codes.redis_error
    description = descriptions.ERR_DATABASE


@add_status_code(503)
class MySQLOperationError(AvengersException):
    error_code = error_codes.mysql_error
    description = descriptions.ERR_DATABASE
