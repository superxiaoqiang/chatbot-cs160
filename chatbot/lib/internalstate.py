# Internal state manager
#
import re

class InternalState:
    def __init__(self):
        self.stack = []
#        print self._xmlparser.get_restaurants({})

    def prepare_input(self, raw_input):
        """Prepare raw input"""

        # push raw input to stack
        return raw_input
   
    def process_input(self, input):
        """Process parsed input"""
        if len(self.stack) > 0:
            self.peek_stack()['input'] = input
        # update the stack with
        if input['type'] is not 'greeting' and input['type'] is not 'nomatch' and \
        input['type'] is not 'confirmation' and input['type'] is not 'quit':
            self.push_stack(input)

        return input

    def reset_stack(self):
        self.stack = []

    def pop_stack(self, count=None):
        """Pop from stack"""
        if len(self.stack) > 0:
            self.stack.pop(count)

    def push_stack(self, element):
        """Push to stack"""
        self.stack.append(element)

    def peek_stack(self, count=-1):
        """Returns element from stack
        
        If count is not specified, returns the last element
        """
        return self.stack[count]
