import sys
import random
#sys.path.append('../')

from brp.svg.base import SVGCanvas
from brp.svg.base import PlotContainer
from brp.svg.plotters.symbol import BaseSymbol, SquareSymbol, LineSymbol
from brp.svg.plotters.symbol import HorizontalErrorBarSymbol
from brp.svg.plotters.symbol import VerticalErrorBarSymbol, CrossHairSymbol
from brp.svg.plotters.symbol import RADECSymbol
from brp.svg.plotters.symbol import RasterDebugSymbol
from brp.svg.plotters.line import LinePlotter
from brp.svg.plotters.scatter import ScatterPlotter
from brp.svg.plotters.gradient import RGBGradient, GradientPlotter
from brp.svg.plotters.crosshair import CrossHairPlotter
from brp.svg.plotters.limit import XLimitPlotter, YLimitPlotter
from brp.svg.plotters.legend import LegendPlotter, UNDER_PLOT, BOTTOMLEFT
from brp.core.interval import stretch_interval
from brp.svg.plotters.histogram import HistogramPlotter, bin_data
from brp.svg.plotters.error import ErrorPlotter
from brp.svg.plotters.linkbox import LinkBox

if __name__ == '__main__':
    # Draw a simple scatter + line plot to SVG (dumped to standard out).
    cv = SVGCanvas(1000, 2500)
    c = PlotContainer(100, 100, 600, 400, background_color="white",
                      x_log=True, y_log=True)
    TMP = [10 * x + 10 for x in range(99)]
    TMP2 = [10 * x + 10 for x in range(99)]
    TMP2.reverse()

    gr = RGBGradient((200, 800), (1, 0, 0), (0, 0, 1))
    c.add_plotter(LinePlotter(TMP, TMP, gradient=gr, gradient_i=1,
                  symbol=BaseSymbol, linepattern='2 2 8 2'))
    c.add_plotter(ScatterPlotter(TMP, TMP2, symbol=BaseSymbol,
                  gradient=gr, gradient_i=0))
    c.add_plotter(CrossHairPlotter(500, 500))
    c.add_plotter(CrossHairPlotter(200, 700, color='red'))
    c.add_plotter(XLimitPlotter(300))
    c.add_plotter(YLimitPlotter(300))
    c.add_plotter(CrossHairPlotter(1e+6, 1e+6))
    c.add_plotter(ScatterPlotter([1000], [1000], symbol=CrossHairSymbol,
                  color='lime'))
    c.add_plotter(LinkBox((100, 100, 10000, 10000), 'http://www.slashdot.org'))

    c.left.set_interval(stretch_interval((10, 1000), 1.2, True), log=False)
    c.right.set_interval(stretch_interval((1000, 10), 1.2, True), log=False)
    c.bottom.set_interval((-100, 100), False)
    c.left.label_link('http://slashdot.org')
    c.right.label_link('http://slashdot.org')
    c.top.label_link('http://slashdot.org')
    c.bottom.label_link('http://slashdot.org')
    c.top.set_label('OH JOY!')
    cv.add_plot_container(c)

    # Histogram testing:
    c = PlotContainer(100, 500, 600, 400, background_color="white",
                      x_log=False, y_log=False)

    cp = LegendPlotter(position=UNDER_PLOT)
    colors = ['green', 'blue', 'red', 'gray', 'yellow', 'orange', 'lime']
    lps = ['6 2', '2 2', '4 4', '2 2 8 2', '']
    for ii in range(2):
        data = []
        for i in range(10000):
            data.append(random.randrange(100))
        bd = bin_data(data, 100)
        c.add_plotter(HistogramPlotter(bd, color='black',
            linepattern=lps[ii % len(lps)]))
        cp.add_entry('Blah Blah %d' % ii, symbols=[LineSymbol, BaseSymbol],
            color='black', linepattern=lps[ii % len(lps)])

    c.add_plotter(XLimitPlotter(99))
    c.add_plotter(XLimitPlotter(0))
    c.add_plotter(CrossHairPlotter(40, 100, color='red'))
    c.add_plotter(cp)
    c.add_plotter(LinkBox((10, 80, 50, 120), 'http://www.slashdot.org'))
    cv.add_plot_container(c)
