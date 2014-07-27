__author__ = 'wwebb'


import MapReduce
import sys
import operator

"""
Consider a simple social network dataset consisting of a set of key-value
pairs (person, friend) representing a friend relationship between two people.
Describe a MapReduce algorithm to count the number of friends for each person.
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    [person, friend] = record

    # Add a relationship for both ways, creating a symmetric friendship
    # if one exists. The relationships can later be filtered (XOR)
    mr.emit_intermediate(person, [person, friend])
    mr.emit_intermediate(friend, [friend, person])

def reducer(key, list_of_values):
    # create tuple of pairs of friends
    friendPairs = [tuple(value) for value in list_of_values]
    allFriends = set(friendPairs)

    # Search for duplicates, create a set to eliminate duplicates
    duplicateFriends = set([x for x in friendPairs if friendPairs.count(x) > 1])

    # Remove duplicate friends by doing an XOR operator on the two lists
    finalFriends = operator.xor(allFriends, duplicateFriends)

    #print 'Friends: {}'.format(finalFriends)

    # for every pair in filtered list, emit this pair
    [mr.emit(friendPair) for friendPair in finalFriends]


# Do not modify below this line
# =============================
if __name__ == '__main__':
    inputdata = open(sys.argv[1])
    mr.execute(inputdata, mapper, reducer)
