'''
Some tests of the rasterized fallback mode.
'''
import sys
import random

from brp.svg.base import SVGCanvas
from brp.svg.base import PlotContainer
from brp.svg.plotters.scatter import ScatterPlotter
from brp.svg.plotters.error import ErrorPlotter
from brp.svg.plotters.symbol import RADECSymbol, SquareSymbol

if __name__ == '__main__':

    cv = SVGCanvas(1200, 1800)

# ------------------------------------------------------
# -- For debugging RADECSymbol raster fallback ---------

    NPULSARS = 100
    P = [random.uniform(0.001, 10) for i in range(NPULSARS)]
    DM = [random.uniform(1, 100) for i in range(NPULSARS)]
    RA = [random.uniform(0, 24) for i in range(NPULSARS)]
    DEC = [random.uniform(-90, 90) for i in range(NPULSARS)]
    SIGMA = [random.uniform(2, 15) for i in range(NPULSARS)]

    # plot
    pc = PlotContainer(0, 0, 600, 400)
    pc.add(ScatterPlotter(P, DM, RA, DEC, SIGMA, symbol=RADECSymbol))
    cv.add(pc)

    pc = PlotContainer(600, 0, 600, 400)
    pc.add(ScatterPlotter(P, DM, RA, DEC, SIGMA, symbols=[RADECSymbol]),
           raster=True)
    cv.add(pc)

# ------------------------------------------------------
# -- For debugging error bar raster fallback -----------

# LINEAR TRANSFORM CASE:

#    c = PlotContainer(0, 400, 600, 400, x_log=True, y_log=True)
    c = PlotContainer(600, 400, 600, 400)
    data_y = [10, 10, 20, 30, 40, 50, 40, 30, 20, 10, 10]
    data_x = [110, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    err_y = [(5, 5) for i in range(len(data_y))]
    ep = ErrorPlotter(data_x, data_y, symbols=[SquareSymbol],
                      err_y=err_y, err_x=err_y)
    c.add_plotter(ep)
    data_x1 = [2, 6, 43, 67]
    data_y1 = [45, 12, 85, 34]
    error_y = [(7, 4), (8, 8), (5, 5), (3, 9)]
    ep1 = ErrorPlotter(data_x1, data_y1, err_y=error_y, color='green')
    c.add(ep1, raster=True)
    ep2 = ErrorPlotter(data_y1, data_x1, err_x=error_y, color='red')
    c.add_plotter(ep2, raster=True)

    cv.add(c)

#    c = PlotContainer(600, 400, 600, 400, x_log=True, y_log=True)
    c = PlotContainer(0, 400, 600, 400)
    data_y = [10, 10, 20, 30, 40, 50, 40, 30, 20, 10, 10]
    data_x = [110, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    ep = ErrorPlotter(data_x, data_y, symbols=[SquareSymbol],
                      err_y=err_y, err_x=err_y)
    c.add_plotter(ep)
    err_y = [(5, 5) for i in range(len(data_y))]
    data_x1 = [2, 6, 43, 67]
    data_y1 = [45, 12, 85, 34]
    error_y = [(7, 4), (8, 8), (5, 5), (3, 9)]
    ep1 = ErrorPlotter(data_x1, data_y1, err_y=error_y, color='green')
    c.add(ep1, raster=False)
    ep2 = ErrorPlotter(data_y1, data_x1, err_x=error_y, color='red')
    c.add_plotter(ep2)

    cv.add(c)

# LOGARITHMIC TRANFORM CASE:

    c = PlotContainer(600, 800, 600, 400, x_log=True, y_log=True)
    data_y = [10, 10, 20, 30, 40, 50, 40, 30, 20, 10, 10]
    data_x = [110, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    err_y = [(5, 5) for i in range(len(data_y))]
    ep = ErrorPlotter(data_x, data_y, symbols=[SquareSymbol],
                      err_y=err_y, err_x=err_y)
    c.add_plotter(ep)
    data_x1 = [2, 6, 43, 67]
    data_y1 = [45, 12, 85, 34]
    error_y = [(7, 4), (8, 8), (5, 5), (3, 9)]
    ep1 = ErrorPlotter(data_x1, data_y1, err_y=error_y, color='green')
    c.add(ep1, raster=True)
    ep2 = ErrorPlotter(data_y1, data_x1, err_x=error_y, color='red')
    c.add_plotter(ep2, raster=True)

    cv.add(c)

    c = PlotContainer(0, 800, 600, 400, x_log=True, y_log=True)
    data_y = [10, 10, 20, 30, 40, 50, 40, 30, 20, 10, 10]
    data_x = [110, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    ep = ErrorPlotter(data_x, data_y, symbols=[SquareSymbol],
                      err_y=err_y, err_x=err_y)
    c.add_plotter(ep)
    err_y = [(5, 5) for i in range(len(data_y))]
    data_x1 = [2, 6, 43, 67]
    data_y1 = [45, 12, 85, 34]
    error_y = [(7, 4), (8, 8), (5, 5), (3, 9)]
    ep1 = ErrorPlotter(data_x1, data_y1, err_y=error_y, color='green')
    c.add(ep1, raster=False)
    ep2 = ErrorPlotter(data_y1, data_x1, err_x=error_y, color='red')
    c.add_plotter(ep2)

    cv.add(c)


# ------------------------------------------------------
# ------------------------------------------------------

    cv.draw(sys.stdout)
