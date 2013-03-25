from __future__ import division
import colorsys
import copy
from math import log10

from brp.svg.plotters.base import BasePlotter
from brp.svg.et_import import ET


class RGBGradient(object):
    def __init__(self, interval, rgb1, rgb2, *args, **kwargs):
        # colors channels have values between 0 and 1
        self.interval = interval

        # If interval is zero length: stretch it
        # TODO XXX: See whether this is more at home somewhere else
        if self.interval[0] == self.interval[1]:
            tmp = abs(self.interval[0])
            if tmp > 0:
                pot = int(log10(tmp))
                delta = 10 ** (pot - 1)
            else:  # in case interval[0] == 0
                delta = 0.1
            self.interval = (interval[0] - delta, interval[0] + delta)

        self.rgb1 = rgb1
        self.rgb2 = rgb2
        self.min_value = kwargs.get('min_value', None)
        self.min_value_color = kwargs.get('min_value_color', (0, 0, 0))
        self.max_value = kwargs.get('max_value', None)
        self.max_value_color = kwargs.get('max_value_color', (1, 1, 1))

    def get_color(self, value):
        if self.min_value is not None and value < self.min_value:
            return self.min_value_color
        if self.max_value is not None and value > self.max_value:
            return self.max_value_color

        if value < self.interval[0]:
            return self.rgb1
        if value > self.interval[1]:
            return self.rgb2

        dv = (value - self.interval[0]) / (self.interval[1] - self.interval[0])
        hls1 = colorsys.rgb_to_hls(*self.rgb1)
        hls2 = colorsys.rgb_to_hls(*self.rgb2)
        dh = hls2[0] - hls1[0]
        dl = hls2[1] - hls1[1]
        ds = hls2[2] - hls1[2]

        rgb = colorsys.hls_to_rgb(hls1[0] + dv * dh, hls1[1] + dv * dl,
                                  hls1[2] + dv * ds)
        return rgb

    def get_css_color(self, value):
        red, green, blue = self.get_color(value)
        return '#%02x%02x%02x' % (255 * red, 255 * green, 255 * blue)

    def get_rgba_color(self, value):
        red, green, blue = self.get_color(value)
        return int(255 * red), int(255 * green), int(255 * blue), 255


class BWGradient(RGBGradient):
    def __init__(self, interval, *args, **kwargs):
        # colors channels have values between 0 and 1
        self.interval = interval
        self.rgb1 = (0.2, 0.2, 0.2)
        self.rgb2 = (0.9, 0.9, 0.9)

    def get_color(self, value):
        if value < self.interval[0]:
            return self.rgb1
        if value > self.interval[1]:
            return self.rgb2
        dv = (value - self.interval[0]) / (self.interval[1] - self.interval[0])
        if dv > 1:
            dv = 1
        return (dv, dv, dv)


# slightly hackish, but ...
class GradientPlotter(BasePlotter):
    def __init__(self, gradient, orientation='vertical'):
        self.gradient = copy.deepcopy(gradient)
        if not orientation in ['vertical', 'horizontal']:
            self.orientation = 'vertical'
        else:
            self.orientation = orientation

        if self.gradient.min_value is not None:
            min_value = min(self.gradient.interval[0], self.gradient.min_value)
        else:
            min_value = self.gradient.interval[0]
        if self.gradient.max_value is not None:
            max_value = max(self.gradient.interval[1], self.gradient.max_value)
        else:
            max_value = self.gradient.interval[1]

        mean = (min_value + max_value) / 2
        half_range = max_value - mean

        self.min_value = mean - 1.1 * half_range
        self.max_value = mean + 1.1 * half_range

    def prepare_bbox(self, data_bbox):
        if self.orientation == 'vertical':
            tmp = (0, self.min_value, 1, self.max_value)
        else:
            tmp = (self.min_value, 0, self.max_value, 1)
        return tmp

    def done_bbox(self, data_bbox, svg_bbox):
        self.svg_bbox = copy.copy(svg_bbox)
        self.data_bbox = copy.copy(data_bbox)

    def draw(self, root_element, x_transform, y_transform, **kwargs):
        N_STEPS = 400
        interval_length = self.max_value - self.min_value
        d_value = interval_length / N_STEPS

        if self.orientation == 'vertical':
            x1, x2 = x_transform(0), x_transform(1)
            for i in range(N_STEPS):
                min_value = self.min_value + i * d_value
                max_value = min_value + d_value
                color = self.gradient.get_css_color((min_value + max_value) / 2)

                rect = ET.SubElement(root_element, 'rect')
                rect.set('x', '%.2f' % x1)
                rect.set('width', '%.2f' % (x2 - x1))
                y1 = y_transform(min_value)
                y2 = y_transform(max_value)
                if y1 > y2:
                    y2, y1 = y1, y2
                rect.set('y', '%.2f' % y1)
                rect.set('height', '%.2f' % (y2 - y1))
                rect.set('fill', color)
                rect.set('stroke', color)
        else:
            y1, y2 = y_transform(0), y_transform(1)
            for i in range(N_STEPS):
                min_value = self.min_value + i * d_value
                max_value = min_value + d_value
                color = self.gradient.get_css_color((min_value + max_value) / 2)

                rect = ET.SubElement(root_element, 'rect')
                rect.set('y', '%.2f' % y2)
                rect.set('height', '%.2f' % (y1 - y2))
                x1 = x_transform(min_value)
                x2 = x_transform(max_value)
                if x1 > x2:
                    x2, x1 = x1, x2
                rect.set('x', '%.2f' % x1)
                rect.set('width', '%.2f' % (x2 - x1))
                rect.set('fill', color)
                rect.set('stroke', color)
