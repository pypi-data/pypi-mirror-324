from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from duauto.actions import Actions
from duauto.locator_mapping import LocatorMapping
import logging


class Assertions:

    def __init__(self, driver, implicit_wait=10):
        """
        Assertions class for all page objects, providing basic Selenium assertions.

        :param driver: WebDriver instance passed during initialization.
        :param implicit_wait: Default wait time for explicit waits.
        """
        self.driver = driver
        self.logger = logging.getLogger(__name__)
        self.wait = WebDriverWait(driver, implicit_wait)
        self.actions = Actions(self.driver)
        self.locator_mapping = LocatorMapping()

    def assert_title(self, expected_title):
        """
        Asserts that the page title matches the expected title.

        :param expected_title: The expected title to assert.
        :raises AssertionError: If the title does not match the expected title.
        """
        actual_title = self.driver.title  # Directly get the current page title

        # Perform the assertion directly
        assert actual_title == expected_title, f"Expected title: {expected_title}, but got: {actual_title}"
        self.logger.info(f"Page title '{actual_title}' matches expected title.")

    def assert_element_text(self, locator_type, locator, expected_text, timeout=10):
        """
        Asserts that the text of a found element matches the expected text.

        :param locator_type: The type of the locator (id, css_selector, xpath, name, class_name).
        :param locator: The actual locator of the element.
        :param expected_text: The expected text to assert.
        :param timeout: Time to wait for the element to be present.
        :raises AssertionError: If the text does not match the expected text.
        """
        element = self.wait.until(
            EC.presence_of_element_located((self.locator_mapping.get_by_type(locator_type), locator))
        )
        actual_text = element.text
        try:
            assert actual_text == expected_text, f"Expected text: {expected_text}, but got: {actual_text}"
            self.logger.info(f"Element text matches expected. Found: '{actual_text}'")
        except AssertionError as e:
            self.logger.error(f"Text assertion failed. Expected: '{expected_text}', but got: '{actual_text}'")
            raise e

    def assert_element_visible(self, locator_type, locator, timeout=10):
        """
        Asserts that an element is visible on the page.

        :param locator_type: The type of the locator (id, css_selector, xpath, name, class_name).
        :param locator: The actual locator of the element.
        :param timeout: Time to wait for the element to become visible.
        :raises TimeoutException: If the element is not visible within the timeout.
        """
        try:
            self.wait.until(
                EC.visibility_of_element_located((self.locator_mapping.get_by_type(locator_type), locator))
            )
            self.logger.info(f"Element is visible with {locator_type} and locator '{locator}'")
        except Exception as e:
            self.logger.error(
                f"Element not visible with {locator_type} and locator '{locator}' after {timeout} seconds")
            raise e

    def assert_element_attribute(self, locator_type, locator, attribute, expected_value, timeout=10):
        """
        Asserts that a specific attribute of an element matches the expected value.

        :param locator_type: The type of the locator (id, css_selector, xpath, name, class_name).
        :param locator: The actual locator of the element.
        :param attribute: The attribute to check (e.g., 'href', 'value', 'class').
        :param expected_value: The expected value of the attribute.
        :param timeout: Time to wait for the element to be present.
        :raises AssertionError: If the attribute's value does not match the expected value.
        """
        element = self.wait.until(
            EC.visibility_of_element_located((self.locator_mapping.get_by_type(locator_type), locator))
        )
        actual_value = element.get_attribute(attribute)
        try:
            assert actual_value == expected_value, f"Expected {attribute}: {expected_value}, but got: {actual_value}"
            self.logger.info(f"Element attribute '{attribute}' matches expected value: '{expected_value}'")
        except AssertionError as e:
            self.logger.error(
                f"Attribute assertion failed. Expected {attribute}: '{expected_value}', but got: '{actual_value}'")
            raise e

    def assert_url(self, expected_url):
        """
        Asserts that the current URL matches the expected URL.

        :param expected_url: The expected URL to assert.
        :raises AssertionError: If the URL does not match the expected URL.
        """
        current_url = self.driver.current_url  # Get the current URL immediately

        # Perform the assertion directly
        assert current_url == expected_url, f"Expected URL: {expected_url}, but got: {current_url}"
        self.logger.info(f"URL assertion passed. Expected and actual URL: '{expected_url}'")

    def assert_iframe(self, locator_type, locator, timeout=10):
        """
        Asserts that the iframe matches the expected iframe located by the locator.

        :param locator_type: The type of the locator (id, css_selector, xpath, name, class_name).
        :param locator: The actual locator of the iframe element.
        :param timeout: Time to wait for the iframe to be present.
        :raises AssertionError: If the current iframe does not match the expected iframe.
        """
        current_iframe = self.driver.current_iframe
        expected_iframe = self.wait.until(
            EC.frame_to_be_available_and_switch_to_it((self.locator_mapping.get_by_type(locator_type), locator))
        )
        try:
            assert current_iframe == expected_iframe, f"Expected iframe: {expected_iframe}, but got: {current_iframe}"
            self.logger.info(f"Iframe assertion passed. Expected and actual iframe: '{expected_iframe}'")
        except AssertionError as e:
            self.logger.error(f"Iframe assertion failed. Expected: {expected_iframe}, but got: {current_iframe}")
            raise e

    def assert_element_not_visible(self, locator_type, locator, timeout=10):
        """
        Asserts that an element is not visible on the page.

        :param locator_type: The type of the locator (id, css_selector, xpath, name, class_name).
        :param locator: The actual locator value.
        :param timeout: Time to wait for the condition.
        :raises AssertionError: If the element is visible.
        """
        try:

            element_present = self.wait.until(EC.presence_of_element_located((locator_type, locator)))
            is_visible = element_present.is_displayed()

            assert not is_visible, f"Expected element not to be visible, but it is. Locator: {locator}"
            self.logger.info(f"Assertion passed: Element with {locator_type} '{locator}' is not visible.")
        except TimeoutException:
            self.logger.info(f"Element with {locator_type} '{locator}' is not present on the page.")
        except AssertionError as e:
            self.logger.error(f"Assertion failed: {str(e)}")
            raise e


    def assert_element_not_present(self, locator_type, locator):
        """
        Asserts that an element is not present in the DOM.

        :param locator_type: The type of the locator (id, css_selector, xpath, name, class_name).
        :param locator: The actual locator value.
        :raises AssertionError: If the element is present in the DOM.
        """
        try:
            locator_strategy = self.locator_mapping.get_by_type(locator_type)
            self.driver.find_element(locator_strategy, locator)
            self.logger.error(f"Assertion failed: Element with {locator_type} '{locator}' is present.")
            raise AssertionError(f"Expected element to be not present, but it is. Locator: {locator}")
        except NoSuchElementException:
            self.logger.info(f"Assertion passed: Element with {locator_type} '{locator}' is not present.")
            print("Element not present on the page.")
        except Exception as e:
            self.logger.error(f"An error occurred while asserting element presence: {str(e)}")
            raise e


    def assert_element_is_present(self, locator_type, locator):
        """
        Asserts that an element is present in the DOM.

        :param locator_type: The type of the locator (id, css_selector, xpath, name, class_name).
        :param locator: The actual locator value.
        :raises AssertionError: If the element is not present in the DOM.
        """
        try:
            locator_strategy = self.locator_mapping.get_by_type(locator_type)
            self.driver.find_element(locator_strategy, locator)
            self.logger.info(f"Assertion passed: Element with {locator_type} '{locator}' is present.")
        except NoSuchElementException:
            self.logger.error(f"Assertion failed: Element with {locator_type} '{locator}' is not present.")
            raise AssertionError(f"Expected element to be present, but it is not. Locator: {locator}")
        except Exception as e:
            self.logger.error(f"An error occurred while asserting element presence: {str(e)}")
            raise e

