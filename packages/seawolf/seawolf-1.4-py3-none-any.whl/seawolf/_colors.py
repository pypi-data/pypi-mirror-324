# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 09:57:59 2019

@author: bayron.torres
"""
import matplotlib as mpl

Category45 = ['#1B7256', '#379683', '#5CDB95', '#8EE4AF', '#8EE3D5',
              '#98D3E1', '#97CAEF', '#97BCEF', '#c293ed', '#E7717D',
              '#FC4445', '#C3073F', '#950740', '#6F2232', '#5D001E',
              '#b3476a', '#c9718e', '#edbbcc', '#C1C8E4', '#84CEEB',
              '#5AB9EA', '#5680E9', '#8860D0', '#A13E97', '#bd3ab1',
              '#c973bf', '#f075b7', '#FE929F', '#ffb3bc', '#fcdce0',
              '#FFD954', '#FEC804', '#F2AB39', '#CF9A41', '#CD7000',
              '#9B4F0F', '#CD5100', '#FF6602', '#F2A122', '#F2C022',
              '#F2DF22', '#E5F222', '#D8F573', '#B1F573', '#bdd6a7']

Category20 = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
              '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
              '#aec7e8', '#ffbb78', '#98df8a', '#ff9896', '#c5b0d5',
              '#c49c94', '#f7b6d2', '#c7c7c7', '#dbdb8d', '#9edae5']

Category10 = ['#01BEFE', '#F12000', '#1BCF28', '#FFDD00', '#8F00FF',
              '#F51899', '#FF7F0E', '#ADFF02', '#4081ED', '#FEA900']

Category6 = ['#01BEFE', '#FFDD00', '#FF8109', '#FF006D', '#ADFF02',
             '#8F00FF']

Colorblind = ['#0072b2', '#e69f00', '#f0e442', '#009e73', '#56b4e9', '#d55e00',
              '#cc79a7', 'black']

Dark = ['#1b9e77', '#d95f02', '#7570b3', '#e7298a', '#66a61e', '#e6ab02',
        '#a6761d', '#666666']

Pastel = ['#fbb4ae', '#b3cde3', '#ccebc5', '#decbe4', '#fed9a6', '#ffffcc',
          '#e5d8bd', '#fddaec', '#f2f2f2']

__all_list__ = {"cat45": Category45,
                "cat20": Category20,
                "cat10": Category10,
                "cat6": Category6,
                "colorblind": Colorblind,
                "dark": Dark,
                "pastel": Pastel}

# =============================================================================
# Set global custom style plot
# =============================================================================


class ColorsSW(object):

    def color_palette(palette=None, ini=0, n_colors=None):
        colors = list()
        rev = False

        if palette == None:
            palette = "cat10"
        elif palette.endswith("_r"):
            palette = palette[:-2]
            rev = True
        try:
            if palette in __all_list__:
                colors = __all_list__.get(palette)

            else:
                cmap = mpl.cm.get_cmap(palette)
                for i in range(cmap.N):
                    rgb = cmap(i)[:3]
                    colors.append(rgb)
        except ValueError as ex:
            print(str(ex) + " " +
                  "".join([", '" + x + "'" for x in __all_list__.keys()]))

        n = len(colors)
        if n_colors is None:
            n_colors = n
        if ini > n:
            raise ValueError('´´ini´´ value is not valid')

        colors = colors[ini: (ini+n_colors)]
        if rev:
            colors.reverse()
        return colors

    def hex_to_rgb(value):
        value = value.lstrip('#')
        lv = len(value)
        return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

    def rgb_to_hex(rgb):
        return '#%02x%02x%02x' % rgb

    def contrastColor(color):
        varHex = False
        if type(color) == str:
            varHex = True
            if color.find('#') == False:
                color = '#' + color
            color = ColorsSW.hex_to_rgb(color)

        if (type(color) == tuple):
            if len(color) == 3:
                contrast = (255-color[0], 255-color[1], 255-color[2])
                if (varHex):
                    contrast = ColorsSW.rgb_to_hex(contrast)
                return contrast
            else:
                raise ValueError('RGB color value is not valid')
        else:
            raise ValueError('COLOR value is not valid')
