# responses used by outputgenerator.py

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
    'single-phone': (
        'The phone number of {name} is {phone}.',
    ),
    'single-phone-empty': (
        'Sorry, I do not have a phone number listed for {name}.',
    ),
    'leading-single-detail': (
        'Is {name} a restaurant? You may respond by saying yes. If not, perhaps {name} is a type of cuisine or a city?',
    ),
    'single-detail': (
        '{name} is located at {location}, and serves {cuisine} cuisine, for {meals_served}. The average cost per person is {cost}$. This restaurant also offers: {extras}.',
    ),
    'single-detail-empty': (
        'Could not find any information about the restaurant {name}.',
        'I have no record of restaurants named {name}.',
        'Sorry, no restaurants named {name} are available.',
    ),
    'single-detail-confirm': (
        'Would you like more information about {name}?',
        'Should I tell you more about {name}?',
        'Interested in knowing more about {name}?',
        'Sure, I can tell you more about {name}, shall I?',
        'You want to know more about {name}, is this correct?',
    ),
    'single-cuisine': (
        'A good {cuisine} restaurant is {name}.',
    ),
    'single-cuisine-confirm': (
        'More information about a {cuisine} restaurant.',
        'Should I tell you a {cuisine} restaurant?',
        'You want a {cuisine} restaurant, is this correct?',
    ),
    'single-cuisine-empty': (
        'Could not find any information about a {cuisine} restaurant.',
        'I have no record of {cuisine} restaurants.',
        'Sorry, no {cuisine} restaurants are available.',
    ),
    'list-price-range': (
        'I have found {count} restaurants with prices between {pmin}$ and {pmax}$. Here are {n} of them: {r_list}.',
    ),
    'list-price-range-empty': (
        'Sorry, I have no restaurants costing between {pmin}$ and {pmax}$ price range.',
        'No restaurants are available in the {pmin}-{pmax}$ price range.',
    ),
    'list-price-single': (
        'I have found {count} restaurants at price {p}$. Here are {n} of them: {r_list}.',
    ),
    'list-price-single-empty': (
        'Sorry, I have no restaurants costing {p}$.',
        'No restaurants are available at price {p}$.',
    ),
    'confirmation': (
        'Ok, great.',
        'I\'m glad to hear that.',
        'Good.',
        'Yay!',
    ),
      'nomatch': (
        'I\'m sorry, I don\'t understand what you mean. Try again.',
        'Could you repeat that, I didn\'t understand.',
        'I\'m sorry, can you rephrase that?',
        'I\'m not sure what you mean, can you repeat that?',
    ),
}
