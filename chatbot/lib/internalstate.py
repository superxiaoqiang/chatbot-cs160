# Internal state manager
#

class InternalState:
    def __init__(self):
        self.stack = []

    def prepare_input(self, raw_input):
        """Prepare raw input"""

        # push raw input to stack
        self.push_stack({'raw_input': raw_input})
        return raw_input

    def process_input(self, input):
        """Process parsed input"""
        self.peek_stack()['input'] = input
        # update the stack with
        print self.stack

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
        return self.stack[count]
