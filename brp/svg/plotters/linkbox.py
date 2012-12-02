'''
Implement linked regions.
'''
from __future__ import division
from brp.svg.plotters.base import BasePlotter
from brp.svg.et_import import ET

class LinkBox(BasePlotter):
    def __init__(self, bbox, link='', *args, **kwargs):
        self.bbox = bbox
        self.link = link
        self.color = kwargs.get('color', 'none')

    def prepare_bbox(self, data_bbox):
        '''Update bounding box with the data for this scatter plot.'''
        if data_bbox != None:
            tmp = list(data_bbox)
            if self.bbox[0] < tmp[0]:
                tmp[0] = self.bbox[0]
            if self.bbox[2] > tmp[2]:
                tmp[2] = self.bbox[2]
            if self.bbox[1] < tmp[1]:
                tmp[1] = self.bbox[1]
            if self.bbox[3] > tmp[3]:
                tmp[3] = self.bbox[3]
        return tuple(tmp)

    def draw(self, root_element, x_transform, y_transform, *args, **kwargs):
        '''Add linked rectangle.'''
        tmp = ET.SubElement(root_element, 'a')
        tmp.set('xlink:href', self.link)
        box = ET.SubElement(tmp, 'rect')
        box.set('fill', 'white')
        box.set('stroke', self.color)
        box.set('fill-opacity', '0.0')
        x = x_transform(self.bbox[0]) 
        y = y_transform(self.bbox[3]) 
        width = x_transform(self.bbox[2]) - x
        height = y_transform(self.bbox[1]) - y
        assert width >= 0
        assert height >= 0
        box.set('x', '%.2f' % x)
        box.set('y', '%.2f' % y)
        box.set('width', '%.2f' % width)
        box.set('height', '%.2f' % height)

