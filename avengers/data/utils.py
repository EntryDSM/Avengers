import traceback
from functools import wraps

from aiomysql import MySQLError
from aioredis import RedisError
from sanic.log import logger

from avengers.presentation.exceptions import (
    MySQLOperationError,
    RedisOperationError,
)


def redis_exception_handling(fn):
    @wraps(fn)
    async def wrapper(*args, **kwargs):
        try:
            return await fn(*args, **kwargs)
        except RedisError:
            logger.critical(traceback.format_exc())
            raise RedisOperationError("")

    return wrapper


def mysql_exception_handling(fn):
    @wraps(fn)
    async def wrapper(*args, **kwargs):
        try:
            return await fn(*args, **kwargs)
        except MySQLError:
            logger.critical(traceback.format_exc())
            raise MySQLOperationError("")

    return wrapper
