from __future__ import division
import copy

from brp.svg.constants import AXIS_SIZE, DATA_PADDING
from brp.core.constants import HARDCODED_STRETCH
from brp.svg.et_import import ET
from brp.svg.plotters.base import BasePlotter

class XLimitPlotter(BasePlotter):
    def __init__(self, x_limit, **kwargs):
        self.x_limit = x_limit
        self.color = kwargs.get('color', 'black')
    
    def done_bbox(self, data_bbox, svg_bbox):
        self.svg_bbox = copy.copy(svg_bbox)
        self.data_bbox = copy.copy(data_bbox)

    def draw(self, root_element, x_transform, y_transform):
        if self.data_bbox[0] <= self.x_limit <= self.data_bbox[2]:
            rh = self.svg_bbox[3] - self.svg_bbox[1] - 2 * AXIS_SIZE
            l = ET.SubElement(root_element, 'line')
            l.set('x1', '%.2f' % x_transform(self.x_limit))
            l.set('x2', '%.2f' % x_transform(self.x_limit))
#            l.set('y1', '%.2f' % (self.svg_bbox[1] + AXIS_SIZE + 0.2 * rh * (HARDCODED_STRETCH - 1)))
#            l.set('y2', '%.2f' % (self.svg_bbox[3] - AXIS_SIZE - 0.2 * rh * (HARDCODED_STRETCH - 1)))
            l.set('y1', '%.2f' % (self.svg_bbox[1] + AXIS_SIZE + DATA_PADDING))
            l.set('y2', '%.2f' % (self.svg_bbox[3] - AXIS_SIZE - DATA_PADDING))
            l.set('stroke', self.color)

class YLimitPlotter(BasePlotter):
    def __init__(self, y_limit, **kwargs):
        self.y_limit = y_limit
        self.color = kwargs.get('color', 'black')
    
    def done_bbox(self, data_bbox, svg_bbox):
        self.svg_bbox = copy.copy(svg_bbox)
        self.data_bbox = copy.copy(data_bbox)

    def draw(self, root_element, x_transform, y_transform):
        if self.data_bbox[1] <= self.y_limit <= self.data_bbox[3]:
            rw = self.svg_bbox[2] - self.svg_bbox[0] - 2 * AXIS_SIZE
            l = ET.SubElement(root_element, 'line')
            l.set('y1', '%.2f' % y_transform(self.y_limit))
            l.set('y2', '%.2f' % y_transform(self.y_limit))
#            l.set('x1', '%.2f' % (self.svg_bbox[0] + AXIS_SIZE + 0.2 * rw * (HARDCODED_STRETCH - 1)))
#            l.set('x2', '%.2f' % (self.svg_bbox[2] - AXIS_SIZE - 0.2 * rw * (HARDCODED_STRETCH - 1)))

            l.set('x1', '%.2f' % (self.svg_bbox[0] + AXIS_SIZE + DATA_PADDING))
            l.set('x2', '%.2f' % (self.svg_bbox[2] - AXIS_SIZE - DATA_PADDING))

            l.set('stroke', self.color)

