"""Unit test for chatbot

Part of the chatbot project for cs160.
"""

import re
import eliza
import unittest
eliza.chatbot.set_interactive(False)

class helloTest(unittest.TestCase):
    def testHello(self):
        """hello response"""
        pairs = (  "Hello... I'm glad you could drop by today.",
                    "Hi there... how are you today?",
                    "Hello, how are you feeling today?",
                )
        for i in range(1, 10):
            if eliza.chatbot.respond('Hello') in pairs:
                match = True
            self.assertEqual(match, True)

if __name__ == "__main__":
    unittest.main()
