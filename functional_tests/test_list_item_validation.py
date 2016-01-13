from .base import FunctionalTest 
from selenium.webdriver.common.keys import Keys 
from unittest import skip

class ItemValidation(FunctionalTest):
    
    def test_cannot_add_empty_list_items(self):
        #Given Edith goes to the home page
        self.browser.get(self.server_url)
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.RETURN)

        #When she tries to submit an empty list item
        #An error message appears
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "You can't have an empty list item")

        #Then she tries again with some text for the item
        self.browser.find_element_by_id('id_new_item').send_keys('Buy milk\n')
        self.check_for_row_in_list_table('1: Buy milk')

        #Then she tries to submit an empty list again
        #She receives the same error message
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.RETURN)
        self.check_for_row_in_list_table('1: Buy milk')
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "You can't have an empty list item")

        #Then Edith fills in the list with text
        self.browser.find_element_by_id('id_new_item').send_keys('Make tea\n')
        self.check_for_row_in_list_table('1: Buy milk')
        self.check_for_row_in_list_table('2: Make tea')
