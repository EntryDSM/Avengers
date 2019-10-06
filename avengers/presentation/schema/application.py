import decimal

from marshmallow import Schema, validate
from marshmallow.fields import Boolean, Decimal, Integer
from marshmallow.fields import List as ListField
from marshmallow.fields import Nested, String

from avengers.presentation.schema.common import Date


class Classification(Schema):
    apply_type = String(
        required=True,
        allow_none=True,
        validate=validate.OneOf(
            [
                "COMMON",
                "MEISTER",
                "SOCIAL_ONE_PARENT",  # 한부모가족
                "SOCIAL_FROM_NORTH",  # 북한이탈주민
                "SOCIAL_MULTICULTURAL",  # 다문화가정
                "SOCIAL_BASIC_LIVING",  # 기초생활수급자
                "SOCIAL_LOWEST_INCOME",  # 차상위계층
                "SOCIAL_TEEN_HOUSEHOLDER",  # 소년소녀(청소년)가장
            ]
        ),
    )
    additional_type = String(
        required=True,
        allow_none=True,
        validate=validate.OneOf(
            ["NATIONAL_MERIT", "PRIVILEGED_ADMISSION", "NOT_APPLICABLE"]
        ),
    )
    is_daejeon = Boolean(required=True, allow_none=True)


class GraduatedClassification(Classification):
    graduated_year = String(
        required=True,
        allow_none=True,
        validate=[validate.Regexp(r"^\d{4}$"), validate.Length(equal=4)],
    )


class PersonalInformation(Schema):
    name = String(
        required=True, allow_none=True, validate=validate.Length(min=2, max=15)
    )
    sex = String(
        required=True,
        allow_none=True,
        validate=validate.OneOf(["MALE", "FEMALE"]),
    )
    birth_date = Date(required=True, allow_none=True)
    parent_name = String(
        required=True, allow_none=True, validate=validate.Length(min=2, max=15)
    )
    parent_tel = String(
        required=True,
        allow_none=True,
        validate=validate.Regexp(r"^01\d{8,9}$"),
    )  # phone number regex
    applicant_tel = String(
        required=True,
        allow_none=True,
        validate=validate.Regexp(r"^01\d{8,9}$"),
    )
    address = String(
        required=True,
        allow_none=True,
        validate=validate.Length(min=1, max=500),
    )
    post_code = String(
        required=True, allow_none=True, validate=validate.Regexp(r"\d{5}")
    )


class PersonalInformationWithSchoolInfo(PersonalInformation):
    student_number = String(
        required=True, allow_none=True, validate=validate.Regexp(r"\d{5}")
    )
    school_name = String(
        required=True, allow_none=True, validate=validate.Length(min=4, max=20)
    )
    school_tel = String(
        required=True,
        allow_none=True,
        validate=validate.Regexp(r"^01\d{8,9}$"),
    )


class GEDGrade(Schema):
    ged_average_score = Decimal(
        required=True,
        allow_none=True,
        places=10,
        rounding=decimal.ROUND_HALF_UP,
    )


class DiligenceGrade(Schema):
    volunteer_time = Integer(required=True, allow_none=True)
    full_cut_count = Integer(required=True, allow_none=True)
    period_cut_count = Integer(required=True, allow_none=True)
    late_count = Integer(required=True, allow_none=True)
    early_leave_count = Integer(required=True, allow_none=True)


