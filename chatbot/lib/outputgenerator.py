# Output manager
#

import random
import re
import constants

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
        response = ''
        itype = input['type']
        if input.get('undo', False):
            response += random.choice(RESPONSES['undo']) + ' '

        # if empty, switch to single-empty
        if not input.get('listitem') and \
            itype in set(['name-detail', 'name-zone', 'name-meal',
                'name-phone', 'name-price', 'name-distance']):
            count = len(input['list'])
            if count == 0:
                itype = itype.split('-')
                itype[0] = 'single'
                itype = '-'.join(itype)

        if itype in set(['quit', 'greeting', 'confirmation', 'nomatch',
            'undo-error', 'undo-empty']):
            response += random.choice(RESPONSES[itype])

        # list by price range
        elif itype == 'list-price-range':
            count = len(input['list'])
            random.shuffle(input['list'])
            n = min((count, constants.LIST_DEFAULT_COUNT))
            
            # if found any
            if n:
                r_names = []
                for i in range(0, n):
                    r_names.append(input['list'][i]['Name'])

                r_list = ", ".join(r_names)
                response += random.choice(RESPONSES[itype]).format(
                    r_list=r_list,
                    count=count,
                    n=n,
                    pmin=input['min'],
                    pmax=input['max'],
                )

            else:
                response += random.choice(RESPONSES[itype+'-empty']).format(
                    count=count,
                    n=n,
                    pmin=input['min'],
                    pmax=input['max'],
                )

        # list by exact price
        elif itype == 'list-price-single':
            count = len(input['list'])
            random.shuffle(input['list'])
            n = min((count, constants.LIST_DEFAULT_COUNT))
            
            # if found any
            if n:
                r_names = []
                for i in range(0, n):
                    r_names.append(input['list'][i]['Name'])

                r_list = ", ".join(r_names)
                response += random.choice(RESPONSES[itype]).format(
                    r_list=r_list,
                    count=count,
                    n=n,
                    p=input['price'],
                )

            else:
                response += random.choice(RESPONSES[itype+'-empty']).format(
                    count=count,
                    n=n,
                    p=input['price'],
                )

        # filter by meals served
        elif itype == 'list-meal-single':
            count = len(input['list'])
            random.shuffle(input['list'])
            n = min((count, constants.LIST_DEFAULT_COUNT))
            
            # if found any
            if n:
                r_names = []
                for i in range(0, n):
                    r_names.append(input['list'][i]['Name'])

                r_list = ", ".join(r_names)
                response += random.choice(RESPONSES[itype]).format(
                    r_list=r_list,
                    count=count,
                    n=n,
                    m=input['meal'],
                )

            else:
                response += random.choice(RESPONSES[itype+'-empty']).format(
                    count=count,
                    n=n,
                    m=input['meal'],
                )

        # show restaurant's location
        elif itype == 'single-distance':
            if input['list']:
                response += random.choice(RESPONSES[itype]).format(
                    name=input['list'][0]['Name'],
                    miles=round(input['miles'], 2),
                )
            else:
                response += random.choice(RESPONSES[itype+'-empty']).format(name=input['restaurant'])

        # show restaurant's location
        elif itype == 'single-location':
            if input['list']:
                response += random.choice(RESPONSES[itype]).format(
                    name=input['list'][0]['Name'],
                    location=input['list'][0]['Address'],
                )    
            else:
                response += random.choice(RESPONSES[itype+'-empty']).format(name=input['restaurant'])
                  
        # show restaurant's neighborhood
        elif itype == 'single-zone':
            if input['list']:
                response += random.choice(RESPONSES[itype]).format(
                    name=input['list'][0]['Name'],
                    zone=input['list'][0]['Zone'],
                )    
            else:
                response += random.choice(RESPONSES[itype+'-empty']).format(name=input['restaurant'])
                        
        # show restaurant's meal
        elif itype == 'single-meal':
            if input['list']:
                response = random.choice(RESPONSES[itype]).format(
                    name=input['list'][0]['Name'],
                    meal=input['list'][0]['Meal'],
                )    
            else:
                response = random.choice(RESPONSES[itype+'-empty']).format(name=input['restaurant'])


        # show restaurant's phone #
        elif itype == 'single-phone':
            if input['list']:
                response += random.choice(RESPONSES[itype]).format(
                    name=input['list'][0]['Name'],
                    phone=input['list'][0]['Phone'],
                )
            else:
                response += random.choice(RESPONSES[itype+'-empty']).format(name=input['restaurant'])
                
        # show restaurant's phone #
        elif itype == 'single-smoke':
            if input['list']:
                response += random.choice(RESPONSES[itype]).format(
                    name=input['list'][0]['Name'],
                    smoke=input['list'][0]['field22'],
                )
            else:
                response += random.choice(RESPONSES[itype+'-empty']).format(name=input['restaurant'])
                
                
        # show restaurant's phone #
        elif itype == 'single-price':
            if input['list']:
                response += random.choice(RESPONSES[itype]).format(
                    name=input['list'][0]['Name'],
                    price=input['list'][0]['Cost'],
                )
            else:
                response += random.choice(RESPONSES[itype+'-empty']).format(name=input['restaurant'])

        # ask leading question for details on a single restaurant
        elif itype == 'leading-name-detail':
            response += random.choice(RESPONSES[itype]).format(name=input['restaurant'])

        # show details about a single restaurant
        elif itype in set(['name-detail', 'name-zone', 'name-meal',
                'name-phone', 'name-price', 'name-distance']):
            count = len(input['list'])
            if count:
                single_response = random.choice(RESPONSES['list-mode-single'])
                response_list = ''
                i = 0
                for r in input['list']:
                    i += 1
                    response_list += single_response.format(
                        i=i,
                        location=r['Address'],
                        zone=r['Zone'],
                    )
                response += random.choice(RESPONSES['list-mode']).format(
                    name=input['restaurant'],
                    n=count,
                    list=response_list,
                )
            else:
                response += random.choice(RESPONSES['single-mode-empty']).format(
                    i=input['listitem']
                )
        # show details about a single restaurant
        elif itype == 'single-detail':
            if input['list']:
                response += random.choice(RESPONSES[itype]).format(
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
                response += random.choice(RESPONSES['single-mode-empty']).format(i=input['listitem'])

        # show a single restaurant for this type of cuisine
        elif itype == 'single-cuisine':
            if input['list']:
                response += random.choice(RESPONSES[itype]).format(
                    cuisine=input['cuisine'].capitalize(),
                    name=input['list'][0]['Name'],
                )
            else:
                response += random.choice(RESPONSES[itype+'-empty']).format(cuisine=input['cuisine'].capitalize())

        # if nothing matches, just repeat the input as a string
        else:
            del input['list']
            response += str(input)

        return response

    def get_intro(self):
        return "\nWelcome to the NYRC (New York Restaurant Chatbot)\n" + \
            ('='*72) + "\n" + \
            "\nTalk to me by typing in plain English, using natural language." + \
            "Enter \"quit\" (or press Ctrl+D) when done.\n\n" + \
            ('='*72) + "\n"
