# Input manager
#

import re
import logging
import string

import nltk
import constants
from grammar import grammar
if constants.SPELLCHECK:
    from didyoumean import DidYouMean

if constants.DEBUG:
    log = logging.getLogger(__name__)
    log.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    formatter = logging.Formatter(constants.colors.DEBUG 
        + "%(name)s - %(message)s" + constants.colors.END)

    ch.setFormatter(formatter)
    log.addHandler(ch)


class InputParser:
    def __init__(self):
        """Compile the regexes in grammar"""
        for item in grammar:
            item['matches_compiled'] = {}
            for name,pattern in item['matches'].items():
                item['matches_compiled'][name] = \
                    re.compile(pattern, re.IGNORECASE)

            item['semantics_compiled'] = {}
            for name,pattern in item['semantics'].items():
                item['semantics_compiled'][name] = \
                    re.compile(pattern)

        if constants.SPELLCHECK:
            self.didyoumean = DidYouMean('en-us', constants.DICT_DIR)

    def parse(self, input):
        """
        Parse user input.

        @type input: C{string}
        @param input: string to be parsed
        @rtype: C{list}
        """

        # removes punctuation from the end of the sentance
        clean_input = input.strip(" !@#$%^&*()_+-=[]\\`~{}|;':\",./<>?")

        # check grammar
        input_s = self.spellcheck(input)

        resp = self.check_grammar(input)
        if constants.SPELLCHECK and not resp and input_s['full'] != input:
            resp = self.check_grammar(input_s['full'])

        # use NLP parser as fallback
        if not resp:
            resp = self.nlp_parse(input)

        if constants.SPELLCHECK and resp['type'] == 'nomatch' \
            and input_s['full'] != input:
            resp = self.nlp_parse(input_s['full'])

        return resp

    def nlp_parse(self, input):
        """Parse input using NLTK parser+chunker"""
        resp = {}
        resp['type'] = 'nomatch'
        VDB_set = {}
        WP_set = {}
        tagset = self.build_tagset(input)
        resp['words'] = self.build_keywords(tagset)
        w = resp['words']

        if not w:
            if constants.DEBUG:
                log.debug("No words: " + str(resp))
            return resp
        
        #finds neighborhood    
        for word in tagset:
            if word[1] == 'VBD':
                VDB_set =  word[0]
        for word in tagset:
            if word[1] == 'WP':
                WP_set =  word[0]        
        if 'neighborhood' in VDB_set and 'what' in WP_set:
            if w.get('NNP', [None])[0]: 
                r_name = w.get('NNP', [None])[0]             
            else :
                return resp
            
            r_name = w.get('NNP', [None])[0] 
            resp['restaurant'] = r_name
            resp['type'] = 'single-zone'
            return resp
        
        #matches "how expensive it is" and "is it expensive"
        if 'expensive' in set(w.get('JJ', ())):
            if w.get('NNP', [None])[0]: 
                r_name = w.get('NNP', [None])[0]             
            else :
                return resp
            
       
            r_name = w.get('NNP', [None])[0] 
            resp['restaurant'] = r_name
            resp['type'] = 'single-price'
            return resp
            
        if 'between' in set(w.get('IN', ())) \
            or 'price' in set(w.get('NN', ())):
            price_range = w.get('CD', ())

            # price between a and b
            # require at least 2 numerals
            if len(price_range) >= 2:
                resp['min'] = min(map(int, price_range))
                resp['max'] = max(map(int, price_range))
                resp['type'] = 'list-price-range'
                return resp

            # price of exactly a
            if len(price_range) > 0:
                price_range = w.get('CD', ())
                resp['price'] = min(price_range)
                resp['type'] = 'list-price-single'
                return resp


        # need to merge NN and JJ for this step
        w['NNJJ'] = set(w.get('NN', []) + w.get('JJ', []))
        meal = constants.MEALS_SET & w['NNJJ']
        if meal:
            resp['type'] = 'list-meal-single'
            resp['meal'] = meal.pop()
            return resp


        # from here on there must be nouns
        NN_set = set(w.get('NN', []))
        if not NN_set:
            if constants.DEBUG:
                log.debug("No NN: " + str(resp))
            return resp

        # matches a phone number request
        if NN_set & constants.PHONE_KEYWORDS:
            r_name = w.get('NNP', [None])[0] or \
                        w['NN'][-1]

            resp['restaurant'] = r_name
            resp['type'] = 'single-phone'
            return resp
            
                
        # matches a single meal request
        if NN_set & constants.MEALS_SET:
            r_name = w.get('NNP', [None])[0] or \
                w['NN'][-1]
              
            resp['restaurant'] = r_name
            resp['type'] = 'single-meal'
            resp['meal'] = word.lower()
            return resp

        # matches a request for a list
        if 'list' in NN_set:
            resp['count'] = w.get('CD', [constants.LIST_DEFAULT_COUNT])[0]
            resp['type'] = 'list'
            return resp

        # matches a request for an address
        if 'address' in NN_set:
            r_name = w.get('NNP', [None])[0] or \
                        w['NN'][-1]
            resp['restaurant'] = r_name
            resp['type'] = 'single-location'
            return resp

        # matches a request for a cuisine type
        if NN_set & constants.NAME_KEYWORDS:
            r_name = w.get('NNP', [None])[0]
            if not r_name:
                for kw in reversed(w['NN']):
                    if kw not in constants.NAME_KEYWORDS:
                        r_name = kw
                        break
            if r_name:
                resp['type'] = 'single-cuisine'
                resp['cuisine'] = string.capitalize(r_name)
                return resp


        if constants.DEBUG:
            log.debug(resp)
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

    def spellcheck(self, input):
        # check if enabled
        if not constants.SPELLCHECK:
            return input

        words = [(w.new, w.corrected, w.old)
            for w in self.didyoumean.suggest(input)]

        full = []
        old = []
        new = []
        for w in words:
            # exclude capitalized words
            # since they are assumed to be proper nouns
            if w[1] and not constants.CAPITAL_REGEX.match(w[2]):
                new.append(w[0])
                full.append(w[0])
            elif not constants.CAPITAL_REGEX.match(w[2]):
                # but add correctly capitalized words
                if w[0] != w[2]:
                    new.append(w[0])
                    full.append(w[0])
                else:
                    old.append(w[2])
                    full.append(w[2])

            else:
                old.append(w[2])
                full.append(w[2])
        return {
            'full': u' '.join(full),
            'new': new,
            'old': old,
        }

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
        # chunk adjectives
            JJ: {<JJ.*>}
        # preposition or conjunction
            IN: {<IN>}
        """
        # parse for keywords
        regexp_parser = nltk.RegexpParser(grammar)
        tree = regexp_parser.parse(tagset)
        if constants.DEBUG:
            log.debug('Tree: ' + str(tree))

        # walk through the grammar tree and pick out keywords
        # go for noun phrases first
        for subtree in tree.subtrees(filter =
            lambda t: t.node == 'NP' or t.node == 'CD' \
                or t.node == 'JJ' or t.node == 'IN'):
            keyword = list(subtree.leaves())
            keyword = self.format_keywords(keyword)

            # append keywords to list
            for kw in keyword:
                # initialize, if no list of this type
                if not keywords.get(kw[1], None):
                    keywords[kw[1]] = []

                keywords[kw[1]].append(kw[0])

        return keywords

    def check_grammar(self, input):
        resp = constants.DEFAULT_RESPONSE.copy()

        # start with matches = False
        matches = False

        for item in grammar:
            # check all matches
            matches = True
            for name, pattern in item['matches_compiled'].items():
                if not pattern.match(input):
                    # build the semantics
                    matches = False

            if matches:
                for name, semantic in item['semantics_compiled'].items():
                    match = semantic.match(input)
                    if not match:
                        matches = False
                    else:
                        resp[name] = match.group('term')

            if matches:
                resp['type'] = item['type']
                break

        if matches:
            if constants.DEBUG:
                log.debug(input + ' -- ' + str(resp))
            return resp
        else:
            if constants.DEBUG:
                log.debug(input + ' -- ' + str(False))
            return False
