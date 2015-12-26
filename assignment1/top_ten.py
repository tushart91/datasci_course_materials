import sys
import json
import operator
from collections import OrderedDict
from time import time


debug = False

def calc_top_ten(fp):
    """
     Computes sentiment for file
    """
    fp.seek(0)
    hashtag_count = OrderedDict()
    total = float(0)
    for line in fp:
        tweet = json.loads(line)
        hashtags = tweet.get('entities', {}).get('hashtags', [])
        for hashtag in hashtags:
            hashtag_count[hashtag['text']] = hashtag_count.get(hashtag['text'], 0) + 1

    hashtag_count = sorted(hashtag_count.items(), key=operator.itemgetter(1), reverse=True)[:10]

    for key, value  in hashtag_count:
        print key, value

    return 1

def lines(fp):
    print str(len(fp.readlines()))

def main():
    # sent_file = open(sys.argv[1])
    tweets_file = open(sys.argv[1])
    # lines(sent_file)
    # lines(tweets_file)

    calc_top_ten(tweets_file)
    # sent_file.close()
    tweets_file.close()

if __name__ == '__main__':

    # debug = True

    if debug:
        start = time()

    main()

    if debug:
        print "exec time:", time() - start
