from __future__ import division
from xml.sax.saxutils import escape

from brp.core.tickmarks import find_tickmarks_log, find_tickmarks

from brp.svg.et_import import ET

from brp.svg.constants import AXIS_SIZE, TICKMARK_LABEL_SPACING, FONT_SIZE
from brp.svg.constants import UNITS_PER_TICKMARK


def get_tickmarks(length, interval, use_log, **options):
    n_tickmarks = length // UNITS_PER_TICKMARK
    if use_log:
        tickmarks = options.get('tickmarks',
                                find_tickmarks_log(interval, n_tickmarks))
    else:
        tickmarks = options.get('tickmarks',
                                find_tickmarks(interval, n_tickmarks))

    return tickmarks


def draw_left_axis(root_element, x_offset, y_offset, height, y_transform,
                   interval, use_log, **options):
    '''
    Draw left axis.

    arguments:
        `root_element` --- ElementTree Element instance, receives the drawing
            commands.
        `x_offset` --- The horizontal offset in SVG screen coordinates of the
            axis.
        `y_offset` --- The vertical offset in SVG screen coordinates of the
            axis.
        `y_transform` --- Transformation function that transforms y data
            coordinates to y SVG screen coordinates.
        `interval` --- Interval in y data coordinates that the axis covers.

        `use_log` --- Boolean, True if axis is to be treated as logarithmic.

    key word arguments:
        `tickmarks` --- list of tickmarks. Tickmarks are tuples like:
            (position, size) with position and size numbers.
        `label` --- Text that labels this axis.

        `hide_label` --- Boolean, True if label should be hidden.

        `hide_tickmarks` --- Boolean, True if tickmarks should be hidden.

        `hide_tickmarklabels` --- Boolean, True if tickmarks and labels for
            this axis should be hidden.
    '''

    color = options.get('color', 'black')

    axes_lines = ET.SubElement(root_element, 'g')
    axes_lines.set('stroke', color)

    axes_text = ET.SubElement(root_element, 'g')
    axes_text.set('fill', color)

    line = ET.SubElement(axes_lines, 'line')
    line.set('x1', '%.2f' % (x_offset + AXIS_SIZE))
    line.set('y1', '%.2f' % (y_offset + AXIS_SIZE))
    line.set('x2', '%.2f' % (x_offset + AXIS_SIZE))
    line.set('y2', '%.2f' % (y_offset + height - AXIS_SIZE))

    hide_tickmarks = options.get('hide_tickmarks', False)

    if not hide_tickmarks:
        tickmarks = get_tickmarks(height, interval, use_log, **options)
        hide_tickmarklabels = options.get('hide_tickmarklabels', False)

        for y, size in tickmarks:
            ny = y_transform(y)
            tm = ET.SubElement(axes_lines, 'line')
            tm.set('x1', '%.2f' % (x_offset + AXIS_SIZE))
            tm.set('x2', '%.2f' % (x_offset + AXIS_SIZE + size * 0.7))
            tm.set('y1', '%.2f' % (ny))
            tm.set('y2', '%.2f' % (ny))
            tm.set('stroke', color)

            if hide_tickmarklabels:
                continue
            if size != 10:
                continue

            ticklabel = ET.SubElement(axes_text, 'text')
            ticklabel.set('font-size', str(FONT_SIZE))
            ticklabel.set('text-anchor', 'middle')
            ticklabel.set('x', '%.2f' % (x_offset + AXIS_SIZE -
                          TICKMARK_LABEL_SPACING)),
            ticklabel.set('y', '%.2f' % ny)
            ticklabel.set('transform', 'rotate(%d %.2f %.2f)' %
                          (-90, x_offset + AXIS_SIZE - TICKMARK_LABEL_SPACING,
                          ny))
            ticklabel.text = escape(str(y))

    hide_label = options.get('hide_label', False)
    label_link = options.get('label_link', None)
    if not hide_label:
        if label_link:
            axes_text = ET.SubElement(axes_text, 'a')
            axes_text.set('xlink:href', label_link)

        lbl = ET.SubElement(axes_text, 'text')
        lbl.set('font-size', str(FONT_SIZE))
        lbl.set('text-anchor', 'middle')
        lbl.set('x', '%.2f' % (x_offset + AXIS_SIZE -
                TICKMARK_LABEL_SPACING - 2 * FONT_SIZE)),
        lbl.set('y', '%.2f' % (y_offset + 0.5 * height))
        lbl.set('transform', 'rotate(%d %.2f %.2f)' %
                (-90, x_offset + AXIS_SIZE - TICKMARK_LABEL_SPACING - 2 *
                 FONT_SIZE, y_offset + 0.5 * height))
        label = options.get('label', 'Y LABEL')
        lbl.text = escape(label)


