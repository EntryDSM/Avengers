import dataclasses
import os
from dataclasses import asdict

import aiofiles
from dacite import from_dict
from marshmallow import EXCLUDE, ValidationError
from sanic.exceptions import NotFound
from sanic.request import Request
from sanic.response import file, json
from sanic.views import HTTPMethodView
from sanic_jwt_extended import jwt_required
from sanic_jwt_extended.tokens import Token

from avengers.config import PICTURE_DIR
from avengers.data.exc import DataNotFoundError
from avengers.data.models.ged_application import GedApplicationModel
from avengers.data.models.graduated_application import (
    GraduatedApplicationModel,
)
from avengers.data.models.ungraduated_application import (
    UngraduatedApplicationModel,
)
from avengers.data.models.user import PreUserModel
from avengers.presentation.exceptions import (
    ImageNotFound,
    InvalidApplication,
    InvalidSignupInfo,
    InvalidVerificationKey,
    TokenError,
    UserNotFound,
    WrongImageData,
)
from avengers.presentation.schema.application import (
    Classification,
    DiligenceGrade,
    GEDApplicationRequestSchema,
    GEDGrade,
    GraduatedApplicationRequestSchema,
    GraduatedSchoolGrade,
    PersonalInformation,
    PersonalInformationWitGraduatedSchoolInfo,
    PersonalInformationWithCurrentSchoolInfo,
    SelfIntroductionAndStudyPlan,
    UngraduatedApplicationRequestSchema,
    UngraduatedSchoolGrade,
)
from avengers.presentation.schema.auth import (
    LoginRequestSchema,
    SignUpRequestSchema,
)
from avengers.services.application import ApplicationService
from avengers.services.auth import AuthService
from avengers.services.finalize import FinalizeApplicationService
from avengers.services.mypage import MyPageService
from avengers.services.school_search import SchoolSearchService


class SchoolSearchView(HTTPMethodView):
    service = SchoolSearchService()

    @jwt_required
    async def get(self, request: Request, token: Token):
        key = request.args.get("query")

        result = await self.service.search(key)
        return json(result, status=200)


class MyPageView(HTTPMethodView):
    service = MyPageService()

    @jwt_required
    async def get(self, request: Request, token: Token):
        try:
            result = await self.service.retrieve_status(token.jwt_identity)
            return json(body=result, status=200)
        except DataNotFoundError:
            raise NotFound("User not found")


class SignUpView(HTTPMethodView):
    service = AuthService()
    signup_schema = SignUpRequestSchema()

    async def post(self, request: Request):
        if not request.json:
            raise InvalidSignupInfo

        try:
            pre_user = self.signup_schema.load(request.json)
        except ValidationError:
            raise InvalidSignupInfo

        pre_user = PreUserModel(**pre_user)

        await self.service.signup(pre_user)

        return json({}, status=204)


class SignUpVerifyView(HTTPMethodView):
    service = AuthService()

    async def get(self, request: Request):
        if not request.args:
            raise InvalidVerificationKey

        key = request.args.get("key")

        if not key:
            raise InvalidVerificationKey

        await self.service.confirm(key)

        return json({}, status=204)


class AuthView(HTTPMethodView):
    service = AuthService()
    login_schema = LoginRequestSchema()

    async def post(self, request: Request):
        if not request.json:
            raise UserNotFound

        try:
            login = self.login_schema.load(request.json)
        except ValidationError:
            raise UserNotFound

        access_token, refresh_token = await self.service.login(
            **login, app=request.app
        )

        return json({'access': access_token, 'refresh': refresh_token}, 201)

    async def patch(self, request: Request):
        try:
            token = request.headers.get("X-Refresh-Token").split("Bearer ")[1]
        except (IndexError, AttributeError):
            raise TokenError

        access_token = await self.service.refresh(token, request.app)

        return json({'access': access_token}, 201)

    async def delete(self, request: Request):
        try:
            token = request.headers.get("X-Refresh-Token").split("Bearer ")[1]
        except (IndexError, AttributeError):
            raise TokenError

        await self.service.logout(token)

        return json({}, status=204)


class PhotoView(HTTPMethodView):
    @jwt_required
    async def put(self, request: Request, token: Token):
        if not os.path.exists(PICTURE_DIR):
            os.makedirs(PICTURE_DIR)

        file = request.files.get('image')

        if not file:
            raise WrongImageData

        ext = file.name.split(".")[-1]
        if ext not in ["png", "jpeg", "jpg", 'jp2', 'j2c']:
            raise WrongImageData

        filename = f"{token.jwt_identity}"

        async with aiofiles.open(f"{PICTURE_DIR}/{filename}", 'wb') as f:
            await f.write(file.body)

        return json({}, status=204)

    @jwt_required
    async def get(self, request: Request, token: Token):
        if not os.path.exists(f"{PICTURE_DIR}/{token.jwt_identity}"):
            raise ImageNotFound

        return await file(
            f"{PICTURE_DIR}/{token.jwt_identity}",
            status=200,
            mime_type="image/*",
        )


