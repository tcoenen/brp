'''
Implementation of the various symbols that show up in scatter and line plots.
'''
from __future__ import division
#from xml.sax.saxutils import escape

from brp.svg.et_import import ET
import math


class BaseSymbol(object):
    def __init__(self, *args, **kwargs):
        self.size = kwargs.get('size', 2)
        self.size = kwargs.get('radius', 2)
        self.link = kwargs.get('link', '')

    def draw_xy(self, root_element, x, y, *datapoint, **kwargs):
        link = kwargs.get('link', self.link)

        if link:
            root_element = ET.SubElement(root_element, 'a')
            root_element.set('xlink:href', link)

        p = ET.SubElement(root_element, 'circle')
        p.set('cx', '%.2f' % x)
        p.set('cy', '%.2f' % y)
        p.set('r', '%.2f' % self.size)

        if 'color' in kwargs:
            p.set('fill', kwargs['color'])

    def draw(self, root_element, x_transform, y_transform, *datapoint,
             **kwargs):
        nx = x_transform(datapoint[0])
        ny = y_transform(datapoint[1])
        self.draw_xy(root_element, nx, ny, *datapoint, **kwargs)

    def rdraw(self, imdraw, x_transform, y_transform, *datapoint, **kwargs):
        nx = x_transform(datapoint[0])
        ny = y_transform(datapoint[1])

        rgba_color = kwargs.get('rgba_color', (0, 0, 0, 255))
        # see the PIL documentation of ImageDraw module for what follows:
        X = 1
        bbox = [
            nx - (self.size),
            ny - (self.size),
            nx + (self.size) + X,
            ny + (self.size) + X,
        ]
        imdraw.ellipse(bbox, fill=rgba_color, outline=rgba_color)


class NoSymbol(BaseSymbol):
    def __init__(self, *args, **kwargs):
        pass

    def draw_xy(self, root_element, x, y, *datapoint, **kwargs):
        pass

    def draw(self, root_element, x_transform, y_transform, *datapoint,
             **kwargs):
        pass

    def rdraw(self, imdraw, x_transform, y_transform, *datapoint, **kwargs):
        pass


class SquareSymbol(BaseSymbol):
    def draw_xy(self, root_element, x, y, *datapoint, **kwargs):
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

        if 'color' in kwargs:
            p.set('fill', kwargs['color'])

    def rdraw(self, imdraw, x_transform, y_transform, *datapoint, **kwargs):
        nx = x_transform(datapoint[0])
        ny = y_transform(datapoint[1])

        rgba_color = kwargs.get('rgba_color', (0, 0, 0, 255))
        size = self.size

        rect = [
            (nx - size, ny - size),
            (nx - size, ny + size),
            (nx + size, ny + size),
            (nx + size, ny - size)
        ]
        imdraw.polygon(rect, fill=rgba_color)


