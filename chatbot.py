import re
from nltk.corpus import wordnet  # wordnet is a lexical DB that defines semantical relationships between words
import random

from api import get_setup, get_punchline

# lines_file = open('movie_lines.txt', encoding='utf-8', errors='ignore').read().split('\n')  # as a string
# raw = ""
# for row in lines_file:
#     line = row.split()
#     line = line[8:]  # only keep the words
#     raw += ' '.join(line)

# build a dictionary, syns_dict, of [keywords]:synonyms
# note: keywords need to be able to have reasonable synonyms
words_list = ['hello', 'bye']
syns_dict = {}

for word in words_list:
    synonyms = []
    for syn in wordnet.synsets(word):
        for lem in syn.lemmas():
            # remove special characters from synonym strings
            lem_name = re.sub('[^a-zA-Z0-9 \n\.]', ' ', lem.name())
            synonyms.append(lem_name)
    syns_dict[word] = set(synonyms)

print(syns_dict)

# build a dictionary, intents_dict, of [intents]:keywords
# for each keyword, reformat in syntax that makes it visible to regular expression's search function
intents_dict = {}
keys_dict = {}  # re.compile version
keys_intents = ['greeting', 'farewell'] # mirrors keys dictionary, renaming keywords as intents
num_keys = 2

# define new keys in keys_dict (keywords as intents)
for index, word in enumerate(keys_intents):
    intents_dict[word] = []

    for syn in list(syns_dict[words_list[index]]):
        intents_dict[word].append('.*\\b' + syn + '\\b.*')

for intent, keys in intents_dict.items():
    # join the values in intents_dict with the OR operator, updating them in keys_dict
    keys_dict[intent] = re.compile('|'.join(keys))



# build a dictionary, responses, of responses
responses = {
    'greeting': ['Hello!', 'What\'s up?', 'Hi there.', 'Howdy!', 'Hey, nice to see you!'],
    'farewell': ['Bye, it was nice talking to you!', 'See ya next time!', 'Alright, have a great day!'],
    'why': ['Why?', 'Hmm, I\'m not sure. Why?', 'I don\'t know, you tell me.', 'I have no idea.'],
    'how': ['Hmm, I don\'t know... How?', 'How?', 'You tell me! How?', 'I have no idea.'],
    'who': ['Who?', 'Hmm... Who?', 'I have no idea.', 'Uh... Tell me, who?', 'Ooh... Who?'],
    'what': ['I don\'t know... what?', 'You tell me! Well?', 'What?', 'I have no idea.'],
    'fallback': ['I don\'t quite understand. Could you repeat that in another way?', 'I\'m sorry, could you rephrase?', 'Could you rephrase? Punctuation is helpful for me.'],
}






def chatbot():
    print(random.choice(responses['greeting']), 'Say goodbye or \"peace\" to leave.')
    just_setup = False  # just set up a joke!

    while(True):
        _input = input().lower()

        if _input == 'peace' or _input in syns_dict['bye']:
            print(random.choice(responses['farewell']))
            break

        chopped_input = _input.split()
        if (('joke' in chopped_input) or ('joke?' in chopped_input)) and (chopped_input[-1][-1] == '?'):
            print(get_setup())
            just_setup = True
            continue
        elif (just_setup):
            print(get_punchline())
            just_setup = False
            continue

        # user asked a question... respond!
        if chopped_input[0] in responses:
            print(random.choice(responses[chopped_input[0]]))

        matched_intent = None
        for intent, pattern in keys_dict.items():
            # use regular expression search function to look for keywords in _input
            if re.search(pattern, _input):
                # if a keyword matches, select the corresponding intent from keys_dict
                matched_intent = intent

        # by default, key = 'fallback'
        key = 'fallback'

        # if there is an intent that isn't 'fallback', replace key
        if matched_intent in responses:
            key = matched_intent

        print(random.choice(responses[key]))





if __name__ == "__main__":
    # chatbot()
    print()