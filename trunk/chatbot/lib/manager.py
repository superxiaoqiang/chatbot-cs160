# Dialog manager
#

from inputparser import *
from outputgenerator import *

class Chatbot(object):
    def __init__(self):
        """
        Initialize the chatbot.
        """

        self.input_parser = InputParser()
        self.output_generator = OutputGenerator()
        # self.internal_state = InternalState()
        self._raw_input = ''
        self._input = self._raw_input
        self._response = ''

    def start(self, quit="quit"):
        """
        Starts the chatbot
        
        @type quit: C{string}
        @param quit: string to quit on
        @rtype: C{list}
        """
        self._raw_input = ""
        while self._raw_input != quit:
            self._raw_input = quit
            try:
                self.set_raw_input()

            except EOFError:
                print self.get_raw_input()

            if self._raw_input:
                self.parse_input()
                # get the response
                self.respond()

                # do some internal state stuff here

                # output response
                print self._response

    def set_raw_input(self):
        self._raw_input = raw_input("\033[1;92mME:\033[1;m ")

    def get_raw_input(self):
        return self._raw_input

    def parse_input(self):
        self._input = self.input_parser.parse(self._raw_input)

    def respond(self):
        self._response = self.output_generator.respond(self._input)

    def get_intro(self):
        self.output_generator.get_intro()


if __name__ == "__main__":
    
    chatbot = Chatbot()
    chatbot.get_intro()
    chatbot.start()
