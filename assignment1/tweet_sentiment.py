import sys
import json
from time import time

debug = True

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
        print "35: Gram became zero. Investigate."
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

    remove_from_to = combine_interval(remove_from_to)

    prev = 0
    for interval in remove_from_to:
        score += sentence_sentiment(word_list[prev:interval['start']], gram - 1, sent_dict)
        prev = interval['end']

    return score




def calc_sentiment(sent_dict, max_gram, fp):
    """
     Computes sentiment for file
    """
    fp.seek(0)
    for line in fp:
        tweet = json.loads(line)
        tweet_text = tweet.get('text', None)
        if not tweet_text:
            continue

        word_list = [word.lower() for word in tweet_text.split(" ") if word]
        score = sentence_sentiment(word_list, max_gram, sent_dict)
        if score != 0 and debug:
            print tweet_text, score
        if not debug:
            print score

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

    debug = False

    if debug:
        start = time()

    main()

    if debug:
        print "exec time:", time() - start