def draw_top_axis(root_element, x_offset, y_offset, width, x_transform,
                  interval, use_log, **options):
    '''
    Draw top axis.

    See the documentation for brp.svg.plotters.axes_procedural.draw_left_axis
    '''
    color = options.get('color', 'black')

    axes_lines = ET.SubElement(root_element, 'g')
    axes_lines.set('stroke', color)

    axes_text = ET.SubElement(root_element, 'g')
    axes_text.set('fill', color)

    line = ET.SubElement(axes_lines, 'line')
    line.set('x1', '%.2f' % (x_offset + AXIS_SIZE))
    line.set('y1', '%.2f' % (y_offset + AXIS_SIZE))
    line.set('x2', '%.2f' % (x_offset + width - AXIS_SIZE))
    line.set('y2', '%.2f' % (y_offset + AXIS_SIZE))

    hide_tickmarks = options.get('hide_tickmarks', False)

    if not hide_tickmarks:
        tickmarks = get_tickmarks(width, interval, use_log, **options)
        hide_tickmarklabels = options.get('hide_tickmarklabels', False)

        for x, size in tickmarks:
            nx = x_transform(x)
            tm = ET.SubElement(axes_lines, 'line')
            tm.set('x1', '%.2f' % (nx))
            tm.set('x2', '%.2f' % (nx))
            tm.set('y1', '%.2f' % (y_offset + AXIS_SIZE))
            tm.set('y2', '%.2f' % (y_offset + AXIS_SIZE + size * 0.7))

            if hide_tickmarklabels:
                continue
            if size != 10:
                continue

            ticklabel = ET.SubElement(axes_text, 'text')
            ticklabel.set('font-size', str(FONT_SIZE))
            ticklabel.set('text-anchor', 'middle')
            ticklabel.set('y', '%.2f' %
                          (y_offset + AXIS_SIZE - TICKMARK_LABEL_SPACING)),
            ticklabel.set('x', '%.2f' % nx)
            ticklabel.text = escape(str(x))

    hide_label = options.get('hide_label', False)
    label_link = options.get('label_link', None)
    if not hide_label:
        if label_link:
            axes_text = ET.SubElement(axes_text, 'a')
            axes_text.set('xlink:href', label_link)
        lbl = ET.SubElement(axes_text, 'text')
        lbl.set('font-size', str(FONT_SIZE))
        lbl.set('text-anchor', 'middle')
        lbl.set('y', '%.2f' %
                (y_offset + AXIS_SIZE - TICKMARK_LABEL_SPACING -
                    2 * FONT_SIZE)),
        lbl.set('x', '%.2f' % (x_offset + 0.5 * width))
        label = options.get('label', 'X LABEL')
        lbl.text = escape(label)


def draw_bottom_axis(root_element, x_offset, y_offset, width, x_transform,
                     interval, use_log, **options):
    '''
    Draw bottom axis.

    See the documentation for brp.svg.plotters.axes_procedural.draw_left_axis
    '''
    color = options.get('color', 'black')

    axes_lines = ET.SubElement(root_element, 'g')
    axes_lines.set('stroke', color)

    axes_text = ET.SubElement(root_element, 'g')
    axes_text.set('fill', color)

    line = ET.SubElement(axes_lines, 'line')
    line.set('x1', '%.2f' % (x_offset + AXIS_SIZE))
    line.set('y1', '%.2f' % (y_offset + AXIS_SIZE))
    line.set('x2', '%.2f' % (x_offset + width - AXIS_SIZE))
    line.set('y2', '%.2f' % (y_offset + AXIS_SIZE))

    hide_tickmarks = options.get('hide_tickmarks', False)

    if not hide_tickmarks:
        tickmarks = get_tickmarks(width, interval, use_log, **options)
        hide_tickmarklabels = options.get('hide_tickmarklabels', False)

        for x, size in tickmarks:
            nx = x_transform(x)
            tm = ET.SubElement(axes_lines, 'line')
            tm.set('x1', '%.2f' % (nx))
            tm.set('x2', '%.2f' % (nx))
            tm.set('y1', '%.2f' % (y_offset + AXIS_SIZE))
            tm.set('y2', '%.2f' % (y_offset + AXIS_SIZE - size * 0.7))

            if hide_tickmarklabels:
                continue
            if size != 10:
                continue

            ticklabel = ET.SubElement(axes_text, 'text')
            ticklabel.set('font-size', str(FONT_SIZE))
            ticklabel.set('text-anchor', 'middle')
            ticklabel.set('y', '%.2f' % (y_offset + AXIS_SIZE +
                          TICKMARK_LABEL_SPACING + 0.5 * FONT_SIZE)),
            ticklabel.set('x', '%.2f' % nx)
            ticklabel.text = escape(str(x))

    hide_label = options.get('hide_label', False)
    label_link = options.get('label_link', None)
    if not hide_label:
        if label_link:
            axes_text = ET.SubElement(axes_text, 'a')
            axes_text.set('xlink:href', label_link)
        lbl = ET.SubElement(axes_text, 'text')
        lbl.set('font-size', str(FONT_SIZE))
        lbl.set('text-anchor', 'middle')
        lbl.set('y', '%.2f' %
                (y_offset + AXIS_SIZE + TICKMARK_LABEL_SPACING + 2.5 *
                 FONT_SIZE)),
        lbl.set('x', '%.2f' % (x_offset + 0.5 * width))
        label = options.get('label', 'X LABEL')
        lbl.text = escape(label)


