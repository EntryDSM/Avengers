from secrets import token_urlsafe

from werkzeug.security import generate_password_hash

from avengers.data.exc import DataNotFoundError
from avengers.presentation.exceptions import UserNotFound, InvalidVerificationKey
from avengers.data.repositories.email_sender import EmailSenderRepository
from avengers.data.repositories.user import UserRepository, ResetPasswordRepository
from avengers.config import settings, RESET_PW_EMAIL_TEMPLATE_B, RESET_PW_EMAIL_TEMPLATE_A


class ResetPasswordService:
    user_repo = UserRepository()
    reset_pw_repo = ResetPasswordRepository()
    email_sender = EmailSenderRepository()

    async def send_email(self, email: str):
        try:
            await self.user_repo.get(email)
        except DataNotFoundError:
            raise UserNotFound

        key = token_urlsafe(4)
        await self.reset_pw_repo.set_verify_key(email, key)

        await self.email_sender.send_mail(
            email,
            title=settings.RESET_PW_EMAIL_TITLE,
            content=RESET_PW_EMAIL_TEMPLATE_A + key + RESET_PW_EMAIL_TEMPLATE_B,
        )

    async def verify_key(self, email: str, key: str):
        try:
            user = await self.user_repo.get(email)
        except DataNotFoundError:
            raise UserNotFound

        saved_key = await self.reset_pw_repo.get_verify_key(email)
        if not saved_key or key != saved_key:
            raise InvalidVerificationKey

        await self.reset_pw_repo.set_verified_email(email)

    async def reset_password(self, email: str, password: str):
        try:
            user = await self.user_repo.get(email)
        except DataNotFoundError:
            raise UserNotFound

        verified_email = await self.reset_pw_repo.get_verified_email(email)
        if not verified_email:
            raise InvalidVerificationKey

        password = generate_password_hash(password)
        await self.user_repo.update(email, {'password': password})
