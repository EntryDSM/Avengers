from typing import Any, Dict, List

import aiomysql

from avengers.data.utils import mysql_exception_handling


class MySQLConnection:
    _read_pool: aiomysql.Pool
    _write_pool: aiomysql.Pool
    _connection_info = None

    @classmethod
    @mysql_exception_handling
    async def initialize(cls, connection_info):
        cls._connection_info = connection_info

        await cls._get_read_pool()
        await cls._get_write_pool()

    @classmethod
    @mysql_exception_handling
    async def release(cls):
        if cls._read_pool is not None:
            cls._read_pool.close()
            await cls._read_pool.wait_closed()
        if cls._write_pool is not None:
            cls._write_pool.close()
            await cls._write_pool.wait_closed()

    @classmethod
    @mysql_exception_handling
    async def _get_read_pool(cls) -> aiomysql.Pool:
        if (
            cls._read_pool and not cls._read_pool._closed
        ):  # pylint: disable=protected-access
            return cls._read_pool

        cls._read_pool = await aiomysql.create_pool(**cls._connection_info)
        return cls._read_pool

    @classmethod
    @mysql_exception_handling
    async def _get_write_pool(cls) -> aiomysql.Pool:
        if (
            cls._write_pool and not cls._write_pool._closed
        ):  # pylint: disable=protected-access
            return cls._write_pool

        cls._write_pool = await aiomysql.create_pool(**cls._connection_info)
        return cls._write_pool

    @classmethod
    @mysql_exception_handling
    async def execute(cls, query: str, *args) -> int:
        pool: aiomysql.Pool = await cls._get_write_pool()
        conn: aiomysql.Connection
        cur: aiomysql.DictCursor
        result: int

        async with pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                result = await cur.execute(query, args)

        return result

    @classmethod
    @mysql_exception_handling
    async def executemany(cls, query: str, *args) -> int:
        pool: aiomysql.Pool = await cls._get_write_pool()
        conn: aiomysql.Connection
        cur: aiomysql.DictCursor
        result: int

        async with pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                result = await cur.executemany(query, args)

        return result

    @classmethod
    @mysql_exception_handling
    async def fetch(cls, query: str, *args) -> List[Dict[str, Any]]:
        pool: aiomysql.Pool = await cls._get_read_pool()
        conn: aiomysql.Connection
        cur: aiomysql.DictCursor
        result: List[Dict[str, Any]]

        async with pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(query, args)
                result = await cur.fetchall()

        return result

    @classmethod
    @mysql_exception_handling
    async def fetchone(cls, query: str, *args) -> Dict[str, Any]:
        pool: aiomysql.Pool = await cls._get_read_pool()
        conn: aiomysql.Connection
        cur: aiomysql.DictCursor
        result: Dict[str, Any]

        async with pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(query, args)
                result = await cur.fetchone()

        return result
