from dacite import from_dict
from pypika import Parameter, Query, Table

from avengers.data.exc import DataNotFoundError
from avengers.data.models.user import UserModel
from avengers.data.repositories import MySqlRepository

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

        return from_dict(
            data_class=UserModel, data=await self.db.fetchone(query, email)
        )

    async def get_count(self) -> int:
        query: str = "SELECT count(*) FROM user"

        return await self.db.execute(query)

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
        query: str = Query.into(USER_TBL).insert(
            user.email,
            user.password,
            user.receipt_code,
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