def draw_right_axis(root_element, x_offset, y_offset, height, y_transform,
                    interval, use_log, **options):
    '''
    Draw right axis.

    See the documentation for brp.svg.plotters.axes_procedural.draw_left_axis
    '''
    color = options.get('color', 'black')

    axes_lines = ET.SubElement(root_element, 'g')
    axes_lines.set('stroke', color)

    axes_text = ET.SubElement(root_element, 'g')
    axes_text.set('fill', color)

    line = ET.SubElement(axes_lines, 'line')
    line.set('x1', '%.2f' % (x_offset + AXIS_SIZE))
    line.set('y1', '%.2f' % (y_offset + AXIS_SIZE))
    line.set('x2', '%.2f' % (x_offset + AXIS_SIZE))
    line.set('y2', '%.2f' % (y_offset + height - AXIS_SIZE))

    hide_tickmarks = options.get('hide_tickmarks', False)

    if not hide_tickmarks:
        tickmarks = get_tickmarks(height, interval, use_log, **options)
        hide_tickmarklabels = options.get('hide_tickmarklabels', False)

        for y, size in tickmarks:
            ny = y_transform(y)
            tm = ET.SubElement(axes_lines, 'line')
            tm.set('x1', '%.2f' % (x_offset + AXIS_SIZE))
            tm.set('x2', '%.2f' % (x_offset + AXIS_SIZE - size * 0.7))
            tm.set('y1', '%.2f' % (ny))
            tm.set('y2', '%.2f' % (ny))

            if hide_tickmarklabels:
                continue
            if size != 10:
                continue

            ticklabel = ET.SubElement(axes_text, 'text')
            ticklabel.set('font-size', str(FONT_SIZE))
            ticklabel.set('text-anchor', 'middle')
            ticklabel.set('x', '%.2f' % (x_offset + AXIS_SIZE +
                          TICKMARK_LABEL_SPACING + 0.5 * FONT_SIZE)),
            ticklabel.set('y', '%.2f' % ny)
            ticklabel.set('transform', 'rotate(%d %.2f %.2f)' %
                          (-90, x_offset + AXIS_SIZE + TICKMARK_LABEL_SPACING +
                          0.5 * FONT_SIZE, ny))
            ticklabel.text = escape(str(y))

    hide_label = options.get('hide_label', False)
    label_link = options.get('label_link', None)
    if not hide_label:
        if label_link:
            axes_text = ET.SubElement(axes_text, 'a')
            axes_text.set('xlink:href', label_link)
        lbl = ET.SubElement(axes_text, 'text')
        lbl.set('font-size', str(FONT_SIZE))
        lbl.set('text-anchor', 'middle')
        lbl.set('x', '%.2f' %
                (x_offset + AXIS_SIZE + TICKMARK_LABEL_SPACING +
                 2.5 * FONT_SIZE)),
        lbl.set('y', '%.2f' % (y_offset + 0.5 * height))
        lbl.set('transform', 'rotate(%d %.2f %.2f)' %
                (-90, x_offset + AXIS_SIZE + TICKMARK_LABEL_SPACING +
                 2.5 * FONT_SIZE, y_offset + 0.5 * height))
        label = options.get('label', 'Y LABEL')
        lbl.text = escape(label)
