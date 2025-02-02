from selenium.common import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
from duauto.locator_mapping import LocatorMapping
from duauto.action_mapping import ActionMapping


class Actions:

    def __init__(self, driver, implicit_wait=10):
        """
        Actions class for all page objects, providing basic Selenium actions.

        :param driver: WebDriver instance passed during initialization.
        """
        self.driver = driver
        self.logger = logging.getLogger(__name__)
        self.wait = WebDriverWait(driver, implicit_wait)
        self.locator_mapping = LocatorMapping()
        self.action_mapping = ActionMapping()

    def find_element(self, locator_type, locator):
        """
        Finds a web element based on locator type and locator value.

        :param locator_type: The type of the locator (id, css_selector, xpath, name, class_name).
        :param locator: The actual locator value (e.g., 'submit-button', '.button-class').
        :return: WebElement found based on the locator type and value.
        """
        try:
            locator_strategy = self.locator_mapping.get_by_type(locator_type)
            # Adding explicit wait here for element visibility
            element = self.wait.until(EC.visibility_of_element_located((locator_strategy, locator)))
            self.logger.info(f"Element found using {locator_type} with locator: {locator}")
            return element
        except NoSuchElementException as e:
            self.logger.error(f"Failed to find element using {locator_type} with locator: {locator}")
            raise e

    def find_elements(self, locator_type, locator):
        """
        Finds multiple elements on the web page using the provided locator type and value.

        :param locator_type: The type of the locator (id, css_selector, xpath, name, class_name).
        :param locator: The actual locator value (e.g., 'submit', 'button-class').
        :return: A list of WebElements found, or raises an exception if not found.
        """
        try:
            locator_strategy = self.locator_mapping.get_by_type(locator_type)
            # Adding explicit wait here for elements presence
            elements = self.wait.until(EC.presence_of_all_elements_located((locator_strategy, locator)))
            self.logger.info(f"Elements found using {locator_type} with locator: {locator}")
            return elements
        except NoSuchElementException as e:
            self.logger.error(f"Failed to find elements using {locator_type} with locator: {locator}")
            raise NoSuchElementException(f"Elements not found: {locator_type} = {locator}")
        except Exception as e:
            self.logger.error(f"Error occurred while finding elements: {locator_type} = {locator}. Error: {e}")
            raise e

    def find_elements_and_click(self, locator_type, locator, index: int):
        """
        Finds multiple elements and clicks one at the specified index.
        """
        try:
            elements = self.find_elements(locator_type, locator)
            if not elements:
                raise Exception("No elements found for the given locator.")
            if index < len(elements):
                elements[index].click()
                self.logger.info(f"Clicked element at index {index} with {locator_type} and locator: {locator}")
            else:
                raise Exception(f"Index {index} is out of range for elements found.")
        except Exception as e:
            raise Exception(f"Failed to click the element at index {index}: {locator_type} = {locator}. Error: {e}")

    def input_text(self, locator_type, locator, text):
        """
        Inputs text into an element found by the specified locator type and value.

        :param locator_type: The type of the locator (id, css_selector, xpath, name, class_name).
        :param locator: The actual locator.
        :param text: The text to input into the found element.
        """
        element = self.find_element(locator_type, locator)
        try:
            element.send_keys(text)
            self.logger.info(f"Input text '{text}' into element with {locator_type} and locator '{locator}'")
        except Exception as e:
            self.logger.error(f"Failed to input text into element with {locator_type} and locator '{locator}'")
            raise e

    def click_element(self, locator_type, locator):
        """
        Clicks an element found by the specified locator type and value.

        :param locator_type: The type of the locator (id, css_selector, xpath, name, class_name).
        :param locator: The actual locator.
        """
        element = self.find_element(locator_type, locator)
        try:
            element.click()
            self.logger.info(f"Clicked element with {locator_type} and locator '{locator}'")
        except Exception as e:
            self.logger.error(f"Failed to click element with {locator_type} and locator '{locator}'")
            raise e

    def send_keys(self, locator_type, locator, input_key):
        """
        Finds an element and sends special keys (like Enter, Tab) to it.
        :param locator_type: Locator strategy (e.g., By.ID, By.CLASS_NAME, By.TAG_NAME).
        :param locator: The value of the locator (e.g., 'input', 'search', etc.).
        :param input_key: The key to be sent (e.g., 'ENTER', 'TAB').
        """
        element = self.find_element(locator_type, locator)
        keys = self.action_mapping.get_action_type(input_key)
        try:
            element.send_keys(keys)
            self.logger.info(f"Input key '{keys}' into element with {locator_type} and locator '{locator}'")
        except Exception as e:
            self.logger.error(f"Failed to send keys to the element: {locator_type} = {locator}. Error: {e}")

    def switch_to_iframe_by_element(self, locator_type, locator):
        """
        Switch to an iframe based on its web element.

        :param locator_type: Locator strategy (e.g., By.ID, By.XPATH).
        :param locator: The value of the locator (e.g., iframe's ID or XPath).
        """
        try:
            iframe_element = self.wait.until(EC.presence_of_element_located((locator_type, locator)))
            self.driver.switch_to.frame(iframe_element)
            self.logger.info(f"Switched to iframe located by {locator_type} = {locator}.")
        except Exception as e:
            raise Exception(f"Failed to switch to iframe located by {locator_type} = {locator}. Error: {e}")


