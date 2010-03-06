"""Unit test for chatbot

Part of the chatbot project for cs160.
"""

from inputparser import *
import unittest

ip = InputParser()

class inputTest(unittest.TestCase):
    def testInput(self):
        """test list input"""
        response = ip.parse("List the 5 most expensive restaurants in New York.")
        
        self.assertEqual(response['type'] == 'list', True)
        self.assertEqual(response['price'] == 'expensive', True)

if __name__ == "__main__":
    unittest.main()
