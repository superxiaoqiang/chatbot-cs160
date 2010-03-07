# Output manager
#

import random

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
        'Would you like more information about {0}?',
        'Should I tell you more about {0}?',
        'Interested in knowing more about {0}?',
        'Sure, I can tell you more about {0}, shall I?',
        'You want to know more about {0}, is this correct?',
    ),
    'single-cuisine': (
        'More information about a {0} restaurant.',
        'Should I tell you a {0} restaurant?',
        'You want a {0} restaurant, is this correct?',
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
        elif itype == 'single-detail':
            response = random.choice(RESPONSES[itype]).format(input['restaurant'])
        elif itype == 'single-cuisine':
            response = random.choice(RESPONSES[itype]).format(input['cuisine'])
        else:
            response = str(input)
            
        return '\033[1;34mNYRC:\033[1;m ' + response

    def get_intro(self):
        print "Welcome to the NYRC (New York Restaurant Chatbot)"
        print '='*72
        print "\nTalk to me by typing in plain English, using natural language."
        print "Enter \"quit\" when done.\n"
        print '='*72 + "\n"
        
        print self.respond({'type': 'greeting'})
