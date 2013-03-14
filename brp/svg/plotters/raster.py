from brp.svg.et_import import ET
from brp.svg.plotters.base import BasePlotter
from brp.core.bbox import combine_bbox


class RasterPlotterMixin(BasePlotter):
    def prepare_bbox(self, data_bbox=None):
        if data_bbox is not None:
            return combine_bbox(self.img_bbox, data_bbox)
        else:
            return tuple(self.img_bbox)

    def draw(self, root_element, x_transform, y_transform):
        # NOTE : the following is a crude way of detecting logarithmic
        # transforms for the axes. Bit of a hack.
        try:
            x_transform(-1)
            y_transform(-1)
        except ValueError:
            msg = 'RasterPlotterMixin does not support logarithmic axes.'
            raise ValueError(msg)
        x = x_transform(self.img_bbox[0])
        y = y_transform(self.img_bbox[3])
        width = x_transform(self.img_bbox[2]) - x
        height = y_transform(self.img_bbox[1]) - y
        img = ET.SubElement(root_element, 'image')
        img.set('xlink:href', self.encoded_png)
        img.set('x', '%.2f' % x)
        img.set('y', '%.2f' % y)
        img.set('width', '%.2f' % width)
        img.set('height', '%.2f' % height)
        img.set('preserveAspectRatio', 'none')
