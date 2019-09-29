from typing import Type

from avengers.data.source.mysql import MySQLConnection


class MySqlRepository:
    def __init__(self, db: Type[MySQLConnection] = MySQLConnection) -> None:
        self.db = db
