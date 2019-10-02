from dataclasses import asdict
from uuid import uuid5, NAMESPACE_URL, UUID

from dacite import from_dict

from avengers.data.models.unauthorized_user import UnauthorizedUserModel
from avengers.data.repositories import RedisRepository

BASE_KEY = "user:verify:{}"
EXPIRE_TIME = 60 * 3


class UnauthorizedUserRepository(RedisRepository):
    async def find_by_email(self, email: str) -> UnauthorizedUserModel:
        user = await self.db.get(BASE_KEY.format(uuid5(NAMESPACE_URL, email)))
        return from_dict(
            data_class=UnauthorizedUserModel,
            data=user
        ) if user else None

    async def find_by_uuid(self, uuid: str) -> UnauthorizedUserModel:
        user = await self.db.get(BASE_KEY.format(uuid))
        return from_dict(
            data_class=UnauthorizedUserModel,
            data=user
        ) if user else None

    async def save(self, user: UnauthorizedUserModel) -> str:
        uuid = uuid5(NAMESPACE_URL, user.email)
        await self.db.set(
            key=BASE_KEY.format(uuid),
            value=asdict(user),
            expire_time=EXPIRE_TIME
        )

        return str(uuid)

    async def delete(self, verify_key: str) -> None:
        await self.db.delete(str(verify_key))
