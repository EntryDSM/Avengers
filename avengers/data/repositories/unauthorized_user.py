from dataclasses import asdict
from uuid import uuid5, NAMESPACE_URL, UUID

from dacite import from_dict

from avengers.data.models.unauthorized_user import UnauthorizedUserModel
from avengers.data.repositories import RedisRepository

BASE_KEY = "user:verify:{}"
EXPIRE_TIME = 60 * 3


class UnauthorizedUserRepository(RedisRepository):
    async def find_by_email(self, email: str) -> UnauthorizedUserModel:
        return from_dict(
            data_class=UnauthorizedUserModel,
            data=await self.db.get(uuid5(NAMESPACE_URL, email))
        )

    async def save(self, user: UnauthorizedUserModel) -> None:
        await self.db.set(
            key=BASE_KEY.format(uuid5(NAMESPACE_URL, user.email)),
            value=asdict(user),
            expire_time=EXPIRE_TIME
        )

    async def delete(self, verify_key: UUID) -> None:
        await self.db.delete(str(verify_key))
