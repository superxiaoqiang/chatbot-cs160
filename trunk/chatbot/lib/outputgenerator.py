# Output manager
#

import random
import re
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
    'phone': (
        'The phone number of {name} is {phone}.',
    ),
    'single-detail': (
        '{name} is located at {location}, and serves {cuisine} cuisine, for {meals_served}. The average cost per person is {cost}$. This restaurant also offers: {extras}.',
    ),
    'single-detail-empty': (
        'Could not find any information about the restaurant {name}.',
        'We have no record of restaurants named {name}.',
        'Sorry, no restaurants named {name} are available.',
    ),
    'single-detail-confirm': (
        'Would you like more information about {name}?',
        'Should I tell you more about {name}?',
        'Interested in knowing more about {name}?',
        'Sure, I can tell you more about {name}, shall I?',
        'You want to know more about {name}, is this correct?',
    ),
    'single-cuisine': (
        'A good {cuisine} restaurant is {name}.',
    ),
    'single-cuisine-confirm': (
        'More information about a {cuisine} restaurant.',
        'Should I tell you a {cuisine} restaurant?',
        'You want a {cuisine} restaurant, is this correct?',
    ),
    'single-cuisine-empty': (
        'Could not find any information about a {cuisine} restaurant.',
        'We have no record of {cuisine} restaurants.',
        'Sorry, no {cuisine} restaurants are available.',
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
        self.xml_source = "data/nyc-restaurants.xml"
        self._xmlparser = xmlParse(self.xml_source)
        self._istate_response= {}
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
        elif itype == 'phone':
            filters = {'Name': input['restaurant']}

            r_list = self._xmlparser.get_restaurants(filters)
            r = r_list[0] if r_list else None
            if r:
                response = random.choice(RESPONSES[itype]).format(
                    name=r['Name'],
                    phone=r['Phone'],
                )
            else:
                response = random.choice(RESPONSES[itype+'-empty']).format(name=input['restaurant'])
        elif itype == 'single-detail':
            filters = {'Name': input['restaurant']}

            r_list = self._xmlparser.get_restaurants(filters)
            r = r_list[0] if r_list else None
            if r:
                response = random.choice(RESPONSES[itype]).format(name=r['Name'],
                    location=r['Address'] + ', ' + r['Zone'], cuisine=r['Cuisine'],
                    meals_served=r['MealsServed'].lower(), cost=r['Cost'],
                    extras=r['Field18'].lower() + ', ' + r['Field19'].lower(),
                )
                x = re.split(r' is located', response)
                self._istate_response = {'type': 'single-detail', 'restaurant': x[0]}
            else:
                response = random.choice(RESPONSES[itype+'-empty']).format(name=input['restaurant'])
        elif itype == 'single-cuisine':
            filters = {'Cuisine': input['cuisine']}

            r_list = self._xmlparser.get_restaurants(filters)
            r_name = None
            if r_list:
                r_name = random.choice(r_list)['Name']
            if r_name:
                response = random.choice(RESPONSES[itype]).format(cuisine=input['cuisine'].capitalize(), name=r_name)
            else:
                response = random.choice(RESPONSES[itype+'-empty']).format(cuisine=input['cuisine'].capitalize())
        else:
            response = str(input)
            
        return response

    def get_intro(self):
        return "\nWelcome to the NYRC (New York Restaurant Chatbot)\n" + \
            ('='*72) + "\n" + \
            "\nTalk to me by typing in plain English, using natural language." + \
            "Enter \"quit\" (or press Ctrl+D) when done.\n\n" + \
            ('='*72) + "\n"
