# Dialog manager
#

from inputparser import *
from outputgenerator import *
from internalstate import *
from datetime import datetime
import logging

class Chatbot(object):
    def __init__(self):
        """
        Initialize the chatbot.
        """

        self.input_parser = InputParser()
        self.output_generator = OutputGenerator()
        self.internal_state = InternalState()
        self._raw_input = ''
        self._input = self._raw_input
        self._response = ''
        self._DEBUG = False

    def start(self, quit="quit"):
        """
        Starts the chatbot
        
        @type quit: C{string}
        @param quit: string to quit on
        @rtype: C{list}
        """
        LOG_FILENAME = chatbot.get_current_id()
        logging.basicConfig(filename='logs/'+LOG_FILENAME,level=logging.INFO,format="")
        print "Dialog Timestamp: " + LOG_FILENAME
        if self._DEBUG:
            logging.info("Dialog Timestamp: " + LOG_FILENAME)

        self._input = {'type': 'greeting'}
        self.respond()
        self.print_response()
        if self._DEBUG:
            logging.info('NYRC: ' + self._response)

        self._raw_input = ""
        while self._raw_input != quit:
            self._raw_input = quit
            try:
                self.set_raw_input()

            except EOFError:
                print self.get_raw_input()

            if self._raw_input:
                # prepare the input
                # according to internal state
                self.prepare_input()

                # parse the input
                self.parse_input()

                # process the parsed input
                # prepare it for output manager
                self.process_input()

                # get the response
                # from the output manager
                self.respond()


                # output response
                self.print_response()
                if self._DEBUG:
                    logging.info('NYRC: ' + self._response)

    def set_raw_input(self):
        self._raw_input = raw_input("\033[1;92mME:\033[1;m ")
        if self._DEBUG:
            logging.info('ME: ' + self._raw_input)

    def get_raw_input(self):
        return self._raw_input

    def parse_input(self):
        self._input = self.input_parser.parse(self._raw_input)

    def prepare_input(self):
        self._raw_input = self.internal_state.prepare_input(self._raw_input)

    def process_input(self):
        self._input = self.internal_state.process_input(self._input)

    def respond(self):
        self._response = self.output_generator.respond(self._input)

    def print_response(self):
        print '\033[1;34mNYRC:\033[1;m ' + self._response

    def get_intro(self):
        print self.output_generator.get_intro()

    def get_current_id(self):
        return str(datetime.now())

    def set_debug(self):
        self._DEBUG = True

if __name__ == "__main__":

    chatbot = Chatbot()
    chatbot.set_debug()
    chatbot.get_intro()
    chatbot.start()
