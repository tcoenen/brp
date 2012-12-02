'''
Utility functions dealing with bounding boxes.

In brp code the bounding boxes 2d by default and defined as a list with the
following entries: [xmin, ymin, xmax, ymax]
'''

from __future__ import division
from math import log10


def find_bounding_box(lx, ly, bbox=None):
    '''
    Find bounding box given list of numbers for x and y.

    Bounding box is given as [xmin, ymin, xmax, ymax].
    Note : assumes that lx and ly can be accessed by index.

    >>> from brp.core.bbox import find_bounding_box
    >>> find_bounding_box([5, 0, 10], [6, 0, 10])
    (0, 0, 10, 10)

    Arguments:

        * `lx` -- List of data x coordinates.
        * `ly` -- List of data y coordinates.
        * `bbox` -- Bounding box to be updated with the new data in lx and ly.

    Returns:
        A tuple representing a bounding box : (xmin, ymin, xmax, ymax).
    '''
    if not bbox:
        bbox = [lx[0], ly[0], lx[0], ly[0]]  # [xmin, ymin, xmax, ymax]
    else:
        bbox = list(bbox)
    for x, y in zip(lx, ly):
        if x < bbox[0]:
            bbox[0] = x
        elif x > bbox[2]:
            bbox[2] = x
        if y < bbox[1]:
            bbox[1] = y
        elif y > bbox[3]:
            bbox[3] = y
    return tuple(bbox)


def stretch_bbox(bbox, x_factor, y_factor, x_log, y_log):
    '''
    Stretch the size of a bounding box by some factor.

    Arguments:

        * `bbox` -- Bounding box, tuple/list like: (xmin, ymin, xmax, ymax)
        * `x_factor` -- Factor by which to stretch the X bounding box.
        * `y_factor` -- Factor by which to stretch the Y bounding box.
        * `x_log` -- Boolean, True if x axis should be treated as logarithmic
          default False.
        * `y_log` -- Boolean, True if y axis should be treated as logarithmic
          default False.

    Returns:
        A tuple representing a bounding box : (xmin, ymin, xmax, ymax).

    Note:
        In case logarithmic transforms are needed the stretch is performed
        such that the result looks the same as the linear case as this
        function is used for creating the margins around the datapoints in a
        graph.
    '''
    tmp = [0, 0, 0, 0]
    X_STRETCH = x_factor / 2
    Y_STRETCH = y_factor / 2

    if x_log:
        b, e = log10(bbox[0]), log10(bbox[2])
        w = e - b
        tmp[0] = 10 ** ((e + b) / 2 - X_STRETCH * w)
        tmp[2] = 10 ** ((e + b) / 2 + X_STRETCH * w)
    else:
        w = bbox[2] - bbox[0]
        tmp[0] = (bbox[0] + bbox[2]) / 2 - X_STRETCH * w
        tmp[2] = (bbox[0] + bbox[2]) / 2 + X_STRETCH * w

    if y_log:
        b, e = log10(bbox[1]), log10(bbox[3])
        h = e - b
        tmp[1] = 10 ** ((e + b) / 2 - Y_STRETCH * h)
        tmp[3] = 10 ** ((e + b) / 2 + Y_STRETCH * h)
    else:
        h = bbox[3] - bbox[1]
        tmp[1] = (bbox[1] + bbox[3]) / 2 - Y_STRETCH * h
        tmp[3] = (bbox[1] + bbox[3]) / 2 + Y_STRETCH * h

    return tuple(tmp)


def combine_bbox(bbox1, bbox2):
    bbox1 = list(bbox1)
    bbox2 = list(bbox2)
    return tuple([min(bbox1[0], bbox2[0]), min(bbox1[1], bbox2[1]),
                 max(bbox1[2], bbox2[2]), max(bbox1[3], bbox2[3])])
