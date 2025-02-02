from selenium.webdriver.common.keys import Keys
import logging

class ActionMapping:

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def get_action_type(self, action_type):
        """
        Returns the action to be performed for sending keys or executing special key events.

        :param action_type: The type of action (text, ENTER, TAB, SPACE, BACKSPACE).
        :return: The appropriate key or text to send to the element.
        """
        action_strategy = {
            "ENTER": Keys.ENTER,
            "TAB": Keys.TAB,
            "SPACE": Keys.SPACE,
            "BACKSPACE": Keys.BACK_SPACE,
        }.get(action_type)


        if action_strategy is None:
            self.logger.info(f"Sending text input: {action_type}")
            return action_type
        else:
            self.logger.info(f"Sending special key: {action_type}")
            return action_strategy
