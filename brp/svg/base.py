'''
Code that deals with the basics of SVG generation
'''
from __future__ import division
from xml.sax.saxutils import escape

from brp.svg.plotters.axes import LeftAxisPlotter
from brp.svg.plotters.axes import BottomAxisPlotter
from brp.svg.plotters.axes import TopAxisPlotter
from brp.svg.plotters.axes import RightAxisPlotter
from brp.svg.plotters.base import BasePlotter

from brp.core.bbox import stretch_bbox, check_bbox_intervals
from brp.core.transform import setup_transforms
from brp.core.exceptions import NotImplementedError

from brp.svg.et_import import ET
from brp.svg.constants import AXIS_SIZE, FONT_SIZE, DATA_PADDING


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

        Note: Only here for backwards compatability, use .add() method instead.
        '''
        self.containers.append(plot_container)

    def add(self, plottable):
        '''
        Add plottable to SVGCanvas.

        Note currently these plottables are subclasses of:
        brp.svg.base.PlotContainer and brp.svg.base.TextFragment .
        '''
        if isinstance(plottable, PlotContainer) or \
                isinstance(plottable, TextFragment):
            self.containers.append(plottable)
        else:
            raise Exception('This cannot be added to an SVGCanvas.')

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
            * `x_min_range` --- tuple of floats (or integers) giving the
              minimum range of the x axis (the horizontal axis)
            * `y_min_range` --- tuple of floats (or integers) giving the
              minimum range of the y axis (the vertical axis)
        '''
        self.update_svg_bbox(x_offset, y_offset, width, height)
        self.data_bbox = None
        self.plot_layers = []

        self.background_color = kwargs.get('background_color', None)
        self.color = kwargs.get('color', 'black')
        self.data_padding = kwargs.get('data_padding', DATA_PADDING)

        self.x_log = kwargs.get('x_log', False)
        self.y_log = kwargs.get('y_log', False)

        self.left = LeftAxisPlotter(log=self.y_log, color=self.color)
        self.top = TopAxisPlotter(log=self.x_log, color=self.color)
        self.right = RightAxisPlotter(log=self.y_log, color=self.color)
        self.bottom = BottomAxisPlotter(log=self.x_log, color=self.color)

        self.draw_axes = True
        self.x_min_range = kwargs.get('x_min_range', None)
        self.y_min_range = kwargs.get('y_min_range', None)

        self.raster_fallback = kwargs.get('raster', False)

    def update_svg_bbox(self, x_offset, y_offset, width, height):
        '''
        Update boundingbox for SVG drawing.
        '''
        self.svg_bbox = [x_offset, y_offset, x_offset + width,
                         y_offset + height]

    def add_plotter(self, plotter, raster=False):
        '''
        Add a BasePlotter sub-class instance to this PlotContainer.

        Note: Only here for backwards compatability, use .add() method instead.
        '''
        self.plot_layers.append((plotter, raster))

    def add(self, plotter, raster=False):
        '''
        Add a BasePlotter sub-class instance to this PlotContainer.
        '''
        if isinstance(plotter, BasePlotter):
            self.plot_layers.append((plotter, raster))
        else:
            raise Exception('This cannot be added to a PlotContainer.')

    def draw(self, root_element):
        '''Draw this PlotContainer.'''
        # Add the *AxisPlotter to the plot_layers
        if self.draw_axes:
            self.plot_layers.append((self.top, False))
            self.plot_layers.append((self.right, False))
            self.plot_layers.append((self.left, False))
            self.plot_layers.append((self.bottom, False))

        # Find the boundingbox that contains all data.
        for plotter, use_raster_fallback in self.plot_layers:
            self.data_bbox = plotter.prepare_bbox(self.data_bbox)
        # If required, set the range of the x and y axes to some minimum.
        if self.x_min_range is not None:
            tmp = list(self.data_bbox)
            tmp[0] = min(tmp[0], self.x_min_range[0])
            tmp[2] = max(tmp[2], self.x_min_range[1])
            self.data_bbox = tuple(tmp)
        if self.y_min_range is not None:
            tmp = list(self.data_bbox)
            tmp[1] = min(tmp[1], self.y_min_range[0])
            tmp[3] = max(tmp[3], self.y_min_range[1])
            self.data_bbox = tuple(tmp)
        # Check that each of the axis covers some range and if not make it so.
        self.data_bbox = check_bbox_intervals(self.data_bbox, self.x_log,
                                              self.y_log)

        # Add some white space around the plot.
        x_available = self.svg_bbox[2] - self.svg_bbox[0] - 2 * AXIS_SIZE
        x_used = x_available - 2 * self.data_padding
        x_factor = x_available / x_used

        y_available = self.svg_bbox[3] - self.svg_bbox[1] - 2 * AXIS_SIZE
        y_used = y_available - 2 * self.data_padding
        y_factor = y_available / y_used

        self.data_bbox = stretch_bbox(self.data_bbox, x_factor, y_factor,
            self.top.kwargs['log'] or self.bottom.kwargs['log'],
            self.left.kwargs['log'] or self.right.kwargs['log'],)

        # Comunicate to each *Plotter object the data bounding box and the
        # SVG plot bounding box.
        for plotter, use_raster_fallback in self.plot_layers:
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
                          height='%.2f' % (svg_y_max - svg_y_min))

        # Draw all the parts of the plot.
        for p_layer, use_raster_fallback in self.plot_layers:
            if use_raster_fallback:
                # find appropriate transforms, i.e. starting at (0, 0)
                # going to width, height
                # XXX TODO: check for off-by-ones!!!!
                img_width = svg_target_bbox[2] - svg_target_bbox[0]
                img_height = abs(svg_target_bbox[3] - svg_target_bbox[1])
                assert img_width > 0
                assert img_height > 0
                img_bbox = [0, img_height, img_width, 0]
                # Add explicit check for logarithmic axes, if present
                # blow up for now. (maybe?)
                xtr2, ytr2 = setup_transforms(self.data_bbox, img_bbox,
                                              x_log=False, y_log=False)
                try:
                    p_layer.rdraw(root_element, xtr2, ytr2, svg_target_bbox)
                except NotImplementedError:
                    p_layer.draw(root_element, xtr, ytr)
            else:
                p_layer.draw(root_element, xtr, ytr)

        # Remove the *AxisPlotters from the parts of the plot again.
        if self.draw_axes:
            self.plot_layers = self.plot_layers[0:-4]
        self.data_bbox = None

        if False:
            rect = ET.SubElement(root_element, 'rect')
            rect.set('x', '%.2f' % (self.svg_bbox[0] + DATA_PADDING))
            rect.set('y', '%.2f' % (self.svg_bbox[1] + DATA_PADDING))
            rect.set('width', '%.2f' % (self.svg_bbox[2] - self.svg_bbox[0] -
                     2 * DATA_PADDING))
            rect.set('height', '%.2f' % (self.svg_bbox[3] - self.svg_bbox[1] -
                     2 * DATA_PADDING))
            rect.set('stroke', 'blue')
            rect.set('fill', 'none')

    def set_minimum_data_bbox(self, bbox):
        self.set_minimum_x_range(bbox[0], bbox[2])
        self.set_minimum_y_range(bbox[1], bbox[3])

    def set_minimum_x_range(self, min_x, max_x):
        self.x_min_range = (min_x, max_x)

    def set_minimum_y_range(self, min_y, max_y):
        self.y_min_range = (min_y, max_y)

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
