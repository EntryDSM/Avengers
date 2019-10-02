from sanic.request import Request
from sanic.response import json
from sanic_jwt_extended import create_access_token, create_refresh_token
from werkzeug.security import check_password_hash, generate_password_hash

from avengers.config import settings
from avengers.data.repositories.refresh_token import RefreshTokenRepository
from avengers.services import send_mail
from avengers.data.exc import DataNotFoundError
from avengers.data.models.user import UserModel
from avengers.data.repositories.user import UserRepository
from avengers.data.models.unauthorized_user import UnauthorizedUserModel
from avengers.data.repositories.unauthorized_user import UnauthorizedUserRepository
from avengers.presentation.exceptions import UserAlreadyExists, InvalidSignupInfo, SignupAlreadyRequested, \
    InvalidVerificationKey, UserNotFound


class AuthService:
    def __init__(self, user_repository: UserRepository, unauthorized_user_repository: UnauthorizedUserRepository,
                 refresh_token_repository: RefreshTokenRepository = None):
        self.user_repository = user_repository
        self.unauthorized_user_repository = unauthorized_user_repository
        self.refresh_token_repository = refresh_token_repository

    async def sign_up(self, email: str, password: str):
        if not email or not password:
            raise InvalidSignupInfo()

        try:
            user_already_exists = await self.user_repository.get(email)
        except DataNotFoundError:
            pass
        else:
            raise UserAlreadyExists("")

        already_requested = await self.unauthorized_user_repository.find_by_email(email)
        if already_requested:
            raise SignupAlreadyRequested("")

        temp_user = UnauthorizedUserModel(email, generate_password_hash(password))
        saved = await self.unauthorized_user_repository.save(temp_user)

        send_mail(email, title=settings.SIGNUP_EMAIL_TITLE, content=settings.SIGNUP_EMAIL_CONTENT.format(saved))

        return json("Verification code and link sent to your email.", 204)

    async def verify_key(self, verify_key: str):
        temp_user = await self.unauthorized_user_repository.find_by_uuid(verify_key)
        if not temp_user:
            raise InvalidVerificationKey("")

        user = UserModel(
            email=temp_user.email,
            password=temp_user.password,
            receipt_code=None,
            is_paid=None,
            is_printed_application_arrived=None,
            is_passed_first_apply=None,
            is_passed_interview=None,
            is_final_submit=None,
            exam_code=None,
            volunteer_score=None,
            attendance_score=None,
            conversion_score=None,
            final_score=None
        )

        await self.user_repository.insert(user)
        await self.unauthorized_user_repository.delete(verify_key)

        return json("Verification success", 204)

    async def login(self, email: str, password: str, app):
        try:
            saved = await self.user_repository.get(email)
        except DataNotFoundError:
            raise UserNotFound("")

        if not check_password_hash(saved.password, password):
            raise UserNotFound("")

        is_refresh_saved = await self.refresh_token_repository.get(email)
        if is_refresh_saved:
            await self.refresh_token_repository.delete(email)

        access = await create_access_token(identity=email, app=app)
        refresh = await create_refresh_token(identity=email, app=app)

        await self.refresh_token_repository.save(email, refresh)
        return json(dict(access=access, refresh=refresh), 201)

    async def refresh_token(self, request: Request):
        ...

    async def logout(self, request: Request):
        ...
