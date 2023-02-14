import sys

from dependency_injector.wiring import inject, Provide

from container import Container
from service.report_generator_service import reportGeneratorService


@inject
def handle(report_generatorService: reportGeneratorService = Provide[Container.reportGeneratorService]):
    return report_generatorService.processReport()


def lambda_handler():
    container = Container()
    container.wire(
        modules=[sys.modules[__name__]])
    return handle()


# lambda_handler()
