from dataclasses import dataclass
from typing import Optional

from avengers.data.models import BaseCommonApplication


@dataclass(frozen=True)
class GraduatedApplicationModel(BaseCommonApplication):
    graduated_year: Optional[str]
