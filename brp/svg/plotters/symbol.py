'''
Implementation of the various symbols that show up in scatter and line plots.
'''
from __future__ import division
#from xml.sax.saxutils import escape

from brp.svg.et_import import ET
import math


class BaseSymbol(object):
    def __init__(self, *args, **kwargs):
        self.color = kwargs.get('color', 'black')
        self.size = kwargs.get('size', 2)
        self.size = kwargs.get('radius', 2)
        self.link = kwargs.get('link', '')

    def draw_xy(self, root_element, x, y, *datapoint, **kwargs):
        color = kwargs.get('color', self.color)
        link = kwargs.get('link', self.link)

        if link:
            root_element = ET.SubElement(root_element, 'a')
            root_element.set('xlink:href', link)

        p = ET.SubElement(root_element, 'circle')
        p.set('cx', '%.2f' % x)
        p.set('cy', '%.2f' % y)
        p.set('r', '%.2f' % self.size)
        p.set('fill', color)

    def draw(self, root_element, x_transform, y_transform, *datapoint,
             **kwargs):
        nx = x_transform(datapoint[0])
        ny = y_transform(datapoint[1])
        self.draw_xy(root_element, nx, ny, *datapoint, **kwargs)


class NoSymbol(BaseSymbol):
    def __init__(self, *args, **kwargs):
        pass

    def draw_xy(self, root_element, x, y, *datapoint, **kwargs):
        pass

    def draw(self, root_element, x_transform, y_transform, *datapoint,
             **kwargs):
        pass


class SquareSymbol(BaseSymbol):
    def draw_xy(self, root_element, x, y, *datapoint, **kwargs):
        color = kwargs.get('color', self.color)
        size = kwargs.get('size', self.size)
        link = kwargs.get('link', self.link)

        if link:
            root_element = ET.SubElement(root_element, 'a')
            root_element.set('xlink:href', link)

        p = ET.SubElement(root_element, 'rect')
        p.set('x', '%.2f' % (x - size))
        p.set('y', '%.2f' % (y - size))
        p.set('width', '%.2f' % (2 * size))
        p.set('height', '%.2f' % (2 * size))
        p.set('fill', color)


class VerticalErrorBarSymbol(BaseSymbol):
    def __init__(self, *args, **kwargs):
        self.color = kwargs.get('color', 'black')

    def draw_xy(self, root_element, x, y, *datapoint, **kwargs):
        color = kwargs.get('color', self.color)

        miny = kwargs.get('miny', y - 7)
        maxy = kwargs.get('maxy', y + 7)

        l1 = ET.SubElement(root_element, 'line')
        l1.set('x1', '%.2f' % x)
        l1.set('x2', '%.2f' % x)
        l1.set('y1', '%.2f' % maxy)
        l1.set('y2', '%.2f' % miny)
        l1.set('stroke', color)

        # Add 'serifs' to error bar.
        l2 = ET.SubElement(root_element, 'line')
        l2.set('x1', '%.2f' % (x - 3))
        l2.set('x2', '%.2f' % (x + 3))
        l2.set('y1', '%.2f' % maxy)
        l2.set('y2', '%.2f' % maxy)
        l2.set('stroke', color)

        l3 = ET.SubElement(root_element, 'line')
        l3.set('x1', '%.2f' % (x - 3))
        l3.set('x2', '%.2f' % (x + 3))
        l3.set('y1', '%.2f' % miny)
        l3.set('y2', '%.2f' % miny)
        l3.set('stroke', color)

    def draw(self, root_element, x_transform, y_transform, *datapoint,
             **kwargs):

        tx = x_transform(datapoint[0])
        ty = y_transform(datapoint[1])
        # Should not be called without error.
        err_y = kwargs['err_y']
        # Assumes the general case of assymetric error bars.
        tmy = y_transform(datapoint[1] - err_y[0])
        tMy = y_transform(datapoint[1] + err_y[1])

        self.draw_xy(root_element, tx, ty, *datapoint, miny=tmy, maxy=tMy,
                     **kwargs)


