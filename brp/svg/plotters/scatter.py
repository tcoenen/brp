'''
Implementation of scatter plots.
'''
import copy
from itertools import izip

import StringIO
from base64 import encodestring
from PIL import Image, ImageDraw

import brp.svg.colornames
from brp.svg.colornames import svg_color2rgba_color



from brp.svg.et_import import ET
from brp.svg.plotters.base import BasePlotter
from brp.core.bbox import find_bounding_box
from brp.svg.plotters.symbol import BaseSymbol

# DEBUGGING:
import sys


class FakeList(object):
    def __init__(self, something):
        self.payload = something

    def next(self):
        return self.payload

    def __getitem__(self, key):
        return self.payload

    def __iter__(self):
        return self


class ScatterPlotter(BasePlotter):
    '''
    Scatter plot, implements BasePlotter interface.

    Note: this second iteration should allow scatter plots to be drawn that
    allow higher dimensionality than just 2 (whithout reimplementing the
    scatter plot part).

    Mapping works as follows:
    args[0] -> X
    args[1] -> Y
    args[2] -> color via the provided gradient (befaults to black)
    args[3->n] -> shape via BaseSymbol subclass
    '''
    def __init__(self, *args, **kwargs):
        # Copy the datapoints.
        if len(args) == 1:
            self.datapoints = [[i for i in xrange(len(args[0]))]]
            self.datapoints.append(copy.copy(args[0]))
        else:
            N = len(args[0])
            for x in args:
                assert len(x) == N
            self.datapoints = copy.deepcopy(args)
        # Copy the color, possible gradient, links and symbol to use.
        self.gradient = kwargs.get('gradient', None)
        self.gradient_i = kwargs.get('gradient_i', None)
        self.colors = kwargs.get('colors', [])
        if self.colors:
            assert len(self.colors) == len(args[0])
        self.color = kwargs.get('color', 'black')
        self.links = kwargs.get('links', [])
        if self.links:
            assert len(self.links) == len(args[0])
        symbol_classes = kwargs.get('symbols', [])
        if not symbol_classes:
            symbol_classes = [kwargs.get('symbol', BaseSymbol)]
        self.symbols = [s(self.color) for s in symbol_classes]

    def prepare_bbox(self, data_bbox):
        '''Update bounding box with the data for this scatter plot.'''
        return find_bounding_box(self.datapoints[0], self.datapoints[1],
                                 data_bbox)

    def draw(self, root_element, x_transform, y_transform):
        '''Draw scatter plot.'''

        if self.links:
            L = self.links
        else:
            L = FakeList('')

        if self.gradient and self.gradient_i is not None:
            for i, datapoint in enumerate(izip(*self.datapoints)):
                for s in self.symbols:
                    s.draw(root_element, x_transform, y_transform, *datapoint,
                           color=self.gradient.get_css_color(
                           datapoint[self.gradient_i]), link=L[i])
        elif self.colors:
            for i, datapoint in enumerate(izip(*self.datapoints)):
                for s in self.symbols:
                    s.draw(root_element, x_transform, y_transform, *datapoint,
                           color=self.colors[i], link=L[i])
        else:
            root_element = ET.SubElement(root_element, 'g')
            root_element.set('stroke', self.color)
            root_element.set('fill', self.color)
            for i, datapoint in enumerate(izip(*self.datapoints)):
                for s in self.symbols:
                    s.draw(root_element, x_transform, y_transform, *datapoint,
                           link=L[i])

    def rdraw(self, root_element, x_transform, y_transform, svg_bbox):

        width = svg_bbox[2] - svg_bbox[0]
        height = svg_bbox[1] - svg_bbox[3]
        assert width > 0
        assert height > 0

        im = Image.new('RGBA', (width, height), (255, 255, 255, 0))
        imdraw = ImageDraw.Draw(im)

        # above should be hidden (not re-implemented in each subclass)
        if self.gradient and self.gradient_i is not None:
            for i, datapoint in enumerate(izip(*self.datapoints)):
                for s in self.symbols:
                    rgba_color = self.gradient.get_rgba_color(
                        datapoint[self.gradient_i])
                    s.rdraw(imdraw, x_transform, y_transform, *datapoint,
                            rgba_color=rgba_color)
        elif self.colors:
            for i, datapoint in enumerate(izip(*self.datapoints)):
                for s in self.symbols:
                    rgba_color = svg_color2rgba_color(self.colors[i])
                    s.rdraw(imdraw, x_transform, y_transform, *datapoint,
                            rgba_color=rgba_color)
        else:
            for datapoint in izip(*self.datapoints):
                rgba_color = svg_color2rgba_color(self.color)
                for s in self.symbols:
                    s.rdraw(imdraw, x_transform, y_transform, *datapoint,
                            rgba_color=rgba_color)
        # below should be hidden (not re-implemented in each subclass)

        tmp = StringIO.StringIO()
        im.save(tmp, format='png')
        encoded_png = 'data:image/png;base64,\n' + encodestring(tmp.getvalue())

        img = ET.SubElement(root_element, 'image')
        img.set('xlink:href', encoded_png)
        img.set('x', '%.2f' % min(svg_bbox[0], svg_bbox[2]))
        img.set('y', '%.2f' % min(svg_bbox[1], svg_bbox[3]))
        img.set('width', '%.2f' % width)
        img.set('height', '%.2f' % height)
        img.set('preserveAspectRatio', 'none')
