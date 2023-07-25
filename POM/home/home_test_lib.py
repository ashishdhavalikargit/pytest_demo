""" Dashboard page Functions """
import logging
from re import I
import time
from POM.base_pom import BasePOM
from POM.home.home_page_objects import home_page_locator
logger = logging.getLogger(__name__)

class homepage(BasePOM):
    """
    Dashboard Functions
    """
    def __init__(self):
        try:
            super().__init__()
            self.driver = self.browser.get_driver()
            self.action.maximize_window(self.driver)
            self.get_home_page(driver=self.driver)
            self.home_page = home_page_locator(self.driver)
        except Exception as e:
            logger.error(
                "Failed to initialize the homepage %s", e)

    def google_search(self):
        search_box = self.home_page.search_box()
        logger.info("searching text")
        self.action.send_value(search_box,"pytest framework")
        outer_page=self.home_page.outer_page()
        self.action.click(outer_page)
        search_buttom = self.home_page.search_buttom()
        logger.info("clicking on search button")
        self.action.click(search_buttom)
        time.sleep(5)
        logger.info("closing browser")
        self.close_driver(self.driver)
        return True