class HorizontalErrorBarSymbol(BaseSymbol):
    def __init__(self, *args, **kwargs):
        self.color = kwargs.get('color', 'black')

    def draw_xy(self, root_element, x, y, *datapoint, **kwargs):
        color = kwargs.get('color', self.color)

        minx = kwargs.get('minx', x - 7)
        maxx = kwargs.get('maxx', x + 7)

        l1 = ET.SubElement(root_element, 'line')
        l1.set('x1', '%.2f' % maxx)
        l1.set('x2', '%.2f' % minx)
        l1.set('y1', '%.2f' % y)
        l1.set('y2', '%.2f' % y)
        l1.set('stroke', color)

        # Add 'serifs' to error bar.
        l2 = ET.SubElement(root_element, 'line')
        l2.set('x1', '%.2f' % maxx)
        l2.set('x2', '%.2f' % maxx)
        l2.set('y1', '%.2f' % (y - 3))
        l2.set('y2', '%.2f' % (y + 3))
        l2.set('stroke', color)

        l3 = ET.SubElement(root_element, 'line')
        l3.set('x1', '%.2f' % minx)
        l3.set('x2', '%.2f' % minx)
        l3.set('y1', '%.2f' % (y + 3))
        l3.set('y2', '%.2f' % (y - 3))
        l3.set('stroke', color)

    def draw(self, root_element, x_transform, y_transform, *datapoint,
             **kwargs):

        tx = x_transform(datapoint[0])
        ty = y_transform(datapoint[1])
        # Should not be called without error.
        err_x = kwargs['err_x']
        # Assumes the general case of assymetric error bars.
        tmx = x_transform(datapoint[0] - err_x[0])
        tMx = x_transform(datapoint[0] + err_x[1])

        self.draw_xy(root_element, tx, ty, *datapoint, minx=tmx, maxx=tMx,
                     **kwargs)


class LineSymbol(BaseSymbol):
    def __init__(self, *args, **kwargs):
        self.color = kwargs.get('color', 'black')
        self.line_pattern = kwargs.get('linepattern', '')

    def draw_xy(self, root_element, x, y, *datapoint, **kwargs):
        color = kwargs.get('color', self.color)
        l = ET.SubElement(root_element, 'line')
        l.set('x1', '%.2f' % (x - 15))
        l.set('x2', '%.2f' % (x + 15))
        l.set('y1', '%.2f' % y)
        l.set('y2', '%.2f' % y)
        l.set('stroke', color)
        if self.line_pattern:
            l.set('style', 'stroke-dasharray:%s' % (self.line_pattern))


class RADECSymbol(BaseSymbol):
    '''
    Plot the Right Ascension and Declination as the hands on a clock.

    Thin long hand is RA, moves over 360 degrees for 24 hours.
    Thick short hand is DEC, moves over 180 degrees for 180 degrees in
    declination.

    The 3rd and 4th entry in the datapoint tuple are mapped to respectively
    Right Ascension and Declination.
    '''
    def draw_xy(self, root_element, x, y, *datapoint, **kwargs):
        ra = datapoint[2]
        dec = datapoint[3]

        color = kwargs.get('color', self.color)
        link = kwargs.get('link', '')

        DEC_SIZE = 7
        RA_SIZE = 12
        # following is wrong:
        dec_pointer_dx = math.cos(math.pi * dec / 180) * DEC_SIZE
        dec_pointer_dy = -math.sin(math.pi * dec / 180) * DEC_SIZE
        # following is ok:
        ra_pointer_dx = math.sin(ra * math.pi / 12) * RA_SIZE
        ra_pointer_dy = -math.cos(ra * math.pi / 12) * RA_SIZE

        if link:
            root_element = ET.SubElement(root_element, 'a')
            root_element.set('xlink:href', link)

        h1 = ET.SubElement(root_element, 'line')
        h1.set('x1', '%.2f' % x)
        h1.set('y1', '%.2f' % y)
        h1.set('x2', '%.2f' % (x + dec_pointer_dx))
        h1.set('y2', '%.2f' % (y + dec_pointer_dy))
        h1.set('stroke', color)
        h1.set('stroke-width', '3')

        h2 = ET.SubElement(root_element, 'line')
        h2.set('x1', '%.2f' % x)
        h2.set('y1', '%.2f' % y)
        h2.set('x2', '%.2f' % (x + ra_pointer_dx))
        h2.set('y2', '%.2f' % (y + ra_pointer_dy))
        h2.set('stroke', color)


class CrossHairSymbol(BaseSymbol):
    def draw_xy(self, root_element, x, y, *datapoint, **kwargs):
        # only draw if the self.x and self.y lie within the data_bbox

        W = 10
        w = W / 2
        H = 10
        h = H / 2

        d = ET.SubElement(root_element, 'rect')
        d.set('x', '%.2f' % (x - w))
        d.set('y', '%.2f' % (y - h))
        d.set('width', '%.2f' % W)
        d.set('height', '%.2f' % H)
        d.set('stroke', self.color)
        d.set('fill', 'none')
        d.set('stroke-width', '2')
