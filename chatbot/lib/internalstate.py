# Internal state manager
#
import logging
import re
import random
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
        self.count = 0

    def prepare_input(self, raw_input):
        """Prepare raw input"""

        # check current input for "it" and replace with restaurant name
        # look behind three lines
        p = re.compile(r'\bit\b', re.IGNORECASE)
        for i in range(-1, -4, -1):
            try:
                item = self.peek_stack(i)

                # stop if no more items on stack
                if not item:
                    break
                raw_input = p.sub(item['input']['list'][0]['Name'], raw_input)
            except:
                pass

        # push raw input to stack
        self.push_stack({'raw_input': raw_input})
        return raw_input

    def process_input(self, input):
        """Process parsed input"""
        top = self.peek_stack()
        if top:
            it = input['type'].split('-')
            input['list'] = []

            # preprocess confirmation
            if it[0] == 'confirmation':
                try:
                    # look at previous item
                    item = self.peek_stack(-2)

                    # stop if no more items on stack
                    log.debug('Previously: {it}'.format(it=it))
                    if item['input']['type'] == 'leading-single' \
                        or item['input']['type'] == 'single-detail':
                        input['type'] = 'single-detail'
                        it = input['type'].split('-')
                        input['restaurant'] = item['input']['restaurant']
                except:
                    pass


            if it[0] == 'single':
                filters = []

                if it[1] == 'detail' \
                  or it[1] == 'phone':
                    filters = {'Name': input['restaurant']}

                elif it[1] == 'cuisine':
                    filters = {'Cuisine': input['cuisine']}

                r_list = self._xmlparser.get_restaurants(filters)
                if r_list:
                    random.shuffle(r_list)
                    input['list'] = [r_list[0]]

            # update the stack with
            if constants.DEBUG:
                log.debug(
                    'just added: {type}; n: {n}'.format(
                        type=input['type'],
                        n=len(input['list']),
                        )
                    )

        top['input'] = input
        return input

    def reset_stack(self):
        self.stack = []

    def pop_stack(self, count=None):
        """Pop from stack"""
        self.stack.pop(count)
        self.count -= 1

    def push_stack(self, element):
        """Push to stack"""
        self.stack.append(element)
        self.count += 1

    def peek_stack(self, count=-1):
        """Returns element from stack
        
        If count is not specified, returns the last element
        """
        try:
            return self.stack[count]
        except IndexError:
            return False
