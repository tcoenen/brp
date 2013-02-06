'''
Implementation of LinePlots.
'''
from __future__ import division
from brp.svg.et_import import ET

from brp.svg.plotters.scatter import ScatterPlotter


class LinePlotter(ScatterPlotter):
    '''Line plot, implements BasePlotter interface.'''
    def __init__(self, *args, **kwargs):
        self.line_pattern = kwargs.get('linepattern', '')
        self.use_markers = kwargs.get('use_markers', True)

        super(LinePlotter, self).__init__(*args, **kwargs)

    def draw(self, root_element, x_transform, y_transform):
        '''Draw line plot.'''

        pl = ET.SubElement(root_element, 'polyline')
        pl.set('stroke', self.color)
        pl.set('fill', 'none')
        points = []
        for x, y in zip(self.datapoints[0], self.datapoints[1]):
            points.append("%.2f,%.2f" % (x_transform(x), y_transform(y)))
        pl.set('points', ' '.join(points))
        if self.line_pattern:
            pl.set('style', 'stroke-dasharray: %s' % self.line_pattern)

        if self.use_markers:
            super(LinePlotter, self).draw(root_element, x_transform,
                  y_transform)
