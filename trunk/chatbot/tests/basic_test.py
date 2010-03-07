"""Unit test for chatbot

Part of the chatbot project for cs160.
"""

from inputparser import *
import unittest

ip = InputParser()

class inputTest(unittest.TestCase):
    def testInputList(self):
        """list input"""
        response = ip.parse("List the 5 most expensive restaurants in Manhattan, New York.")
        
        self.assertEqual(response['type'], 'list')
        self.assertEqual(response['price'], 'expensive')
        
    def testInputSingleMore(self):
        """single (more) input"""
        response = ip.parse("I want to know more about Gilt.")
        
        self.assertEqual(response['type'], 'single-detail')
        self.assertEqual(response['restaurant'], 'Gilt')
        
    def testInputSingleMore(self):
        """single (cuisine) input"""
        response = ip.parse("I want a good Mexican restaurant.")
        self.assertEqual(response['type'], 'single-cuisine')
        self.assertEqual(response['cuisine'], 'Mexican')
    
        response = ip.parse("What is a good Mexican restaurant?")
        self.assertEqual(response['type'], 'single-cuisine')
        self.assertEqual(response['cuisine'], 'Mexican')

    def testInputQuit(self):
        """quit input"""
        response = ip.parse("quit")
        
        self.assertEqual(response['type'], 'quit')
        
    def testInputGreeting(self):
        """greeting input"""
        response = ip.parse("Hi")
        
        self.assertEqual(response['type'] == 'greeting', True)

    def testInputConfirmation(self):
        """confirmation input"""
        response = ip.parse("Yes, go ahead")
        self.assertEqual(response['type'] == 'confirmation', True)

        response = ip.parse("Ok, good")
        self.assertEqual(response['type'] == 'confirmation', True)

        response = ip.parse("Sure, go ahead")
        self.assertEqual(response['type'] == 'confirmation', True)

        response = ip.parse("Yeah")
        self.assertEqual(response['type'] == 'confirmation', True)

if __name__ == "__main__":
    unittest.main()
