import os
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class HTTPConfiguration:
    host: str
    port: int


@dataclass(frozen=True)
class SentryConfiguration:
    dsn: Optional[str]


@dataclass(frozen=True)
class Configuration:
    debug: bool
    environment: Optional[str]
    http: HTTPConfiguration
    sentry: SentryConfiguration


def init_config(d: dict = None) -> Configuration:
    d = d or os.environ
    return Configuration(
        d.get('AVENGERS_DEBUG', str(False)).upper() == str(True).upper(),
        d.get('AVENGERS_ENVIRONMENT'),
        HTTPConfiguration(
            d.get('AVENGERS_HTTP_HOST', '0.0.0.0'),
            int(d.get('AVENGERS_HTTP_PORT', 8000)),
        ),
        SentryConfiguration(d.get('AVENGERS_SENTRY_DSN')),
    )
