# Dialog manager
#

from inputparser import *
from outputgenerator import *
from datetime import datetime
import logging
import cmd
import sys

class Chatbot(cmd.Cmd):
    prompt = "\033[1;92mME:\033[1;m "
    output_generator = OutputGenerator()
    input_parser = InputParser()

    def _response(self, response):
        return '\033[1;34mNYRC:\033[1;m ' + response

    def start(self):
        intro = self.output_generator.get_intro() + "\n" +\
            self._response(self.output_generator.respond({'type': 'greeting'}))
        self.cmdloop(intro)

    def default(self, line):
        # parse the input
        input = self.input_parser.parse(line)

        # process the parsed input
        # prepare it for output manager
        response = self.output_generator.respond(input)

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
