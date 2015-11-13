from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        #Given Edith vists the website
        self.browser.get('http://localhost:8000')

        #When Edith notices the header mentions a to-do lists
        self.assertIn('To-Do', self.browser.title)
        
        #Then Edith enters a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
                inputbox.get_attribute('placeholder'),'Enter a to-do item')

        #And Edith types "Buy peacock feathers" into a text box
        inputbox.send_keys('Buy peacock feathers')

        #When Edith hits enter, the page updates and lists a to-do table
        input_send_keys(Keys.ENTER)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
                any(row.text == '1: Buy peacock feathers' for row in rows))

        #Edit needs to enter another item
        self.fail('Finish the test!')

if __name__ == '__main__':
    unittest.main(warnings='ignore')
