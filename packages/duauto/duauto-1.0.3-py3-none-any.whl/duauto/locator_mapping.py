from selenium.webdriver.common.by import By
import logging

class LocatorMapping:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def get_by_type(self, locator_type):
        """
        Returns the By strategy based on the locator type.

        :param locator_type: The type of the locator (id, css_selector, xpath, name, class_name).
        :return: The appropriate By strategy.
        """
        # Mapping locator types to Selenium By strategies
        locator_strategy = {
            "id": By.ID,
            "css_selector": By.CSS_SELECTOR,
            "xpath": By.XPATH,
            "name": By.NAME,
            "class_name": By.CLASS_NAME
        }.get(locator_type.lower())  # Ensure case insensitivity

        if locator_strategy is None:
            self.logger.error(f"Unsupported locator type: {locator_type}")
            raise ValueError(f"Unsupported locator type: {locator_type}")

        # Log the strategy for debugging
        self.logger.info(f"Locator strategy for '{locator_type}': {locator_strategy}")
        return locator_strategy

