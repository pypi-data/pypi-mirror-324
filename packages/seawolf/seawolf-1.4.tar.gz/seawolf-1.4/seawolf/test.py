# -*- coding: utf-8 -*-
"""
Created on Sat May 23 07:40:01 2020

@author: Bayron
"""

import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import seawolf as sw
import time

url = "https://raw.github.com/mattdelhey/kaggle-titanic/master/Data/train.csv"
titanic = pd.read_csv(url)
# print(titanic.columns)

sw.style.set(figsize=(8, 6))

ax = sns.countplot(data=titanic, y="pclass", hue='sex')
sw.show_values( minvalue=100, maxvalue=200,
    ax=ax, dec=0, color="black", fontweight="bold", loc="top"
)
# sw.set_values(dec=1, values=[1,2,3,4,5,6], color='red')
sw.set_legend(
    title="Sexo",
    ncols=1,
    labels=["Hombre", "Mujer"],
    label_fontsize=8,
    title_fontsize=10,
    title_loc="center",
    borderpad=1.22,
)
sw.set_title(title="Tabla 3", fontweight="bold")
sw.set_subtitle(title="Conteo de sobrevivientes")
sw.set_tickslabel(
    axis="y",
    labelrotation=0,
    loc='in',
    xpad=0,
    ypad=0,
    color="blue",
    # colors = ['white', 'red', 'white'],
    shadow=0.5,
    shadowcolor="black",
    labels=["Baja", "Media", "Alta"],
)
sw.theme(op='spine', left=True, bottom=True, spine_butt='left')
ax.xaxis.grid(True)
ax.set_axisbelow(True)
plt.show()