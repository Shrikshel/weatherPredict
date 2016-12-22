# -*- coding: utf-8 -*-

import os
import datetime
from pandas import Series, DataFrame
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
from mpltools import style
import seaborn as sns
import scipy.stats as stats
from pandas.tools.plotting import bootstrap_plot, radviz

df = pd.read_csv("weatherData/weather20042013.csv")
df['date'] = pd.to_datetime(df['date'])
cols = ['minTemp', 'maxTemp', 'rainfall', 'morningHumidity', 'eveningHumidity']

df['rainfall'] = df['rainfall'].astype(int)
df['maxTemp'] = df['maxTemp'].astype(int)
df['minTemp'] = df['minTemp'].astype(int)
df['zero'] = df["minTemp"].apply(lambda x : "1" if x >= 0 else "0")
df['year'] = df['date'].apply(lambda x : x.year)
df = df[df['rainfall'] > 0]

#bootstrap_plot(df['rainfall'], size=50, samples=500, color='grey')

#g = sns.FacetGrid(df, col="year", col_wrap=4)
#g.map(plt.scatter, "maxTemp", "minTemp")

#sns.corrplot(df)
#sns.lmplot("minTemp", "maxTemp", df, ci=50, x_jitter=.15, x_estimator=np.mean)
#sns.residplot("minTemp", "maxTemp", df, lowess=True)

#df = df[df['rainfall'] > 0]
#g = sns.factorplot('rainfall', data=df, palette="Blues")
#sns.kdeplot(df["maxTemp"], df["minTemp"], shade=False)
sns.jointplot("maxTemp", "minTemp", df, kind="kde")

#df.plot(kind='hexbin', x='minTemp', y='maxTemp', gridsize=25)
# df.plot(kind="scatter", x='minTemp', y='maxTemp', s=df["rainfall"]*10)
plt.show()

#g = sns.PairGrid(df.reset_index()[cols])
#g.map_diag(plt.hist)
#g.map_lower(sns.kdeplot, cmap="Blues_d")
#g.map_upper(plt.scatter)
#plt.savefig("test.png")
