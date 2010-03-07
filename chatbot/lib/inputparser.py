# Input manager
#

import re

# grammar has the following format:
# dict of productions, each has:
#   # matches
#       a dict of matches name -> pattern(string regex)
#       compiled using IGNORECASE
#   # semantics
#       similar to matches
#       compiled without IGNORECASE
#       
#       These will be returned as a list.
#   # type (string)
grammar = [
    # matches: List the 5 most expensive restaurants in Location Name
    { 'matches': {
      'list': r'.*\blist\b.*',
      'restaurants': r'.*\brestaurants\b.*',
      },
      'semantics': {
      'count': r'.*(?P<term>[0-9]+).*',
      'price': r'.*\b(?P<term>expensive|pricey|cheap|low cost)\b.*',
      'location': r'.*\bin (?P<term>[A-Z][a-z]+(([\s,:]+[A-Z][a-z]+)+)?)\b.*',
      },
      'type': 'list',
    },
    # matches: I want to know more about Gilt
    { 'matches': {
      'more': r'.*\b(more about|know more)\b.*',
      'restaurant': r'.+\b(restaurant|[A-Z]+)\b.*',
      },
      'semantics': {
      'restaurant': r'.*\b((more about)|(know more)|(restaurant))\b.+?(?P<term>[A-Z][a-z]+(([\s,:]+[A-Z][a-z]+)+)?)\b.*',
      },
      'type': 'single-detail',
    },
    # matches: What is a good Mexican restaurant?
    { 'matches': {
      'question': r'(.*\?$)|(^I want.*a good.*restaurant)',
      'restaurant': r'.+\brestaurant\b.*',
      },
      'semantics': {
      'cuisine': r'.*\b(?P<term>[A-Z][a-z]+(( [A-Z][a-z]+)+)?)\b[\s]+restaurant\b.*',
      },
      'type': 'single-cuisine',
    },
    # matches: quit
    { 'matches': {
      'quit': r'quit.*',
      },
      'semantics': {
      },
      'type': 'quit',
    },
    # matches: Hello
    { 'matches': {
      'greeting': r'hi|hello|hey.{0,20}',
      },
      'semantics': {
      },
      'type': 'greeting',
    },
    # matches: Yes
    { 'matches': {
      'greeting': r'yes|yeah|sure|ok|go ahead|sounds good.{0,20}',
      },
      'semantics': {
      },
      'type': 'confirmation',
    },
]

DEFAULT_RESPONSE = {'type': 'nomatch'}

class InputParser:
    def __init__(self):
        for item in grammar:
            item['matches_compiled'] = {}
            for name,pattern in item['matches'].items():
                item['matches_compiled'][name] = \
                    re.compile(pattern, re.IGNORECASE)

            item['semantics_compiled'] = {}
            for name,pattern in item['semantics'].items():
                item['semantics_compiled'][name] = \
                    re.compile(pattern)
    
    def parse(self, input):
        """
        Parse user input.
        
        @type input: C{string}
        @param input: string to be parsed
        @rtype: C{list}
        """
        
        # clean up input
        clean_input = input
        while clean_input[-1] in "!.":
            clean_input = clean_input[:-1]

        # check grammar
        resp = DEFAULT_RESPONSE.copy()
        for item in grammar:
            # check all matches
            matches = True
            for name,pattern in item['matches_compiled'].items():
                if not pattern.match(input):
                    # build the semantics
                    matches = False
                    # print 'No match: ' + name

            if matches:
                for name,semantic in item['semantics_compiled'].items():
                    match = semantic.match(input)
                    if not match:
                        matches = False
                        # print 'No match: ' + name
                    else:
                        resp[name] = match.group('term')

            if matches:
                resp['type'] = item['type']
                break

        return resp
