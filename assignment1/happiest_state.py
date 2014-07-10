import sys
import json
import re

stateList = {
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


def calculate_happiest_state(sent_file, tweet_file):
    sentList = SentScore(sent_file)

    tweetList = filter(lambda tweet: 'delete' not in tweet.keys(), load_tweets(tweet_file))

    stateAbbreviations = set(map(lambda (state, abbrev): abbrev, stateList.items()))

    stateScores = dict.fromkeys(stateAbbreviations, 0)

    state_tweets = filter(
        lambda tweet: 'place' in tweet.keys() \
                  and tweet['place'] is not None \
                  and tweet['place']['name'].lower() in stateList.keys(), tweetList)

    tweetsWithStates = set(map(lambda tweet: tweet['id'], state_tweets))

    otherTweets = filter(lambda tweet: tweet['id'] not in tweetsWithStates, tweetList)

    if len(state_tweets) > 0:
        otherTweets.extend(state_tweets)

    for tweet in otherTweets:
        text = parse_tweet(tweet)
        if len(text) is 0:
            continue

        score = sum([sentList.lookup_score(word) for word in text])

        if tweet['id'] in tweetsWithStates:
            state = tweet['place']['name'].lower()
            key = stateList[state]
        else:
            key = parse_location(tweet, stateAbbreviations)
            if key is None:
                continue

        stateScores[key] += score

    sent_max = 0
    happiest_state = ""
    for (state, sentiment) in stateScores.items():
        if sentiment > sent_max:
            sent_max = sentiment
            happiest_state = state

    print happiest_state.upper()


def parse_location(tweet, states):

    regexToken = re.compile(r'\w+')

    words = regexToken.findall(tweet['user']['location'])
    stateAbbreviation = filter(lambda x: x in states, words)

    if len(stateAbbreviation) is not 0:
        return stateAbbreviation[0]

    stateFound = filter(lambda t: t in stateList.keys(), words)

    if not len(stateFound) is 0:
        state = stateFound[0]
        return stateList[state]

    return None


def load_tweets(tweetFile):
    tweetList = []

    for line in tweetFile:
        temp = json.loads(line)
        tweetList.append(temp)

    return tweetList


def parse_tweet(tweet):
    pattern = re.compile(r'\w*')

    if 'text' in tweet.keys():
        words = pattern.findall(tweet['text'])
        return words
    else:
        return []


def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])

    calculate_happiest_state(sent_file, tweet_file)


if __name__ == '__main__':
    main()
