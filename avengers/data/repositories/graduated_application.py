from dacite import from_dict
from pypika import Parameter, Query, Table

from avengers.data.exc import DataNotFoundError
from avengers.data.models.graduated_application import (
    GraduatedApplicationModelBase,
)
from avengers.data.repositories import MySqlRepository

GRADUATED_APPLICATION_TBL = Table('graduated_application')


class GraduatedApplicationRepository(MySqlRepository):
    async def get(self, email: str) -> GraduatedApplicationModelBase:
        query: str = Query.from_(GRADUATED_APPLICATION_TBL).select(
            GRADUATED_APPLICATION_TBL.user_email,
            GRADUATED_APPLICATION_TBL.apply_type,
            GRADUATED_APPLICATION_TBL.additional_type,
            GRADUATED_APPLICATION_TBL.is_daejeon,
            GRADUATED_APPLICATION_TBL.name,
            GRADUATED_APPLICATION_TBL.sex,
            GRADUATED_APPLICATION_TBL.birth_date,
            GRADUATED_APPLICATION_TBL.parent_name,
            GRADUATED_APPLICATION_TBL.parent_tel,
            GRADUATED_APPLICATION_TBL.applicant_tel,
            GRADUATED_APPLICATION_TBL.address,
            GRADUATED_APPLICATION_TBL.post_code,
            GRADUATED_APPLICATION_TBL.student_number,
            GRADUATED_APPLICATION_TBL.graduated_year,
            GRADUATED_APPLICATION_TBL.school_code,
            GRADUATED_APPLICATION_TBL.school_tel,
            GRADUATED_APPLICATION_TBL.volunteer_time,
            GRADUATED_APPLICATION_TBL.full_cut_count,
            GRADUATED_APPLICATION_TBL.period_cut_count,
            GRADUATED_APPLICATION_TBL.late_count,
            GRADUATED_APPLICATION_TBL.early_leave_count,
            GRADUATED_APPLICATION_TBL.korean,
            GRADUATED_APPLICATION_TBL.social,
            GRADUATED_APPLICATION_TBL.history,
            GRADUATED_APPLICATION_TBL.math,
            GRADUATED_APPLICATION_TBL.science,
            GRADUATED_APPLICATION_TBL.tech_and_home,
            GRADUATED_APPLICATION_TBL.english,
            GRADUATED_APPLICATION_TBL.self_introduction,
            GRADUATED_APPLICATION_TBL.study_plan,
        ).where(GRADUATED_APPLICATION_TBL.email == Parameter("%s")).get_sql(
            quote_char=None
        )

        return from_dict(
            data_class=GraduatedApplicationModelBase,
            data=await self.db.fetchone(query, email),
        )

    async def upsert(self, new_data: GraduatedApplicationModelBase) -> None:
        try:
            past_data = await self.get(new_data.user_email)
        except DataNotFoundError:
            pass
        else:
            await self.delete(past_data.user_email)
        finally:
            await self.insert(new_data)

    async def insert(self, data: GraduatedApplicationModelBase):
        query: str = Query.into(GRADUATED_APPLICATION_TBL).insert(
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
            data.graduated_year,
            data.school_code,
            data.school_tel,
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
        ).get_sql(quote_char=None)

        await self.db.execute(query)

    async def delete(self, email: str):
        query: str = Query.from_(GRADUATED_APPLICATION_TBL).delete().where(
            GRADUATED_APPLICATION_TBL.email == Parameter("%s")
        ).get_sql(quote_char=None)

        await self.db.execute(query, email)
