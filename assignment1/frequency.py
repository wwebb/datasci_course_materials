import sys
import json
import re


def calculate_frequency(tweet_file):
    rawTweets = load_tweets(tweet_file)
    parsedTweets = parse_tweets(rawTweets)

    wordList = {}

    for tweet in parsedTweets:
        for word in tweet:
            if word in wordList.keys():
                wordList[word] += 1
            else:
                wordList[word] = 1

    wordList.pop("", None)

    for word, frequency in wordList.items():
        print '{} {}'.format(word, frequency)



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
    tweet_file = open(sys.argv[1])

    calculate_frequency(tweet_file)

if __name__ == '__main__':
    main()
