""" Selenium Operations"""
import logging
from selenium import webdriver
from os.path import dirname, abspath, join
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

""" This Package create webdriver for guiLib """

base_path = dirname(dirname(abspath(__file__)))
logger = logging.getLogger(__name__)


class Browsers:
    def __init__(self):

        self.__log = logging.getLogger(__name__)
        self.__driver_provider = {
            "firefox": (webdriver.Firefox, webdriver.FirefoxProfile),
            "chrome": (webdriver.Chrome, webdriver.ChromeOptions),
        }

    def get_driver(
        self, browser_type="chrome", headless=False, grid=False, grid_status=None
    ):
        """
        :param browser_type: browser on which user want to run the test
        :param headless:  Headless mode for linux
        :param grid: To run the test on selenium Grid
        :param grid_status : value of grid hub
        :return: driver instance to initiate the test.
        """
        self.__log.debug("Initiating the driver...!")
        #  browser path is required for execution using headless
        #  browser.
        logger.info(f"base path is : {base_path}")
        browser_path = join(base_path, "webdrivers", browser_type, "chromedriver.exe")
        dreiver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        return dreiver


class SeleniumElementSearch(object):
    """Selenium Element Search"""

    def __init__(self):
        self.__log = logging.getLogger(__name__)
        self.__locator = {
            "id": By.ID,
            "name": By.NAME,
            "xpath": By.XPATH,
            "linktext": By.LINK_TEXT,
            "classname": By.CLASS_NAME,
            "partiallinktext": By.PARTIAL_LINK_TEXT,
            "tagname": By.TAG_NAME,
            "cssselector": By.CSS_SELECTOR,
        }
        self.__require_element = [
            EC.presence_of_element_located,
            EC.presence_of_all_elements_located,
        ]

    def find_element(
        self, webdriver, locator, element, multiple=False, timeout=20, poll_frequency=5
    ):
        wait = WebDriverWait(
            webdriver,
            timeout,
            poll_frequency=poll_frequency,
            ignored_exceptions=[NoSuchElementException],
        )
        self.__log.debug(f"finding element {element} which is {locator}")
        return wait.until(
            self.__require_element[multiple]((self.__locator[locator], element))
        )


class Action(object):
    """this class contains all actions regarding guiLib"""

    def __init__(self):
        pass

    def click(self, element):
        """
        perform click operation
        :param element:
        :return:
        """
        try:
            element.click()
        except Exception as e:
            logger.error("Failed to perform click action : %s", e)

    def maximize_window(self, webdriver):
        """
        maximize the guiLib webdriver window
        :param webdriver:
        :return:webdriver
        """
        try:
            webdriver.maximize_window()
            return webdriver
        except Exception as e:
            logger.error("Failed to maximize_window : %s", e)

    def previous_page(self, webdriver):
        """
        move to previous page
        :param webdriver:
        :return:webdriver
        """
        try:
            webdriver.back()
            return webdriver
        except Exception as e:
            logger.error("Failed to load previous_page: %s", e)

    def next_page(self, webdriver):
        """
        move to next page
        :param webdriver:
        :return:webdriver
        """
        try:
            webdriver.forward()
            return webdriver
        except Exception as e:
            logger.error("failed to load forward page: %s", e)

    def clear(self, element):
        """
        clear the element
        :param element:
        :return:
        """
        try:
            element.clear()
        except Exception as e:
            logger.error("Failed to perform clear operation: %s", e)

    def double_click(self, webdriver, element):
        """
        perform double click action on element
        :param webdriver:
        :param element:
        :return:webdriver
        """
        try:
            actionchains = ActionChains(webdriver)
            actionchains.double_click(element).perform()
            return webdriver
        except Exception as e:
            logger.error("Failed to perform double_click action: %s", e)

    def screenshot(self, webdriver, filename):
        """
        It takes screenshot of webdriver at that point of time
        :param webdriver:
        :param filename:
        :return: webdriver
        """
        try:
            webdriver.get_screenshot_as_file(filename)
            return webdriver
        except Exception as e:
            logger.error("Failed to take screenshot : %s", e)

    def hover(self, webdriver, element):
        """
        this module hover on the element
        :param webdriver:
        :param element:
        :return: webdriver
        """
        try:
            actionchains = ActionChains(webdriver)
            actionchains.move_to_element(element).perform()
            return webdriver
        except Exception as e:
            logger.error("Failed to hover: %s", e)

    def long_press(self, webdriver, element):
        """
        this does the longpress action on the element
        :param webdriver:
        :param element:
        :return: webdriver
        """
        try:
            actionchains = ActionChains(webdriver)
            actionchains.click_and_hold(element).perform()
            return webdriver
        except Exception as e:
            logger.error("Failed to perform long_press action: %s", e)

    def context_click(self, webdriver, element):
        """
        this perform context click on the given element
        :param webdriver:
        :param element:
        :return:web driver
        """
        try:
            actionchains = ActionChains(webdriver)
            actionchains.context_click(element).perform()
            return webdriver
        except Exception as e:
            logger.error("Failed to perform context_click action: %s", e)

    def switch_window(self, webdriver, window_name):
        """
        this module switch window in webdriver
        :param webdriver:
        :param window_name:
        :return: webdriver
        """
        try:
            webdriver.switch_to_window(window_name)
            return webdriver
        except Exception as e:
            logger.error("Failed to switch window: %s", e)

    def switch_frame(self, webdriver, element):
        """
        this module switches frame in webdriver
        :param webdriver:
        :param element:
        :return: webdriver
        """
        try:
            webdriver.switch_to.frame(element)
            return webdriver
        except Exception as e:
            logger.error("Failed to switch frame : %s", e)

    def send_value(self, element, value, do_clear=True):
        """
        It performs the send value operation on given element
        :param element:
        :param value:
        :param do_clear:
        :return:
        """
        try:
            if do_clear:
                element.clear()
            element.send_keys(value)
        except Exception as e:
            logger.error("Failed to send value %s with error msg : %s", value, e)

    def drag_and_drop(self, webdriver, source, target):
        """
        this perform drag and drop on given element
        :param webdriver:
        :param source:
        :param target:
        :return:webdriver
        """
        try:
            actionchains = ActionChains(webdriver)
            actionchains.drag_and_drop(source, target).perform()
            return webdriver
        except Exception as e:
            logger.error("Failed to erform drag and drop : %s", e)

    def get_url(self, driver, url):
        """
        Navigate to the required url
        :param driver: guiLib web driver
        :param url: url to navigate
        """
        try:
            logger.info("Trying to navigate from url %s", url)
            return driver.get(url)
        except Exception as e:
            logger.error("Failed to get URL with msg : %s", e)

    def scroll(self, driver, x_axis=0, y_axis=0):
        """
        Scrolls the page
        :param web driver:
        :param x_axis: x-co-ordinate
        :param y_axis: y-co-ordinate
        :return:
        """
        try:
            driver.execute_script(
                "window.scrollTo(" + str(x_axis) + ", " + str(y_axis) + ")"
            )
            return driver
        except Exception as e:
            logger.error("Failed to scroll with msg : %s", e)

    def set_browser_size(self, driver, width, height):
        try:
            logger.info(
                f"Trying to set the browser size to width {width} and height {height}"
            )
            driver.set_window_size(width, height)
        except Exception as e:
            logger.error("Trying to navigate from url %s to %s", e)