class GraduatedSchoolGrade(Schema):
    korean = ListField(
        String(
            required=True,
            allow_none=False,
            validate=validate.OneOf(["A", "B", "C", "D", "E", "X"]),
        ),
        required=True,
        allow_none=False,
        validate=validate.Length(equal=6),
    )
    social = ListField(
        String(
            required=True,
            allow_none=False,
            validate=validate.OneOf(["A", "B", "C", "D", "E", "X"]),
        ),
        required=True,
        allow_none=False,
        validate=validate.Length(equal=6),
    )
    history = ListField(
        String(
            required=True,
            allow_none=False,
            validate=validate.OneOf(["A", "B", "C", "D", "E", "X"]),
        ),
        required=True,
        allow_none=False,
        validate=validate.Length(equal=6),
    )
    math = ListField(
        String(
            required=True,
            allow_none=False,
            validate=validate.OneOf(["A", "B", "C", "D", "E", "X"]),
        ),
        required=True,
        allow_none=False,
        validate=validate.Length(equal=6),
    )
    science = ListField(
        String(
            required=True,
            allow_none=False,
            validate=validate.OneOf(["A", "B", "C", "D", "E", "X"]),
        ),
        required=True,
        allow_none=False,
        validate=validate.Length(equal=6),
    )
    tech_and_home = ListField(
        String(
            required=True,
            allow_none=False,
            validate=validate.OneOf(["A", "B", "C", "D", "E", "X"]),
        ),
        required=True,
        allow_none=False,
        validate=validate.Length(equal=6),
    )
    english = ListField(
        String(
            required=True,
            allow_none=False,
            validate=validate.OneOf(["A", "B", "C", "D", "E", "X"]),
        ),
        required=True,
        allow_none=False,
        validate=validate.Length(equal=6),
    )


class UngraduatedSchoolGrade(GraduatedSchoolGrade):
    korean = ListField(
        String(
            required=True,
            allow_none=False,
            validate=validate.OneOf(["A", "B", "C", "D", "E", "X"]),
        ),
        required=True,
        allow_none=False,
        validate=validate.Length(equal=5),
    )
    social = ListField(
        String(
            required=True,
            allow_none=False,
            validate=validate.OneOf(["A", "B", "C", "D", "E", "X"]),
        ),
        required=True,
        allow_none=False,
        validate=validate.Length(equal=5),
    )
    history = ListField(
        String(
            required=True,
            allow_none=False,
            validate=validate.OneOf(["A", "B", "C", "D", "E", "X"]),
        ),
        required=True,
        allow_none=False,
        validate=validate.Length(equal=5),
    )
    math = ListField(
        String(
            required=True,
            allow_none=False,
            validate=validate.OneOf(["A", "B", "C", "D", "E", "X"]),
        ),
        required=True,
        allow_none=False,
        validate=validate.Length(equal=5),
    )
    science = ListField(
        String(
            required=True,
            allow_none=False,
            validate=validate.OneOf(["A", "B", "C", "D", "E", "X"]),
        ),
        required=True,
        allow_none=False,
        validate=validate.Length(equal=5),
    )
    tech_and_home = ListField(
        String(
            required=True,
            allow_none=False,
            validate=validate.OneOf(["A", "B", "C", "D", "E", "X"]),
        ),
        required=True,
        allow_none=False,
        validate=validate.Length(equal=5),
    )
    english = ListField(
        String(
            required=True,
            allow_none=False,
            validate=validate.OneOf(["A", "B", "C", "D", "E", "X"]),
        ),
        required=True,
        allow_none=False,
        validate=validate.Length(equal=5),
    )


class SelfIntroductionAndStudyPlan(Schema):
    self_introduction = String(
        required=True, allow_none=True, validate=validate.Length(max=1600)
    )
    study_plan = String(
        required=True, allow_none=True, validate=validate.Length(max=1600)
    )


class GEDApplicationRequestSchema(Schema):
    classification = Nested(Classification, required=True, allow_none=False)
    personal_information = Nested(
        PersonalInformation, required=True, allow_none=False
    )
    ged_grade = Nested(GEDGrade, required=True, allow_none=False)
    self_introduction_and_study_plan = Nested(
        SelfIntroductionAndStudyPlan, required=True, allow_none=False
    )


class GraduatedApplicationRequestSchema(Schema):
    classification = Nested(
        GraduatedClassification, required=True, allow_none=False
    )
    personal_information = Nested(
        PersonalInformationWithSchoolInfo, required=True, allow_none=False
    )
    diligence_grade = Nested(DiligenceGrade, required=True, allow_none=False)
    school_grade = Nested(
        GraduatedSchoolGrade, required=True, allow_none=False
    )
    self_introduction_and_study_plan = Nested(
        SelfIntroductionAndStudyPlan, required=True, allow_none=False
    )


class UngraduatedApplicationRequestSchema(GraduatedApplicationRequestSchema):
    personal_information = Nested(
        PersonalInformationWithSchoolInfo, required=True, allow_none=False
    )
    school_grade = Nested(
        UngraduatedSchoolGrade, required=True, allow_none=False
    )
