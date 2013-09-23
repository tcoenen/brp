'''
Refactor of the 2d histogramming in brp.
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
from brp.svg.plotters.base import BasePlotter




def get_data_url(ar, gradient):
    '''
    Color code array according to gradient and turn into data url.
    '''
    colors = colorcode(ar, gradient)
    img = make_image(colors)
    buffer = StringIO.StringIO()
    img.save(buffer, format='png')

    return 'data:image/png;base64,\n' + encodestring(buffer.getvalue())


def make_image(colors):
    '''
    Turn color coded array into a correctly oriented PIL image.
    '''
    # change orientation so that the PNG comes out right
    colors = numpy.swapaxes(colors, 0, 1)
    colors = numpy.flipud(colors)
    # Create a PNG image from the histogram
    return Image.fromarray(colors)


def colorcode(ar, gradient):
    '''
    Color code a 2d array according to the provided gradient.
    '''
    assert len(ar.shape) == 2
    shape = ar.shape
    colors = numpy.zeros((shape[0], shape[1], 3), dtype=numpy.uint8)

    for ix in range(shape[0]):
        for iy in range(shape[1]):
            r, g, b = gradient.get_color(ar[ix, iy])
            colors[ix, iy] = (r * 255, g * 255, b * 255)
    return colors


def bin_data_2d(x_seq, y_seq, x_bins, y_bins, hist_bbox):
    '''
    Create a 2d histogram.
    '''
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


class Array2dPlotter(RasterPlotterMixin):
    def __init__(self, ar, ar_bbox, *args, **kwargs):
        self.array = ar
        self.img_bbox = ar_bbox
        self.gradient = kwargs.get('gradient', None)

    # TODO: check the following for switched x and y
    def collapse_x(self, *args, **kwargs):
        dw = (self.img_bbox[3] - self.img_bbox[1]) / self.array.shape[1]
        # the + 0.5 below because we want the mid points
        lx = self.array.sum(axis=0)
        ly = [self.img_bbox[1] + (i + 0.5) * dw for i in
              range(self.array.shape[1])]

        return lx, ly

    def collapse_y(self, *args, **kwargs):
        dh = (self.img_bbox[2] - self.img_bbox[0]) / self.array.shape[0]

        lx = [self.img_bbox[0] + (i + 0.5) * dh for i in
              range(self.array.shape[0])]
        ly = self.array.sum(axis=1)

        return lx, ly

    def get_gradient(self):
        if self.gradient is None:
            interval = (numpy.amin(self.array), numpy.amax(self.array))
            return RGBGradient(interval, (0, 0, 1), (1, 0, 0))
        else:
            return self.gradient

    def draw(self, *args, **kwargs):
        self.encoded_png = get_data_url(self.array, self.get_gradient())
        super(Array2dPlotter, self).draw(*args, **kwargs)


class Histogram2dPlotter(Array2dPlotter):
    def __init__(self, x_seq, y_seq, *args, **kwargs):
        x_bins = kwargs.get('x_bins', 10)
        y_bins = kwargs.get('y_bins', 10)
        # First pass through data, find the range of values:
        bbox = kwargs.get('hist_bbox', find_bounding_box(x_seq, y_seq))
        # bounding box needs stretching!
        self.img_bbox = bbox
        # Second pass trough the data to create the histogram.
        self.array = bin_data_2d(x_seq, y_seq, x_bins, y_bins, bbox)
        # Color code the data (on gray scale for now).
        # save the relevant information:
        self.gradient = kwargs.get('gradient', None)
