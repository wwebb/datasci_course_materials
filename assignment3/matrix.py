__author__ = 'wwebb'

import MapReduce
import sys

matrixDimensionRow = 5
matrixDimensionCol = 5

"""
Assume you have two matrices A and B in a sparse matrix format, where
each record is of the form i, j, value. Design a MapReduce algorithm to
compute the matrix multiplication A x B
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line


def mapper(record):
    [matrix, row, col, value] = record
    #print 'Matrix: {}, i: {}, j: {}, Value: {}'.format(matrix, row, col ,value)

    if matrix == 'a':
        for k in xrange(0, matrixDimensionCol):
            mr.emit_intermediate((row, k), [matrix, col, value])
    elif matrix == 'b':
        for l in xrange(0, matrixDimensionRow):
            mr.emit_intermediate((l, col), [matrix, row, value])


def reducer(key, list_of_values):

    (row, col) = key

    # create blank dictionary for two matrices
    dictA = {key: 0 for key in xrange(5)}
    dictB = {key: 0 for key in xrange(5)}
    total = 0

    # populate matrices from list_of_values
    for (matrix, cell, value) in list_of_values:
        if matrix == 'a':
            dictA[cell] = value
        elif matrix == 'b':
            dictB[cell] = value

    # multiply and sum each value through range
    for x in xrange(5):
        total += dictA[x] * dictB[x]

    # emit the row, col, and total
    mr.emit((row, col, total))


# Do not modify below this line
# =============================
if __name__ == '__main__':
    inputdata = open(sys.argv[1])
    mr.execute(inputdata, mapper, reducer)
