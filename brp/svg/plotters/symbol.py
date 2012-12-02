from __future__ import division
from xml.sax.saxutils import escape

from brp.svg.et_import import ET
import math
import sys

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

    def draw(self, root_element, x_transform, y_transform, *datapoint, **kwargs): 
        nx = x_transform(datapoint[0])
        ny = y_transform(datapoint[1])
        self.draw_xy(root_element, nx, ny, *datapoint, **kwargs)


class NoSymbol(BaseSymbol):
    def __init__(self, *args, **kwargs):
        pass
    def draw_xy(self, root_element, x, y, *datapoint, **kwargs):
        pass
    def draw(self, root_element, x_transform, y_transform, *datapoint, **kwargs):
        pass


class SquareSymbol(BaseSymbol):
    def draw_xy(self, root_element, x, y, *datapoint, **kwargs):
        color = kwargs.get('color', self.color)
        hover_text = kwargs.get('hover_text', '')
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


# All the Error*Symbol classes need a little refactor.
# The way I use draw_xy does not match the rest of the symbols.
class VerticalErrorBarSymbol(BaseSymbol):
    def __init__(self, *args, **kwargs):
        self.color = kwargs.get('color', 'black')

    def draw_xy(self, root_element, x, y, *datapoint, **kwargs):
        # TODO : add 'serifs'
        color = kwargs.get('color', self.color)
        l1 = ET.SubElement(root_element, 'line')
        l1.set('x1', '%.2f' % x)
        l1.set('x2', '%.2f' % x)
        l1.set('y1', '%.2f' % (y + 7))
        l1.set('y2', '%.2f' % (y - 7))
        l1.set('stroke', color)

        l2 = ET.SubElement(root_element, 'line')
        l2.set('x1', '%.2f' % (x - 3))
        l2.set('x2', '%.2f' % (x + 3))
        l2.set('y1', '%.2f' % (y + 7))
        l2.set('y2', '%.2f' % (y + 7))
        l2.set('stroke', color)

        l3 = ET.SubElement(root_element, 'line')
        l3.set('x1', '%.2f' % (x - 3))
        l3.set('x2', '%.2f' % (x + 3))
        l3.set('y1', '%.2f' % (y - 7))
        l3.set('y2', '%.2f' % (y - 7))
        l3.set('stroke', color)

    def draw(self, root_element, x_transform, y_transform, *datapoint, **kwargs):
        color = kwargs.get('color', self.color)
        x = datapoint[0]
        y = datapoint[1]
        err_y = kwargs.get('err_y', [])
        tx = x_transform(x)
        ty = y_transform(y)

        if err_y:
            my = y - err_y[0]
            My = y + err_y[1]
            tmy = y_transform(my)
            tMy = y_transform(My)
            l1 = ET.SubElement(root_element, 'line')
            l1.set('x1', '%.2f' % tx)
            l1.set('x2', '%.2f' % tx)
            l1.set('y1', '%.2f' % tmy)
            l1.set('y2', '%.2f' % tMy)
            l1.set('stroke', color)
            # TODO : add 'serifs'
            l2 = ET.SubElement(root_element, 'line')
            l2.set('x1', '%.2f' % (tx - 3))
            l2.set('x2', '%.2f' % (tx + 3))
            l2.set('y1', '%.2f' % tmy)
            l2.set('y2', '%.2f' % tmy)
            l2.set('stroke', color)
            l3 = ET.SubElement(root_element, 'line')
            l3.set('x1', '%.2f' % (tx - 3))
            l3.set('x2', '%.2f' % (tx + 3))
            l3.set('y1', '%.2f' % tMy)
            l3.set('y2', '%.2f' % tMy)
            l3.set('stroke', color)


