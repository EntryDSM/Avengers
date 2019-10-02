from avengers.config import settings
from avengers.data.repositories import RedisRepository

BASE_KEY = "user:refresh:{}"


class RefreshTokenRepository(RedisRepository):
    async def get(self, email: str) -> str:
        is_refresh_saved = await self.db.get(BASE_KEY.format(email))

        return is_refresh_saved if is_refresh_saved else None

    async def get_by_refresh(self, refresh: str) -> str:
        is_email_saved = await self.db.get(BASE_KEY.format(refresh))

        return is_email_saved if is_email_saved else None

    async def save(self, email: str, refresh: str) -> None:
        await self.db.set(BASE_KEY.format(email), refresh, expire_time=settings.JWT_REFRESH_EXPIRES)
        await self.db.set(BASE_KEY.format(refresh), email, expire_time=settings.JWT_REFRESH_EXPIRES)

        return

    async def delete(self, email) -> None:
        saved_refresh = await self.get(email)

        await self.db.delete(BASE_KEY.format(saved_refresh))
        await self.db.delete(BASE_KEY.format(email))

        return
