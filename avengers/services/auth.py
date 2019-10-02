from sanic.request import Request
from sanic.response import json

from avengers.config import settings
from avengers.data.exc import DataNotFoundError
from avengers.data.models.unauthorized_user import UnauthorizedUserModel
from avengers.data.repositories.unauthorized_user import UnauthorizedUserRepository
from avengers.data.repositories.user import UserRepository
from avengers.presentation.exceptions import UserAlreadyExists, InvalidSignupInfo, SignupAlreadyRequested, \
    InvalidVerificationKey
from avengers.services import send_mail


class AuthService:
    def __init__(self, user_repository: UserRepository, unauthorized_user_repository: UnauthorizedUserRepository):
        self.user_repository = user_repository
        self.unauthorized_user_repository = unauthorized_user_repository

    async def sign_up(self, email: str, password: str):
        if not email or not password:
            raise InvalidSignupInfo()

        try:
            user_already_exists = await self.user_repository.get(email)
        except DataNotFoundError:
            pass
        else:
            raise UserAlreadyExists()

        already_requested = await self.unauthorized_user_repository.find_by_email(email)
        if already_requested:
            raise SignupAlreadyRequested("")

        temp_user = UnauthorizedUserModel(email, password)
        saved = await self.unauthorized_user_repository.save(temp_user)

        send_mail(email, title=settings.SIGNUP_EMAIL_TITLE, content=settings.SIGNUP_EMAIL_CONTENT.format(saved))

        return json("Verification code and link sent to your email.", 204)

    async def verify_key(self, verify_key: str):
        user = await self.unauthorized_user_repository.find_by_uuid(verify_key)
        if not user:
            raise InvalidVerificationKey()

        ...

    async def login(self, request: Request):
        ...

    async def refresh_token(self, request: Request):
        ...

    async def logout(self, request: Request):
        ...
