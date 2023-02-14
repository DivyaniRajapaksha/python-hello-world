import logging
import os
import sys
import boto3
from dependency_injector import containers, providers
from shared.constants import APP_ENV, DEFAULT_APP_ENV, APP_NAME
from service.report_generator_service import reportGeneratorService


def getAppEnv():
    return os.getenv(APP_ENV, DEFAULT_APP_ENV)


def get_logger():
    extra = {'app_name': APP_NAME, 'app_env': getAppEnv()}

    logger = logging.getLogger(__name__)
    for handler in logger.handlers:
        logger.removeHandler(handler)
    syslog = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        '{"AppName" : "%(app_name)s", "AppEnv" : "%(app_env)s, "Date" : "%(asctime)s", "Message" : "%(message)s"}'
    )
    syslog.setFormatter(formatter)
    logger.setLevel(logging.INFO)
    logger.addHandler(syslog)
    logger.propagate = False

    logger = logging.LoggerAdapter(logger, extra)
    return logger


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    session = boto3.session.Session()

    reportGeneratorService = providers.Singleton(
        reportGeneratorService, logger=get_logger())
