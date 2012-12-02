'''
Code that deals with the basics of SVG generation
'''
from __future__ import division
from xml.sax.saxutils import escape

from brp.svg.plotters.axes import LeftAxisPlotter
from brp.svg.plotters.axes import BottomAxisPlotter
from brp.svg.plotters.axes import TopAxisPlotter 
from brp.svg.plotters.axes import RightAxisPlotter

from brp.core.bbox import stretch_bbox
from brp.core.constants import HARDCODED_STRETCH
from brp.core.transform import setup_transforms

from brp.svg.et_import import ET
from brp.svg.constants import AXIS_SIZE, FONT_SIZE, DATA_PADDING

import sys


class SVGCanvas(object):
    '''SVGCanvas implements drawing PlotContainer instances to SVG.'''
    def __init__(self, width, height, **kwargs):
        '''
        Arguments :

            * `width` --- Width of SVG image in screen coordinates.
            * `height` --- Height of SVG image in screen coordinates.

        '''
        self.width = width
        self.height = height
        self.containers = []
        self.background_color = kwargs.get('background_color', 'none')

    def add_plot_container(self, plot_container):
        '''
        Add a PlotContainer instance to this SVGCanvas.

        Arguments :

            * `plot_container` --- Add a brp.svg.base.PlotContainer

        '''
        self.containers.append(plot_container)
    
    def draw(self, file):
        '''
        Draw all plot.

        Arguments :

            * `file` --- File like object that receives the plot.

        '''
        root = ET.Element('svg')
        root.set('xmlns', 'http://www.w3.org/2000/svg')
        root.set('xmlns:xlink', 'http://www.w3.org/1999/xlink')
        root.set('height', '%.2f' % self.height)
        root.set('width', '%.2f' % self.width)
        root.set('version', '1.1')
        # TODO : Figure out the exact corner coordinates given width and 
        # height for an SVG file.
        rect = ET.SubElement(root, 'rect')
        rect.set('x', '0')
        rect.set('y', '0')
        rect.set('width', '%.2f' % self.width) 
        rect.set('height', '%.2f' % self.height) 
        rect.set('fill', self.background_color)


        for c in self.containers:
            c.draw(root)

        tree = ET.ElementTree(root)
        tree.write(file)

class PlotContainer(object):
    '''
    Complete plot (axes + drawing). 
    
    Keeps state and acts as a container for BasePlotter sub-classes.
    '''
    def __init__(self, x_offset, y_offset, width, height, **kwargs):
        '''
        Arguments :

            * `x_offset` --- Horizontal offset in SVG screen coordinates where
              this plot will be drawn.
            * `y_offset` --- Vertical offset in SVG screen coordinates where
              this plot will be drawn.
            * `width` --- Width of this plot in SVG screen coordinates.
            * `height` --- Height of this plot in SVG screen coordinates.

        Keyword arguments :
            * `background_color` --- String, HTML/SVG color. This is currently
              not checked for validity, wrong colors can cause problems with
              the generated SVG. 
            * `data_padding` --- Integer, number of svg units (pixels) to use
              as padding around the plot inside of the axis.
        '''
        self.update_svg_bbox(x_offset, y_offset, width, height)
        self.data_bbox = None
        self.plot_layers = []
 
        self.background_color = kwargs.get('background_color', None)
        self.color = kwargs.get('color', 'black')
        self.data_padding = kwargs.get('data_padding', DATA_PADDING)
 
        self.left = LeftAxisPlotter(log=kwargs.get('y_log', False), color=self.color)
        self.top = TopAxisPlotter(log=kwargs.get('x_log', False), color=self.color)
        self.right = RightAxisPlotter(log=kwargs.get('y_log', False), color=self.color)
        self.bottom = BottomAxisPlotter(log=kwargs.get('x_log', False), color=self.color)

        self.draw_axes = True

    def update_svg_bbox(self, x_offset, y_offset, width, height):
        '''
        Update boundingbox for SVG drawing.
        '''
        self.svg_bbox = [x_offset, y_offset, x_offset + width, 
            y_offset + height]
    
    def add_plotter(self, plotter):
        '''
        Add a BasePlotter sub-class instance to this PlotContainer.
        '''
        self.plot_layers.append(plotter)
    
    def draw(self, root_element):
        '''Draw this PlotContainer.'''
        # Add the *AxisPlotter to the plot_layers
        if self.draw_axes:
            self.plot_layers.append(self.top)
            self.plot_layers.append(self.right)
            self.plot_layers.append(self.left)
            self.plot_layers.append(self.bottom)
        
        # Find the boundingbox that contains all data.
        for plotter in self.plot_layers:
            self.data_bbox = plotter.prepare_bbox(self.data_bbox)

        # Add some white space around the plot.
        x_available = self.svg_bbox[2] - self.svg_bbox[0] - 2 * AXIS_SIZE
        x_used = x_available - 2 * self.data_padding
        x_factor = x_available / x_used

        y_available = self.svg_bbox[3] - self.svg_bbox[1] - 2 * AXIS_SIZE
        y_used = y_available - 2 * self.data_padding
        y_factor = y_available / y_used
