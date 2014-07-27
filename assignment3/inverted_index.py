__author__ = 'wwebb'

import MapReduce
import sys

"""
Problem 1
Create an Inverted index. Given a set of documents, an inverted index is a dictionary where each word is
associated with a list of the document identifiers in which that word appears.

Mapper Input
The input is a 2 element list: [document_id, text], where document_id is a string representing a
document identifier and text is a string representing the text of the document. The document text may
have words in upper or lower case and may contain punctuation. You should treat each token as if it
was a valid word; that is, you can just use value.split() to tokenize the string.
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    # key: document identifier
    # value: book text
    key = record[0]
    value = record[1]
    words = value.split()
    for w in words:
      mr.emit_intermediate(w, key)

def reducer(key, list_of_values):
    # key: word
    # value: id list

    # Take list of values (docids), remove duplicates by turning it into
    # a set, and then emit emit index for the word (key)
    docList = list(set(list_of_values))
    mr.emit((key, docList))

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)