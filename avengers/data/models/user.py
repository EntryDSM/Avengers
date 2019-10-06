from dataclasses import dataclass
from decimal import Decimal
from typing import Optional


@dataclass(frozen=True)
class UserModel:
    email: str
    password: str
    receipt_code: Optional[int]
    is_paid: Optional[bool]
    is_printed_application_arrived: Optional[bool]
    is_passed_first_apply: Optional[bool]
    is_passed_interview: Optional[bool]
    is_final_submit: Optional[bool]
    exam_code: Optional[str]
    volunteer_score: Optional[Decimal]
    attendance_score: Optional[int]
    conversion_score: Optional[Decimal]
    final_score: Optional[Decimal]
