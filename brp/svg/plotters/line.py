'''
Implementation of LinePlots.
'''
from __future__ import division
import StringIO
from itertools import izip
from base64 import encodestring

from PIL import Image, ImageDraw

from brp.svg.et_import import ET
from brp.svg.plotters.scatter import ScatterPlotter
from brp.svg.colornames import svg_color2rgba_color


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

    def rdraw(self, root_element, x_transform, y_transform, svg_bbox):

        width = svg_bbox[2] - svg_bbox[0]
        height = svg_bbox[1] - svg_bbox[3]
        assert width > 0
        assert height > 0

        im = Image.new('RGBA', (width, height), (255, 255, 255, 0))
        imdraw = ImageDraw.Draw(im)
        rgba_color = svg_color2rgba_color(self.color)

        # above should be hidden (not re-implemented in each subclass)
        if len(self.datapoints) > 1:
            tmp = []
            for datapoint in izip(*self.datapoints):
                x = x_transform(datapoint[0])
                y = y_transform(datapoint[1])
                tmp.append(x)
                tmp.append(y)
            imdraw.line(tmp, fill=rgba_color, width=1)
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

        if self.use_markers:
            super(LinePlotter, self).rdraw(root_element, x_transform,
                                           y_transform, svg_bbox)
