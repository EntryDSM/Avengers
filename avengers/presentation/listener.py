from sanic.log import logger

from avengers.config import settings
from avengers.data.source.mysql import MySQLConnection
from avengers.data.source.redis import RedisConnection


async def initialize(app, loop):
    database_connection_info = (
        app.database_connection_info
        if hasattr(app, "database_connection_info")
        else settings.database_connection_info
    )

    cache_connection_info = (
        app.cache_connection_info
        if hasattr(app, "cache_connection_info")
        else settings.cache_connection_info
    )

    await MySQLConnection.initialize(database_connection_info)
    await RedisConnection.initialize(cache_connection_info)

    logger.info("Connection initialize complete")


async def release(app, loop):
    await MySQLConnection.release()
    await RedisConnection.release()

    logger.info("Connection release complete")
