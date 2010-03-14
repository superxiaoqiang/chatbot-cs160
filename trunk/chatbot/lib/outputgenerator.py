# Output manager
#

import random
import re

from responses import RESPONSES


class OutputGenerator:
    def __init__(self):
        pass

    def respond(self, input):
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
            if input['list']:
                response = random.choice(RESPONSES[itype]).format(
                    name=input['list'][0]['Name'],
                    phone=input['list'][0]['Phone'],
                )
            else:
                response = random.choice(RESPONSES[itype+'-empty']).format(name=input['restaurant'])
        elif itype == 'single-detail':
            if input['list']:
                response = random.choice(RESPONSES[itype]).format(
                    name=input['list'][0]['Name'],
                    location=input['list'][0]['Address'],
                    zone=input['list'][0]['Zone'],
                    cuisine=input['list'][0]['Cuisine'],
                    meals_served=input['list'][0]['MealsServed'],
                    cost=input['list'][0]['Cost'],
                    extras=input['list'][0]['Field18'].lower() + ', ' + \
                        input['list'][0]['Field19'].lower(),
                )
            else:
                response = random.choice(RESPONSES[itype+'-empty']).format(name=input['restaurant'])
        elif itype == 'single-cuisine':
            if input['list']:
                response = random.choice(RESPONSES[itype]).format(
                    cuisine=input['cuisine'].capitalize(),
                    name=input['list'][0]['Name'],
                )
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
