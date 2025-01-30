# =============================================================================
# Tools for Axes manage
# =============================================================================
import math
from operator import contains
from string import Template

import matplotlib as _mpl
import matplotlib.patheffects as path_effects
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from ._style import StyleSW as style


class _axTools(object):

    __keys__ = {
            "color": style.get_ticksColor(),
            "colors": style.get_ticksColor(),
            "shadow" : 0,
            "shadow_color": style.get_axesColor(),
            "xpad": 0,
            "ypad": 0,
            "rotation": 0
        }

    artistList = (_mpl.patches.Wedge,
                  _mpl.patches.Ellipse,
                  _mpl.patches.Circle,
                  _mpl.patches.Shadow,
                  _mpl.lines.Line2D,
                  _mpl.collections.PathCollection,
                  _mpl.collections.PolyCollection)

    def gca(ax):
            return plt.gca()

    def orient(ax=None):
        orient = 'v'
        factor = 0
        axes = _axTools.get_axes(ax)
        rects = axes[0].patches
        if len(rects) > 0:
            for _, t in enumerate(axes):
                rects = t.patches
                if len(rects) > 1:
                    if not isinstance(rects[0], _mpl.patches.Wedge):
                        q = [round(x.get_width(), 2) for x in rects]
                        if (all(x == q[0] for x in q)):
                            orient = 'v'
                            factor = q[0]
                        else:
                            orient = 'h'
                            factor = rects[0].get_height()
                elif len(rects) == 1:
                    if not isinstance(rects[0], _mpl.patches.Wedge):
                        if (rects[0].get_x() == 0):
                            orient = 'h'
                        else:
                            orient = 'v'
        return orient, factor

    def get_axes(ax=None):
        axes = []
        if isinstance(ax, sns.axisgrid.FacetGrid):
            axes = ax.axes[0]
        elif isinstance(ax, list):
            axes = ax
        else:
            axes = [ax]
        return axes

    def getColorList(size: int, color):
        colors = list()
        if type(color) is str:
            colors = [color] * size
        elif type(color) is list:
            miss = size - len(color)
            if miss < 0:
                colors = color[:size]
            elif miss > 0:
                colors = color
                for i in range(0, miss):
                    colors.append('white')
            else:
                colors = color
        return colors

    def values_bars(ax=None, normBy: str() = 'c', loc: str() = 'top', stack=False):
        pos = 0
        orient, _ = _axTools.orient(ax)
        data = pd.DataFrame(columns=['x', 'y', 'value', 'value_norm',
                                     'index_color','ax', 'type', 'color'])
        data = data.astype({'x': 'float32', 'y': 'float32',
                            'value': 'float32','ax': 'int32',
                            'index_color': 'int32', })
        axes = _axTools.get_axes(ax)
        # Getting values
        for k, t in enumerate(axes):
            hist = {}
            rects = t.patches
            if len(rects) > 1:
                for rect in rects:
                    if not isinstance(rect, _mpl.patches.Wedge):
                        color = rect.get_fc()
                        h = 0
                        if orient == 'v':
                            value = (0 if math.isnan(rect.get_height()) else rect.get_height())
                            x = rect.get_x() + rect.get_width() / 2
                            if stack:
                                h = hist[x] if x in hist else 0
                            hist[x] = y = value + h
                        elif orient == 'h':
                            value = (0 if math.isnan(rect.get_width()) else rect.get_width())
                            y = rect.get_y() + rect.get_height() / 2
                            if stack:
                                h = hist[y] if y in hist else 0
                            hist[y] = x = value + h
                        data.loc[pos] = (x, y, value, 0, 0, int(k), 'bar', color)
                        pos = pos+1
            elif len(rects) == 1:
                rect = rects[0]
                if not isinstance(rect, _mpl.patches.Wedge):
                    color = rect.get_fc()
                    if orient == 'h':
                        value = x = rect.get_width()
                        y = rect.get_x()
                    elif orient == 'v':
                        value = y = rect.get_height()
                        x = rect.get_y()
                    data.loc[pos] = (x, y, value, 0, 0, int(k), 'bar', color)

        # Grouping data by condition
        if normBy == 'g':
            if isinstance(ax, sns.axisgrid.FacetGrid):
                data.loc[:, 'index_color'] = data.loc[:, 'ax']
            else:
                for i, color in enumerate(data['color'].unique()):
                    dt = data[data['color'] == color]
                    data.loc[dt.index, 'index_color'] = i
        elif normBy == 'c':
            if orient == 'v':
                data.loc[:, 'index_color'] = data.loc[:,'x'].round(0).astype('int')
            else:
                data.loc[:, 'index_color'] = data.loc[:,'y'].round(0).astype('int')
        data.drop('color', axis=1, inplace=True)

        # Set position values
        vals = data.loc[:, 'value']
        vals = vals.apply(lambda x: x if x > 0 else -x)
        if loc == 'center':
            vals = vals.apply(lambda x: x/2)
        if orient == 'v':
            if loc in ['bottom', "center"]:
                data.loc[:, 'y'] = data.loc[:, 'y'] - vals
        else:
            if loc in ['bottom', "center"]:
                data.loc[:, 'x'] = data.loc[:, 'x'] - vals
        return data

    def values_line(ax, orient):
        lnum = 0
        data = pd.DataFrame(
            columns=['x', 'y', 'value', 'value_norm', 'index_color', 'ax', 'type'])
        axes = _axTools.get_axes(ax)
        for l in axes[0].lines:
            if orient == 'v':
                y = l.get_ydata()
                if not np.isnan(y).any():
                    lnum += 1
                else:
                    x = l.get_xdata()
                    if not np.isnan(x).any():
                        lnum += 1
        if lnum > 0:
            x_all = list()
            y_all = list()
            ax_all = list()
            color_all = list()

            for ax in axes:
                lines = ax.lines
                if len(lines) > 0:
                    for l in enumerate(lines):
                        y = l[1].get_ydata()
                        ax_all.extend(y.tolist())
                        color_all.extend(y.tolist())
                        if all(isinstance(p, str) for p in y):
                            y = list(np.arange(0, len(y)))
                        for _ in y:
                            x = l[1].get_xdata()
                            if any(isinstance(p, str) for p in x):
                                x = list(np.arange(0, len(x)))
                        if len(x) > 0 and len(y) > 0:
                            x_all.extend(x)
                            y_all.extend(y)
            # Set value location
            if orient == 'h':
                data['x'] = x_all
                data['y'] = y_all
                data['value'] = x_all
            else:
                data['y'] = y_all
                data['x'] = x_all
                data['value'] = y_all
            # Set other columns values
            data['index_color'] = color_all
            data['ax'] = 0
            data['type'] = 'line'
            data['value_norm'] = 0
        # Setting data types
        data = data[data['index_color'].notna()]
        data = data.astype({'index_color': 'int32', 'ax': 'int32'})
        data = data[pd.notna(data['value'])].reset_index()
        return data.drop('index', axis=1)

    def values_points(ax):
        data = pd.DataFrame(columns=['x', 'y', 'value', 'value_norm',
                                     'index_color', 'ax', 'type'])
        axes = _axTools.get_axes(ax)
        # Getting value points
        for i, h in enumerate(axes):
            d = h.collections
            for d1 in d:
                data1 = pd.DataFrame()
                values = d1.get_offsets().tolist()
                if len(values) > 0:
                    rg = range(len(values))
                    data1['x'] = [v[0] for v in values]
                    data1['y'] = [v[1] for v in values]
                    data1['value'] = [v[1] for v in values]
                    data1['index_color'] = [0 for x in rg]
                    data1['ax'] = [i for x in rg]
                    data1['type'] = ['point' for x in rg]
                    data1['value_norm'] = 0
                    data = pd.concat([data, data1])
        return data

    def plot_values(ax=None, data: pd.DataFrame = None,
                    minvalue: float = 0.0, maxvalue: float = 0.0,
                    dec: int = 2, ha: str = 'auto', va: str = 'auto',
                    fontsize=_mpl.rcParams['font.size'],
                    fontweight: str = 'normal', color='black',
                    display: str = 'v',
                    orient: str = 'v', **kwargs):
        # Initial variables
        template = _axTools.template_print_value(display)

        if isinstance(fontsize, str) != True:
            fontsize = fontsize * 0.6 if fontsize > 10 else fontsize - 2
        axes = _axTools.get_axes(ax)

        d , kwargs = _axTools.get_init_kwargs(kwargs=kwargs, clean=True)
        shadow = d['shadow']
        rotation = d['rotation']
        shadow_color = d['shadow_color']

        # Check if is Digit function
        def isDigit(x):
            try:
                x = float(x)
                return True
            except ValueError:
                return False

        # Segment data with True values
        data = data[data['value'].notnull()].copy().reset_index(inplace=False,
                                                                drop=True)
        colors = _axTools.getColorList(data.shape[0], color)
        # Setting data types
        if dec > 0:
            vector = data['value'].to_numpy()
            for i, row in enumerate(vector):
                if isinstance(row, (float)):
                    vector[i] = round(row, dec)
            data['value'] = vector
        else:
            data['value'] = data['value'].astype('int32')
        # Print values
        for k, g in enumerate(axes):
            data_sub = data[(data['ax'] == k)]
            for c, row in zip(colors, data_sub.to_numpy()):
                x = row[0]
                y = row[1]
                value = row[2]
                value_norm = round(row[3]*100, dec)
                graph = row[6]
                if isDigit(value):
                    valid_value = True if (value >= minvalue and value <= maxvalue) else False
                else:
                    valid_value = True

                if (valid_value):
                    # Choosing graph type
                    if graph == 'bar':
                        if orient == 'v':
                            if va == 'auto':
                                va_h = 'bottom' if y >= 0 else 'top'
                            else:
                                va_h = va
                            ha_h = 'center' if ha == 'auto' else ha

                        else:
                            if ha == 'auto':
                                ha_h = 'right' if x > 0 else 'left'
                            else:
                                ha_h = ha
                            va_h = 'center_baseline' if va == 'auto' else va

                        text = g.text(x, y,
                                      template.substitute(value=value,
                                                          value_norm=value_norm),
                                      fontsize=fontsize, color=c, rotation=rotation,
                                      ha=ha_h, va=va_h, fontweight=fontweight, **kwargs)
                    else:
                        ha_h = 'center' if ha == 'auto' else ha
                        va_h = 'center_baseline' if va == 'auto' else va
                        if graph == 'line':
                            text = g.text(
                                x, y, template.substitute(value=value,
                                                          value_norm=value_norm),
                                fontsize=fontsize, color=c,
                                ha=ha_h, va=va_h,
                                fontweight=fontweight, **kwargs)
                        elif graph == 'point':
                            text = g.text(x, y, value, fontsize=fontsize, ha=ha_h,
                                          va=va_h, color=c, **kwargs)
                    if shadow > 0:
                        text.set_path_effects([
                            path_effects.Stroke(
                                linewidth=shadow, foreground=shadow_color, alpha=.8),
                            path_effects.Normal()])

    def normalize_data(df: pd.DataFrame = None):
        data = df.copy(deep=True)
        # Normalize data values
        grp = data.groupby(['type', 'index_color'],
                           as_index=False)['value'].sum()
        for row in data.itertuples():
            total = grp['value'][(grp['type'] == row.type) & (
                grp['index_color'] == row.index_color)].values[0]
            data['value_norm'] = data['value']/total
        return data

    def values_pie(ax, valid_wedges, frm, fontsize, dec, minvalue):
        data = pd.DataFrame()
        x = y = list()
        val_list = label_list = list()
        for i, p in enumerate(valid_wedges):
            val = (p.theta2 - p.theta1)
            ang = (p.theta2 - p.theta1)/2. + p.theta1
            y.append(np.sin(np.deg2rad(ang)))
            x.append(np.cos(np.deg2rad(ang))-0.2)
            val_list.append((val/360)*100)
            label_list.append(p.get_label())
        data['x'] = x
        data['y'] = y
        data['val'] = val_list
        data['labels'] = label_list
        # Setting bbox style
        bbox_props = dict(boxstyle="round",
                          ec=(0.1, 0.1, 0.1, 0.2),
                          fc=(1., 1.0, 0.9, 0.75))
        kw = dict(bbox=bbox_props, zorder=99, va="center")
        # Printing data
        for i in range(data.shape[0]):
            if data.val[i] > minvalue:
                value = frm % np.round(data.val[i], dec) + "%"
                ax.annotate(value,
                            xy=(data.x[i], data.y[i]),
                            fontsize=fontsize,
                            xytext=((.75*data.x[i]), (.45*data.y[i])), **kw)
        return data

    def template_print_value(display: str = str()):
        if display == 'fv':
            template = Template('$value_norm%\n($value)')
        elif display == 'fh':
            template = Template('$value_norm% ($value)')
        elif display == 'v':
            template = Template('$value')
        elif display == 'p':
            template = Template('$value_norm%')
        else:
            raise ValueError(
                'The alternatives for display are "f=full", "v=values" or "p=percent"')
        return template

    def get_init_kwargs(kwargs, defaults: dict={}, clean=False) -> tuple:

        dic_args = {}
        values = list()

        for k, v in _axTools.__keys__.items():
            values.append(kwargs.get(k, v))
        dic_args = dict(zip(_axTools.__keys__, values))

        for k, v in defaults.items():
            dic_args[k] = v

        if clean:
            for key in _axTools.__keys__:
                if key in kwargs:
                    del kwargs[key]

        return dic_args, kwargs