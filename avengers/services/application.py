from typing import Optional, Union, Tuple

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
from avengers.presentation.exceptions import ApplicationNotFound

ApplicationUnion = Union[
    GedApplicationModel, GraduatedApplicationModel, UngraduatedApplicationModel
]


# 저는 시키는대로 한거에여 제가 만든거 아니에요
class ApplicationService:
    ged_repo = GedApplicationRepository()
    graduated_repo = GraduatedApplicationRepository()
    ungraduated_repo = UnGraduatedApplicationRepository()

    async def get(self, email: str) -> Tuple[ApplicationUnion, str]:
        ged = await _get_optional_data(email, self.ged_repo), "GED"
        graduated = await _get_optional_data(email, self.graduated_repo), "GRADUATED"
        ungraduated = await _get_optional_data(email, self.ungraduated_repo), "UNGRADUATED"

        res = ged or graduated or ungraduated
        if not res:
            raise ApplicationNotFound

        return res

    async def sync_ged_application(
        self, application: GedApplicationModel
    ) -> None:
        await self.graduated_repo.delete(application.user_email)
        await self.ungraduated_repo.delete(application.user_email)

        await self.ged_repo.upsert(application)

    async def sync_graduated_applicant(
        self, application: GraduatedApplicationModel
    ) -> None:
        await self.ged_repo.delete(application.user_email)
        await self.ungraduated_repo.delete(application.user_email)

        await self.graduated_repo.upsert(application)

    async def sync_ungraduated_applicant(
        self, application: UngraduatedApplicationModel
    ) -> None:
        await self.ged_repo.delete(application.user_email)
        await self.graduated_repo.delete(application.user_email)

        await self.ungraduated_repo.upsert(application)


async def _get_optional_data(email: str, repo) -> Optional[ApplicationUnion]:
    try:
        return await repo.get(email)
    except DataNotFoundError:
        return None
