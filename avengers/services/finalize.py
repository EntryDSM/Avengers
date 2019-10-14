import decimal
import os
from dataclasses import asdict

from dacite import from_dict

from avengers import config
from avengers.data.exc import DataNotFoundError
from avengers.data.models import BaseCommonApplication
from avengers.data.models.ged_application import GedApplicationModel
from avengers.data.models.graduated_application import GraduatedApplicationModel
from avengers.data.models.ungraduated_application import UngraduatedApplicationModel
from avengers.data.repositories.ged_application import GedApplicationRepository
from avengers.data.repositories.graduated_application import GraduatedApplicationRepository
from avengers.data.repositories.ungraduated_application import UnGraduatedApplicationRepository
from avengers.data.repositories.user import UserRepository
from avengers.presentation.exceptions import (
    AlreadyFinalSubmitted,
    ApplicationNotFound,
    FinalValidationFailed,
)
from avengers.services.application import ApplicationService
from avengers.services.mypage import MyPageService


class FinalizeApplicationService:
    application_service = ApplicationService()
    my_page_service = MyPageService()

    user_repo = UserRepository()
    ged_repo = GedApplicationRepository()
    graduated_repo = GraduatedApplicationRepository()
    ungraduated_repo = UnGraduatedApplicationRepository()

    async def final_submit(self, email):
        if (await self.my_page_service.retrieve_status(email))[
            "is_final_submit"
        ]:
            raise AlreadyFinalSubmitted

        try:
            application = await self.application_service.get(email)
        except ApplicationNotFound:
            raise FinalValidationFailed

        for c in asdict(application).values():
            if c is None:
                raise FinalValidationFailed

        try:
            user = await self.user_repo.get(email)
        except DataNotFoundError:
            raise FinalValidationFailed

        if not os.path.exists(f"{config.PICTURE_DIR}/{email}"):
            raise FinalValidationFailed

        if isinstance(application, GedApplicationModel):
            if application.ged_average_score < decimal.Decimal(60):
                raise FinalValidationFailed
            grades = await _process_ged_grades(application)

        else:
            grades, application_grade_score = await _process_applicant_grades(application)
            new_application = asdict(application)
            new_application.update(**application_grade_score)

            if isinstance(application, GraduatedApplicationModel):
                new_application = from_dict(data_class=GraduatedApplicationModel, data=new_application)
                await self.graduated_repo.upsert(new_application)

            elif isinstance(application, UngraduatedApplicationModel):
                new_application = from_dict(data_class=UngraduatedApplicationModel, data=new_application)
                await self.ungraduated_repo.upsert(new_application)

        await self.user_repo.update(
            user.email, {**grades, 'is_final_submit': True}
        )


async def _process_ged_grades(application: GedApplicationModel):
    avg_score = application.ged_average_score
    max_conversion_score = 90

    volunteer_score = decimal.Decimal(
        (avg_score - 40) / 60 * 12 + 3
    ).quantize(decimal.Decimal('0.001'), decimal.ROUND_HALF_UP)
    attendance_score = 15

    if application.apply_type == 'COMMON':
        max_conversion_score = 150

    conversion_score = decimal.Decimal(
        (avg_score - 50) / 50 * max_conversion_score
    ).quantize(decimal.Decimal('0.001'), decimal.ROUND_HALF_UP)

    return {
        "volunteer_score": volunteer_score,
        "attendance_score": attendance_score,
        "conversion_score": conversion_score,
        "final_score": volunteer_score + attendance_score + conversion_score,
    }


