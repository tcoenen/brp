from __future__ import division

from itertools import izip
import StringIO
from base64 import encodestring

from PIL import Image, ImageDraw

from brp.svg.et_import import ET
from brp.svg.plotters.scatter import ScatterPlotter, FakeList
from brp.svg.plotters.symbol import HorizontalErrorBarSymbol
from brp.svg.plotters.symbol import VerticalErrorBarSymbol
from brp.svg.colornames import svg_color2rgba_color


class ErrorPlotter(ScatterPlotter):
    def __init__(self, *args, **kwargs):
        '''Plot 2d scatter plot with errors (can do asymmetrical ones).'''
        super(ErrorPlotter, self).__init__(*args, **kwargs)
        N = len(self.datapoints[0])
        self.err_x = kwargs.get('err_x', [(0, 0) for i in xrange(N)])
        self.err_y = kwargs.get('err_y', [(0, 0) for i in xrange(N)])
        self.symbols.extend([HorizontalErrorBarSymbol(),
                            VerticalErrorBarSymbol()])

    def prepare_bbox(self, bbox):
        '''Update bounding box taking into account also the errors.'''
        if not bbox:
            bbox = [self.datapoints[0][0], self.datapoints[1][0],
                    self.datapoints[0][0], self.datapoints[1][0]]
            # bounding boxes are like : [xmin, ymin, xmax, ymax]
        else:
            bbox = list(bbox)
        for x, y, ex, ey in zip(self.datapoints[0], self.datapoints[1],
                                self.err_x, self.err_y):
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

        if self.gradient and self.gradient_i is not None:
            for i, datapoint in enumerate(izip(*self.datapoints)):
                color = self.gradient.get_css_color(datapoint[self.gradient_i])
                for s in self.symbols:
                    s.draw(root_element, x_transform, y_transform, *datapoint,
                           color=color, link=L[i], err_x=self.err_x,
                           err_y=self.err_y)
        elif self.colors:
            for i, datapoint in enumerate(izip(*self.datapoints)):
                color = self.colors[i]
                for s in self.symbols:
                    s.draw(root_element, x_transform, y_transform, *datapoint,
                           color=color, link=L[i], err_x=self.err_x[i],
                           err_y=self.err_y[i])
        else:
            root_element = ET.SubElement(root_element, 'g')
            root_element.set('stroke', self.color)
            root_element.set('fill', self.color)
            for i, datapoint in enumerate(izip(*self.datapoints)):
                for s in self.symbols:
                    s.draw(root_element, x_transform, y_transform, *datapoint,
                           link=L[i], err_x=self.err_x[i], err_y=self.err_y[i])

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
                rgba_color = self.gradient.get_rgba_color(
                    datapoint[self.gradient_i])
                for s in self.symbols:
                    s.draw(imdraw, x_transform, y_transform, *datapoint,
                           err_x=self.err_x, err_y=self.err_y,
                           rgba_color=rgba_color)
        elif self.colors:
            for i, datapoint in enumerate(izip(*self.datapoints)):
                rgba_color = svg_color2rgba_color(self.colors[i])
                for s in self.symbols:
                    s.rdraw(imdraw, x_transform, y_transform, *datapoint,
                            err_x=self.err_x[i], err_y=self.err_y[i],
                            rgba_color=rgba_color)
        else:
            rgba_color = svg_color2rgba_color(self.color)
            for i, datapoint in enumerate(izip(*self.datapoints)):
                for s in self.symbols:
                    s.rdraw(imdraw, x_transform, y_transform, *datapoint,
                            err_x=self.err_x[i], err_y=self.err_y[i],
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
