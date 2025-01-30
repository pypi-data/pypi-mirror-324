from math import log

from scipy.special import entr


def binary_entropy(x):
    return entr(x) / log(2)


binary_entropy._platform = "Scipy"
