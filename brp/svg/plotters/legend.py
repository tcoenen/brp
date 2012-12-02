from __future__ import division
from brp.svg.et_import import ET
import copy
from xml.sax.saxutils import escape

from brp.svg.plotters.base import BasePlotter
from brp.svg.plotters.symbol import BaseSymbol
from brp.svg.constants import AXIS_SIZE

TOPLEFT = 0
TOPRIGHT = 1
BOTTOMLEFT = 2
BOTTOMRIGHT = 3
UNDER_PLOT = 4

LEGEND_FONT_SIZE = 12

class LegendPlotter(BasePlotter):
    def __init__(self, position=BOTTOMRIGHT):
        self.entries = []
        self.position = position

    def add_entry(self, text, **kwargs):
        symbols = kwargs.get('symbols', [BaseSymbol])
        color = kwargs.get('color', 'black')
        linepattern = kwargs.get('linepattern', '')
        symbol_kwargs = {'color' : color, 'linepattern' : linepattern}
        ls = []
        for symbol in symbols:
            s = symbol(**symbol_kwargs)
            ls.append(s)
        self.entries.append((ls, text))

    def done_bbox(self, data_bbox, svg_bbox):
        self.svg_bbox = copy.copy(svg_bbox)
        self.data_bbox = copy.copy(data_bbox)

    def draw(self, root_element, x_transform, y_transform):
        legend_height = len(self.entries) * 18
        w = self.svg_bbox[2] - self.svg_bbox[0] - 2 * AXIS_SIZE
        legend_width = w / 2 - 20
        legend = ET.SubElement(root_element, 'rect')
        legend.set('stroke', 'black')
        legend.set('fill', 'white')
        legend.set('fill-opacity', '0.8')
        # Calculate the SVG coordinates of the top left point of the rectangle
        # that encloses the legend:
        if self.position == TOPLEFT:
            x = self.svg_bbox[0] + AXIS_SIZE + 10
            y = self.svg_bbox[1] + AXIS_SIZE + 10
        elif self.position == TOPRIGHT:
            x = self.svg_bbox[0] + AXIS_SIZE + w / 2 + 10
            y = self.svg_bbox[1] + AXIS_SIZE + 10
        elif self.position == BOTTOMLEFT:
            x = self.svg_bbox[0] + AXIS_SIZE + 10
            y = self.svg_bbox[3] - AXIS_SIZE - legend_height - 10
        elif self.position == BOTTOMRIGHT:
            x = self.svg_bbox[0] + AXIS_SIZE + w / 2 + 10
            y = self.svg_bbox[3] - AXIS_SIZE - legend_height - 10
        elif self.position == UNDER_PLOT:
            x = self.svg_bbox[0] + AXIS_SIZE
            y = self.svg_bbox[3]
            legend_width = self.svg_bbox[2] - self.svg_bbox[0] - 2 * AXIS_SIZE

        legend.set('x', '%.2f' % x) 
        legend.set('y', '%.2f' % y)
        legend.set('width', '%.2f' % legend_width)
        legend.set('height', '%.2f' % legend_height) 
        # symbol + color + text
        for i, entry in enumerate(self.entries):
            symbols, text = entry
            # Some of the code below assumes that the font-size for entries in
            # the Legends is 18 (I futzed around a bit to find the off-sets
            # that look good).
            sx = x + 20
            sy = y + 9 + i * 18
            for symbol in symbols:
                symbol.draw_xy(root_element, sx, sy)
            t = ET.SubElement(root_element, 'text')
            t.set('font-size', str(LEGEND_FONT_SIZE)) 
            t.set('x', '%.2f' % (sx + 20))
            t.set('y', '%.2f' % (sy + LEGEND_FONT_SIZE / 2 - 2))
            t.set('text-anchor', 'left')
            t.text = escape(text) 

