from dataclasses import dataclass

from avengers.data.models import UnGedApplication


@dataclass(frozen=True)
class GraduatedApplicationModel(UnGedApplication):
    """Grades include up to 3-2(semester 6)"""
