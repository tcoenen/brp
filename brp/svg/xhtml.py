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

class XHTMLCanvas(object):
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
        root = ET.Element('html')
        root.set('xmlns', 'http://www.w3.org/1999/xhtml')
        body = ET.SubElement(root, 'body')
        t = ET.SubElement(body, 'h1')
        t.text = 'XHTML TEST'
        l = ET.SubElement(body, 'a')
        l.set('href', 'http://www.slashdot.org')
        l.text = 'link?'
        
        r = ET.SubElement(root, 'svg')
        r.set('xmlns', 'http://www.w3.org/2000/svg')
        r.set('xmlns:xlink', 'http://www.w3.org/1999/xlink')
        r.set('height', '%.2f' % self.height)
        r.set('width', '%.2f' % self.width)
        r.set('version', '1.1')
        # TODO : Figure out the exact corner coordinates given width and 
        # height for an SVG file.
        rect = ET.SubElement(r, 'rect')
        rect.set('x', '0')
        rect.set('y', '0')
        rect.set('width', '%.2f' % self.width) 
        rect.set('height', '%.2f' % self.height) 
        rect.set('fill', self.background_color)


        for c in self.containers:
            c.draw(r)

        tree = ET.ElementTree(root)
        tree.write(file)