# -- DEMO plot with error bars ------------------------

    c = PlotContainer(100, 1000, 600, 400, x_log=True, y_log=True)
    data_y = [10, 10, 20, 30, 40, 50, 40, 30, 20, 10, 10]
    data_x = [110, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    err_y = [(5, 5) for i in range(len(data_y))]
    ep = ErrorPlotter(data_x, data_y, symbols=[SquareSymbol],
                      err_y=err_y, err_x=err_y)
    c.add_plotter(ep)
    lp = LegendPlotter(position=BOTTOMLEFT)
    data_x1 = [2, 6, 43, 67]
    data_y1 = [45, 12, 85, 34]
    error_y = [(7, 4), (8, 8), (5, 5), (3, 9)]
    ep1 = ErrorPlotter(data_x1, data_y1, err_y=error_y, color='green')
    c.add_plotter(ep1)
    ep2 = ErrorPlotter(data_y1, data_x1, err_x=error_y, color='red')
    c.add_plotter(ep2)

    lp.add_entry('Blah', symbols=[HorizontalErrorBarSymbol,
        VerticalErrorBarSymbol, SquareSymbol])
    lp.add_entry('Blah', symbols=[VerticalErrorBarSymbol, BaseSymbol],
                 color='green')
    lp.add_entry('Blah', symbols=[HorizontalErrorBarSymbol, BaseSymbol],
                 color='red')
    c.add_plotter(lp)
    cv.add_plot_container(c)

# -- DEMO of 5 dimensional data in a scatter plot ----
# -- BASED on pulsar data ----------------------------
    NPULSARS = 100
    P = [random.uniform(0.001, 10) for i in range(NPULSARS)]
    DM = [random.uniform(1, 100) for i in range(NPULSARS)]
    RA = [random.uniform(0, 24) for i in range(NPULSARS)]
    DEC = [random.uniform(-90, 90) for i in range(NPULSARS)]
    SIGMA = [random.uniform(2, 15) for i in range(NPULSARS)]

    gr2 = RGBGradient((2, 15), (0, 0, 1), (1, 0, 0))

    c = PlotContainer(100, 1500, 600, 400)
    c.bottom.set_label('Pulse period (s)')
    c.top.set_label('Pulse period (s)')
    c.left.set_label('Dispersion measure (cm^-3 pc)')
    c.right.hide_label()
    c.right.hide_tickmarklabels()
    c.add_plotter(ScatterPlotter(P, DM, RA, DEC, SIGMA, symbol=RADECSymbol,
                  gradient=gr2, gradient_i=4))
    cv.add_plot_container(c)

    c = PlotContainer(620, 1500, 120, 400, data_padding=0)
    c.top.hide_all()
    c.bottom.hide_all()
    c.left.hide_label()
    c.left.hide_tickmarklabels()
    c.right.set_label('Significance (sigma)')
    c.add_plotter(GradientPlotter(gr2))
    cv.add_plot_container(c)
# ------------------------------------------------------
# -- For debugging raster fallback ---------------------

# The raster fallback might still have some off-by-one problems.

    gr = RGBGradient((0, 25), (0, 0, 1), (1, 0, 0))
    gr2 = RGBGradient((0, 25), (1, 0, 0), (0, 0, 1))
    c = PlotContainer(100, 1900, 600, 400)
    xdata = list(range(25))
    c.add_plotter(ScatterPlotter(xdata, symbols=[RasterDebugSymbol]), True)
    c.add_plotter(ScatterPlotter(xdata, symbols=[RasterDebugSymbol]))
    xdata.reverse()
    colors = ['yellow' for x in xdata]
    c.add_plotter(ScatterPlotter(xdata, symbols=[BaseSymbol], colors=colors))
    c.add_plotter(ScatterPlotter(xdata, gradient=gr, gradient_i=0), True)
    cv.add_plot_container(c)

#
# ------------------------------------------------------

    cv.draw(sys.stdout)
