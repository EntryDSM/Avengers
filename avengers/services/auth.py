from sanic.request import Request
from sanic.response import json
from sanic_jwt_extended import create_access_token, create_refresh_token
from werkzeug.security import check_password_hash, generate_password_hash

from avengers.config import settings
from avengers.data.exc import DataNotFoundError
from avengers.data.models.unauthorized_user import UnauthorizedUserModel
from avengers.data.models.user import UserModel
from avengers.data.repositories.email import send_mail
from avengers.data.repositories.refresh_token import RefreshTokenRepository
from avengers.data.repositories.unauthorized_user import UnauthorizedUserRepository
from avengers.data.repositories.user import UserRepository
from avengers.presentation.exceptions import UserAlreadyExists, InvalidSignupInfo, SignupAlreadyRequested, \
    InvalidVerificationKey, UserNotFound, TokenError


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
            raise UserAlreadyExists()

        already_requested = await self.unauthorized_user_repository.find_by_email(email)
        if already_requested:
            raise SignupAlreadyRequested()

        temp_user = UnauthorizedUserModel(email, generate_password_hash(password))
        saved = await self.unauthorized_user_repository.save(temp_user)

        send_mail(
            email, title=settings.SIGNUP_EMAIL_TITLE, content=settings.SIGNUP_EMAIL_CONTENT.format(saved)
        )

        return json("Verification code and link sent to your email.", 204)

    async def verify_key(self, verify_key: str):
        temp_user = await self.unauthorized_user_repository.find_by_uuid(verify_key)
        if not temp_user:
            raise InvalidVerificationKey()

        count_of_users = await self.user_repository.get_count()
        user = UserModel(
            email=temp_user.email,
            password=temp_user.password,
            receipt_code=count_of_users,
            is_paid=False,
            is_printed_application_arrived=False,
            is_passed_first_apply=False,
            is_passed_interview=False,
            is_final_submit=False,
            exam_code=None,
            volunteer_score=None,
            attendance_score=None,
            conversion_score=None,
            final_score=None
        )

        await self.user_repository.insert(user)
        await self.unauthorized_user_repository.delete(verify_key)

        return json("Verification success", 204)

    async def login(self, request: Request):
        email = request.json.get("email")
        password = request.json.get("password")

        try:
            saved = await self.user_repository.get(email)
        except DataNotFoundError:
            raise UserNotFound()

        if not check_password_hash(saved.password, password):
            raise UserNotFound()

        is_refresh_saved = await self.refresh_token_repository.get(email)
        if is_refresh_saved:
            await self.refresh_token_repository.delete(email)

        access = await create_access_token(identity=email, app=request.app)
        refresh = await create_refresh_token(identity=email, app=request.app)

        await self.refresh_token_repository.save(email, refresh)
        return json(dict(access=access, refresh=refresh), 201)

    async def refresh_token(self, request: Request):
        try:
            refresh = request.headers.get("X-Refresh-Token").split("Bearer ")[1]
        except IndexError:
            raise TokenError("missing 'Bearer '")

        email = await self.refresh_token_repository.get_by_refresh(refresh)
        if not email:
            raise TokenError()

        access = await create_access_token(identity=email, app=request.app)
        return json({"access": access}, 201)

    async def logout(self, request: Request):
        try:
            refresh = request.headers.get("X-Refresh-Token").split("Bearer ")[1]
        except IndexError:
            raise TokenError("missing 'Bearer '")

        saved_refresh = await self.refresh_token_repository.get_by_refresh(refresh)
        if not saved_refresh:
            raise TokenError()

        await self.refresh_token_repository.delete(saved_refresh)
        return json(dict(msg="Logout succeed"), 204)
