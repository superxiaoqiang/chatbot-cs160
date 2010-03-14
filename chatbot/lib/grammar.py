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
      'more': r'.*\b(know more about)|(tell .* more about)\b.*',
      },
      'semantics': {
      'restaurant': r'.+?\b(?P<term>[A-Z][a-z]+(([\s,:]+[A-Z][a-z]+)+)?)\b.*',
      },
      'type': 'single-detail',
    },
    # matches: What is a good Mexican restaurant?
    { 'matches': {
      'question': r'(^.+\ba\b.*?[A-Z][a-z]+.*?\b.+\brestaurant)',
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
