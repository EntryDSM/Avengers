from dataclasses import dataclass

from avengers.data.models import BaseCommonApplication


@dataclass(frozen=True)
class UngraduatedApplicationModelBase(BaseCommonApplication):
    """Grades include up to 3-1(semester 5)"""
