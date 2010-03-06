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
    { 'matches': {
      'list': r'.*\blist\b.*',
      'restaurants': r'.*\brestaurants\b.*',
      },
      'semantics': {
      'count': r'.*([0-9]+).*',
      'price': r'.*\b(expensive|pricey|cheap|low cost)\b.*',
      'location': r'.*\bin ([A-Z][a-z]+(( [A-Z][a-z]+)+)?).*',
      },
      'type': 'list',
    }
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
                    # print name

            if matches:
                for name,semantic in item['semantics_compiled'].items():
                    match = semantic.match(input)
                    if not match:
                        matches = False
                        # print name
                    else:
                        resp[name] = match.group(1)

            if matches:
                resp['type'] = item['type']
                break

        return resp
