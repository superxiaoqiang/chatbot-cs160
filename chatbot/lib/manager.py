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
    # removed color b/c it screws up prompt len
    # delete using backspace wouldn't work right
    prompt = "ME: "
    output_generator = OutputGenerator()
    input_parser = InputParser()
    internal_state = InternalState()

    def _response(self, response):
        # make entire response one color
        return constants.colors.NYRC + 'NYRC: ' + response + constants.colors.END

    def start(self):
        intro = self.output_generator.get_intro() + "\n" +\
            self._response(self.output_generator.respond({'type': 'greeting'}))
        
        LOG_FILENAME = str(datetime.now())
        logging.basicConfig(filename='logs/'+LOG_FILENAME,level=logging.DEBUG,format="")
        print  "Dialog Timestamp: " + LOG_FILENAME
        
        self.cmdloop(intro)

    def default(self, line):
        
        logging.debug('ME: ' + line)

        # prepare_input
        prepared = self.internal_state.prepare_input(line)
        # parse the input
        input = self.input_parser.parse(prepared)

        # process the parsed input
        # prepare it for output manager
        input = self.internal_state.process_input(input)
        response = self.output_generator.respond(input)

        # output response

        print self._response(response)
        logging.debug('NYRC: ' + response)


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
