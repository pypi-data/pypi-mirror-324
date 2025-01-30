# -*- coding: utf-8 -*-
"""
Created on Sun May 24 05:58:23 2020

@author: Bayron Torres
"""
import matplotlib as _mpl
import matplotlib.patheffects as path_effects
import numpy as _np
import seaborn as _sns
from matplotlib import pyplot as _plt
from matplotlib.axis import Tick

from ._axesTools import _axTools
from ._style import StyleSW as style

# =============================================================================
# Principal Axis class (implements new methods here)
# =============================================================================


def set_axislabel(
    ax=None, xlabel: str = str(), ylabel: str = str(), **kwargs
) -> _plt.Axes:
    ax = _axTools.gca(ax)
    # Getting initial vars
    d, kwargs = _axTools.get_init_kwargs(kwargs, defaults={"fontweight": "bold"})

    # Setting font style
    font = {"color": d["color"], "fontweight": d["fontweight"], "size": d["fontsize"]}

    # If not FaceGrid plot
    if isinstance(ax, _sns.axisgrid.FacetGrid):
        # If is FaceGrid plot
        if isinstance(ax.axes[0], _mpl.axes.Axes):
            ncols = ax.axes[0].get_subplotspec().get_gridspec().get_geometry()[1]
            tam_grp = len(ax.axes)
            is_axes = True
            iterate_group = ax.axes
        else:
            is_axes = False
            iterate_group = ax.axes[0]
        xlabel_ = iterate_group[0].get_xlabel()
        ylabel_ = iterate_group[0].get_ylabel()
        # Iter for each plot
        for i, a in enumerate(iterate_group):
            if xlabel is None:
                xlabel_ = ""
            elif len(xlabel) > 0:
                xlabel_ = xlabel
            if ylabel is None:
                ylabel_ = ""
            elif len(ylabel) > 0:
                ylabel_ = ylabel
            if is_axes:
                if (i + 1 + ncols) > tam_grp:
                    xlabel_ = xlabel
                else:
                    xlabel_ = ""
                if i % ncols != 0:
                    ylabel_ = ""
            else:
                if i > 0:
                    ylabel_ = ""
            a.set_xlabel(xlabel_, fontdict=font, labelpad=d["xpad"])
            a.set_ylabel(ylabel_, fontdict=font, labelpad=d["ypad"])
    else:
        if xlabel is None:
            xlabel = ""
        elif len(xlabel) == 0:
            xlabel = ax.get_xlabel()
        if ylabel is None:
            ylabel = ""
        elif len(ylabel) == 0:
            ylabel = ax.get_ylabel()
        ax.set_xlabel(xlabel, fontdict=font, labelpad=d["xpad"])
        ax.set_ylabel(ylabel, fontdict=font, labelpad=d["ypad"])
    return ax


def get_axislabel(ax=None) -> tuple:
    ax = _axTools.gca(ax)
    x = ax.get_xlabel()
    y = ax.get_ylabel()
    return x, y


def get_tickslabel(ax=None) -> tuple:
    ax = _axTools.gca(ax)
    y = [y.get_text() for y in ax.get_yticklabels()]
    x = [x.get_text() for x in ax.get_xticklabels()]
    return x, y


