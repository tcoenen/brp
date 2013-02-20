'''
Implementation of scatter plots.
'''
import copy
from itertools import izip

from brp.svg.plotters.base import BasePlotter
from brp.core.bbox import find_bounding_box
from brp.svg.plotters.symbol import BaseSymbol
# Temporary imports to allow BaseSymbol2 to work
from brp.svg.et_import import ET


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
            for i, datapoint in enumerate(izip(*self.datapoints)):
                for s in self.symbols:
                    s.draw(root_element, x_transform, y_transform, *datapoint,
                           color=self.color, link=L[i])
