from typing import Any, Dict, Optional

import aioredis
import ujson

from avengers.data.utils import redis_exception_handling

EXPIRE_TIME_SHORT = 60 * 1
EXPIRE_TIME_NORMAL = 60 * 60
EXPIRE_TIME_LONG = 60 * 60 * 24


class RedisConnection:
    redis: Optional[aioredis.Redis] = None

    @classmethod
    @redis_exception_handling
    async def _get_redis_connection(cls):
        if cls.redis and not cls.redis.closed:
            return cls.redis

        cls.redis = await aioredis.create_redis_pool(**cls.connection_info)

        return cls.redis

    @classmethod
    @redis_exception_handling
    async def initialize(cls, connection_info):
        cls.connection_info = connection_info
        await cls._get_redis_connection()

    @classmethod
    @redis_exception_handling
    async def release(cls):
        if cls.redis:
            cls.redis.close()
            await cls.redis.wait_closed()

        cls.redis = None

    @classmethod
    @redis_exception_handling
    async def set(
        cls, key: str, value: Any, expire_time: int = EXPIRE_TIME_LONG
    ) -> None:
        redis = await cls._get_redis_connection()

        dumped_value = ujson.dumps(value)
        await redis.set(key, dumped_value, expire=expire_time)

    @classmethod
    @redis_exception_handling
    async def multiset(
        cls, pairs: Dict[str, Any], expire_time: int = EXPIRE_TIME_LONG
    ):
        redis = await cls._get_redis_connection()

        tr = redis.multi_exec()

        for k, v in pairs.items():
            tr.set(k, ujson.dumps(v), expire=expire_time)

        try:
            await tr.execute(return_exceptions=True)
        except aioredis.MultiExecError as e:
            rollback_tr = redis.multi_exec()
            for k in pairs.keys():
                rollback_tr.delete(k)

            raise e

    @classmethod
    @redis_exception_handling
    async def get(cls, key: str) -> Any:
        redis = await cls._get_redis_connection()
        value = await redis.get(key)
        value = ujson.loads(value) if value else None

        return value

    @classmethod
    @redis_exception_handling
    async def delete(cls, *keys: str):
        redis = await cls._get_redis_connection()
        await redis.delete(*keys)