class HorizontalErrorBarSymbol(BaseSymbol):
    def __init__(self, *args, **kwargs):
        self.color = kwargs.get('color', 'black')

    def draw_xy(self, root_element, x, y, *datapoint, **kwargs):
        color = kwargs.get('color', self.color)
        # TODO : add 'serifs'
        l1 = ET.SubElement(root_element, 'line')
        l1.set('x1', '%.2f' % (x + 7))
        l1.set('x2', '%.2f' % (x - 7))
        l1.set('y1', '%.2f' % y)
        l1.set('y2', '%.2f' % y)
        l1.set('stroke', color)

        l2 = ET.SubElement(root_element, 'line')
        l2.set('x1', '%.2f' % (x + 7))
        l2.set('x2', '%.2f' % (x + 7))
        l2.set('y1', '%.2f' % (y - 3))
        l2.set('y2', '%.2f' % (y + 3))
        l2.set('stroke', color)

        l3 = ET.SubElement(root_element, 'line')
        l3.set('x1', '%.2f' % (x - 7))
        l3.set('x2', '%.2f' % (x - 7))
        l3.set('y1', '%.2f' % (y + 3))
        l3.set('y2', '%.2f' % (y - 3))
        l3.set('stroke', color)

    def draw(self, root_element, x_transform, y_transform, *datapoint, **kwargs):
        color = kwargs.get('color', self.color)
        x = datapoint[0]
        y = datapoint[1]

        err_x = kwargs.get('err_x', [])
        tx = x_transform(x)
        ty = y_transform(y)

        if err_x: # assume the general case of asymmetric errors
            mx = x - err_x[0]
            Mx = x + err_x[1]
            tmx = x_transform(mx)
            tMx = x_transform(Mx)
            l1 = ET.SubElement(root_element, 'line')
            l1.set('x1', '%.2f' % tmx)
            l1.set('x2', '%.2f' % tMx)
            l1.set('y1', '%.2f' % ty)
            l1.set('y2', '%.2f' % ty)
            l1.set('stroke', color)
            # TODO : add 'serifs'
            l2 = ET.SubElement(root_element, 'line')
            l2.set('x1', '%.2f' % tmx)
            l2.set('x2', '%.2f' % tmx)
            l2.set('y1', '%.2f' % (ty - 3))
            l2.set('y2', '%.2f' % (ty + 3))
            l2.set('stroke', color)
            l3 = ET.SubElement(root_element, 'line')
            l3.set('x1', '%.2f' % tMx)
            l3.set('x2', '%.2f' % tMx)
            l3.set('y1', '%.2f' % (ty - 3))
            l3.set('y2', '%.2f' % (ty + 3))
            l3.set('stroke', color)
          

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

#        l1 = ET.SubElement(root_element, 'line')
#        l1.set('x1', '%.2f' % x_transform(self.x))
#        l1.set('y1', '%.2f' % (y_transform(self.y) - 0.7 * rh))
#        l1.set('x2', '%.2f' % x_transform(self.x))
#        l1.set('y2', '%.2f' % (y_transform(self.y) - 0.3 * rh))
#        l1.set('stroke', self.color)
#        l1.set('stroke-width', '2')
#
#        l1 = ET.SubElement(root_element, 'line')
#        l1.set('x1', '%.2f' % x_transform(self.x))
#        l1.set('y1', '%.2f' % (y_transform(self.y) + 0.3 * rh))
#        l1.set('x2', '%.2f' % x_transform(self.x))
#        l1.set('y2', '%.2f' % (y_transform(self.y) + 0.7 * rh))
#        l1.set('stroke', self.color)
#        l1.set('stroke-width', '2')
#        
#        l2 = ET.SubElement(root_element, 'line')
#        l2.set('x1', '%.2f' % (x_transform(self.x) - 0.7 * rw))
#        l2.set('y1', '%.2f' % y_transform(self.y))
#        l2.set('x2', '%.2f' % (x_transform(self.x) - 0.3 * rw))
#        l2.set('y2', '%.2f' % y_transform(self.y))
#        l2.set('stroke', self.color)
#        l2.set('stroke-width', '2')
#
#        l2 = ET.SubElement(root_element, 'line')
#        l2.set('x1', '%.2f' % (x_transform(self.x) + 0.3 * rw))
#        l2.set('y1', '%.2f' % y_transform(self.y))
#        l2.set('x2', '%.2f' % (x_transform(self.x) + 0.7 * rw))
#        l2.set('y2', '%.2f' % y_transform(self.y))
#        l2.set('stroke', self.color)
#        l2.set('stroke-width', '2')
        
#        d = ET.SubElement(root_element, 'rect')
#        d.set('x', '%.2f' % (x_transform(self.x) - 0.5 * rw))
#        d.set('y', '%.2f' % (y_transform(self.y) - 0.5 * rh))
#        d.set('width', '%.2f' % rw)
#        d.set('height', '%.2f' % rh)
#        d.set('stroke', self.color)
#        d.set('fill', 'none')
#        d.set('stroke-width', '2')
        W = 10
        w = W/2
        H = 10
        h = H/2

        d = ET.SubElement(root_element, 'rect')
        d.set('x', '%.2f' % (x - w))
        d.set('y', '%.2f' % (y - h))
        d.set('width', '%.2f' % W)
        d.set('height', '%.2f' % H)
        d.set('stroke', self.color)
        d.set('fill', 'none')
        d.set('stroke-width', '2')

