"""" Home Page Objects """
import logging
from POM.element_locators import home_page
from gui.gui_core_lib import SeleniumElementSearch
from selenium.common.exceptions import NoSuchElementException

logger = logging.getLogger(__name__)
class home_page_locator:
    """
    Dashboard Page Objects
    """
    def __init__(self, driver):
        self.elem = None
        self.driver = driver
        self.element_search = SeleniumElementSearch()
        self.locators = home_page

    def search_box(self):
        try:
            self.elem = self.element_search.find_element(self.driver, home_page.search_box["locator_type"],home_page.search_box["locator_value"])
        except NoSuchElementException:
            logger.info('No element of that id present!')
        return self.elem

    def outer_page(self):
        try:
            self.elem = self.element_search.find_element(
                self.driver, home_page.outer_page["locator_type"],home_page.outer_page["locator_value"])
        except NoSuchElementException:
            logger.info('No element of that id present!')
        return self.elem

    def search_buttom(self):
        try:
            self.elem = self.element_search.find_element(
                self.driver, home_page.search_buttom["locator_type"],home_page.search_buttom["locator_value"])
        except NoSuchElementException:
            logger.info('No element of that id present!')
        return self.elem