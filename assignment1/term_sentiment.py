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

    noSentimentList = {}

    for tweet in parsedTweets:

        positive = 0
        negative = 0
        temp = []

        for word in tweet:
            sentiment = sentList.lookup_score(word)
            if sentiment < 0:
                negative += 1
            elif sentiment > 0:
                positive += 1
            else:
                temp.append(word)

        if negative is 0:
            ratio = float(positive)
        else:
            ratio = float(positive)/float(negative)

        for t in temp:
            if t in noSentimentList.keys():
                noSentimentList[t] += ratio
            else:
                noSentimentList[t] = ratio

    noSentimentList.pop("", None)

    for term, value in noSentimentList.items():
        print '{} {}'.format(term, value)


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
