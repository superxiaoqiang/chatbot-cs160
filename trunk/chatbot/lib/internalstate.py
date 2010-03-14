# Internal state manager
#
import logging
import constants
from xmlParse import *

if constants.DEBUG:
    log = logging.getLogger(__name__)
    log.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    formatter = logging.Formatter(constants.colors.DEBUG 
        + "%(name)s - %(message)s" + constants.colors.END)

    ch.setFormatter(formatter)
    log.addHandler(ch)

class InternalState:
    def __init__(self):
        self.stack = []
        self._xmlparser = xmlParse(constants.XML_SOURCE)

    def prepare_input(self, raw_input):
        """Prepare raw input"""

        # push raw input to stack
        self.push_stack({'raw_input': raw_input})
        return raw_input

    def process_input(self, input):
        """Process parsed input"""
        top = self.peek_stack()
        if top:
            top['input'] = input
            it = input['type'].split('-')
            print it
            input['list'] = []

            if it[0] == 'single':
                filters = []

                if it[1] == 'detail' \
                  or it[1] == 'phone':
                    filters = {'Name': input['restaurant']}

                elif it[1] == 'cuisine':
                    filters = {'Cuisine': input['cuisine']}

                input['list'] = self._xmlparser.get_restaurants(filters)

            # update the stack with
            if constants.DEBUG:
                log.debug(
                    'just added: {type}; n: {n}'.format(
                        type=input['type'],
                        n=len(input['list']),
                        )
                    )

        return input

    def reset_stack(self):
        self.stack = []

    def pop_stack(self, count=None):
        """Pop from stack"""
        self.stack.pop(count)

    def push_stack(self, element):
        """Push to stack"""
        self.stack.append(element)

    def peek_stack(self, count=-1):
        """Returns element from stack
        
        If count is not specified, returns the last element
        """
        try:
            return self.stack[count]
        except IndexError:
            log.debug('IndexError: peek_stack(' + str(count) + ')')
            return False
