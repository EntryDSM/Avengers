from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Optional


@dataclass(frozen=True)
class BaseApplication:
    user_email: str
    apply_type: Optional[str]  # enum
    additional_type: Optional[str]  # enum
    is_daejeon: Optional[bool]
    name: Optional[str]
    sex: Optional[str]  # enum
    birth_date: Optional[date]
    parent_name: Optional[str]
    parent_tel: Optional[str]
    applicant_tel: Optional[str]
    address: Optional[str]
    post_code: Optional[str]


@dataclass(frozen=True)
class BaseCommonApplication(BaseApplication):
    student_number: Optional[str]
    school_name: Optional[str]
    school_tel: Optional[str]
    school_code: Optional[str]
    volunteer_time: Optional[int]
    full_cut_count: Optional[int]
    period_cut_count: Optional[int]
    late_count: Optional[int]
    early_leave_count: Optional[int]
    korean: Optional[str]
    social: Optional[str]
    history: Optional[str]
    math: Optional[str]
    science: Optional[str]
    tech_and_home: Optional[str]
    english: Optional[str]
    self_introduction: Optional[str]
    study_plan: Optional[str]
    first_grade_score: Optional[Decimal]
    second_grade_score: Optional[Decimal]
    third_grade_score: Optional[Decimal]
