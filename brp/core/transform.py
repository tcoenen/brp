'''
Utility code dealing with the finding of transforms.

Note: brp is not designed to deal with a general linear transform. The design
assumes that there is a separate transform for the X axis and the Y axis.
'''

from __future__ import division
from math import log10

def setup_transform_1d(interval, target_interval, log=False):
    '''
    Create transform function from `interval' to `target_interval'.

    Arguments:

        * `interval` --- Two number tuple or list representing an interval.
        * `target_interval`
        * `log` --- Boolean, True if data should be plot logarithmically. 

    Returns:
        A transformation function.
    
    >>> from brp.core.transform import setup_transform_1d
    >>> setup_transform_1d([0, 10], [0, 10], False)(7)
    7.0
    >>> setup_transform_1d([0, 10], [10, 0], False)(7)
    3.0
    
    >>> setup_transform_1d([1, 100], [0, 2], True)(100)
    2.0
    >>> setup_transform_1d([1, 100], [0, 2], True)(10)
    1.0
    >>> setup_transform_1d([1, 100], [0, 2], True)(1)
    0.0
    >>> setup_transform_1d([1, 100], [0, 2], True)(0.1)
    -1.0

    >>> setup_transform_1d([1, 100], [2, 0], True)(100)
    0.0
    >>> setup_transform_1d([1, 100], [2, 0], True)(1)
    2.0
    '''

    if log: # 'Logarithmic' transform.
        scale = (target_interval[1] - target_interval[0]) / \
            (log10(interval[1]) - log10(interval[0]))
        in_shift = interval[0]
        out_shift = target_interval[0]

        def transform(x):
            return (log10(x) - log10(in_shift)) * scale + out_shift

    else: # Normal 'linear' transform.
        if interval[1] - interval[0] == 0:
            if interval[1] == 0:
                oom = 0
            else:
                oom = abs(interval[0])
            interval = (interval[0] - 10 ** (oom - 1), 
                interval[1] + 10 ** (oom - 1))
 
        scale = (target_interval[1] - target_interval[0])/ \
            (interval[1] - interval[0]) 
        in_shift = interval[0]
        out_shift = target_interval[0]

        def transform(x):
            return (x - in_shift) * scale + out_shift

    return transform


def setup_transforms(bbox, target_bbox, x_log=False, y_log=False):
    '''
    Create the x and y transform needed for plotting.

    Arguments :

        * `bbox` --- List or tuple representing a 2d bounding box containing
          the data to be plot like (xmin, ymin, xmax, ymax).
        * `target_bbox` --- List or tuple representing a 2d bouding box in SVG
          screen coordinates. 
        * `x_log` --- Boolean, True if x-axis should be transformed 
          logarithmically, default False.
        * `y_log` --- Boolean, True if y-axis should be transformed 
          logarithmically, default False.

    Returns : 
        Two transformation function (one for x-data, one for y-data).

    >>> from brp.core.transform import setup_transforms
    >>> fx, fy = setup_transforms([0, 0, 10, 10], [0, 0, 10, 10])
    >>> fx(4)
    4.0
    >>> fy(6)
    6.0
    >>> fx, fy = setup_transforms([0, 0, 10, 10], [10, 10, 0, 0])
    >>> fx(6)
    4.0
    >>> fy(6)
    4.0
    '''
    x_interval = (bbox[0], bbox[2])
    x_target_interval = (target_bbox[0], target_bbox[2])
    x_transform = setup_transform_1d(x_interval, x_target_interval,x_log)

    y_interval = (bbox[1], bbox[3])
    y_target_interval = (target_bbox[1], target_bbox[3])
    y_transform = setup_transform_1d(y_interval, y_target_interval,y_log)
    
    return x_transform, y_transform

