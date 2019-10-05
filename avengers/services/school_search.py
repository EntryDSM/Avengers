from typing import List

from avengers.data.repositories.school import SchoolRepository


class SchoolSearchService:
    repo = SchoolRepository()

    bad_query = ("중학교", "중학", "학교")

    async def search(self, key: str) -> List[str]:
        if not key or (key in self.bad_query) or (len(key) < 2):
            return []

        result = await self.repo.search(key)

        return result
