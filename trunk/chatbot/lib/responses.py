# responses used by outputgenerator.py

RESPONSES = {
    'quit': (
        'Thank you for using NYRC, your friendly New York Restaurant Chatbot.',
        'Thank you, come again!',
        'Goodbye.',
        'Good idea, I\'m hungry too!',
        'It\'s FOOD TIME!!!!',
        'Now get out there and stick some food in your mouth!', 
        'Have a fun, safe, and enjoyable time eating!',
        'Take care!',
    ),
    'greeting': (
        'Hello. How may I help you?',
        'Hi there, are you looking for a restaurant?',
        'Let\'s get you some food!',
        'Hi. My purpose in life is to serve you... a restaurant.',
        'Hi, would you like my assistance in finding a good meal?',
        'Hi, my job is to find the best place for you to stick food in your mouth',
        'Hey there.  What type of food would you like to eat today?',
    ),
    'single-phone': (
        'The phone number of {name} is {phone}.',
        '{name}\'s phone number is: {phone}.', 
        'I believe {name}\'s phone number is {phone}.',
        'The number for {name} is {phone}.',
    ),
    'single-phone-empty': (
        'Sorry, I do not have a phone number listed for {name}.',
        'I\'m sorry, I have no phone number for {name}.',
        'Ooops... I don\'t think I have the phone number for {name}.',
    ),
    'single-smoke': (
        '{name} says that {smoke}.',
    ),
    'single-smoke-empty': (
        'Sorry, I do not have a info on smoking at {name}.',
        'I\'m sorry, I dont know if you can smoke at {name}.',
    ),
    'single-location': (
        '{name} is located at {location}.',
        '{name}\'s address is {location}.',
        'The address of {name} is {location}.',
        '{name} can be found at {location}.',
    ),
    'single-location-empty': (
        'Sorry, I do not have an address listed for {name}.',
        'I\'m sorry, I cannot find an address for {name}.',
        'Ooops... I don\'t think I have the address for {name}.',
    ),
    'single-zone': (
        '{name} is in {zone}.',
        '{name}\'s neighborhood is {zone}.',
        '{name} can be found in {zone}.',
    ),
    'single-zone-empty': (
        'Sorry, I do not have a neighborhood listed for {zone}.',
        'I\'m sorry, I cannot find a neighborhood for {zone}.',
        'Ooops... I don\'t think I have the neighborhood for {zone}.',
    ),
    'single-price': (
        'An average meal at {name} costs {price}$.',
    ),
    'single-price-empty': (
        'Sorry, I don\'t have any information about how expensive {name} is.',
    ),
    'leading-name-detail': (
        'Is {name} a restaurant? You may respond by saying yes. If not, perhaps {name} is a type of cuisine or a city?',
        'Wait, you\'re referring to {name} as a restaurant, and not a city or cuisine, correct?',
        'Would you like more information about the restaurant {name}?',
        'Should I tell you more about {name} restaurant?',
        'Interested in knowing more about {name} restaurant?',
        'Sure, I can tell you more about {name} restaurant, shall I?',
        'You want to know more about {name} restaurant, is this correct?',
    ),
    'name-detail-single': (
        "\n{i}. In {zone}, address {location}",
        "\n{i}. At {location} {zone}",
    ),
    'name-detail-empty': (
        'Sorry, I could not find any information about the restaurant {name}.',
        'Could not find any information about the restaurant {name}.',
        'I have no record of restaurants named {name}.',
        'Sorry, no restaurants named {name} are available.',
    ),
    'single-detail': (
        '{name} is located at {location} {zone}, and serves {cuisine} cuisine, for {meals_served}. The average cost per person is ${cost}. This restaurant also offers: {extras}.',
        '{name} serves {cuisine} food for {meals_served}, which should roughly cost ${cost}.  They are located at {location} {zone}, and they also offer: {extras}.',
    ),
    'single-cuisine': (
        'A good {cuisine} restaurant is {name}.',
        'I heard of a decent restaurant called {name} that serves {cuisine} food.',
        'Well... {name} is a good {cuisine} restaurant.',
        'If you want {cuisine} food, perhaps you should try {name}.',
        'For a {cuisine} restaurant, I would recommend {name}.',
        'Mmmmm.... {cuisine} food.... Try {name}. I have heard good things about that place.',
    ),
    'single-cuisine-confirm': (
        'Do you want more information about a {cuisine} restaurant.',
        'Should I tell you a {cuisine} restaurant?',
        'You want a {cuisine} restaurant, is this correct?',
        'Would you like to know more information about a {cuisine} restaurant?',
    ),
    'single-cuisine-empty': (
        'Could not find any information about a {cuisine} restaurant.',
        'I have no record of {cuisine} restaurants.',
        'Sorry, no {cuisine} restaurants are available.',
        'I can\'t find any {cuisine} restaurants in my database',
        'I have never heard of {cuisine} restaurants before.  Think of something else...',
        'Never heard of {cuisine} food before...  try something else.',
    ),
    'list-price-range': (
        'I have {count} restaurants with prices between {pmin}$ and {pmax}$. Here are {n} of them: {r_list}.',
    ),
    'list-price-range-empty': (
        'Sorry, I have no restaurants costing between {pmin}$ and {pmax}$ price range.',
        'No restaurants are available in the {pmin}-{pmax}$ price range.',
    ),
    'list-price-single': (
        'I have {count} restaurants at price {p}$. Here are {n} of them: {r_list}.',
    ),
    'list-price-single-empty': (
        'Sorry, I have no restaurants costing {p}$.',
        'No restaurants are available at price {p}$.',
    ),
    'list-meal-single': (
        'I have {count} restaurants serving {m}. Here are {n} of them: {r_list}.',
    ),
    'list-meal-single-empty': (
        'Sorry, I have no restaurants serving {m}.',
        'No restaurants are available that serve {m}.',
    ),
    'undo': (
        'Ok, your previous request was undone.',
    ),
    'undo-error': (
        'Sorry, could not undo.',
        'I could not undo your request.',
        'Nothing to undo.'
    ),
    'undo-empty': (
        'Ok. You are now starting your search from scratch.',
        'Request undone. Starting from scratch.',
    ),
    'confirmation': (
        'Ok, great.',
        'I\'m glad to hear that.',
        'Good.',
        'Yay!',
        'Excellent',
        'Alrighty!',
        'Sounds good!',
        'Brilliant!!!', 
        'YEEEEEEEEEEAAAAAAAHHHHHHHHHHHHH!!!!!!!',
    ),
      'nomatch': (
        'I\'m sorry, I don\'t understand what you mean. Try again.',
        'Could you repeat that, I didn\'t understand.',
        'I\'m sorry, can you rephrase that?',
        'I\'m not sure what you mean, can you repeat that?',
        'My apologies. I am not sure what you mean... can you rephrase your question?'
        'I\'m afraid I don\'t understand what you mean... can you say that in a different way?',
        'Wait... I\'m confused.  Can you say that in a different way?',
    ),
    'name-detail': (
        'I have {n} restaurants named {name}. {list}\nEnter a number (1-{n}) for more information about that specific restaurant.',
    ),
    'name-detail-single': (
        "\n{i}. In {zone}, address {location}",
        "\n{i}. At {location} {zone}",
    ),
    'single-detail-empty': (
        '{i} is not in the list.',
        'Oops, {i} is not in my list.',
    ),
    'name-zone': (
        'I have {n} restaurants named {name}. {list}\nEnter a number (1-{n}) for more information about that specific restaurant.',
    ),
    'name-zone-single': (
        "\n{i}. In {zone}, address {location}",
        "\n{i}. At {location} {zone}",
    ),
    'single-zone-empty': (
        '{i} is not in the list.',
        'Oops, {i} is not in my list.',
    ),
    'name-meal': (
        'I have {n} restaurants named {name}. {list}\nEnter a number (1-{n}) for more information about that specific restaurant.',
    ),
    'name-meal-single': (
        "\n{i}. In {zone}, address {location}",
        "\n{i}. At {location} {zone}",
    ),
    'single-meal-empty': (
        '{i} is not in the list.',
        'Oops, {i} is not in my list.',
    ),
    'name-phone': (
        'I have {n} restaurants named {name}. {list}\nEnter a number (1-{n}) for more information about that specific restaurant.',
    ),
    'name-phone-single': (
        "\n{i}. In {zone}, address {location}",
        "\n{i}. At {location} {zone}",
    ),
    'single-phone-empty': (
        '{i} is not in the list.',
        'Oops, {i} is not in my list.',
    ),
    'name-price': (
        'I have {n} restaurants named {name}. {list}\nEnter a number (1-{n}) for more information about that specific restaurant.',
    ),
    'name-price-single': (
        "\n{i}. In {zone}, address {location}",
        "\n{i}. At {location} {zone}",
    ),
    'single-price-empty': (
        '{i} is not in the list.',
        'Oops, {i} is not in my list.',
    ),
}
