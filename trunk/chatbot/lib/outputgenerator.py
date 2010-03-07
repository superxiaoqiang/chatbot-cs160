# Output manager
#

import random
from xmlParse import *

RESPONSES = {
    'quit': (
        'Thank you for using NYRC, your friendly New York Restaurant Chatbot.',
        'Thank you, come again!',
        'Goodbye.',
        'Good idea, I\'m hungry too!',
    ),
    'greeting': (
        'Hello. How may I help you?',
        'Hi there, are you looking for a restaurant?',
        'Let\'s get you some food!',
        'Hi. My purpose in life is to serve you... a restaurant.',
        'Hi, would you like my assistance in finding a good meal?',
    ),
    'single-detail': (
        '{0} is located at {1}, and serves {2} cuisine, for {3}. The average cost per person is {4}$. This restaurant also offers: {5}.',
    ),
    'single-detail-empty': (
        'Could not find any information about the restaurant {0}.',
        'We have no record of restaurants named {0}.',
        'Sorry, no restaurants named {0} are available.',
    ),
    'single-detail-confirm': (
        'Would you like more information about {0}?',
        'Should I tell you more about {0}?',
        'Interested in knowing more about {0}?',
        'Sure, I can tell you more about {0}, shall I?',
        'You want to know more about {0}, is this correct?',
    ),
    'single-cuisine': (
        'A good {0} restaurant is {1}.',
    ),
    'single-cuisine-confirm': (
        'More information about a {0} restaurant.',
        'Should I tell you a {0} restaurant?',
        'You want a {0} restaurant, is this correct?',
    ),
    'single-cuisine-empty': (
        'Could not find any information about a {0} restaurant.',
        'We have no record of {0} restaurants.',
        'Sorry, no {0} restaurants are available.',
    ),
    'confirmation': (
        'Ok, great.',
        'I\'m glad to hear that.',
        'Good.',
        'Yay!',
    ),
}

class OutputGenerator:
    def __init__(self):
        self._init = True
        self.xml_source = "data/nyc-restaurants.xml"
        self._xmlparser = xmlParse(self.xml_source)
    
    def respond(self, input, filters={}):
        """
        Respond to semantic input.
        
        @type input: C{list}
        @param input: list to be understood
        @rtype: C{string}
        """
        itype = input['type']
        if itype == 'nomatch':
            response = "I'm sorry, I don't understand what you mean. Try again."
        elif itype == 'quit' or itype == 'greeting' or itype == 'confirmation':
            response = random.choice(RESPONSES[itype])
        elif itype == 'single-detail':
            filters = {'Name': input['restaurant']}

            r_list = self._xmlparser.get_restaurants(filters)
            r = None
            if r_list:
                r = r_list[0]
            if r:
                response = random.choice(RESPONSES[itype]).format(r['Name'],
                    r['Address'] + ', ' + r['Zone'], r['Cuisine'],
                    r['MealsServed'].lower(), r['Cost'],
                    r['Field18'].lower() + ', ' + r['Field19'].lower(),
                )
            else:
                response = random.choice(RESPONSES[itype+'-empty']).format(input['restaurant'])
        elif itype == 'single-cuisine':
            filters = {'Cuisine': input['cuisine']}

            r_list = self._xmlparser.get_restaurants(filters)
            r_name = None
            if r_list:
                r_name = random.choice(r_list)['Name']
            if r_name:
                response = random.choice(RESPONSES[itype]).format(input['cuisine'], r_name)
            else:
                response = random.choice(RESPONSES[itype+'-empty']).format(input['cuisine'])
        else:
            response = str(input)
            
        return '\033[1;34mNYRC:\033[1;m ' + response

    def get_intro(self):
        print "\nWelcome to the NYRC (New York Restaurant Chatbot)"
        print '='*72
        print "\nTalk to me by typing in plain English, using natural language."
        print "Enter \"quit\" (or press Ctrl+D) when done.\n"
        print '='*72 + "\n"
        
        print self.respond({'type': 'greeting'})
