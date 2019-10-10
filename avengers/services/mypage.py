from avengers.data.exc import DataNotFoundError
from avengers.data.repositories.user import UserRepository
from avengers.presentation.exceptions import UserNotFound


class MyPageService:
    repo = UserRepository()

    async def retrieve_status(self, user_email: str):
        try:
            result = await self.repo.get(user_email)
        except DataNotFoundError:
            raise UserNotFound

        return {
            "receipt_code": result.receipt_code,
            "is_paid": result.is_paid,
            "is_printed_application_arrived": result.is_printed_application_arrived,
            "is_passed_first_apply": result.is_passed_first_apply,
            "is_passed_interview": result.is_passed_interview,
            "is_final_submit": result.is_final_submit,
            "exam_code": result.exam_code,
        }
