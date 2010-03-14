# Input manager
#

import re
import nltk
import constants
if constants.SPELLCHECK:
    from didyoumean import DidYouMean
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s")

ch.setFormatter(formatter)
log.addHandler(ch)

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
      'question': r'(.*\?$)|(^.+\ba\b.+\brestaurant)',
      },
      'semantics': {
      'cuisine': r'.*\b(?P<term>[a-z]+(( [a-z]+)+)?)\b[\s]+restaurant\b.*',
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
        
        # removes punctuation from the end of the sentance
        clean_input = input.rstrip("!.")
       
        # start with matches = False
        matches = False

        # check grammar
        resp = DEFAULT_RESPONSE.copy()
        for item in grammar:
            # check all matches
            matches = True
            for name,pattern in item['matches_compiled'].items():
                if not pattern.match(input):
                    # build the semantics
                    matches = False
                    log.debug(  'No match: ' + name)

            if matches:
                for name,semantic in item['semantics_compiled'].items():
                    match = semantic.match(input)
                    if not match:
                        matches = False
                        log.debug( 'No match: ' + name)
                    else:
                        resp[name] = match.group('term')

            if matches:
                resp['type'] = item['type']
                break

        # use NLP parser as fallback
        if not matches:
            resp = self.nlp_parse(input)

        return resp

    def nlp_parse(self, input):
        resp = {}
        resp['type'] = 'nomatch'
      
        tagset = self.build_tagset(input)
        print tagset
        resp['words'] = self.build_keywords(tagset)

        
        if not resp['words']:
            print "no words: %s" % resp
            return resp

        if not resp['words'].get('NN', None):
            print "No NN: %s" % resp
            print resp
            return resp

        for word in resp['words'].get('NN', None):
            print "NN found: %s" % word 
			
			#matchs a phone number request
            if word.lower() in constants.PHONE_KEYWORDS:
                r_name = resp['words'].get('NNP', [None])[0] or \
                         resp['words']['NN'][-1]

                resp['restaurant'] = r_name
                resp['type'] = 'phone'
                break
				
			# matches a request for a list
            if word.lower() == 'list':
                resp['count'] = resp['words'].get('CD', [constants.LIST_DEFAULT_COUNT])[0]
                resp['type'] = 'list'
                break 
				
            #matches a request for a restaurant name
            if word.lower() in constants.NAME_KEYWORDS:
                r_name = resp['words'].get('NNP', [None])[0]
                if not r_name:
                    for kw in reversed(resp['words']['NN']):
                        if kw not in constants.NAME_KEYWORDS:
                            r_name = kw
                            break

                if r_name:
                    resp['type'] = 'single-detail'
                    resp['restaurant'] = r_name

        log.debug( resp)
        return resp

    def format_keywords(self, keyword):
        trimmed = []

        # check if word is a DT or PP type and removes it if so
        if (keyword[0][1][0] == 'D' or
            keyword[0][1][0] == 'P'):
            keyword.remove(keyword[0])

        # makes a list of just the strings
        for (x, y) in keyword:
            trimmed.append((x, y))
        return trimmed

    def build_tagset(self, input):
        # tokenize input
        tokens = nltk.word_tokenize(input)
        return nltk.pos_tag(tokens)

    def build_keywords(self, tagset):
        keywords = {}

        # regexp grammar to catch our keywords
        #  <DT|PP\$>?: an optional determiner (a,the) or posesive (his, hers).
        #  <JJ.*>* zero or more adjectives of any type
        #  <NN.*>+ one or more nouns of any type
        grammar = r"""
        # chunk determiner/possessive, adjectives and nouns
            NP: {<DT|PP\$>?<JJ>*<NN.*>+}
        # chunk sequences of proper nouns
            CD: {<CD>}
        """
        # parse for keywords
        regexp_parser = nltk.RegexpParser(grammar)
        tree = regexp_parser.parse(tagset)

        # walk through the grammar tree and pick out keywords
        # go for noun phrases first
        for subtree in tree.subtrees(filter =
            lambda t: t.node == 'NP' or t.node == 'CD'):
            keyword = list(subtree.leaves())
            keyword = self.format_keywords(keyword)

            # append keywords to list
            for kw in keyword:
                # initialize, if no list of this type
                if not keywords.get(kw[1], None):
                    keywords[kw[1]] = []

                keywords[kw[1]].append(kw[0])

        return keywords
