# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 06:08:47 2020

@author: Bayron
"""

import matplotlib as mpl
from os import listdir
from os.path import isfile, join
from matplotlib import font_manager
import os

# =============================================================================
# Set global custom style plot
# =============================================================================


class _styleBase(object):
    # Variables
    __axes_color__ = "#0B0201"
    __ticks_color__ = '#0B0201'
    __font_scale__ = 1.1
    __rc_plot__ = {'grid.linestyle': 'dashed',
                   'lines.linewidth': 2.8,
                   #    'axes.labelcolor': __axes_color__,
                   #    'axes.edgecolor': __ticks_color__,
                   #    'ytick.color': __ticks_color__,
                   #    'xtick.color': __ticks_color__,
                   'font.weight': 'normal'}
    __default_font__ = 'Cambria'


# =============================================================================
# Seawolf Style class
# =============================================================================


class StyleSW(_styleBase):

    def set(figsize=None, font_weight='normal', font_family=None, fontsize=None,
            rc: dict = None):

        if rc is None:
            rc = {}

        if figsize is None:
            mpl.rcParams['figure.figsize'] = (12, 10)
        elif type(figsize) is tuple:
            mpl.rcParams['figure.figsize'] = figsize

        if font_family is not None:
            rc['font.family'] = font_family

        for i, k in rc.items():
            _styleBase.__rc_plot__[i] = k

        if fontsize is None:
            fontsize = mpl.rcParams['figure.figsize'][0]
        elif fontsize > 10:
            _styleBase.__rc_plot__['font.size'] = fontsize * 0.85
            _styleBase.__rc_plot__['figure.titlesize'] = fontsize * 1.8
            _styleBase.__rc_plot__['ytick.labelsize'] = fontsize * 0.7
            _styleBase.__rc_plot__['xtick.labelsize'] = fontsize * 0.7
            _styleBase.__rc_plot__['axes.labelsize'] = fontsize * 0.7
            _styleBase.__rc_plot__['legend.fontsize'] = fontsize * 0.5
            _styleBase.__rc_plot__['legend.title_fontsize'] = fontsize * 0.65
        else:
            _styleBase.__rc_plot__['font.size'] = 10
            _styleBase.__rc_plot__['figure.titlesize'] = 'x-large'
            _styleBase.__rc_plot__['ytick.labelsize'] = 'medium'
            _styleBase.__rc_plot__['xtick.labelsize'] = 'medium'
            _styleBase.__rc_plot__['axes.labelsize'] = 'medium'
            _styleBase.__rc_plot__['legend.fontsize'] = 'small'

        _styleBase.__rc_plot__['font.weight'] = font_weight
        mpl.rcParams.update(_styleBase.__rc_plot__)

    def addPathFonts(font_path=''):
        onlyfiles = [f for f in listdir(
            font_path) if isfile(join(font_path, f))]
        for of in onlyfiles:
            font_manager.fontManager.addfont(font_path + of)
            prop = font_manager.FontProperties(fname=font_path + of)
            print(prop.get_name())

    def setFont(font_name: str = 'Cambria'):
        if font_name == _styleBase.__default_font__:
            StyleSW.addPathFonts(os.path.dirname(
                os.path.abspath(__file__)) + '\\fonts\\')
        mpl.rcParams['font.family'] = 'sans-serif'
        mpl.rcParams['font.sans-serif'] = font_name

    def reset_default():
        _styleBase.__rc_plot__
        mpl.rcdefaults()
        mpl.rcParams['figure.figsize'] = (12, 10)

    def get_axesColor():
        return _styleBase.__axes_color__

    def get_ticksColor():
        return _styleBase.__ticks_color__

    def get_figSize():
        return mpl.rcParams['figure.figsize']

    def set_style(name: str = 'seaborn'):
        lst_style = mpl.style.available
        if name is not None:
            if name in lst_style:
                a = mpl.style.context(name)
                return a
            else:
                raise NameError('Style names valid are: {0}'.format(lst_style))
        else:
            raise NameError('None type is not a valid style')

    def get_figsize():
        return mpl.rcParams['figure.figsize']
