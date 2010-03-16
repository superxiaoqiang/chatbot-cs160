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
        self.last_list_pos = None

    def prepare_input(self, raw_input):
        """Prepare raw input"""
        new = {}
        new['filters'] = {}

        # check current input for "it" and replace with restaurant name
        p_match = re.compile(r'.*\b(it|its)\b.*', re.IGNORECASE).match(raw_input)
        p = re.compile(r'\b(it|its|this place|that place)\b', re.IGNORECASE)
        if p_match:
            for i in range(-1, constants.LOOKBACK, -1):
                try:
                    item = self.peek_stack(i)
                    # stop if no more items on stack
                    if not item:
                        break
                    raw_input = p.sub(item['input']['list'][0]['Name'], raw_input)
                    # mark that context is added
                    new['internal'] = True
                    carry_key = item['filters'].get('Key', None)
                    if carry_key:
                        new['filters']['Key'] = carry_key
                    break
                except:
                    pass

        # mark list position
        item = self.peek_stack()
        if item and item.get('listmode', None):
            self.last_list_pos = self.count - 1
            if constants.DEBUG:
                log.debug(self.last_list_pos)

        new['raw_input'] = raw_input
        # push raw input to stack
        self.push_stack(new)
        return raw_input

    def process_input(self, input):
        """Process parsed input"""
        # get current item
        top = self.peek_stack()
        filters = top['filters']
        # get previous item
        prev = self.peek_stack(-2)
        it = input['type'].split('-')
        input['list'] = []

        # preprocess confirmation
        if it[0] == 'confirmation' and prev:
            if constants.DEBUG:
                log.debug('Previous type: {it}'.format(
                    it=prev['input']['type'],
                ))
            try:
                # carry over restaurant
                if prev['input']['type'] == 'leading-name-detail' \
                    or prev['input']['type'] == 'name-detail':
                    input = prev['input']
                    input['type'] = 'name-detail'
                    it = input['type'].split('-')
            except:
                pass

        # if it already has context, skip confirmation step
        if top.get('internal', False) and \
            it[0] == 'leading' and it[1] == 'name':
            input['type'] = 'name-detail'
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
                if constants.DEBUG:
                    log.debug('Filters: {f}'.format(f=item['filters']))
                return input
            elif popped:
                input['type'] = 'undo-empty'
            else:
                input['type'] = 'undo-error'

        if it[0] == 'name':

            if prev['filters'].get('Name', False) and \
                top.get('internal', False):
                r_list = prev['input']['list']
                filters = prev['filters']

            elif it[1] in set(['detail', 'phone', 'zone',
                'price', 'location' , 'field22']):
                filters.update({'Name': input['restaurant']})
                r_list = self._xmlparser.get_restaurants(filters)

            else:
                r_list = []

            r_len = len(r_list)
            if r_len == 1:
                it[0] = 'single'
                input['type'] = '-'.join(it)
                input['list'] = r_list
            elif r_len > 1:
                random.shuffle(r_list)
                input['list'] = r_list
                top['listmode'] = True

        if it[0] == 'list':
            # check whether to start from previous or from scratch
            if constants.DEBUG:
                log.debug(input)
            if prev and prev['input']['type'].split('-')[0] == 'list':
                filters.update(prev['filters'])
                if it[1] == 'price':
                    if filters.get('Cost', None):
                        del filters['Cost']
                    if filters.get('minPrice', None):
                        del filters['minPrice']
                    if filters.get('maxPrice', None):
                        del filters['maxPrice']

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

        if it[0] == 'single':

            if it[1] == 'listitem' and self.last_list_pos:
                # get the last listmode from stack
                stack_list = self.peek_stack(self.last_list_pos)
                # update input type
                it = stack_list['input']['type'].split('-')
                it[0] = 'single'
                input['type'] = '-'.join(it)

                if input['listitem'] > 0 and \
                    input['listitem'] <= len(stack_list['input']['list']):
                    # this is the restaurant just picked
                    r = stack_list['input']['list'][input['listitem']-1]
                    # update filters accordingly
                    filters = stack_list['filters']
                    filters.update({'Key': r['Key'], })
                    # finally, update the input
                    input['list'] = [r]

            elif it[1] == 'listitem':
                input['type'] = 'nomatch'
                del input['listitem']

            elif it[1] == 'cuisine':
                filters.update({'Cuisine': input['cuisine']})
                r_list = self._xmlparser.get_restaurants(filters)
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
        top['filters'] = filters
        if constants.DEBUG:
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