class ApplicationRetrieveView(HTTPMethodView):
    service = ApplicationService()

    @jwt_required
    async def get(self, request: Request, token: Token):
        application = await self.service.get(token.jwt_identity)
        classification = Classification().load(
            asdict(application), unknown=EXCLUDE
        )

        if isinstance(application, GedApplicationModel):
            application = asdict(application)

            return json(
                {
                    "classification": classification,
                    "personal_information": PersonalInformation().load(
                        application, unknown=EXCLUDE
                    ),
                    "ged_grade": GEDGrade().load(application, unknown=EXCLUDE),
                    'self_introduction_and_study_plan': SelfIntroductionAndStudyPlan().load(
                        application, unknown=EXCLUDE
                    ),
                },
                200,
            )

        elif isinstance(application, GraduatedApplicationModel):
            application = asdict(application)
            for v in [
                "korean",
                "social",
                "history",
                "math",
                "english",
                "tech_and_home",
                "science",
            ]:
                application[v] = list(application[v])

            return json(
                {
                    "classification": classification,
                    "personal_information": PersonalInformationWitGraduatedSchoolInfo().load(
                        application, unknown=EXCLUDE
                    ),
                    "diligence_grade": DiligenceGrade().load(
                        application, unknown=EXCLUDE
                    ),
                    "school_grade": GraduatedSchoolGrade().load(
                        application, unknown=EXCLUDE
                    ),
                    'self_introduction_and_study_plan': SelfIntroductionAndStudyPlan().load(
                        application, unknown=EXCLUDE
                    ),
                },
                200,
            )

        elif isinstance(application, UngraduatedApplicationModel):
            application = asdict(application)
            for v in [
                "korean",
                "social",
                "history",
                "math",
                "english",
                "tech_and_home",
                "science",
            ]:
                application[v] = list(application[v])

            return json(
                {
                    "classification": classification,
                    "personal_information": PersonalInformationWithCurrentSchoolInfo().load(
                        application, unknown=EXCLUDE
                    ),
                    "diligence_grade": DiligenceGrade().load(
                        application, unknown=EXCLUDE
                    ),
                    "school_grade": UngraduatedSchoolGrade().load(
                        application, unknown=EXCLUDE
                    ),
                    'self_introduction_and_study_plan': SelfIntroductionAndStudyPlan().load(
                        application, unknown=EXCLUDE
                    ),
                },
                200,
            )


class GEDApplicationView(HTTPMethodView):
    service = ApplicationService()
    schema = GEDApplicationRequestSchema()

    @jwt_required
    async def put(self, request: Request, token: Token):
        if not request.json:
            raise InvalidApplication

        try:
            raw_application = self.schema.load(request.json)
        except ValidationError:
            raise InvalidApplication

        application = {"user_email": token.jwt_identity}
        for v in raw_application.values():
            application.update(v)

        application = from_dict(
            data_class=GedApplicationModel, data=application
        )

        await self.service.sync_ged_application(application)
        return json({}, status=204)


class GraduatedApplicationView(HTTPMethodView):
    service = ApplicationService()
    schema = GraduatedApplicationRequestSchema()

    @jwt_required
    async def put(self, request: Request, token: Token):
        if not request.json:
            raise InvalidApplication

        try:
            raw_application = self.schema.load(request.json)
        except ValidationError:
            raise InvalidApplication

        application = {"user_email": token.jwt_identity}
        for v in raw_application.values():
            application.update(v)

        for v in [
            "korean",
            "social",
            "history",
            "math",
            "english",
            "tech_and_home",
            "science",
        ]:
            application[v] = ''.join(application[v])

        application = from_dict(
            data_class=GraduatedApplicationModel, data=application
        )
        dataclasses.replace(application, school_name="2019")

        await self.service.sync_graduated_applicant(application)
        return json({}, status=204)


class UngraduatedApplicationView(HTTPMethodView):
    service = ApplicationService()
    schema = UngraduatedApplicationRequestSchema()

    @jwt_required
    async def put(self, request: Request, token: Token):
        if not request.json:
            raise InvalidApplication

        try:
            raw_application = self.schema.load(request.json)
        except ValidationError:
            raise InvalidApplication

        application = {"user_email": token.jwt_identity}
        for v in raw_application.values():
            application.update(v)

        for v in [
            "korean",
            "social",
            "history",
            "math",
            "english",
            "tech_and_home",
            "science",
        ]:
            application[v] = ''.join(application[v])

        application = from_dict(
            data_class=UngraduatedApplicationModel, data=application
        )

        await self.service.sync_ungraduated_applicant(application)
        return json({}, status=204)


class FinalSubmitView(HTTPMethodView):
    service = FinalizeApplicationService()

    @jwt_required
    async def patch(self, request: Request, token: Token):
        await self.service.final_submit(token.jwt_identity)

        return json({}, status=204)
