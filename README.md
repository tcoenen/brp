brp
===

Browser Plot, small library to do static SVG 2d plots The brp library is not
a general replacement for Matplotlib. Developed on Python 2.6 and 2.7

Features
--------

* Scatter (with or without errors), line, 1d histogram plots
* 2d Histogram plots
* Data points can be color-coded and have shapes depending on values in data.
* Rasterized fallback implemented for busy scatter and line plots (using base64
  encoded PNGs embedded in the SVG files). This helps avoiding giant, slow to 
  render SVG files.

External dependencies
---------------------

* Python Imaging Library for raster image generation
* Numpy

Examples
--------

For some examples see the tests directory.
