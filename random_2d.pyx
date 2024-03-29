# cython: infer_types=True
import numpy as np
from libc.stdlib cimport rand, srand
cimport cython

# Version of numpy.random.randint that handles drawing without
# replacement. It always returns a two dimensional matrix, where
# the first dimension (columns) is sampled without replacement
# and the second dimension (rows) is not, so each row contains
# unique integers, but the rows are independent from each other.
#
# If we need a function more like randint, in that it allows more
# or less than two dimensions, we can easily layer such a function
# on top of this one, by doing a reshape of the resulting array.
@cython.boundscheck(False)
@cython.wraparound(False)
def randint_2d(int low, int high, int rows, int cols):
    max_size = high - low
    if cols > max_size:
        raise ValueError("randint_2d: cols is larger than high - low")

    # Use reservoir-sampling algorithm for each row to select the elements
    # then use fisher-yates algorithm to shuffle the result:
    result = np.zeros((rows, cols), np.int)
    cdef int[:, :] result_view = result
    for row in range(rows):
        reservoir_sampling_range(result_view[row], low, high, cols)
        fisher_yates(result_view[row], cols)
    return result

@cython.boundscheck(False)
@cython.wraparound(False)
def reservoir_sampling_range(int[:] row, int low, int high, int cols):

    # start by filling the array with sequential numbers from low to low + cols
    for i in range(cols):
        row[i] = i + low

    # for the remaining integers (low + cols to high), pick a column to replace
    cdef int j   
    for i in range(cols, high - low):
        j = randint(i)
        if j < cols:
            row[j] = i + low

@cython.boundscheck(False)
@cython.wraparound(False)
def reservoir_sampling_from(int[:] row, int[:] source, int cols, int source_cols):

    assert(source_cols >= cols)

    # start by filling the array from the source
    for i in range(cols):
        row[i] = source[i]

    # for the remainder of the source, pick a column to replace
    cdef int j    
    for i in range(cols, source_cols):
        j = randint(i)
        if j < cols:
            row[j] = source[i]

@cython.boundscheck(False)
@cython.wraparound(False)
def fisher_yates(int[:] row, int n):
    cdef int j
    for i in range(n - 1, 0, -1):
        j = randint(i)
        tmp = row[i]
        row[i] = row[j]
        row[j] = tmp

# Rather trivial function for returning a random integer between
# zero and i. Implemented here so we can easily replace it in
# Cython with native C randint function.
@cython.boundscheck(False)
@cython.wraparound(False)
def randint(int i):
    cdef int r = rand()
    return r % i

# Two dimensional version of numpy.random.choice. It always returns
# a two dimensional matrix, where the first dimension
# may or may not be sampled without replacement, according to the
# flag passed in, and the second dimension always uses replacement.
# Thus each row contains uniquely sampled members, but the rows are
# independent from each other. The size parameter refers to how many
# items to choose from each row. It must be an int. The results have
# the same number of rows as the input array, if the input array is
# 2d. Otherwise, the rows parameter must be passed in, and the
# results are constructed by repeatedly drawing from the input vector.

@cython.boundscheck(False)
def choice_2d(a, int cols, rows = None):
    # Validate that the array and size parameters are compatible
    a_shape = a.shape
    dim = len(a_shape)
    if dim == 2:
        if rows is not None:
            raise ValueError("choice_2d: if array a is two dimensional, rows must be None")
        out_rows = a.shape[0]
    elif dim == 1:
        out_rows = int(rows)
    else:
        raise ValueError("choice_2d: input array a must be one or two dimensional")
    a_cols = a_shape[-1]
    if cols > a_cols:
        raise ValueError(f"choice: cols ({cols}) is larger than columns of a ({a_cols})")

    result = np.zeros((out_rows, cols), a.dtype)
    cdef int[:, :] result_view = result

    # Draw samples one row at a time, either from a vector or a 2d array.
    # For each, we first sample the items we need, then shuffle them
    cdef int i
    for i in range(out_rows):
        reservoir_sampling_from(result_view[i], a[i] if dim == 2 else a, cols, a_cols)
        fisher_yates(result_view[i], cols)

    return result
 