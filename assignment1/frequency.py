import sys
import json
import re
from collections import OrderedDict
from time import time

debug = False

def calc_frequency(fp):
    """
     Computes sentiment for file
    """
    fp.seek(0)
    regex = re.compile('\n')
    word_dict = OrderedDict()
    total = float(0)
    for line in fp:
        tweet = json.loads(line)
        tweet_text = tweet.get('text', None)
        if not tweet_text:
            continue

        word_list = [regex.sub(' ', word.lower()) for word in tweet_text.split(" ") if word]
        for word in word_list:
            word_dict[word] = word_dict.get(word, 0) + 1
            total += 1

    for word, count in word_dict.items():
        print word.encode('utf-8'), count/total

    return 1

def lines(fp):
    print str(len(fp.readlines()))

def main():
    # sent_file = open(sys.argv[1])
    tweets_file = open(sys.argv[1])
    # lines(sent_file)
    # lines(tweets_file)

    calc_frequency(tweets_file)
    # sent_file.close()
    tweets_file.close()

if __name__ == '__main__':

    # debug = True

    if debug:
        start = time()

    main()

    if debug:
        print "exec time:", time() - start
