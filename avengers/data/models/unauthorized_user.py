from dataclasses import dataclass


@dataclass
class UnauthorizedUserModel:
    email: str
    password: str
