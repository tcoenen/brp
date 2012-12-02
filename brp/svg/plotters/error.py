from __future__ import division

from itertools import izip

from brp.svg.et_import import ET
from brp.svg.plotters.base import BasePlotter
from brp.svg.plotters.scatter import ScatterPlotter, FakeList
from brp.svg.plotters.symbol import BaseSymbol, HorizontalErrorBarSymbol
from brp.svg.plotters.symbol import VerticalErrorBarSymbol


class ErrorPlotter(ScatterPlotter):
    def __init__(self, *args, **kwargs):
        '''Plot 2d scatter plot with errors (can do asymmetrical ones).'''
        super(ErrorPlotter, self).__init__(*args, **kwargs)
        N = len(self.datapoints[0])
        self.err_x = kwargs.get('err_x', [(0, 0) for i in xrange(N)])
        self.err_y = kwargs.get('err_y', [(0, 0) for i in xrange(N)])
        self.symbols.extend([HorizontalErrorBarSymbol(), VerticalErrorBarSymbol()])

    def prepare_bbox(self, bbox):
        '''Update bounding box taking into account also the errors.''' 
        if not bbox:
            bbox = [self.datapoints[0][0], self.datapoints[1][0], 
                self.datapoints[0][0], self.datapoints[1][0]] 
            # bounding boxes are like : [xmin, ymin, xmax, ymax]
        else:
            bbox = list(bbox)
        for x, y, ex, ey in zip(self.datapoints[0], self.datapoints[1], self.err_x, self.err_y):
            if x - ex[0] < bbox[0]:
                bbox[0] = x - ex[0]
            elif x + ex[1] > bbox[2]: 
                bbox[2] = x + ex[1]
            if y - ey[0] < bbox[1]: 
                bbox[1] = y - ey[0]
            elif y + ey[1] > bbox[3]: 
                bbox[3] = y + ey[1]
        return tuple(bbox)

    def draw(self, root_element, x_transform, y_transform):

        if self.links:
            L = self.links
        else:
            L = FakeList('')

        if self.gradient and self.gradient_i != None:
            for i, datapoint in enumerate(izip(*self.datapoints)):
                color = self.gradient.get_css_color(datapoint[self.gradient_i])
                for s in self.symbols:
                    s.draw(root_element, x_transform, y_transform, *datapoint,
                        color=color, link = L[i], err_x=self.err_x, err_y=self.err_y)
        elif self.colors:
            for i, datapoint in enumerate(izip(*self.datapoints)):
                color = color[i]
                for s in self.symbols:
                    s.draw(root_element, x_transform, y_transform, *datapoint,
                        color=color, link = L[i], err_x=self.err_x[i], err_y=self.err_y[i])
        else:
            for i, datapoint in enumerate(izip(*self.datapoints)):
                for s in self.symbols:
                    s.draw(root_element, x_transform, y_transform, *datapoint,
                        color=self.color, link = L[i], err_x=self.err_x[i], err_y=self.err_y[i])

