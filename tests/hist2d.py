#!/usr/bin/env python
'''
Test the 2d histogramming functions in brp (the NEW ones).
'''
from __future__ import division
import sys
from random import random as r

from brp.svg.base import SVGCanvas, PlotContainer
from brp.svg.plotters import newhist2d
from brp.svg.plotters.gradient import GradientPlotter
from brp.svg.plotters.line import LinePlotter

if __name__ == '__main__':

    x_data = [r() for i in range(1000)]
    y_data = [r() for i in range(1000)]

    cv = SVGCanvas(1200, 800)

    p = PlotContainer(0, 0, 600, 400)
    h = newhist2d.Histogram2dPlotter(x_data, y_data, x_bins=100)
    gr = h.get_gradient()
    collapsed_x, yvalues = h.collapse_x()
    xvalues, collapsed_y = h.collapse_y()
    p.add(h)
    cv.add(p)

    p = PlotContainer(800, 0, 160, 400)
    p.add(GradientPlotter(gr, 'vertical'))
    cv.add(p)

    p = PlotContainer(600, 0, 200, 400)
    p.add(LinePlotter(collapsed_x, yvalues))
    cv.add(p)

    p = PlotContainer(0, 400, 600, 200)
    p.add(LinePlotter(xvalues, collapsed_y))
    cv.add(p)

    cv.draw(sys.stdout)
