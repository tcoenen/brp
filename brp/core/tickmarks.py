'''
Utility code to find appropriate tickmarks given some range.
'''
from __future__ import division
from math import log10

# Tickmarks are represented as a list [(value, size), ..] with size in [0, 10]

def find_tickmarks(interval, n=11):
    '''
    Find appropriate tickmarks given an interval, produces only major tickmarks.
    
    Arguments:

        * `interval` -- interval to produce tickmarks for (two element 
          iterable)
        * `n` -- Number of tickmarks to produce (default 11)
    
    Note:
        Tickmarks returned are a list [(value_1, size_1), ..., 
        (value_n, size_n)].
    '''
    # Format for tickmarks : [(value_1, size_1), ..., (value_n, size_n)] .
    interval = list(interval)
    
    if interval[1] - interval[0] == 0:
        if interval[1] == 0:
            oom = 0
        else:
            oom = abs(interval[0])
        interval = (interval[0] - 10 ** (oom - 1), 
            interval[1] + 10 ** (oom - 1))


    if interval[0] > interval[1]:
        interval[0], interval[1] = interval[1], interval[0]

    # Find the rough stepsize (between tickmarks).
    rough_stepsize = (interval[1] - interval[0]) / n
    try:
        pot = int(log10(rough_stepsize))
    except ValueError, e:
        print rough_stepsize
        raise

    # Find a correct stepsize (between tickmarks).
    MULTIPLICATION_FACTORS = [0.1, 0.2, 0.5, 1, 2, 5, 10]
    for i, multiplyer in enumerate(MULTIPLICATION_FACTORS):
        if multiplyer * (10 ** pot) > rough_stepsize:
            break
    stepsize = (10 ** pot) * multiplyer
    if stepsize > interval[1] - interval[0]:
        stepsize = (10 ** pot) * MULTIPLICATION_FACTORS[i-1]

    # Find the tickmarks themselves.
    if interval[0] % stepsize == 0:
        t0 = interval[0]
    else:
        if interval[0] >= 0:
            t0 = (int(interval[0] / stepsize)+1) * stepsize
        else:
            t0 = (int(interval[0] / stepsize)) * stepsize
    tickmarks = []
    for i in range(int((interval[1]-t0)/stepsize)+1):
        tickmarks.append((t0 + i * stepsize, 10))
    # Temporary fix is to only return 2 tickmarks in case where too many 
    # tickmarks were found.
    if len(tickmarks) > n:
        tickmarks = [(tickmarks[0], 10), (tickmarks[-1], 10)]
    return tickmarks

def find_tickmarks_log(interval, n=11):
    '''
    Find logarithmicly spaced tickmarks.
    
    Arguments:

        * `interval` -- interval to produce tickmarks for (two element 
          iterable)
        * `n` -- Number of tickmarks to produce (default 11) - Is ignored,
          present only for compatibility with the non logarithmic tickmark
          finder. 

    Note:
        Tickmarks returned are a list [(value_1, size_1), ..., 
        (value_n, size_n)].
    '''
    l, h = interval
    tickmarks = []
    for i in range(int(log10(l) - 1), int(log10(h))+1):
        for ii in range(1, 10):
            tickmark_position = ii * 10 ** i
            if l <= tickmark_position <= h:
                if ii == 1:
                    size = 10
                else:
                    size = ii
                tickmarks.append((tickmark_position, size))
    return tickmarks

