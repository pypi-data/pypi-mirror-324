import sys

from loguru import logger
from pydantic import HttpUrl
import sentry_sdk

from ._types import Environment


def setup_logger(environment: Environment) -> None:
    logger.remove()
    logger.add(sys.stdout, level='INFO', serialize=environment != Environment.LOCAL)


def setup_sentry(sentry_dsn: HttpUrl | None, environment: Environment) -> None:
    if sentry_dsn:
        sentry_sdk.init(
            dsn=str(sentry_dsn),
            environment=environment,
            traces_sample_rate=0.2 if environment == Environment.PROD else 1.0,
        )
