from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

from avengers.data.models import BaseApplication


@dataclass(frozen=True)
class GedApplicationModel(BaseApplication):
    ged_average_score: Optional[Decimal]
    self_introduction: Optional[str]
    study_plan: Optional[str]
