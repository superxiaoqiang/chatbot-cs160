# constants defined here
import re

LIST_DEFAULT_COUNT = 5


NAME_KEYWORDS = set(['restaurant', 'place', 'bar', 'joint', 'cafeteria', 'cafe', 'canteen', 'chophouse', 'coffee shop', 'diner', 'dining room', 'dive', 'doughtnut shop', 'drive-in', 'eatery', 'eating house', 'eating place', 'fast-food place', 'greasy spoon', 'grill', 'hamburger stand', 'hashery', 'hideaway', 'hotdog stand', 'inn', 'luncheonette', 'lunchroom', 'night club', 'outlet', 'pizzeria', 'saloon', 'soda fountain', 'watering hole', 'charcuterie', 'deli', 'sandwich shop', 'subway sho'])

PHONE_KEYWORDS = set(['phone'])

SPELLCHECK = True
DICT_DIR = '/usr/share/myspell/dicts/'

DEBUG = True

DEFAULT_RESPONSE = {'type': 'nomatch'}

CAPITAL_REGEX = re.compile('^[A-Z].*', re.MULTILINE)

class colors:
    NYRC = '\033[94m'
    ME = '\033[92m'
    DEBUG = '\033[91m'
    END = '\033[0m'
