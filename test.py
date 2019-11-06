import numpy as np
import math
import time
import random_2d_slow
import random_2d

# Version of numpy.random.randint that handles drawing without
# replacement. It always returns a two dimensional matrix, where
# the first dimension (columns) is sampled without replacement
# and the second dimension (rows) is not, so each row contains
# unique integers, but the rows are independent from each other.
#
# If we need a function more like randint, in that it allows more
# or less than two dimensions, we can easily layer such a function
# on top of this one, by doing a reshape of the resulting array.
def randint_2d(low: int, high: int, rows: int, cols: int):
    max_size = high - low
    if cols > max_size:
        raise ValueError("randint_2d: cols is larger than high - low")

    # set up an array of ascending integers, then use choice_2d
    choose_from = np.arange(low, high)
    return choice_2d(choose_from, cols, rows)

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

def choice_2d(a, cols: int, rows = None):
    # Validate that the array and size parameters are compatible
    a_shape = a.shape
    dim = len(a_shape)
    if dim == 2:
        if rows is not None:
            raise ValueError("numpyplus.choice_2d: if array a is two dimensional, rows must be None")
        out_rows = a.shape[0]
    elif dim == 1:
        out_rows = int(rows)
    else:
        raise ValueError("numpyplus.choice_2d: input array a must be one or two dimensional")
    a_cols = a_shape[-1]
    if cols > a_cols:
        raise ValueError(f"numpyplus.choice: cols ({cols}) is larger than columns of a ({a_cols})")

    result = np.zeros((out_rows, cols), a.dtype)

    # draw samples one row at a time, either from a vector or a 2d array
    for row in range(out_rows):
        result[row] = np.random.choice(a[row] if dim == 2 else a, cols, replace = False)

    return result

def test_randint_2d(title: str, randint_fn):
    max = 1000
    shape = (200, 300)
    start = time.process_time()
    result = randint_fn(0, max, shape[0], shape[1])
    elapsed = time.process_time() - start
    
    assert(result.shape == shape)
    #nl = "\n"
    #print(f"test_randint: {nl}{result}")
    for i in np.nditer(result):
        assert(i >= 0 and i < max)
    
    for row in result:
        u = np.unique(row)
        assert(len(u) == len(row))

    mean = np.mean(result)
    stdev = np.std(result)
    print(f"{title} succeeded after {elapsed} seconds: mean={mean} stdev = {stdev}")
    #print(f"  expected mean = {max * 0.5} stdev = {max / math.sqrt(12)}")
    assert(math.isclose(mean, max * 0.5, abs_tol = 3))
    assert(math.isclose(stdev, max / math.sqrt(12), abs_tol = 3))

def test_choice_2d(title: str, choice_fn):
    cols = 123
    shape = (200, 300)
    max = np.prod(shape)
    array = np.arange(max).reshape(shape)
    start = time.process_time()
    result = choice_fn(array, cols)
    elapsed = time.process_time() - start

    #nl = "\n"
    #print(f"test_choice: shape={nl}{result.shape}")
    assert(result.shape == (shape[0], cols))
    #print(f"test_choice: {nl}{result}")

    for i in np.nditer(result):
        assert(i >= 0 and i < max)

    result_from = 0
    result_to = shape[1]   
    for row in result:
        u = np.unique(row)
        assert(len(u) == len(row))
        for i in row:
            assert(i >= result_from and i < result_to)
        result_from = result_to
        result_to = result_to + shape[1]

    mean = np.mean(result)
    stdev = np.std(result)
    print(f"{title} succeeded after {elapsed} seconds: mean={mean} stdev = {stdev}")
    #print(f"  expected mean = {max * 0.5} expected stdev = {max / math.sqrt(12)}")

    assert(math.isclose(mean, max * 0.5, abs_tol = 3))
    assert(math.isclose(stdev, max / math.sqrt(12), abs_tol = 3))

if __name__ == '__main__':
    test_randint_2d("test.randint_2d", randint_2d)
    test_choice_2d("test.choice_2d", choice_2d)

    test_randint_2d("random_2d_slow.randint_2d", random_2d_slow.randint_2d)
    test_choice_2d("random_2d_slow.choice_2d", random_2d_slow.choice_2d)

    test_randint_2d("random_2d.randint_2d", random_2d.randint_2d)
    test_choice_2d("random_2d.choice_2d", random_2d.choice_2d)
    