class VerticalErrorBarSymbol(BaseSymbol):
    def draw_xy(self, root_element, x, y, *datapoint, **kwargs):
        miny = kwargs.get('miny', y - 7)
        maxy = kwargs.get('maxy', y + 7)

        l1 = ET.SubElement(root_element, 'line')
        l1.set('x1', '%.2f' % x)
        l1.set('x2', '%.2f' % x)
        l1.set('y1', '%.2f' % maxy)
        l1.set('y2', '%.2f' % miny)

        # Add 'serifs' to error bar.
        l2 = ET.SubElement(root_element, 'line')
        l2.set('x1', '%.2f' % (x - 3))
        l2.set('x2', '%.2f' % (x + 3))
        l2.set('y1', '%.2f' % maxy)
        l2.set('y2', '%.2f' % maxy)

        l3 = ET.SubElement(root_element, 'line')
        l3.set('x1', '%.2f' % (x - 3))
        l3.set('x2', '%.2f' % (x + 3))
        l3.set('y1', '%.2f' % miny)
        l3.set('y2', '%.2f' % miny)

        if 'color' in kwargs:
            l1.set('stroke', kwargs['color'])
            l2.set('stroke', kwargs['color'])
            l3.set('stroke', kwargs['color'])

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
    def draw_xy(self, root_element, x, y, *datapoint, **kwargs):
        minx = kwargs.get('minx', x - 7)
        maxx = kwargs.get('maxx', x + 7)

        l1 = ET.SubElement(root_element, 'line')
        l1.set('x1', '%.2f' % maxx)
        l1.set('x2', '%.2f' % minx)
        l1.set('y1', '%.2f' % y)
        l1.set('y2', '%.2f' % y)

        # Add 'serifs' to error bar.
        l2 = ET.SubElement(root_element, 'line')
        l2.set('x1', '%.2f' % maxx)
        l2.set('x2', '%.2f' % maxx)
        l2.set('y1', '%.2f' % (y - 3))
        l2.set('y2', '%.2f' % (y + 3))

        l3 = ET.SubElement(root_element, 'line')
        l3.set('x1', '%.2f' % minx)
        l3.set('x2', '%.2f' % minx)
        l3.set('y1', '%.2f' % (y + 3))
        l3.set('y2', '%.2f' % (y - 3))

        if 'color' in kwargs:
            l1.set('stroke', kwargs['color'])
            l2.set('stroke', kwargs['color'])
            l3.set('stroke', kwargs['color'])

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
        self.line_pattern = kwargs.get('linepattern', '')

    def draw_xy(self, root_element, x, y, *datapoint, **kwargs):
        l = ET.SubElement(root_element, 'line')
        l.set('x1', '%.2f' % (x - 15))
        l.set('x2', '%.2f' % (x + 15))
        l.set('y1', '%.2f' % y)
        l.set('y2', '%.2f' % y)
        if self.line_pattern:
            l.set('style', 'stroke-dasharray:%s' % (self.line_pattern))

        if 'color' in kwargs:
            l.set('stroke', kwargs['color'])


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
        h1.set('stroke-width', '3')

        h2 = ET.SubElement(root_element, 'line')
        h2.set('x1', '%.2f' % x)
        h2.set('y1', '%.2f' % y)
        h2.set('x2', '%.2f' % (x + ra_pointer_dx))
        h2.set('y2', '%.2f' % (y + ra_pointer_dy))

        if 'color' in kwargs:
            h1.set('stroke', kwargs['color'])
            h2.set('stroke', kwargs['color'])

    def rdraw(self, imdraw, x_transform, y_transform, *datapoint, **kwargs):
        ra = datapoint[2]
        dec = datapoint[3]

        nx = x_transform(datapoint[0])
        ny = y_transform(datapoint[1])

        rgba_color = kwargs.get('rgba_color', (0, 0, 0, 255))
        # see the PIL documentation of ImageDraw module for what follows:
        DEC_SIZE = 7
        RA_SIZE = 12
        # following is wrong:
        dec_pointer_dx = math.cos(math.pi * dec / 180) * DEC_SIZE
        dec_pointer_dy = -math.sin(math.pi * dec / 180) * DEC_SIZE
        # following is ok:
        ra_pointer_dx = math.sin(ra * math.pi / 12) * RA_SIZE
        ra_pointer_dy = -math.cos(ra * math.pi / 12) * RA_SIZE

        imdraw.line([nx, ny, nx + dec_pointer_dx, ny + dec_pointer_dy],
                    fill=rgba_color, width=3)
        imdraw.line([nx, ny, nx + ra_pointer_dx, ny + ra_pointer_dy],
                    fill=rgba_color, width=1)


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
        d.set('fill', 'none')
        d.set('stroke-width', '2')

        if 'color' in kwargs:
            d.set('stroke', kwargs['color'])


class RasterDebugSymbol(object):
    def __init__(self, *args, **kwargs):
        '''Shows (mis-)alignment of PNG (raster) and SVG coordinates.'''
        self.size = kwargs.get('size', 2)
        self.size = kwargs.get('radius', 5)
        self.link = kwargs.get('link', '')

    def draw_xy(self, root_element, x, y, *datapoint, **kwargs):
        link = kwargs.get('link', self.link)

        if link:
            root_element = ET.SubElement(root_element, 'a')
            root_element.set('xlink:href', link)

        p = ET.SubElement(root_element, 'circle')
        p.set('cx', '%.2f' % x)
        p.set('cy', '%.2f' % y)
        p.set('r', '%.2f' % self.size)
        p.set('fill', 'none')
        p.set('stroke', 'lime')

    def draw(self, root_element, x_transform, y_transform, *datapoint,
             **kwargs):
        nx = x_transform(datapoint[0])
        ny = y_transform(datapoint[1])
        self.draw_xy(root_element, nx, ny, *datapoint, **kwargs)

    def rdraw(self, imdraw, x_transform, y_transform, *datapoint, **kwargs):
        nx = x_transform(datapoint[0])
        ny = y_transform(datapoint[1])

        rgba_color = kwargs.get('rgba_color', (0, 255, 0, 255))
        imdraw.point((nx, ny), fill=rgba_color)

        size = 5
        bbox = [
            nx - size,
            ny - size,
            nx + size,
            ny + size,
        ]
        imdraw.ellipse(bbox, fill=None, outline=rgba_color)
