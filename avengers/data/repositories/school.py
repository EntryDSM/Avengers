from typing import List

from avengers.data.repositories import MySqlRepository


class SchoolRepository(MySqlRepository):
    async def search(self, key: str) -> List[str]:
        query = "SELECT school_full_name, code FROM school WHERE school_name LIKE %s"

        result = await self.db.fetch(query, f"%{key}%")
        print(result)
        result = [{"name": i["school_full_name"], "code": i["code"]} for i in result]

        return result
