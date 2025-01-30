from math import log

from .helpers import optionally_numba


@optionally_numba
def binary_entropy(x):
    return - x * log(x) / log(2.0)
