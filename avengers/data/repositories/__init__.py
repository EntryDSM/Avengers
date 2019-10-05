from typing import Type

from avengers.data.source.mysql import MySQLConnection
from avengers.data.source.redis import RedisConnection


class MySqlRepository:
    def __init__(self, db: Type[MySQLConnection] = MySQLConnection) -> None:
        self.db = db


class RedisRepository:
    def __init__(self, db: Type[RedisConnection] = RedisConnection) -> None:
        self.db = db
