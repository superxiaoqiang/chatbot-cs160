# Dialog manager
#

from inputparser import *
from outputgenerator import *
from datetime import datetime
from internalstate import * 
import constants
import logging
import cmd
import sys

class Chatbot(cmd.Cmd):
    prompt = constants.colors.ME + "ME: " + constants.colors.END
    output_generator = OutputGenerator()
    input_parser = InputParser()
    internal_state = InternalState()

    def _response(self, response):
        return constants.colors.NYRC + 'NYRC: ' + constants.colors.END + response

    def start(self):
        intro = self.output_generator.get_intro() + "\n" +\
            self._response(self.output_generator.respond({'type': 'greeting'}))
        self.cmdloop(intro)

    def default(self, line):
        # prepare_input
        self.internal_state.prepare_input(line)
        # parse the input
        input = self.input_parser.parse(line)

        # process the parsed input
        # prepare it for output manager
        self.internal_state.process_input(input)
        response = self.output_generator.respond(input)

        # output response

        print self._response(response)

    def do_help(self, cmd):
        print self.output_generator.get_intro()

    def do_quit(self, cmd):
        self.default("quit")
        sys.exit(0)

    def do_EOF(self, cmd):
        self.do_quit(cmd)

if __name__ == "__main__":

    chatbot = Chatbot()
    chatbot.start()
