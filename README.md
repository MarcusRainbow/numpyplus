# numpyplus
Extensions to numpy. So far there are two extension functions:

## randint_2d

A commonly reported issue with randint is that it does not handle selection
without replacement. It results in a vector or other shape of independent
random integers, where some may be duplicates of others.

Commonly what is required is a 2d matrix, where each row is drawn independently,
but within each row, there are no duplicates -- in other words within each row,
selection is made without replacement.

In other cases, such as different shapes, or the columns having no duplicates,
it should be a trivial bit of numpy manipulation to get the results into the
desired form.

## choice_2d

A commonly reported issue with choice is that it is only single dimensional.
As with randint_2d, we take the simplifying assumption that selection should
be without replacement along the rows, and independent between rows. (Other
possibilities may be relevant, but they could be simulated using randint_2d
and reshaping.)

For speed, both of this functions use the native C library function rand.
