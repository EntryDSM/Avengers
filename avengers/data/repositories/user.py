from typing import Any, Dict

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

    async def update(self, email: str, target: Dict[str, Any]):
        query = Query.update(USER_TBL).where(
            USER_TBL.applicant_email == Parameter("%s")
        )

        for col in target:
            query = query.set(col, target[col])

        await self.db.execute(query.get_sql(quote_char=None), email)

    async def insert(self, user: UserModel):
        query: str = Query.into(UserModel).insert(
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
