__author__ = 'wwebb'

import MapReduce
import sys

"""
Consider a set of key-value pairs where each key is sequence id and each
value is a string of nucleotides, e.g., GCTTCCGAAATGCTCGAA....

Write a MapReduce query to remove the last 10 characters from each
string of nucleotides, then remove any duplicates generated.
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    [sequenceID, nucleotide] = record

    # Remove last 10 characters from each nucleotide
    nucleotide = nucleotide[:-10]

    # Emit trimmed down nucleotide list
    mr.emit_intermediate(nucleotide, sequenceID)


def reducer(key, list_of_values):
    # Emit just the key
    mr.emit(key)
    return


# Do not modify below this line
# =============================
if __name__ == '__main__':
    inputdata = open(sys.argv[1])
    mr.execute(inputdata, mapper, reducer)
