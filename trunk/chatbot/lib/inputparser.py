# Input manager
#

import re
import logging

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

        tagset = self.build_tagset(input)
        resp['words'] = self.build_keywords(tagset)


        if not resp['words']:
            if constants.DEBUG:
                log.debug("No words: " + str(resp))
            return resp

        if not resp['words'].get('NN', None):
            if constants.DEBUG:
                log.debug("No NN: " + str(resp))
            return resp

        for word in resp['words'].get('NN', None):
            if constants.DEBUG:
                log.debug("NN found: " + word)

            # matches a phone number request
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

            # matches a request for a restaurant name
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
                or t.node == 'JJ'):
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