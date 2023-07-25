import logging
import config
from rest_api.rest_client import RestClient

logger = logging.getLogger(__name__)
class home_lib:

    def __init__(self):
        try:
            self.http = RestClient(config.base_url)
        except Exception as e:
            logger.error(
                "Failed to initialize the home lib %s", e)

    def get_homepage_api_status(self):
        status = self.http.get_request("",fmt="raw")
        return str(status.status_code)