from dataclasses import dataclass

from avengers.data.models import UnGedApplication


@dataclass(frozen=True)
class UngraduatedApplicationModel(UnGedApplication):
    """Grades include up to 3-1(semester 5)"""
