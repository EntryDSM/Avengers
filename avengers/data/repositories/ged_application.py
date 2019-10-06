from dacite import from_dict
from pypika import Parameter, Query, Table

from avengers.data.exc import DataNotFoundError
from avengers.data.models.ged_application import GedApplicationModel
from avengers.data.repositories import MySqlRepository

GED_APPLICATION_TBL = Table('ged_application')


class GedApplicationRepository(MySqlRepository):
    async def get(self, email: str) -> GedApplicationModel:
        query: str = Query.from_(GED_APPLICATION_TBL).select(
            GED_APPLICATION_TBL.user_email,
            GED_APPLICATION_TBL.apply_type,
            GED_APPLICATION_TBL.additional_type,
            GED_APPLICATION_TBL.is_daejeon,
            GED_APPLICATION_TBL.name,
            GED_APPLICATION_TBL.sex,
            GED_APPLICATION_TBL.birth_date,
            GED_APPLICATION_TBL.parent_name,
            GED_APPLICATION_TBL.parent_tel,
            GED_APPLICATION_TBL.applicant_tel,
            GED_APPLICATION_TBL.address,
            GED_APPLICATION_TBL.post_code,
            GED_APPLICATION_TBL.ged_average_score,
            GED_APPLICATION_TBL.self_introduction,
            GED_APPLICATION_TBL.study_plan,
        ).where(GED_APPLICATION_TBL.user_email == Parameter("%s")).get_sql(
            quote_char=None
        )

        data = await self.db.fetchone(query, True, email)
        data["is_daejeon"] = bool(data["is_daejeon"])

        return from_dict(
            data_class=GedApplicationModel,
            data=data,
        )

    async def upsert(self, new_data: GedApplicationModel) -> None:
        try:
            past_data = await self.get(new_data.user_email)
        except DataNotFoundError:
            print("Except")
        else:
            print("Else")
            await self.delete(past_data.user_email)
        finally:
            print("final")
            await self.insert(new_data)

    async def insert(self, data: GedApplicationModel):
        query: str = Query.into(GED_APPLICATION_TBL).insert(
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
            data.ged_average_score,
            data.self_introduction,
            data.study_plan,
        ).get_sql(quote_char=None)

        await self.db.execute(query)

    async def delete(self, email: str):
        query: str = Query.from_(GED_APPLICATION_TBL).delete().where(
            GED_APPLICATION_TBL.user_email == Parameter("%s")
        ).get_sql(quote_char=None)

        await self.db.execute(query, email)
