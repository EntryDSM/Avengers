import secrets
from dataclasses import asdict

from dacite import from_dict
from werkzeug.security import generate_password_hash

from avengers.config import settings
from avengers.data.exc import DataNotFoundError
from avengers.data.models.user import PreUserModel, UserModel
from avengers.data.repositories.email_sender import EmailSenderRepository
from avengers.data.repositories.user import PreUserRepository, UserRepository
from avengers.presentation.exceptions import (
    SignupAlreadyRequested,
    UserAlreadyExists,
    InvalidVerificationKey)


class AuthService:
    preuser_repo = PreUserRepository()
    user_repo = UserRepository()
    email_sender = EmailSenderRepository()

    async def signup(self, pre_user: PreUserModel):
        if await self.preuser_repo.get(pre_user.email):
            raise SignupAlreadyRequested

        try:
            await self.user_repo.get(pre_user.email)
        except DataNotFoundError:
            pass
        else:
            raise UserAlreadyExists

        key = secrets.token_urlsafe(6)
        pre_user.password = generate_password_hash(pre_user.password)

        await self.preuser_repo.set(pre_user, key)
        await self.email_sender.send_mail(
            pre_user.email,
            title=settings.SIGNUP_EMAIL_TITLE,
            content=settings.SIGNUP_EMAIL_CONTENT.format(key),
        )

    async def confirm(self, verification_key: str):
        pre_user = await self.preuser_repo.get(verification_key)

        if not pre_user:
            raise InvalidVerificationKey

        await self.preuser_repo.confirm(verification_key)

        user = from_dict(
            data_class=UserModel,
            data={**asdict(pre_user)}
        )

        await self.user_repo.insert(user)
