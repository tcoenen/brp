from __future__ import division
from brp.svg.et_import import ET
from math import log10
from brp.svg.plotters.base import BasePlotter


def bin_data(lx, n_bins, normed=False):
    '''
    Bin histogram data.

    Note: Binned data is [(x_min1, x_max1, val1), ..., (x_min2, x_max2, val2)]
    '''
    m = min(lx)
    M = max(lx)

    # TODO XXX : remove this hack:
    if m == M:
        tmp = abs(m)
        if tmp > 0:
            pot = int(log10(tmp))
            delta = 10 ** (pot - 1)
        else:  # in case interval[0] == 0
            delta = 0.1
        m = m - delta
        M = M + delta

    interval = (M - m)
    # n_bins - 1, because you want 0.5 bins 'overhang' at either end of the
    # histogram.
    bin_width = interval / (n_bins - 1)
    bin_edges = [m + (i - 0.5) * bin_width for i in range(n_bins + 1)]
    bin_values = [0 for i in range(n_bins)]

    for x in lx:
        index = int((x - m) / bin_width)
        try:
            bin_values[index] += 1
        except IndexError:
            bin_values[-1] += 1

    if normed:
        factor = 1 / max(bin_values)
        for i in range(n_bins):
            bin_values[i] /= factor

    return [(bin_edges[i], bin_edges[i + 1], bin_values[i])
            for i in range(n_bins)]


def bin_data_log(lx, n_bins, normed=False):
    '''
    Bin data with logarithmically sized bins.
    '''
    # Just take the logarithm of all data points and call the normal binning
    # function, and fix the bin edges thereafter.
    log_lx = [log10(x) for x in lx]
    log_bins = bin_data(log_lx, n_bins, normed)

    bins = []
    for x1, x2, v in log_bins:
        bins.append((10 ** x1, 10 ** x2, v))

    return bins


def merge_bins(bins):
    out = []
    begin_x, last_x, value = bins[0]

    for x1, x2, v in bins[1:]:
        if x1 == last_x and v == value:
            last_x = x2
        else:
            out.append((begin_x, last_x, value))
            begin_x, last_x, value = x1, x2, v
    out.append((begin_x, last_x, value))

    return out


def make_y_log_safe(binned_data):
    return [x for x in binned_data if x[2] > 0]


class HistogramPlotter(BasePlotter):
    def __init__(self, binned_data, data_range=True, **kwargs):
        # THIS CLASS WAS ORIGINALLY ONLY MEANT TO PLOT HORIZONTAL HISTOGRAMS
        # CURRENTLY IT DOES ALSO VERTICAL ONES (THROUGH A HACK)
        self.orientation = kwargs.get('orientation', 'horizontal')
        if not self.orientation in ['horizontal', 'vertical']:
            self.orientation = 'horizontal'

        self.binned_data = binned_data
        self.data_range = data_range
        self.color = kwargs.get('color', 'black')
        self.line_pattern = kwargs.get('linepattern', '')

    def prepare_bbox(self, data_bbox):
        x_min = self.binned_data[0][0]
        x_max = self.binned_data[-1][1]
        if self.data_range:
            y_min = min((x[2] for x in self.binned_data))
        if not self.data_range:
            y_min = 0
        y_max = max((x[2] for x in self.binned_data))

        # HACKY WAY TO DEAL WITH ORIENTATION:
        if self.orientation == 'vertical':
            x_min, y_min = y_min, x_min
            x_max, y_max = y_max, x_max

        if not data_bbox:
            return [x_min, y_min, x_max, y_max]
        else:
            data_bbox = list(data_bbox)

        if x_min < data_bbox[0]:
            data_bbox[0] = x_min
        if x_max > data_bbox[2]:
            data_bbox[2] = x_max
        if y_min < data_bbox[1]:
            data_bbox[1] = y_min
        if y_max > data_bbox[3]:
            data_bbox[3] = y_max

        return tuple(data_bbox)

    def draw(self, root_element, x_transform, y_transform):
        L = len(self.binned_data)
        # Still needs the optimization for line segments that extend each other
        # (those need to be merged).
        points = []
        for i in range(L):
            if i == 0:
                x1, x2, y = self.binned_data[0]
                if self.orientation == 'horizontal':
                    points.append('%.2f,%.2f' % (x_transform(x1),
                                  y_transform(y)))
                else:
                    points.append('%.2f,%.2f' % (x_transform(y),
                                  y_transform(x1)))
            else:
                x1, x2, y = self.binned_data[i]
                previous_x1, previous_x2, previous_y = self.binned_data[i - 1]
                if x1 == previous_x2:
                    if self.orientation == 'horizontal':
                        points.append('%.2f,%.2f' % (x_transform(x1),
                                      y_transform(previous_y)))
                        if y != previous_y:
                            points.append('%.2f,%.2f' % (x_transform(x1),
                                          y_transform(y)))
                    else:
                        points.append('%.2f,%.2f' % (x_transform(previous_y),
                                                     y_transform(x1)))
                        if y != previous_y:
                            points.append('%.2f,%.2f' % (x_transform(y),
                                          y_transform(x1)))
                else:  # a 'break' in the histogram
                    if self.orientation == 'horizontal':
                        points.append('%.2f,%.2f' % (x_transform(previous_x2),
                                      y_transform(previous_y)))
                    else:
                        points.append('%.2f,%.2f' % (x_transform(previous_y),
                                      y_transform(previous_x2)))
                    pl = ET.SubElement(root_element, 'polyline')
                    pl.set('stroke', self.color)
                    pl.set('fill', 'none')
                    pl.set('points', ' '.join(points))
                    if self.line_pattern:
                        pl.set('style', 'stroke-dasharray:%s' %
                               self.line_pattern)
                    if self.orientation == 'horizontal':
                        points = ['%.2f,%.2f' % (x_transform(x1),
                                  y_transform(y))]
                    else:
                        points = ['%.2f,%.2f' % (x_transform(y),
                                  y_transform(x1))]
            if i == L - 1:
                x1, x2, y = self.binned_data[-1]
                if self.orientation == 'horizontal':
                    points.append('%.2f,%.2f' % (x_transform(x2),
                                  y_transform(y)))
                else:
                    points.append('%.2f,%.2f' % (x_transform(y),
                                  y_transform(x2)))
                pl = ET.SubElement(root_element, 'polyline')
                pl.set('stroke', self.color)
                pl.set('fill', 'none')
                pl.set('points', ' '.join(points))
                if self.line_pattern:
                    pl.set('style', 'stroke-dasharray:%s' % self.line_pattern)
