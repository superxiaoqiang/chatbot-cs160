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
        if itype == 'quit' or itype == 'greeting' or itype == 'confirmation' or itype == 'nomatch':
            response = random.choice(RESPONSES[itype])

        # list by price range
        elif itype == 'list-price-range':
            count = len(input['list'])
            n = min((count, 5))
            
            # if found any
            if n:
                r_names = []
                for i in range(0, n):
                    r_names.append(input['list'][i]['Name'])

                r_list = ", ".join(r_names)
                response = random.choice(RESPONSES[itype]).format(
                    r_list=r_list,
                    count=count,
                    n=n,
                    pmin=input['min'],
                    pmax=input['max'],
                )

            else:
                response = random.choice(RESPONSES[itype+'-empty']).format(
                    count=count,
                    n=n,
                    pmin=input['min'],
                    pmax=input['max'],
                )

        # show restaurant's location
        elif itype == 'single-location':
            if input['list']:
                response = random.choice(RESPONSES[itype]).format(
                    name=input['list'][0]['Name'],
                    location=input['list'][0]['Address'],
                )    
            else:
                response = random.choice(RESPONSES[itype+'-empty']).format(name=input['restaurant'])        

        # show restaurant's phone #
        elif itype == 'single-phone':
            if input['list']:
                response = random.choice(RESPONSES[itype]).format(
                    name=input['list'][0]['Name'],
                    phone=input['list'][0]['Phone'],
                )
            else:
                response = random.choice(RESPONSES[itype+'-empty']).format(name=input['restaurant'])

        # ask leading question for details on a single restaurant
        elif itype == 'leading-single-detail':
            response = random.choice(RESPONSES[itype]).format(name=input['restaurant'])

        # show details about a single restaurant
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

        # show a single restaurant for this type of cuisine
        elif itype == 'single-cuisine':
            if input['list']:
                response = random.choice(RESPONSES[itype]).format(
                    cuisine=input['cuisine'].capitalize(),
                    name=input['list'][0]['Name'],
                )
            else:
                response = random.choice(RESPONSES[itype+'-empty']).format(cuisine=input['cuisine'].capitalize())

        # if nothing matches, just repeat the input as a string
        else:
            response = str(input)

        return response

    def get_intro(self):
        return "\nWelcome to the NYRC (New York Restaurant Chatbot)\n" + \
            ('='*72) + "\n" + \
            "\nTalk to me by typing in plain English, using natural language." + \
            "Enter \"quit\" (or press Ctrl+D) when done.\n\n" + \
            ('='*72) + "\n"
