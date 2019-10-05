from dataclasses import asdict
from datetime import timedelta

from dacite import from_dict
from pypika import Parameter, Query, Table

from avengers.data.exc import DataNotFoundError
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
            data[i] = bool([i])

        return from_dict(data_class=UserModel, data=data)

    async def upsert(self, new_data: UserModel) -> None:
        try:
            past_data = await self.get(new_data.email)
        except DataNotFoundError:
            pass
        else:
            await self.delete(past_data.email)
        finally:
            await self.insert(new_data)

    async def insert(self, user: UserModel):
        receipt_code = user.receipt_code

        if not receipt_code:
            query = "SELECT count(*) as count FROM user;"
            receipt_code = (await self.db.fetchone(query))["count"] + 1

        query: str = Query.into(USER_TBL).insert(
            user.email,
            user.password,
            receipt_code,
            user.is_paid,
            user.is_printed_application_arrived,
            user.is_passed_first_apply,
            user.is_passed_interview,
            user.is_final_submit,
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
            expire_time=timedelta(minutes=3).seconds,
        )

    async def get(self, key: str) -> PreUserModel:
        result = await self.db.get(self.key_template.format(key))

        if result:
            return from_dict(data_class=PreUserModel, data=result)

    async def confirm(self, verification_key: str):
        await self.db.delete(verification_key)
