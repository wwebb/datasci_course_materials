__author__ = 'wwebb'

import MapReduce
import sys

"""
Consider a simple social network dataset consisting of a set of key-value
pairs (person, friend) representing a friend relationship between two people.
Describe a MapReduce algorithm to count the number of friends for each person.
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    # key: document identifier
    # value: document contents
    personA = record[0]
    #value = record[1]
    #words = value.split()
    mr.emit_intermediate(personA, 1)

def reducer(key, list_of_values):
    # key: word
    # value: list of occurrence counts
    total = 0
    for v in list_of_values:
      total += v
    mr.emit((key, total))

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
