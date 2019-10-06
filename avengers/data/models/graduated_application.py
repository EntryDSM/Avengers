from dataclasses import dataclass
from typing import Optional

from avengers.data.models import BaseCommonApplication


@dataclass(frozen=True)
class GraduatedApplicationModel(BaseCommonApplication):
    """Grades include up to 3-2(semester 6)"""

    graduated_year = Optional[str]
