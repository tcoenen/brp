'''
Some tests of the rasterized fallback mode.
'''
import sys
import random

from brp.svg.base import SVGCanvas
from brp.svg.base import PlotContainer
from brp.svg.plotters.scatter import ScatterPlotter
from brp.svg.plotters.symbol import RADECSymbol

if __name__ == '__main__':
# ------------------------------------------------------
# -- For debugging RASymbol raster fallback ------------

    NPULSARS = 100
    P = [random.uniform(0.001, 10) for i in range(NPULSARS)]
    DM = [random.uniform(1, 100) for i in range(NPULSARS)]
    RA = [random.uniform(0, 24) for i in range(NPULSARS)]
    DEC = [random.uniform(-90, 90) for i in range(NPULSARS)]
    SIGMA = [random.uniform(2, 15) for i in range(NPULSARS)]

    # plot
    cv = SVGCanvas(800, 600)
    pc = PlotContainer(0, 0, 800, 600)
    pc.add(ScatterPlotter(P, DM, RA, DEC, SIGMA, symbol=RADECSymbol))
    pc.add(ScatterPlotter(P, DM, RA, DEC, SIGMA, symbols=[RADECSymbol],
           color='red'), raster=True)
    cv.add(pc)
    cv.draw(sys.stdout)
