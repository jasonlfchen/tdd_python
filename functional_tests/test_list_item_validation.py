from .base import FunctionalTest 
from unittest import skip

class ItemValidation(FunctionalTest):
    
    def test_cannot_add_empty_list_items(self):
        #Given Edith goes to the home page

        #When she tries to submit an empty list item
        #An error message appears

        #Then she tries to submit an empty list again
        #She receives the same error message

        #Then Edith fills in the list with text
        self.fail('write me!')
