'''
Module containing the base class for all plotters (defining their API).
'''

class BasePlotter(object):
    '''Base class for ..Plotter class definitions, defines interface.'''
    def __init__(self):
        pass

    def prepare_bbox(self, data_bbox):
        '''Update data boundingbox in a way that is appropriate.'''
        return data_bbox

    def done_bbox(self, data_bbox, svg_bbox):
        '''Callback, is called when data and SVG bounding boxes are known.'''
        pass

    def draw(self, root_element, x_transform, y_transform):
        '''Draw the graphical element that is represented by this plotter.'''
        pass

