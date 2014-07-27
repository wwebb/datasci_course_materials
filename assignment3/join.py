__author__ = 'wwebb'

import MapReduce
import itertools
import sys

"""
Word Count Example in the Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    # key: document identifier
    # value: document contents
    key = record[1]
    #value = record[1]
    #words = value.split()
    #print 'Key: {} - Record: {}'.format(key, record)
    mr.emit_intermediate(key, record)

def reducer(key, list_of_values):
    # key: word
    # value: list of occurrence counts

    order = list_of_values[0]
    items = list_of_values[1:]

    #print 'Order: {} - Items: {}'.format(order, items)

    for item in items:
        mr.emit(order + item)

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