async def _process_applicant_grades(application: BaseCommonApplication):
    volunteer_score = _calculate_volunteer_score(application.volunteer_time)

    attendance_score = _calculate_attendance_score(
        application.period_cut_count,
        application.late_count,
        application.early_leave_count,
        application.full_cut_count,
    )

    score_matrix_by_semester = list(
        zip(
            *[
                _convert_to_score(application.korean),
                _convert_to_score(application.english),
                _convert_to_score(application.math),
                _convert_to_score(application.science),
                _convert_to_score(application.social),
                _convert_to_score(application.tech_and_home),
                _convert_to_score(application.history),
            ]
        )
    )

    subject_scores_by_semester = [
        _calculate_semester_total_score(s) for s in score_matrix_by_semester
    ]

    is_graduated = len(subject_scores_by_semester) == 6

    first_grade_li = subject_scores_by_semester[:2]
    second_grade_li = subject_scores_by_semester[2:4]
    third_grade_score = (
        sum(subject_scores_by_semester[4:])
        if is_graduated
        else subject_scores_by_semester[4] * 2
    )

    is_first_grade_empty = first_grade_li == ['X', 'X']
    is_second_grade_empty = second_grade_li == ['X', 'X']

    if is_first_grade_empty and is_second_grade_empty:
        first_grade_score = second_grade_score = third_grade_score
    elif is_first_grade_empty and not is_second_grade_empty:
        first_grade_score = (
            sum(second_grade_li) + third_grade_score
        ) * decimal.Decimal('0.5')
        second_grade_score = sum(second_grade_li)
    elif not is_first_grade_empty and is_second_grade_empty:
        first_grade_score = sum(first_grade_li)
        second_grade_score = (
            sum(first_grade_li) + third_grade_score
        ) * decimal.Decimal('0.5')
    else:
        validated_first_grade = [
            s for s in first_grade_li if isinstance(s, decimal.Decimal)
        ]
        validated_second_grade = [
            s for s in second_grade_li if isinstance(s, decimal.Decimal)
        ]

        first_grade_score = (
            validated_first_grade[0] * 2
            if len(validated_first_grade) == 1
            else sum(validated_first_grade)
        )
        second_grade_score = (
            validated_second_grade[0] * 2
            if len(validated_second_grade) == 1
            else sum(validated_second_grade)
        )

    multiple12 = decimal.Decimal('2.7')
    multiple3 = decimal.Decimal('3.6')

    if application.apply_type == 'COMMON':
        multiple12 = decimal.Decimal('4.5')
        multiple3 = 6

    first_grade_score *= multiple12
    second_grade_score *= multiple12
    third_grade_score *= multiple3

    conversion_score = decimal.Decimal(
        first_grade_score + second_grade_score + third_grade_score
    ).quantize(decimal.Decimal("0.001"), decimal.ROUND_HALF_UP)

    return {
               "volunteer_score": volunteer_score,
               "attendance_score": attendance_score,
               "conversion_score": conversion_score,
               "final_score": volunteer_score + attendance_score + conversion_score,
           }, {
               "first_grade_score": first_grade_score,
               "second_grade_score": second_grade_score,
               "third_grade_score": third_grade_score,
           }


def _convert_to_score(subject_score: str) -> list:
    return [
        {'A': 5, 'B': 4, 'C': 3, 'D': 2, 'E': 1, 'X': 'X'}[s]
        for s in subject_score
    ]


def _calculate_semester_total_score(scores: tuple):
    cnt = 0
    s = 0
    for score in scores:
        if isinstance(score, int):
            cnt += 1
            s += score

    return decimal.Decimal(str(s / cnt)) if cnt else 'X'


def _calculate_volunteer_score(volunteer_time: int) -> decimal.Decimal:
    if volunteer_time >= 50:
        volunteer_score = decimal.Decimal('15')
    elif 49 >= volunteer_time >= 15:
        volunteer_score = decimal.Decimal(
            decimal.Decimal(str(volunteer_time - 14)) / 36 * 12 + 3
        ).quantize(decimal.Decimal('0.001'), decimal.ROUND_HALF_UP)
    else:
        volunteer_score = decimal.Decimal('3')

    return volunteer_score


def _calculate_attendance_score(
    period_cut_count: int,
    late_count: int,
    early_leave_count: int,
    full_cut_count: int,
) -> int:
    conversion_absence_days: int = (
        period_cut_count + late_count + early_leave_count
    ) // 3
    total_absence_days: int = full_cut_count + conversion_absence_days

    if total_absence_days >= 15:
        attendance_score = 0
    else:
        attendance_score = 15 - total_absence_days

    return attendance_score
