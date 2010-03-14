# Dialog manager
#

from inputparser import *
from outputgenerator import *
from datetime import datetime
from internalstate import * 
import logging
import cmd
import sys

class Chatbot(cmd.Cmd):
    prompt = "\033[1;92mME:\033[1;m "
    output_generator = OutputGenerator()
    input_parser = InputParser()
    internal_state = InternalState()

    def _response(self, response):
        return '\033[1;34mNYRC:\033[1;m ' + response

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

        if len(self.output_generator._istate_response) >0:
            self.internal_state.pop_stack(-1)
            self.internal_state.push_stack(self.output_generator._istate_response)
            self.output_generator._istate_response = {}
    
        print "stack size is: " + str(len(self.internal_state.stack))
        print "the stack is currently:" + str(self.internal_state.stack)
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