def set_tickslabel(
    ax=None, axis: str = "x", visible: bool = True,
    labels: list = [], rotation: int = 0, loc="default",
    bgcolors=list(), **kwargs,
) -> _plt.Axes:

    ax = _axTools.gca(ax)
    d, kwargs = _axTools.get_init_kwargs(kwargs)
    shadow_line =d["shadow"]

    fig = ax.get_figure()
    fig.canvas.draw()

    if axis in ["x", "y"]:
        if visible == False:
            if axis == "x":
                ax.axes.xaxis.set_visible(False)
            elif axis == "y":
                ax.axes.yaxis.set_visible(False)
            return

        if axis == "x":
            ticklabels = ax.get_xticklabels()
            ax.xaxis.set_ticks_position(loc)
        elif axis == "y":
            ticklabels = ax.get_yticklabels()
            ax.yaxis.set_ticks_position(loc)

        labels_ax = [t.get_text() for t in ticklabels]

        if isinstance(labels, list):
            if labels:
                del labels[len(ticklabels):]
                for i in [*range(0, len(labels))]:
                    labels_ax[i] = labels[i]
        elif isinstance(labels, dict):
            for i, v in zip(labels.keys(), labels.values()):
                labels_ax[i] = v

        if len(bgcolors) > 0:
            del bgcolors[len(ticklabels):]
            bbox = dict(boxstyle="square", alpha=0.3)
            for i, c in enumerate(bgcolors):
                ticklabels[i].set_bbox(bbox)
                ticklabels[i].set_backgroundcolor(c)

        if axis == "x":
            ax.xaxis.set_ticks([l.get_position()[0] for l in ticklabels],
                            labels=labels_ax,
                            rotation=rotation,
                            weight="normal"
                            )

        elif axis == "y":
            ax.yaxis.set_ticks([l.get_position()[1] for l in ticklabels],
                            labels=labels_ax,
                            rotation=rotation,
                            weight="normal"
                            )

        if shadow_line > 0:
            shadow_color = kwargs.get("shadow_color", d["shadow_color"])
            effects = [
                path_effects.Stroke(
                    linewidth=shadow_line,
                    foreground=shadow_color,
                    alpha=0.8,
                ),
                path_effects.Normal(),
            ]
            for t in ticklabels:
                t.set_path_effects(effects)
    else:
        raise ValueError("axis value {0} is not available".format(axis))

    return ax


def theme(
    op="spine",
    top: bool = False,
    right: bool = False,
    left: bool = False,
    bottom: bool = False,
    despine_trim: bool = False,
    despine_offset: int = 0,
    spine_butt="left",
    ax=None,
):
    ax = _axTools.gca(ax)
    options = ["despine", "spine", "clear"]
    if not op in options:
        raise ValueError("Value is not in '{0}'".format(options))

    if op == options[0]:
        _sns.despine(
            top=top,
            right=right,
            left=left,
            bottom=bottom,
            trim=despine_trim,
            offset=despine_offset,
        )

    elif op == options[1]:
        ax.spines["left"].set_visible(left)
        ax.spines["top"].set_visible(top)
        ax.spines["bottom"].set_visible(bottom)
        ax.spines["right"].set_visible(right)
        ax.spines[spine_butt].set_lw(1.5)
        ax.spines[spine_butt].set_capstyle("butt")

    elif op == options[2]:
        orient = _axTools.orient(ax)
        _sns.despine(top=True, bottom=True, right=True, left=True, trim=True, offset=3)
        if orient == "v":
            ax.get_yaxis().set_visible(False)
        elif orient == "h":
            ax.get_xaxis().set_visible(False)
        set_axislabel(xlabel=None, ylabel=None)

    else:
        _sns.despine(top=True, bottom=False, right=False, left=False, trim=False)

    return ax


def set_title(ax=None, title: str = str(), loc: str = "left", **kwargs) -> None:
    d, kwargs = _axTools.get_init_kwargs(
        kwargs,
        defaults={
            "fontweight": "bold",
            "color": "black",
            "fontsize": _mpl.rcParams["figure.titlesize"],
        },
    )

    if loc == "center":
        pos = 0.5
    elif loc == "left":
        pos = 0.0
    elif loc == "right":
        pos = 0.96
    else:
        pos = 0.0
        loc = "left"

    if ax is None:
        ax = _axTools.gca(ax)

    # Check if set figure or Axesplot
    if isinstance(ax, _mpl.axes.SubplotBase):
        ax = _axTools.gca(ax)
        ax.set_title(
            label=title,
            x=pos + d["xpad"],
            y=1.05 + d["ypad"],
            verticalalignment="bottom",
            horizontalalignment=loc,
            color=d["color"],
            fontweight=d["fontweight"],
            fontsize=d["fontsize"],
        )

    elif isinstance(ax, _mpl.figure.Figure):
        _plt.suptitle(
            title,
            y=1 + d["ypad"],
            x=pos + d["xpad"],
            verticalalignment="bottom",
            horizontalalignment=loc,
            fontsize=d["fontsize"],
            fontweight=d["fontweight"],
            color=d["color"],
        )


