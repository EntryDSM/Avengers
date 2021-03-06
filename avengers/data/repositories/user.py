from dataclasses import asdict
from datetime import timedelta
from typing import Any, Dict

from dacite import from_dict
from pypika import Parameter, Query, Table

from avengers.config import settings
from avengers.data.models.user import PreUserModel, UserModel
from avengers.data.repositories import MySqlRepository, RedisRepository

USER_TBL = Table('user')


class UserRepository(MySqlRepository):
    async def get(self, email: str) -> UserModel:
        query: str = Query.from_(USER_TBL).select(
            USER_TBL.email,
            USER_TBL.password,
            USER_TBL.receipt_code,
            USER_TBL.is_paid,
            USER_TBL.is_printed_application_arrived,
            USER_TBL.is_passed_first_apply,
            USER_TBL.is_passed_interview,
            USER_TBL.is_final_submit,
            USER_TBL.exam_code,
            USER_TBL.volunteer_score,
            USER_TBL.attendance_score,
            USER_TBL.conversion_score,
            USER_TBL.final_score,
        ).where(USER_TBL.email == Parameter("%s")).get_sql(quote_char=None)

        data = await self.db.fetchone(query, True, email)

        for i in [
            "is_paid",
            "is_printed_application_arrived",
            "is_passed_first_apply",
            "is_passed_interview",
            "is_final_submit",
        ]:
            data[i] = bool(data[i])

        return from_dict(data_class=UserModel, data=data)

    async def update(self, email: str, target: Dict[str, Any]):
        query = Query.update(USER_TBL).where(USER_TBL.email == Parameter("%s"))

        for col in target:
            query = query.set(col, target[col])

        await self.db.execute(query.get_sql(quote_char=None), email)

    async def insert(self, user: UserModel):
        receipt_code = user.receipt_code

        if not receipt_code:
            query = "SELECT count(*) as count FROM user;"
            receipt_code = (await self.db.fetchone(query))["count"] + 1

        query: str = Query.into(USER_TBL).insert(
            user.email,
            user.password,
            receipt_code,
            False if user.is_paid is None else user.is_paid,
            False
            if user.is_printed_application_arrived is None
            else user.is_printed_application_arrived,
            False
            if user.is_passed_first_apply is None
            else user.is_passed_first_apply,
            False
            if user.is_passed_interview is None
            else user.is_passed_interview,
            False if user.is_final_submit is None else user.is_final_submit,
            user.exam_code,
            user.volunteer_score,
            user.attendance_score,
            user.conversion_score,
            user.final_score,
        ).get_sql(quote_char=None)

        await self.db.execute(query)

    async def delete(self, email: str) -> None:
        query: str = Query.from_(USER_TBL).delete().where(
            USER_TBL.email == Parameter("%s")
        ).get_sql(quote_char=None)

        await self.db.execute(query, email)


class PreUserRepository(RedisRepository):
    key_template = "avengers:verification:{0}"

    async def set(self, pre_user: PreUserModel, verification_key: str):
        await self.db.multiset(
            {
                self.key_template.format(verification_key): asdict(pre_user),
                self.key_template.format(pre_user.email): asdict(pre_user),
            },
            expire_time=timedelta(minutes=10).seconds,
        )

    async def get(self, key: str) -> PreUserModel:
        result = await self.db.get(self.key_template.format(key))

        if result:
            return from_dict(data_class=PreUserModel, data=result)

    async def confirm(self, verification_key: str):
        pair = await self.db.get(self.key_template.format(verification_key))

        await self.db.delete(
            self.key_template.format(verification_key),
            self.key_template.format(pair["email"]),
        )


class UserTokenRepository(RedisRepository):
    key_template = "avengers:refresh:{}"

    async def set(self, email: str, token: str):
        await self.delete(email)

        await self.db.multiset(
            {
                self.key_template.format(email): token,
                self.key_template.format(token): email,
            },
            settings.JWT_REFRESH_EXPIRES,
        )

    async def get(self, key: str):
        return await self.db.get(self.key_template.format(key))

    async def delete(self, email):
        pair = await self.get(email)

        await self.db.delete(
            self.key_template.format(email), self.key_template.format(pair)
        )


class ResetPasswordRepository(RedisRepository):
    key_template = "avengers:password_reset:{}"

    async def set_verify_key(self, email: str, key: str) -> None:
        await self.delete_verify_key(email)

        await self.db.set(
            self.key_template.format(email), key)

    async def set_verified_email(self, email: str) -> None:
        await self.delete_verify_key(email)

        await self.db.set(
            self.key_template.format("verified:" + email), dict(verified=True)
        )

    async def get_verify_key(self, email: str) -> str:
        return await self.db.get(self.key_template.format(email))

    async def get_verified_email(self, email: str):
        saved = await self.db.get(self.key_template.format("verified:" + email))
        return saved["verified"] if saved else None

    async def delete_verify_key(self, email) -> None:
        await self.db.delete(self.key_template.format(email))

    async def delete_verified_email(self, email: str) -> None:
        await self.db.delete(self.key_template.format("verified:" + email))