#        x_factor, y_factor = 1.2, 1.2

        self.data_bbox = stretch_bbox(self.data_bbox, x_factor, y_factor,
            self.top.kwargs['log'] or self.bottom.kwargs['log'],
            self.left.kwargs['log'] or self.right.kwargs['log'],)
        
        # Comunicate to each *Plotter object the data bounding box and the
        # SVG plot bounding box.
        for plotter in self.plot_layers:
            plotter.done_bbox(self.data_bbox, self.svg_bbox)

        # Check that all the required to construct the transforms is available
        if not (self.svg_bbox and self.data_bbox):
            raise Exception('No transforms can be calculated.')

        # Determine which transforms to use:
        svg_x_min, svg_y_min, svg_x_max, svg_y_max = self.svg_bbox
        x_min, y_min, x_max, y_max = self.data_bbox
        # Note: SVG has its coordinates 'upside down'
        svg_target_bbox = (svg_x_min + AXIS_SIZE, svg_y_max - AXIS_SIZE,
            svg_x_max - AXIS_SIZE, svg_y_min + AXIS_SIZE)

        xtr, ytr = setup_transforms(self.data_bbox, svg_target_bbox, 
            x_log=self.top.kwargs['log'] or self.bottom.kwargs['log'],
            y_log=self.left.kwargs['log'] or self.right.kwargs['log'] 
        ) 

        # Draw background color (or not).
        if self.background_color:
            ET.SubElement(root_element, 'rect', fill=self.background_color, 
                x='%.2f' % svg_x_min, 
                y='%.2f' % svg_y_min, 
                width='%.2f' % (svg_x_max - svg_x_min), 
                height='%.2f' % (svg_y_max - svg_y_min),
            )

        # Draw all the parts of the plot.        
        for p_layer in self.plot_layers:
            p_layer.draw(root_element, xtr, ytr)
        
        # Remove the *AxisPlotters from the parts of the plot again.
        if self.draw_axes:
            self.plot_layers = self.plot_layers[0:-4]
        self.data_bbox = None

        if False:
            rect = ET.SubElement(root_element, 'rect')        
            rect.set('x', '%.2f' % (self.svg_bbox[0] + DATA_PADDING))
            rect.set('y', '%.2f' % (self.svg_bbox[1] + DATA_PADDING))
            rect.set('width', '%.2f' % (self.svg_bbox[2] - self.svg_bbox[0] - 2 * DATA_PADDING))
            rect.set('height', '%.2f' % (self.svg_bbox[3] - self.svg_bbox[1] - 2 * DATA_PADDING))
            rect.set('stroke', 'blue')
            rect.set('fill', 'none')

    def set_minimum_data_bbox(self, bbox):
        if self.data_bbox:
            if bbox[0] < self.data_bbox[0]:
                self.data_bbox[0] = bbox[0]
            if bbox[1] < self.data_bbox[1]:
                self.data_bbox[1] = bbox[1]
            if bbox[2] > self.data_bbox[2]:
                self.data_bbox[2] = bbox[2]
            if bbox[3] > self.data_bbox[3]:
                self.data_bbox[3] = bbox[3]
        else:
            self.data_bbox = bbox

    def hide_axes(self):
        self.draw_axes = False


class TextFragment(object):
    def __init__(self, x, y, text, color='black', alignment='start', **kwargs):
        self.x = x
        self.y = y
        self.text = text
        if alignment in ['start', 'middle', 'end']:
            self.alignment = alignment
        else:
            self.alignment = 'start'
        self.color = color
        self.font_size = str(kwargs.get('font_size', FONT_SIZE))
        self.link = kwargs.get('link', '')

    def draw(self, root_element):
        if self.link:
            root_element = ET.SubElement(root_element, 'a')
            # TODO add validation to check that self.link is in fact an URL
            root_element.set('xlink:href', self.link)
        tf = ET.SubElement(root_element, 'text')
        tf.set('x', '%.2f' % self.x) 
        tf.set('y', '%.2f' % self.y)
        tf.set('font-size', self.font_size)
        tf.set('text-anchor', self.alignment)
        tf.set('fill', self.color)
#        tf.set('stroke', self.color)
        tf.text = escape(self.text)

