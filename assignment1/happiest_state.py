import sys
import json
from collections import OrderedDict
from time import time

debug = False
states = {
        'Alaska': 'AK',
        'Alabama': 'AL',
        'Arkansas': 'AR',
        'American Samoa': 'AS',
        'Arizona': 'AZ',
        'California': 'CA',
        'Colorado': 'CO',
        'Connecticut': 'CT',
        'District of Columbia': 'DC',
        'Delaware': 'DE',
        'Florida': 'FL',
        'Georgia': 'GA',
        'Guam': 'GU',
        'Hawaii': 'HI',
        'Iowa': 'IA',
        'Idaho': 'ID',
        'Illinois': 'IL',
        'Indiana': 'IN',
        'Kansas': 'KS',
        'Kentucky': 'KY',
        'Louisiana': 'LA',
        'Massachusetts': 'MA',
        'Maryland': 'MD',
        'Maine': 'ME',
        'Michigan': 'MI',
        'Minnesota': 'MN',
        'Missouri': 'MO',
        'Northern Mariana Islands': 'MP',
        'Mississippi': 'MS',
        'Montana': 'MT',
        'National': 'NA',
        'North Carolina': 'NC',
        'North Dakota': 'ND',
        'Nebraska': 'NE',
        'New Hampshire': 'NH',
        'New Jersey': 'NJ',
        'New Mexico': 'NM',
        'Nevada': 'NV',
        'New York': 'NY',
        'Ohio': 'OH',
        'Oklahoma': 'OK',
        'Oregon': 'OR',
        'Pennsylvania': 'PA',
        'Puerto Rico': 'PR',
        'Rhode Island': 'RI',
        'South Carolina': 'SC',
        'South Dakota': 'SD',
        'Tennessee': 'TN',
        'Texas': 'TX',
        'Utah': 'UT',
        'Virginia': 'VA',
        'Virgin Islands': 'VI',
        'Vermont': 'VT',
        'Washington': 'WA',
        'Wisconsin': 'WI',
        'West Virginia': 'WV',
        'Wyoming': 'WY'
}


def read_sentiments(fp):
    fp.seek(0)
    sent_dict = {}
    max_gram = 0
    for line in fp:
        term, score = line.split("\t")
        max_gram = max(len(term.split(" ")), max_gram)
        sent_dict[term] = int(score)
    return sent_dict, max_gram

def combine_interval(intervals):
    if not intervals:
        return []

    stack = [intervals[0]]

    for i in range(1, len(intervals)):
        top = len(stack) - 1
        if intervals[i]['start'] > stack[top]['end']:
            stack.append(intervals[i])
        elif stack[top]['end'] >= intervals[i]['start']:
            stack[top]['end'] = max(intervals[i]['end'], stack[top]['end'])

    return stack

def sentence_sentiment(word_list, gram, sent_dict):
    length = len(word_list)

    if gram == 0 and length != 0:
        return 0

    if length == 0:
        return 0

    if length < gram:
        return sentence_sentiment(word_list, gram - 1, sent_dict)

    score = 0
    ngrams = []
    for start in range(0, length - gram + 1):
        ngrams.append([" ".join(word_list[start:start + gram]), {'start': start, 'end': start + gram}])

    remove_from_to = []
    for key, value in ngrams:
        if key in sent_dict:
            score += sent_dict[key]
            remove_from_to.append(value)

    if not remove_from_to:
        return sentence_sentiment(word_list, gram - 1, sent_dict)

    remove_from_to = combine_interval(remove_from_to)

    prev = 0
    for interval in remove_from_to:
        score += sentence_sentiment(word_list[prev:interval['start']], gram - 1, sent_dict)
        prev = interval['end']
    score += sentence_sentiment(word_list[remove_from_to[-1]['start']:], gram - 1, sent_dict)

    return score




def calc_sentiment(sent_dict, max_gram, fp):
    """
     Computes sentiment for file
    """
    fp.seek(0)
    state_score = OrderedDict()
    state_num   = OrderedDict()
    for line in fp:
        tweet = json.loads(line)
        tweet_text = tweet.get('text', None)
        if not tweet_text:
            continue

        word_list = [word.lower() for word in tweet_text.split(" ") if word]
        score = sentence_sentiment(word_list, max_gram, sent_dict)

        place = tweet.get('place', None)

        if place:
            cntry = place.get('country', "")
            ccode = place.get('country_code', "")
            ptype = place.get('place_type', "")


            if cntry == "United States" and ccode == "US" and ptype:
                cname = place.get('full_name', "").strip()
                aname = place.get('name', "").strip()
                if ptype == "city":
                    state = cname.split(",")[1].strip()
                elif ptype == "admin":
                    state = states[aname]
                if state:
                    state_score[state] = float(state_score.get(state, 0) + score)
                    state_num[state]   = state_num.get(state, 0) + 1

    happiest_score = 0
    happiest_state = ""
    for key, value in state_score.items():

        avg = value / state_num[key]

        if debug:
            print key, value, state_num[key], avg

        if not happiest_state:
            happiest_score = avg
            happiest_state = key

        if avg > happiest_score:
            happiest_score = avg
            happiest_state = key

    print happiest_state
    return 1

def lines(fp):
    print str(len(fp.readlines()))

def main():
    sent_file = open(sys.argv[1])
    tweets_file = open(sys.argv[2])
    # lines(sent_file)
    # lines(tweets_file)

    sent_dict, max_gram = read_sentiments(sent_file)
    calc_sentiment(sent_dict, max_gram, tweets_file)
    sent_file.close()
    tweets_file.close()

if __name__ == '__main__':

    # debug = True

    if debug:
        start = time()

    main()

    if debug:
        print "exec time:", time() - start
