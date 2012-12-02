'''
Implementation of coordinate axis plotting.
'''

from __future__ import division

from brp.svg.plotters.base import BasePlotter
from brp.svg.plotters.axes_procedural import draw_top_axis
from brp.svg.plotters.axes_procedural import draw_right_axis
from brp.svg.plotters.axes_procedural import draw_bottom_axis
from brp.svg.plotters.axes_procedural import draw_left_axis

from brp.core.transform import setup_transform_1d
from brp.svg.constants import AXIS_SIZE

class AxisPlotterMixin(object):
    '''Implements member functions necessary to update axis appearance.'''
    def set_label(self, label):
        '''
        Set the axis label.

        Arguments:
            `label` --- String, text for the axis label.        
        '''
        self.kwargs['label'] = label
    
    def hide_label(self, toggle = True):
        '''
        Hide the axis label if so desired. 

        Arguments:
            `toggle` --- Boolean, True if the axis label needs to be hidden. 
        '''
        self.kwargs['hide_label'] = toggle
    
    def set_tickmarks(self, tickmarks):
        '''Override the automatically generated tickmarks.'''
        self.kwargs['tickmarks'] = tickmarks
    
    def hide_tickmarks(self, toggle=True):
        '''
        Hide tickmarks.
        
        Arguments:
            `toggle` --- Boolean, True is tickmarks need to be hidden.    
        '''
        self.kwargs['hide_tickmarks'] = toggle
    
    def hide_tickmarklabels(self, toggle=True):
        '''Hide tickmark labelling if toggle is True.'''
        self.kwargs['hide_tickmarklabels'] = toggle
    
    def label_link(self, uri=''):
        '''Make this axis label a link to the give uri.'''
        self.kwargs['label_link'] = uri

    def hide_all(self):
        self.kwargs['hide_tickmarks'] = True
        self.kwargs['hide_label'] = True
    
    def set_interval(self, interval, log = False):
        '''Override the automatically determined interval on this axis.'''
        # Think about not storing this information in self.kwargs (since that
        # goes directly to the underlying plotting functions). (TODO)
        self.kwargs['s_interval'] = interval
        self.kwargs['s_log'] = log

class LeftAxisPlotter(BasePlotter, AxisPlotterMixin):
    '''Left axis plotting wrapper, implements BasePlotter interface.'''
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def done_bbox(self, data_bbox, svg_bbox):
        x_min, y_min, x_max, y_max = data_bbox
        self.interval = (y_min, y_max)        

        svg_x_min, svg_y_min, svg_x_max, svg_y_max = svg_bbox
        self.x_offset = svg_x_min
        self.y_offset = svg_y_min
        self.height = svg_y_max - svg_y_min
    
    def draw(self, root_element, x_transform, y_transform):
        '''Draw left axis.'''
        # This is a bit of a hack, to be able to define a different interval for
        # this axis.
        if self.kwargs.has_key('s_interval') and self.kwargs.has_key('s_log'):
            log = self.kwargs['s_log']
            interval = self.kwargs['s_interval']
            y_transform = setup_transform_1d(interval, (self.y_offset + \
                self.height - AXIS_SIZE, self.y_offset + AXIS_SIZE), log)
        else:
            interval = self.interval
            log = self.kwargs.get('log', False)

        draw_left_axis(root_element, self.x_offset, self.y_offset, self.height, 
            y_transform, interval, log, **self.kwargs)


class RightAxisPlotter(BasePlotter, AxisPlotterMixin):
    '''Right axis plotting wrapper, implements BasePlotter interface.'''
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def done_bbox(self, data_bbox, svg_bbox):
        x_min, y_min, x_max, y_max = data_bbox
        self.interval = (y_min, y_max)        

        svg_x_min, svg_y_min, svg_x_max, svg_y_max = svg_bbox
        self.x_offset = svg_x_max - 2 * AXIS_SIZE
        self.y_offset = svg_y_min
        self.height = svg_y_max - svg_y_min

    def draw(self, root_element, x_transform, y_transform):
        # This is a bit of a hack, to be able to define a different interval for
        # this axis.
        if self.kwargs.has_key('s_interval') and self.kwargs.has_key('s_log'):
            log = self.kwargs['s_log']
            interval = self.kwargs['s_interval']
            y_transform = setup_transform_1d(interval, (self.y_offset + \
                self.height - AXIS_SIZE, self.y_offset + AXIS_SIZE), log)
        else:
            interval = self.interval
            log = self.kwargs.get('log', False)

        draw_right_axis(root_element, self.x_offset, self.y_offset, self.height, 
            y_transform, interval, log, **self.kwargs)
    

class TopAxisPlotter(BasePlotter, AxisPlotterMixin):
    '''Top axis plotting wrapper, implements BasePlotter interface.'''
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def done_bbox(self, data_bbox, svg_bbox):
        x_min, y_min, x_max, y_max = data_bbox
        self.interval = (x_min, x_max)        

        svg_x_min, svg_y_min, svg_x_max, svg_y_max = svg_bbox
        self.x_offset = svg_x_min
        self.y_offset = svg_y_min
        self.width = svg_x_max - svg_x_min

    def draw(self, root_element, x_transform, y_transform):
        # This is a bit of a hack, to be able to define a different interval for
        # this axis.
        if self.kwargs.has_key('s_interval') and self.kwargs.has_key('s_log'):
            log = self.kwargs['s_log']
            interval = self.kwargs['s_interval']
            x_transform = setup_transform_1d(interval, (self.x_offset + AXIS_SIZE, self.x_offset + self.width - AXIS_SIZE), False)
        else:
            interval = self.interval
            log = self.kwargs.get('log', False)

        draw_top_axis(root_element, self.x_offset, self.y_offset, self.width, 
            x_transform, interval, log, **self.kwargs)


class BottomAxisPlotter(BasePlotter, AxisPlotterMixin):
    '''Botttom axis plotting wrapper, implements BasePlotter interface.'''
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def done_bbox(self, data_bbox, svg_bbox):
        x_min, y_min, x_max, y_max = data_bbox
        self.interval = (x_min, x_max)        

        svg_x_min, svg_y_min, svg_x_max, svg_y_max = svg_bbox
        self.x_offset = svg_x_min
        self.y_offset = svg_y_max - 2 * AXIS_SIZE
        self.width = svg_x_max - svg_x_min

    def draw(self, root_element, x_transform, y_transform):
        # This is a bit of a hack, to be able to define a different interval for
        # this axis.
        if self.kwargs.has_key('s_interval') and self.kwargs.has_key('s_log'):
            log = self.kwargs['s_log']
            interval = self.kwargs['s_interval']
            x_transform = setup_transform_1d(interval, (self.x_offset + AXIS_SIZE, self.x_offset + self.width - AXIS_SIZE), False)
        else:
            interval = self.interval
            log = self.kwargs.get('log', False)

        draw_bottom_axis(root_element, self.x_offset, self.y_offset, self.width, 
            x_transform, interval, log, **self.kwargs)

