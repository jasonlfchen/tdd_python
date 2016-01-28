from .base import FunctionalTest 
from selenium.webdriver.common.keys import Keys 
from unittest import skip

class ItemValidation(FunctionalTest):
    
    def get_error_element(self):
        return self.browser.find_element_by_css_selector('.has-error')

    def test_cannot_add_empty_list_items(self):
        #Given Edith goes to the home page
        self.browser.get(self.server_url)
        inputbox = self.get_item_input_box()
        inputbox.send_keys(Keys.RETURN)

        #When she tries to submit an empty list item
        #An error message appears
        error = self.get_error_element()
        self.assertEqual(error.text, "You can't have an empty list item")

        #Then she tries again with some text for the item
        inputbox = self.get_item_input_box()
        inputbox.send_keys('Buy milk\n')
        self.check_for_row_in_list_table('1: Buy milk')

        #Then she tries to submit an empty list again
        #She receives the same error message
        inputbox = self.get_item_input_box()
        inputbox.send_keys(Keys.RETURN)
        self.check_for_row_in_list_table('1: Buy milk')
        error = self.get_error_element()
        self.assertEqual(error.text, "You can't have an empty list item")

        #Then Edith fills in the list with text
        inputbox = self.get_item_input_box()
        inputbox.send_keys(Keys.RETURN)
        inputbox = self.get_item_input_box()
        inputbox.send_keys('Make tea\n')
        self.check_for_row_in_list_table('1: Buy milk')
        self.check_for_row_in_list_table('2: Make tea')

    def test_cannot_add_duplicate_items(self):
        #Given Edith goes to the home page and starts a new list
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('Buy wellies\n')
        self.check_for_row_in_list_table('1: Buy wellies')

        #When she tries to enter a duplicate item
        self.get_item_input_box().send_keys('Buy wellies\n')

        #Then shees an error message
        self.check_for_row_in_list_table('1: Buy wellies')
        error = self.get_error_element()
        self.assertEqual(error.text, "You've already got this in your list")

    def test_error_messages_are_cleared_on_input(self):
        #Given Edith starts a new list that causes a validation error
        self.browser.get(self.server_url)
        inputbox = self.get_item_input_box()
        inputbox.send_keys(Keys.RETURN)
        error = self.get_error_element()
        self.assertTrue(error.is_displayed())

        #When she starts typing in the input box to clear the error
        inputbox = self.get_item_input_box()
        inputbox.send_keys('a')
        error = self.get_error_element()
        self.assertFalse(error.is_displayed())
