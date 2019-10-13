from typing import Optional, Tuple, Union, Dict, Any

from avengers.data.exc import DataNotFoundError
from avengers.data.models.ged_application import GedApplicationModel
from avengers.data.models.graduated_application import (
    GraduatedApplicationModel,
)
from avengers.data.models.ungraduated_application import (
    UngraduatedApplicationModel,
)
from avengers.data.repositories.ged_application import GedApplicationRepository
from avengers.data.repositories.graduated_application import (
    GraduatedApplicationRepository,
)
from avengers.data.repositories.ungraduated_application import (
    UnGraduatedApplicationRepository,
)
from avengers.data.repositories.user import UserRepository
from avengers.presentation.exceptions import (
    AlreadyFinalSubmitted,
    ApplicationNotFound,
    UserNotFound, FinalValidationFailed, InvalidApplication)
from avengers.services.mypage import MyPageService

ApplicationUnion = Union[
    GedApplicationModel, GraduatedApplicationModel, UngraduatedApplicationModel
]


# 저는 시키는대로 한거에여 제가 만든거 아니에요
class ApplicationService:
    my_page_service = MyPageService()

    user_repo = UserRepository()
    ged_repo = GedApplicationRepository()
    graduated_repo = GraduatedApplicationRepository()
    ungraduated_repo = UnGraduatedApplicationRepository()

    async def get(self, email: str) -> ApplicationUnion:
        ged = await _get_optional_data(email, self.ged_repo)
        graduated = await _get_optional_data(email, self.graduated_repo)
        ungraduated = await _get_optional_data(email, self.ungraduated_repo)

        res = ged or graduated or ungraduated
        if not res:
            raise ApplicationNotFound

        return res

    async def sync_ged_application(
        self, application: GedApplicationModel
    ) -> None:
        if (
            await self.my_page_service.retrieve_status(application.user_email)
        )["is_final_submit"]:
            raise AlreadyFinalSubmitted

        await self.graduated_repo.delete(application.user_email)
        await self.ungraduated_repo.delete(application.user_email)

        await self.ged_repo.upsert(application)

    async def sync_graduated_applicant(
        self, application: GraduatedApplicationModel
    ) -> None:
        if (
            await self.my_page_service.retrieve_status(application.user_email)
        )["is_final_submit"]:
            raise AlreadyFinalSubmitted

        await self.ged_repo.delete(application.user_email)
        await self.ungraduated_repo.delete(application.user_email)

        await self.graduated_repo.upsert(application)

    async def sync_ungraduated_applicant(
        self, application: UngraduatedApplicationModel
    ) -> None:
        if (
            await self.my_page_service.retrieve_status(application.user_email)
        )["is_final_submit"]:
            raise AlreadyFinalSubmitted

        await self.ged_repo.delete(application.user_email)
        await self.graduated_repo.delete(application.user_email)

        await self.ungraduated_repo.upsert(application)

    async def get_calculated_score(self, email: str) -> Dict[str, Any]:
        try:
            user = await self.user_repo.get(email)
        except DataNotFoundError:
            raise UserNotFound

        scores = {
            "volunteer_score": user.volunteer_score,
            "attendance_score": user.attendance_score,
            "conversion_score": user.conversion_score,
            "final_score": user.final_score
        }
        application = await self.get(email)

        if isinstance(application, GedApplicationModel):
            scores["ged_average_score"] = application.ged_average_score

        else:
            scores["first_grade_score"] = application.first_grade_score
            scores["second_grade_score"] = application.second_grade_score
            scores["third_grade_score"] = application.third_grade_score

        return scores


async def _get_optional_data(email: str, repo) -> Optional[ApplicationUnion]:
    try:
        return await repo.get(email)
    except DataNotFoundError:
        return None