def set_subtitle(ax=None, title: str = str(), loc: str = "left", **kwargs) -> None:
    ax = _axTools.gca(ax)
    d, kwargs = _axTools.get_init_kwargs(kwargs)

    ad = 0.04 if (isinstance(ax, _mpl.figure.Figure)) else 0
    if loc == "center":
        pos = 0.50
    elif loc == "left":
        pos = 0 + ad
    elif loc == "right":
        pos = 1 - ad
    else:
        pos = 0.048
        loc = "left"

    if isinstance(ax, _mpl.axes._subplots.SubplotBase):
        txt = ax.text(
            x=pos + d["xpad"],
            y=1.02 + d["ypad"],
            s=title,
            transform=ax.transAxes,
            fontsize=d["fontsize"],
            fontweight=d["fontweight"],
            horizontalalignment=loc,
            verticalalignment="bottom",
        )
        _plt.setp(txt, color=d["color"])
    elif isinstance(ax, _mpl.figure.Figure):
        ax.text(
            s=title,
            x=pos + d["xpad"],
            y=1 + d["ypad"],
            fontsize=d["fontsize"],
            fontweight=d["fontweight"],
            color=d["color"],
            horizontalalignment=loc,
            verticalalignment="bottom",
        )


def set_legend(
    ax=None,
    show: bool = True,
    title: str = None,
    ncols: int = 1,
    loc=0,
    title_fontsize=None,
    title_loc: str = "left",
    label_fontsize=None,
    labels: list() = None,
    handles: list() = None,
    borderpad=0.82,
    **kwargs,
) -> _plt.Axes.legend:
    legend = None

    if type(loc) is tuple:
        bbox_to_anchor = loc
        loc = 0
    else:
        bbox_to_anchor = None

    if label_fontsize is None:
        label_fontsize = _mpl.rcParams["legend.fontsize"]
    if title_fontsize is None:
        title_fontsize = _mpl.rcParams["legend.fontsize"]

    propF = {"weight": "normal", "size": label_fontsize}

    if not isinstance(ax, _mpl.figure.Figure):
        ax = _axTools.gca(ax)

        if show:
            leg = ax.legend()
            leg = ax.legend(["Graph 1"]) if leg is not None else leg

            if title == "" and ax.get_legend() != None:
                title = ax.get_legend().get_title().get_text()
                title = title.capitalize()
            elif title is None:
                ax.legend_.set_title(None)

            if handles is None or labels is None:
                handles1, legs1 = ax.get_legend_handles_labels()
                handles = handles1 if handles is None else handles
                labels = legs1 if labels is None else labels
                for h, l in zip(handles, labels):
                    h.set_label(l)

            if not handles:
                print("No legend to show")
        else:
            # Remove legend
            l = ax.get_legend()
            if l is not None:
                l.remove()
    else:
        axs = list()
        loc = 8 if loc == 0 else loc

        if ax is None:
            axs = ax.axes
        else:
            if isinstance(ax, list):
                axs.extend(ax)
            else:
                axs.append(ax)
            for a in ax.axes:
                leg = a.legend(["Graph 1"])
                leg.remove()

        handles, legs = list(), list()
        ax.legends = []
        for a in axs:
            h, l = a.get_legend_handles_labels()
            handles.extend(h)
            legs.extend(l)
        legs = labels if labels is not None else legs

    legend = ax.legend(
        title=title,
        handles=handles,
        prop=propF,
        labels=labels,
        loc=loc,
        title_fontsize=title_fontsize,
        borderpad=borderpad,
        ncol=ncols,
        bbox_to_anchor=bbox_to_anchor,
        **kwargs,
    )

    if not title_loc in ["left", "right", "center"]:
        title_loc = "left"
    legend._legend_box.align = title_loc
    legend.get_title().set_position((0, 5))

    return legend


def get_values(
    ax=None, kind: str = "bar", normalized: bool = False, normBy="c", stack=False
):
    ax = _axTools.gca(ax)
    data = None
    if kind == "bar":
        data = _axTools.values_bars(ax=ax, normBy=normBy, stack=stack)
    elif kind == "line":
        data = _axTools.values_line(ax=ax, orient="v")
    elif kind == "point":
        data = _axTools.values_points(ax=ax)
    if normalized and data is not None:
        return _axTools.normalize_data(data)
    else:
        return data


