# Output manager
#

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
        
        if input['type'] == 'list':
            return input
        else:
            return 'NYRC: \033[1;34m' + \
                "I'm sorry, I don't understand what you mean. Try again." + \
                '\033[1;m'

    def get_intro(self):
        print "Welcome to the NYRC (New York Restaurant Chatbot)"
        print '='*72
        print "\nTalk to me by typing in plain English, using natural language."
        print "Enter \"quit\" when done.\n"
        print '='*72 + "\n"
        print 'NYRC: \033[1;34m' + \
            "Hello.  How may I help you?" + \
                '\033[1;m'
