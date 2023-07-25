import logging
import os
import time
import config
from platform import system
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException
from gui.gui_core_lib import SeleniumElementSearch, Action, Browsers

logger = logging.getLogger(__name__)


class BasePOM(object):
    def __init__(self):
        """Contructor for Base POM"""
        self.action = Action()
        self.browser = Browsers()
        self.elementsearch = SeleniumElementSearch()
        self.home_page_url = config.base_url

    def wait_until_element_is_clickable(self, driver, repo, wait_time):
        """
        This module will wait until element is click able
        :param driver: Selenium web driver
        :param repo: element value from repository
        :param wait_time: wait time
        :return:
        """
        result = False
        try:
            logger.info("Fetching element %s", repo)
            fetch_enable_element = self.elementsearch.get_element(
                driver, self.page_element_repo.get(repo)
            )
            logger.info("Waiting the element to be enabled ...")
            timeout = time.time() + wait_time  # 5 minutes from now 300
            while not fetch_enable_element.is_enabled():
                if time.time() > timeout:
                    logger.info("time out...")
                    break
                fetch_enable_element = self.elementsearch.get_element(
                    driver, self.page_element_repo.get(repo)
                )
            logger.info("Detecting the element ...")
            if fetch_enable_element.is_enabled():
                result = True
                logger.info("element is enabled now ...")
            return fetch_enable_element, result
        except Exception as e:
            logger.error(
                "Failed to wait until element is click able with message : %s", e
            )

    def wait_until_element_is_displayed(self, driver, repo, wait_time):
        """
        This module will wait until element is displayed
        :param driver: Selenium web driver
        :param repo: element value from repository
        :param wait_time: wait time
        :return:
        """
        result = False
        try:
            displayed_element = self.elementsearch.get_element(
                driver, self.page_element_repo.get(repo)
            )
            timeout = time.time() + wait_time
            while not displayed_element.is_displayed():
                displayed_element = self.elementsearch.get_element(
                    driver, self.page_element_repo.get(repo)
                )
                if time.time() > timeout:
                    logger.info("time out...")
                    break
            if displayed_element.is_displayed():
                result = True
                logger.info("element is displayed now ...")
            return displayed_element, result
        except Exception as e:
            logger.error(
                "Failed to wait until element is displayed with message : %s", e
            )

    def check_ui_element_presence(self, driver, element):
        """
        Check the ui element is present or not
        :param driver: selenium web driver
        :param element: element value from repository
        :return: Boolean value of element present or not
        """
        try:
            logger.info("Finding element using ===>%s", element)
            element = self.elementsearch.get_element(
                driver,
                self.page_element_repo.get(element),
                number_of_itrations=10,
                time_out=10,
            )
            if element:
                logger.info("Element found is True")
                return True
            else:
                logger.error("Failed to find element")
                return False
        except Exception as e:
            logger.error("Failed to get element %s", e)

    def get_ui_values(
        self,
        driver,
        repo,
        tooltip=False,
        class_value=False,
        href=False,
        search_number_of_times=5,
        inner_html=False,
        inner_text=False,
    ):
        """
        return required ui text
        :param driver: selenium web driver
        :param repo: value of element from repository
        :param tooltip: In case tooltip value required
        :param class_value : In case class value required
        :param href : In case href value required
        :return: required value fetched from ui
        """
        try:
            time.sleep(10)  # waiting for page to load
            logger.info("try to fetch data from ui using string -->%s", repo)
            element_obj = self.elementsearch.get_element(
                driver,
                self.page_element_repo.get(repo),
                number_of_itrations=search_number_of_times,
            )
            if tooltip:
                result = element_obj.get_attribute("tooltip")
            elif class_value:
                result = element_obj.get_attribute("class")
            elif href:
                result = element_obj.get_attribute("href")
            elif inner_html:
                result = element_obj.get_attribute("innerHTML")
            elif inner_text:
                result = element_obj.get_attribute("innerText")
            else:
                result = element_obj.text
                logger.info("Text value of element %s", result)
                count = 0
                while result == None:
                    logger.info("The text is none in the element fetching it again")
                    if count < 6:
                        logger.info(
                            "Attempted the maximum time and no text value found coming out"
                        )
                        break
                    time.sleep(20)
                    result = self.get_ui_values(driver, repo)
                    count += 1
            logger.info("Getting value from UI ===> %s", result)
            return result
        except StaleElementReferenceException:
            time.sleep(10)
            logger.info("Element stale exception trying to fetch the value again")
            if tooltip:
                self.get_ui_values(driver, repo, tooltip=True)
            elif class_value:
                self.get_ui_values(driver, repo, class_value=True)
            elif href:
                self.get_ui_values(driver, repo, href=True)
            else:
                self.get_ui_values(driver, repo)
        except Exception as e:
            logger.error("failed to get text from ui as : %s", e)

    def check_for_waiting_item(self, driver, repo, time_out=False):
        """
        Wait until the page loading item appears
        :param driver: Selenium web driver
        :param repo: element's key in repository
        :return: None
        """
        try:
            driver.implicitly_wait(3)
            logger.info("Please wait while page is loading ...")
            fetch_wait_icon = self.elementsearch.get_element(
                driver,
                self.page_element_repo.get(repo),
                expect_single_elem=False,
                number_of_itrations=3,
                time_out=5,
            )
            timeout = time.time() + 180
            while fetch_wait_icon:
                fetch_wait_icon = self.elementsearch.get_element(
                    driver,
                    self.page_element_repo.get(repo),
                    expect_single_elem=False,
                    number_of_itrations=3,
                    time_out=5,
                )
                if time.time() > timeout and time_out:
                    logger.info("time out...")
                    break
            logger.info("Page loading complete ...")
            time.sleep(5)
        except Exception as e:
            logger.error("Failed to fetch waiting icon for reason : %s", e)

    def get_home_page(self, driver):
        """
        this method moves to job home page
        :param:Selenium driver
        """
        try:
            logger.info("Moving to URL: %s", self.home_page_url)
            self.action.get_url(driver, self.home_page_url)
            logger.info("home page loaded...")
        except Exception as e:
            logger.error("Unable to move to home page %s", e)

    def close_driver(self, driver):
        driver.close()
