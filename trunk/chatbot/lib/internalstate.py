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
        new = {}
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

                # mark that context is added
                new['internal'] = True
            except:
                pass

        new['raw_input'] = raw_input
        # push raw input to stack
        self.push_stack(new)
        return raw_input

    def process_input(self, input):
        """Process parsed input"""
        # get current item
        top = self.peek_stack()
        filters = {}
        # get previous item
        prev = self.peek_stack(-2)
        if top:
            it = input['type'].split('-')
            input['list'] = []

            # preprocess confirmation
            if it[0] == 'confirmation' and prev:
                try:
                    log.debug('Previous type: {it}'.format(
                        it=prev['input']['type'],
                    ))
                    # carry over restaurant
                    if prev['input']['type'] == 'leading-single-detail' \
                        or prev['input']['type'] == 'single-detail':
                        input['type'] = 'single-detail'
                        it = input['type'].split('-')
                        input['restaurant'] = prev['input']['restaurant']
                except:
                    pass

            # if it already has context, skip confirmation step
            if top.get('internal', None) and \
                it[0] == 'leading' and it[1] == 'single':
                input['type'] = 'single-detail'
                it = input['type'].split('-')

            if it[0] == 'undo':
                popped = False
                for i in range(0, 2):
                    item = self.pop_stack()
                    if not item:
                        break
                    elif i == 1:
                        popped = True
                item = self.peek_stack()
                if item:
                    input = item['input'].copy()
                    input['undo'] = True
                    top['input'] = input
                    log.debug('Filters: {f}'.format(f=item['filters']))
                    return input
                elif popped:
                    input['type'] = 'undo-empty'
                else:
                    input['type'] = 'undo-error'

            if it[0] == 'single':

                if it[1] in set(['detail', 'phone', 'zone'
                    'price', 'location' , 'field22']):
                    filters.update({'Name': input['restaurant']})

                elif it[1] == 'cuisine':
                    filters.update({'Cuisine': input['cuisine']})

                r_list = self._xmlparser.get_restaurants(filters)
                if r_list:
                    random.shuffle(r_list)
                    input['list'] = [r_list[0]]

            if it[0] == 'list':
                # check whether to start from previous or from scratch
                if prev and prev['input']['type'].split('-')[0] == 'list':
                    filters.update(prev['filters'])

                # price range
                if it[1] == 'price' and it[2] == 'range':
                    filters.update({
                        'minPrice': input['min'],
                        'maxPrice': input['max'],
                    })

                # exact price
                if it[1] == 'price' and it[2] == 'single':
                    filters.update({
                        'Cost': input['price'],
                    })

                # meal
                if it[1] == 'meal' and it[2] == 'single':
                    filters.update({
                        'MealsServed': input['meal'],
                    })

                input['list'] = self._xmlparser.get_restaurants(filters)


            # update the stack with
            if constants.DEBUG:
                log.debug(
                    'just added: {type}; n: {n}'.format(
                        type=input['type'],
                        n=len(input['list']),
                        )
                    )

        top['input'] = input
        top['filters'] = filters
        log.debug('Filters: {f}'.format(f=filters))
        return input

    def reset_stack(self):
        self.stack = []

    def pop_stack(self, count=-1):
        """Pop from stack"""
        if self.count <= 0:
            return None
        self.count -= 1
        return self.stack.pop(count)

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
