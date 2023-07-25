import pytest
import logging
from POM.home.home_test_lib import homepage
from lib.home_lib import home_lib

logger = logging.getLogger(__name__)

class Test_homepage:

    @pytest.mark.tc_example
    def test_tc_1_example(self, request):
        home_obj = homepage()
        logger.info("checking the search functionality")
        assert home_obj.google_search()

    @pytest.mark.tc_example2
    def test_tc_2_example(self, request):
        home = home_lib()
        check_response = home.get_homepage_api_status()
        logger.info("Checking the status of the request")
        logger.info(check_response)
        assert "200" in check_response, "response to the get request is not 200"
