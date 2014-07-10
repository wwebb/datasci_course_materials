import sys
import json
import re


class SentScore(object):

    lookup = {}

    def __init__(self, sentFile):

        self.lookup = self.build_lookup(sentFile)
        return

    def build_lookup(self, sentFile):
        scores = {}

        for line in sentFile:
            term, score = line.split("\t")
            scores[term] = int(score)
        return scores

    def lookup_score(self, term):
        score = self.lookup.get(term, 0)
        return score

    def print_list(self):
        print self.lookup
        return


def calculate_sentiments(sent_file, tweet_file):
    rawTweets = load_tweets(tweet_file)
    sentList = SentScore(sent_file)
    parsedTweets = parse_tweets(rawTweets)

    sums = []

    for words in parsedTweets:
        score = [sentList.lookup_score(w) for w in words]
        totalScore = sum(score)
        print totalScore


def load_tweets(tweetFile):
    tweetList = []

    for line in tweetFile:
        temp = json.loads(line)
        tweetList.append(temp)

    return tweetList


def parse_tweets(rawTweets):
    parsed = []
    pattern = re.compile(r'\w*')

    for tweet in rawTweets:
        if 'text' in tweet.keys():
            words = pattern.findall(tweet['text'])
            parsed.append(words)

    return parsed


def hw():
    print 'Hello, world!'


def lines(fp):
    print str(len(fp.readlines()))


def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])

    calculate_sentiments(sent_file, tweet_file)

if __name__ == '__main__':
    main()
