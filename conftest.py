import logging
import pytest
import config
from rest_api.rest_client import RestClient


logger = logging.getLogger(__name__)

def pytest_addoption(parser):
    parser.addoption("--dirname", action="store", default="report directory")

@pytest.fixture(scope="class")
def dirname(pytestconfig):
    return pytestconfig.getoption("dirname")

@pytest.fixture(scope='class', autouse=True)
def setup_teardown(request):
    print("=========================================================")
    logger.info("==============Setup Inititalised=============")
    logger.info("creating driver instance created")
    request.cls.restclient = RestClient(config.base_url)
    logger.info("==============Setup Completed=============")
    yield
    logger.info("==============Teardown Inititalised=============")
    logger.info("Clean-up started")
    logger.info("Clean-up completed")
    logger.info("==============Teardown Completed=============")