import base64
import copy
import StringIO
from xml.sax.saxutils import escape

from brp.svg.et_import import ET 
from brp.svg.plotters.raster import RasterPlotterMixin

def png2data_url(png_file):
    encoded_png = StringIO.StringIO()
    encoded_png.write('data:image/png;base64,\n')
    try:
        f = open(png_file, 'rb')
        try:
            base64.encode(f, encoded_png)
        finally:
            f.close()
    except OSError, e:
        raise
    return encoded_png.getvalue()

class PNGWrapperPlotter(RasterPlotterMixin):
    def __init__(self, png_file, min_x, min_y, max_x, max_y):
        self.encoded_png = png2data_url(png_file)
        self.img_bbox = [min_x, min_y, max_x, max_y]


