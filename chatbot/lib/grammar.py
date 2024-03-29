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
    # matches: I want to know more about Gilt
    { 'matches': {
      'more': r'.*\b(know more about)|(tell .* more about)\b.*',
      },
      'semantics': {
      'restaurant': r'.+?\b(?P<term>[A-Z][a-z]+(([\s,:]+[A-Z][a-z]+)+)?)\b.*',
      },
      'type': 'leading-name-detail',
    },
    # matches: What is a good Mexican restaurant?
    { 'matches': {
      'question': r'(^.+\ba\b.*?[A-Z][a-z]+.*?\b.+\brestaurant)',
      },
      'semantics': {
      'cuisine': r'.*\b(?P<term>[A-Z][a-z]+(( [A-Z][a-z]+)+)?)\b[\s]+restaurant\b.*',
      },
      'type': 'random-cuisine',
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
      'greeting': r'(hi|hello|hey|sup|yo)\b.{0,20}',
      },
      'semantics': {
      },
      'type': 'greeting',
    },
    # matches: Yes
    { 'matches': {
      'confirm': r'(yes|yeah|sure|ok|go ahead|sounds good)\b.{0,20}',
      },
      'semantics': {
      },
      'type': 'confirmation',
    },
    # matches: start over
    { 'matches': {
      'reset': r'.*\bstart\b\s+\bover\b.*',
      },
      'semantics': {
      },
      'type': 'reset',
    },
    # matches: undo
    { 'matches': {
      'undo': r'.*\b(undo|scratch\b\s+\bthat|go\b\s+\bback)\b.*',
      },
      'semantics': {
      },
      'type': 'undo',
    },
]
