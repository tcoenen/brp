from __future__ import division
from brp.svg.et_import import ET
import copy
from brp.svg.plotters.base import BasePlotter

# TODO reimplement using ScatterPlotter or remove entirely


class CrossHairPlotter(BasePlotter):
    def __init__(self, x, y, **kwargs):
        self.x = x
        self.y = y
        self.color = kwargs.get('color', 'black')

    def done_bbox(self, data_bbox, svg_bbox):
        self.svg_bbox = copy.copy(svg_bbox)
        self.data_bbox = copy.copy(data_bbox)

    def draw(self, root_element, x_transform, y_transform):
        # only draw if the self.x and self.y lie within the data_bbox
        if (self.data_bbox[0] <= self.x <= self.data_bbox[2]) and \
            (self.data_bbox[1] <= self.y <= self.data_bbox[3]):

            rw = 0.1 * (self.svg_bbox[2] - self.svg_bbox[0])
            rh = 0.1 * (self.svg_bbox[3] - self.svg_bbox[1])

            l1 = ET.SubElement(root_element, 'line')
            l1.set('x1', '%.2f' % x_transform(self.x))
            l1.set('y1', '%.2f' % (y_transform(self.y) - 0.7 * rh))
            l1.set('x2', '%.2f' % x_transform(self.x))
            l1.set('y2', '%.2f' % (y_transform(self.y) - 0.3 * rh))
            l1.set('stroke', self.color)
            l1.set('stroke-width', '2')

            l1 = ET.SubElement(root_element, 'line')
            l1.set('x1', '%.2f' % x_transform(self.x))
            l1.set('y1', '%.2f' % (y_transform(self.y) + 0.3 * rh))
            l1.set('x2', '%.2f' % x_transform(self.x))
            l1.set('y2', '%.2f' % (y_transform(self.y) + 0.7 * rh))
            l1.set('stroke', self.color)
            l1.set('stroke-width', '2')

            l2 = ET.SubElement(root_element, 'line')
            l2.set('x1', '%.2f' % (x_transform(self.x) - 0.7 * rw))
            l2.set('y1', '%.2f' % y_transform(self.y))
            l2.set('x2', '%.2f' % (x_transform(self.x) - 0.3 * rw))
            l2.set('y2', '%.2f' % y_transform(self.y))
            l2.set('stroke', self.color)
            l2.set('stroke-width', '2')

            l2 = ET.SubElement(root_element, 'line')
            l2.set('x1', '%.2f' % (x_transform(self.x) + 0.3 * rw))
            l2.set('y1', '%.2f' % y_transform(self.y))
            l2.set('x2', '%.2f' % (x_transform(self.x) + 0.7 * rw))
            l2.set('y2', '%.2f' % y_transform(self.y))
            l2.set('stroke', self.color)
            l2.set('stroke-width', '2')

            d = ET.SubElement(root_element, 'rect')
            d.set('x', '%.2f' % (x_transform(self.x) - 0.5 * rw))
            d.set('y', '%.2f' % (y_transform(self.y) - 0.5 * rh))
            d.set('width', '%.2f' % rw)
            d.set('height', '%.2f' % rh)
            d.set('stroke', self.color)
            d.set('fill', 'none')
            d.set('stroke-width', '2')
