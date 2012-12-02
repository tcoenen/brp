from __future__ import division
from math import log10


def stretch_interval(interval, factor, log):
    '''
    Stretch an interval by some factor.

    Arguments:

        * `interval` -- Interval to stretch (two-element iterable)
        * `factor` -- Factor that describes the amount of stretching
        * `log` -- If true this stretches by the same factor (visually) as for
          the non logarithmic case.

    Note:
        Returns a two-tuple with the stretched interval.
    '''
    tmp = list(interval)
    STRETCH = factor / 2

    if log:
        b, e = log10(interval[0]), log10(interval[1])
        l = e - b
        tmp[0] = 10 ** ((e + b) / 2 - STRETCH * l)
        tmp[1] = 10 ** ((e + b) / 2 + STRETCH * l)
    else:
        l = interval[1] - interval[0]
        tmp[0] = (interval[0] + interval[1]) / 2 - STRETCH * l
        tmp[1] = (interval[0] + interval[1]) / 2 + STRETCH * l

    return tuple(tmp)

