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
    interval = M - m
    bin_width = interval / n_bins
    bin_edges = [m + i * bin_width for i in range(n_bins + 1)]
    bin_values = [0 for i in range(n_bins)]
    for x in lx:
        index = int((x - m) / bin_width)
        try:
            bin_values[index] += 1
        except IndexError, e:
            bin_values[-1] += 1
    if normed:
        factor = 1 / max(bin_values)
        for i in range(n_bins):
            bin_values[i] /= factor
    return [(bin_edges[i], bin_edges[i+1], bin_values[i]) \
        for i in range(n_bins)]

def merge_bins(binned_data):
    out = []
    last = binned_data.pop()
    while binned_data:
        current = binned_data.pop()
        if current[2] == last[2] and current[0] == last[1]:
            last = (last[0], current[1], current[2])
        else:
            out.append(last)
            last = current
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
        
        if x_min < data_bbox[0]: data_bbox[0] = x_min  
        if x_max > data_bbox[2]: data_bbox[2] = x_max
        if y_min < data_bbox[1]: data_bbox[1] = y_min
        if y_max > data_bbox[3]: data_bbox[3] = y_max
        
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
                    points.append('%.2f,%.2f' % (x_transform(x1), y_transform(y)))
                else:
                    points.append('%.2f,%.2f' % (x_transform(y), y_transform(x1)))
            else:
                x1, x2, y = self.binned_data[i]
                previous_x1, previous_x2, previous_y = self.binned_data[i-1]
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
                else: # a 'break' in the histogram
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
                        pl.set('style', 'stroke-dasharray:%s' % self.line_pattern)
                    if self.orientation == 'horizontal':
                        points = ['%.2f,%.2f' % (x_transform(x1), y_transform(y))]
                    else:
                        points = ['%.2f,%.2f' % (x_transform(y), y_transform(x1))]
            if i == L - 1:
                x1, x2, y = self.binned_data[-1]
                if self.orientation == 'horizontal':
                    points.append('%.2f,%.2f' % (x_transform(x2), y_transform(y)))
                else:
                    points.append('%.2f,%.2f' % (x_transform(y), y_transform(x2)))
                pl = ET.SubElement(root_element, 'polyline')
                pl.set('stroke', self.color)
                pl.set('fill', 'none')
                pl.set('points', ' '.join(points))
                if self.line_pattern:
                    pl.set('style', 'stroke-dasharray:%s' % self.line_pattern)

