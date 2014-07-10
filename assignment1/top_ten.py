import sys
import json
import re
import operator


class SentScore(object):
    lookup = {}

    def __init__(self, sent_file):
        self.lookup = self.build_lookup(sent_file)
        return

    @staticmethod
    def build_lookup(sent_file):
        scores = {}

        for line in sent_file:
            term, score = line.split("\t")
            scores[term] = int(score)
        return scores

    def lookup_score(self, term):
        score = self.lookup.get(term, 0)
        return score

    def print_list(self):
        print self.lookup
        return


def calculate_top_ten_hashtags(tweet_file):

    filtered_tweets = filter(
        lambda tweets: 'delete' not in tweets.keys()
        and len(tweets['entities']['hashtags']) is not 0, load_tweets(tweet_file)
    )

    hashtag_count = {}

    for tweet in filtered_tweets:
        for hashtag in tweet['entities']['hashtags']:
            tag = hashtag['text']
            if tag not in hashtag_count.keys():
                hashtag_count[tag] = 1
            else:
                hashtag_count[tag] += 1

    sorted_hashtag_count = sorted(hashtag_count.iteritems(), key=operator.itemgetter(1))[-10:]

    for tag, count in sorted_hashtag_count[::-1]:
        print '{} {}'.format(tag, count)


def load_tweets(tweet_file):
    tweet_list = []

    for line in tweet_file:
        temp = json.loads(line)
        tweet_list.append(temp)

    return tweet_list


def parse_tweet(tweet):
    pattern = re.compile(r'\w*')

    if 'text' in tweet.keys():
        words = pattern.findall(tweet['text'])
        return words
    else:
        return []


def main():
    tweet_file = open(sys.argv[1])

    calculate_top_ten_hashtags(tweet_file)


if __name__ == '__main__':
    main()
