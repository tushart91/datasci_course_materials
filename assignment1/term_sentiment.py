import sys
import json
import re
from collections import OrderedDict
from time import time

debug = False

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

def sentence_sentiment(word_list, gram, sent_dict, remaining):
    length = len(word_list)

    if gram == 0 and length != 0:
        remaining.extend(word_list)
        return 0

    if length == 0:
        return 0

    if length < gram:
        return sentence_sentiment(word_list, gram - 1, sent_dict, remaining)

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
        return sentence_sentiment(word_list, gram - 1, sent_dict, remaining)

    remove_from_to = combine_interval(remove_from_to)

    prev = 0
    for interval in remove_from_to:
        score += sentence_sentiment(word_list[prev:interval['start']], gram - 1, sent_dict, remaining)
        prev = interval['end']
    score += sentence_sentiment(word_list[remove_from_to[-1]['end']:], gram - 1, sent_dict, remaining)

    return score




def calc_sentiment(sent_dict, max_gram, fp):
    """
     Computes sentiment for file
    """
    fp.seek(0)
    rem_word_score = OrderedDict()
    regex = re.compile('\n')
    for line in fp:
        tweet = json.loads(line)
        tweet_text = tweet.get('text', None)
        if not tweet_text:
            continue
        remaining = []
        word_list = [regex.sub(' ', word.lower()) for word in tweet_text.split(" ") if word]
        score = sentence_sentiment(word_list, max_gram, sent_dict, remaining)

        for word in remaining:
            rem_word_score[word] = float(rem_word_score.get(word, 0) + score)

    for word, score in rem_word_score.items():
        print word.encode('utf-8'), score


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