def show_values(
    ax=None,
    dec: int = 1,
    minvalue: int = -_np.Infinity,
    maxvalue: int = _np.Infinity,
    loc: str = "top",
    kind: str = "bar",
    normBy: str = "c",
    display: str = "v",
    stack=False,
    **kwargs,
) -> _plt.Axes:
    ax = _axTools.gca(ax)
    orient = "v"

    d, kwargs = _axTools.get_init_kwargs(kwargs)

    if dec == None:
        dec = 2 if display != "v" else 1

    if kind not in ["bar", "line", "point"]:
        raise ValueError("kind is not in bar, line or point")

    # Bars
    if kind == "bar":
        orient, _ = _axTools.orient(ax)
        data = _axTools.values_bars(ax=ax, normBy=normBy, loc=loc, stack=stack)
        if display != "v":
            data = _axTools.normalize_data(data)

    # Lines shape
    elif kind == "line":
        data = _axTools.values_line(ax, "v")

        # For y values
        for u in data["index_color"].unique():
            df = data.loc[data["index_color"] == u]
            dfy = df["y"].to_numpy()
            dfy_len = len(dfy)
            new_dat = [0] * dfy_len
            for i in range(0, dfy_len):
                j = i + 1
                if i == dfy_len - 1:
                    j = i - 1
                if dfy[i] < dfy[j]:
                    new_dat[i] = dfy[i] - d["ypad"]
                else:
                    new_dat[i] = dfy[i] + d["ypad"]
            data.loc[data["index_color"] == u, "y"] = new_dat

        # For x values
        data["x"] = data["x"] + d["xpad"]

        # Normalizing data
        if display != "v":
            data = _axTools.normalize_data(data)

    # Points shape
    elif kind == "point":
        data = _axTools.values_points(ax)
        # Normalizing data
        if display != "v":
            data = _axTools.normalize_data(data)

    # Add spacing for the data
    if kind != "line":
        if d["xpad"] != 0:
            data["x"] = [x + d["xpad"] if x >= 0 else x - d["xpad"] for x in data["x"]]
        if d["ypad"] != 0:
            data["y"] = [y + d["ypad"] if y >= 0 else y - d["ypad"] for y in data["y"]]

    # Print values on plot
    _axTools.plot_values(
        ax=ax,
        data=data,
        minvalue=minvalue,
        maxvalue=maxvalue,
        dec=dec,
        display=display,
        orient=orient,
        **kwargs
    )


def set_values(
    ax=None,
    values=list(),
    dec: int = 1,
    minvalue: int = -_np.Infinity,
    maxvalue: int = _np.Infinity,
    loc: str = "top",
    kind: str = "bar",
    display: str = "v",
    stack=False,
    **kwargs,
):
    orient = "v"

    ax = _axTools.gca(ax)
    d, _ = _axTools.get_init_kwargs(kwargs=kwargs)

    if values is not None or not isinstance(values, (list)):
        if kind == "bar":
            data = _axTools.values_bars(ax=ax, normBy="c", loc=loc, stack=stack)
            orient, _ = _axTools.orient(ax)
        elif kind == "line":
            data = _axTools.values_line(ax=ax, orient=orient)
        elif kind == "point":
            data = _axTools.values_points(ax=ax)

        # Add spacing for the data
        xpad = d["xpad"]
        ypad = d["ypad"]
        if kind != "line":
            if xpad != 0:
                data["x"] = [x + xpad if x >= 0 else x - xpad for x in data["x"]]
            if ypad != 0:
                data["y"] = [y + ypad if y >= 0 else y - ypad for y in data["y"]]

        if data.shape[0] >= len(values):
            n_items = len(values)
        else:
            n_items = data.shape[0]
        data["value"] = values[:n_items]

        _axTools.plot_values(
            ax=ax,
            data=data,
            minvalue=minvalue,
            maxvalue=maxvalue,
            dec=dec,
            display=display,
            orient=orient,
            **kwargs,
        )

    else:
        raise ValueError("`Values` data type is invalid")


def set_figsize(figsize):
    try:
        _plt.figure(figsize=figsize, dpi=80)
    except:
        raise ValueError("Figsize value has incorrect")


def get_figsize():
    return _mpl.rcParams["figure.figsize"]


def set_alpha(ax=None, alpha: float = 1.0):
    if ax is not None:
        if isinstance(ax, _mpl.axes.Axes):
            ch = ax.get_children()
            for c in ch:
                if isinstance(c, _axTools.artistList):
                    c.set_alpha(alpha)
                elif isinstance(c, _mpl.patches.Rectangle):
                    """All rectangles and not background rectangle"""
                    if (
                        not float(c.get_width()) == 1.0
                        and not float(c.get_height()) == 1.0
                    ):
                        c.set_alpha(alpha)
