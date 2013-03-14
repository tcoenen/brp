'''
Prototype brp raster image generation. Needs PIL and Numpy to work.
'''
# TODO : Check that histogram with single counts get colored correctly
# there might an off by one in the color mapping.
from __future__ import division
import StringIO
from base64 import encodestring

import numpy
import Image

from brp.core.bbox import find_bounding_box
from brp.svg.plotters.raster import RasterPlotterMixin
from brp.svg.plotters.gradient import RGBGradient


def bin_data_2d(x_seq, y_seq, x_bins, y_bins, hist_bbox):
    ar = numpy.zeros((x_bins, y_bins), dtype=numpy.int_)
    dw = (hist_bbox[2] - hist_bbox[0]) / x_bins
    dh = (hist_bbox[3] - hist_bbox[1]) / y_bins
    for x, y in zip(x_seq, y_seq):
        if not (hist_bbox[0] <= x < hist_bbox[2]):
            continue
        if not hist_bbox[1] <= y < hist_bbox[3]:
            continue
        x_idx = int((x - hist_bbox[0]) / dw)
        y_idx = int((y - hist_bbox[1]) / dh)
        ar[x_idx, y_idx] += 1
    return ar


def colorcode_ar_2d(ar, gradient):

    shape = ar.shape
    colors = numpy.zeros((shape[0], shape[1], 3), dtype=numpy.uint8)

    if numpy.amax(ar) != 0:
        for ix in range(shape[0]):
            for iy in range(shape[1]):
                r, g, b = gradient.get_color(ar[ix, iy])
                colors[ix, iy] = (r * 255, g * 255, b * 255)
    return colors


def colorcoded_ar_2d2png_string(color_ar):
    # Swap the axes of array so that the resulting PIL image comes out
    # oriented correctly.
    color_ar = numpy.swapaxes(color_ar, 0, 1)
    color_ar = numpy.flipud(color_ar)
    # Create a PNG image from the histogram
    im = Image.fromarray(color_ar)
    tmp = StringIO.StringIO()
    im.save(tmp, format='png')
    return 'data:image/png;base64,\n' + encodestring(tmp.getvalue())


class Histogram2dPlotter(RasterPlotterMixin):
    def __init__(self, x_seq, y_seq, *args, **kwargs):
        x_bins = kwargs.get('x_bins', 10)
        y_bins = kwargs.get('y_bins', 10)
        # First pass through data, find the range of values:
        hist_bbox = kwargs.get('hist_bbox', find_bounding_box(x_seq, y_seq))
        # Second pass trough the data to create the histogram.
        ar = bin_data_2d(x_seq, y_seq, x_bins, y_bins, hist_bbox)
        # Color code the data (on gray scale for now).
        max_val = numpy.amax(ar)
        min_val = 0
        gradient = kwargs.get('gradient',
                              RGBGradient((min_val, max_val), (0, 0, 1),
                              (1, 0, 0)))
        colors = colorcode_ar_2d(ar, gradient)
        # save the relevant information:
        self.gradient = gradient
        self.encoded_png = colorcoded_ar_2d2png_string(colors)
        self.img_bbox = hist_bbox
