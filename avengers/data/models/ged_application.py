from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Optional


@dataclass(frozen=True)
class GedApplicationModel:
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
    ged_average_score: Optional[Decimal]
    self_introduction: Optional[str]
    study_plan: Optional[str]
