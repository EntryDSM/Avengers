from dacite import from_dict
from pypika import Parameter, Query, Table

from avengers.data.exc import DataNotFoundError
from avengers.data.models.ungraduated_application import (
    UngraduatedApplicationModel,
)
from avengers.data.repositories import MySqlRepository

UNGRADUATED_APPLICATION_TBL = Table('ungraduated_application')


class UnGraduatedApplicationRepository(MySqlRepository):
    async def get(self, email: str) -> UngraduatedApplicationModel:
        query: str = Query.from_(UNGRADUATED_APPLICATION_TBL).select(
            UNGRADUATED_APPLICATION_TBL.user_email,
            UNGRADUATED_APPLICATION_TBL.apply_type,
            UNGRADUATED_APPLICATION_TBL.additional_type,
            UNGRADUATED_APPLICATION_TBL.is_daejeon,
            UNGRADUATED_APPLICATION_TBL.name,
            UNGRADUATED_APPLICATION_TBL.sex,
            UNGRADUATED_APPLICATION_TBL.birth_date,
            UNGRADUATED_APPLICATION_TBL.parent_name,
            UNGRADUATED_APPLICATION_TBL.parent_tel,
            UNGRADUATED_APPLICATION_TBL.applicant_tel,
            UNGRADUATED_APPLICATION_TBL.address,
            UNGRADUATED_APPLICATION_TBL.post_code,
            UNGRADUATED_APPLICATION_TBL.student_number,
            UNGRADUATED_APPLICATION_TBL.school_name,
            UNGRADUATED_APPLICATION_TBL.school_tel,
            UNGRADUATED_APPLICATION_TBL.school_code,
            UNGRADUATED_APPLICATION_TBL.volunteer_time,
            UNGRADUATED_APPLICATION_TBL.full_cut_count,
            UNGRADUATED_APPLICATION_TBL.period_cut_count,
            UNGRADUATED_APPLICATION_TBL.late_count,
            UNGRADUATED_APPLICATION_TBL.early_leave_count,
            UNGRADUATED_APPLICATION_TBL.korean,
            UNGRADUATED_APPLICATION_TBL.social,
            UNGRADUATED_APPLICATION_TBL.history,
            UNGRADUATED_APPLICATION_TBL.math,
            UNGRADUATED_APPLICATION_TBL.science,
            UNGRADUATED_APPLICATION_TBL.tech_and_home,
            UNGRADUATED_APPLICATION_TBL.english,
            UNGRADUATED_APPLICATION_TBL.self_introduction,
            UNGRADUATED_APPLICATION_TBL.study_plan,
            UNGRADUATED_APPLICATION_TBL.first_grade_score,
            UNGRADUATED_APPLICATION_TBL.second_grade_score,
            UNGRADUATED_APPLICATION_TBL.third_grade_score,
        ).where(
            UNGRADUATED_APPLICATION_TBL.user_email == Parameter("%s")
        ).get_sql(
            quote_char=None
        )
        data = await self.db.fetchone(query, True, email)
        data["is_daejeon"] = bool(data["is_daejeon"])

        return from_dict(data_class=UngraduatedApplicationModel, data=data)

    async def upsert(self, new_data: UngraduatedApplicationModel) -> None:
        try:
            past_data = await self.get(new_data.user_email)
        except DataNotFoundError:
            pass
        else:
            await self.delete(past_data.user_email)
        finally:
            await self.insert(new_data)

    async def insert(self, data: UngraduatedApplicationModel):
        query: str = Query.into(UNGRADUATED_APPLICATION_TBL).insert(
            data.user_email,
            data.apply_type,
            data.additional_type,
            data.is_daejeon,
            data.name,
            data.sex,
            data.birth_date,
            data.parent_name,
            data.parent_tel,
            data.applicant_tel,
            data.address,
            data.post_code,
            data.student_number,
            data.school_name,
            data.school_tel,
            data.school_code,
            data.volunteer_time,
            data.full_cut_count,
            data.period_cut_count,
            data.late_count,
            data.early_leave_count,
            data.korean,
            data.social,
            data.history,
            data.math,
            data.science,
            data.tech_and_home,
            data.english,
            data.self_introduction,
            data.study_plan,
            data.first_grade_score,
            data.second_grade_score,
            data.third_grade_score,
        ).get_sql(quote_char=None)

        await self.db.execute(query)

    async def delete(self, email: str):
        query: str = Query.from_(UNGRADUATED_APPLICATION_TBL).delete().where(
            UNGRADUATED_APPLICATION_TBL.user_email == Parameter("%s")
        ).get_sql(quote_char=None)

        await self.db.execute(query, email)
