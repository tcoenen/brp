import sys
#sys.path.append('../')

from brp.svg.base import SVGCanvas, PlotContainer, TextFragment
from brp.svg.plotters.histogram import HistogramPlotter, merge_bins

if __name__ == '__main__':
    bins = [(0, 1, 10), (1, 2, 10), (2, 3, 11), (3, 4, 10), (4, 5, 10),
            (5, 6, 7)]

    cv = SVGCanvas(1200, 1200)

    # Histogram testing:
    c = PlotContainer(0, 0, 600, 400)
    c.add(HistogramPlotter(bins))
    cv.add(c)
    cv.add(TextFragment(100, 100, 'Unmerged bins', color='red'))

    merged = merge_bins(bins)

    c2 = PlotContainer(600, 0, 600, 400)
    c2.add(HistogramPlotter(merged))
    cv.add(c2)
    cv.add(TextFragment(700, 100, 'Merged bins', color='red'))

    cv.draw(sys.stdout)
