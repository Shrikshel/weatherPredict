# -*- coding: utf-8 -*-

import os
import datetime
from pandas import Series, DataFrame
import pandas as pd
import numpy as np
from scipy.spatial import distance
import matplotlib.pyplot as plt

df = pd.read_csv("weatherData/weather20042013.csv")
df['date'] = pd.to_datetime(df['date'])
df = df.set_index(df['date'])
cf = df.ix['2004':'2004']
#gf = df.ix['2012':'2012']
#aobo = DataFrame({"ao":df["rainfall"].ix['2013':'2013'], "bo":df["rainfall"].ix['2005':'2005']})
#df['mon'] = df.index.month
years = [2004, 2005, 2006]#[2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013]
#fig, axes = plt.subplots(nrows=4, ncols=3, figsize=(20,10))
#yC = 0
#for row in range(3):
#	for col in range(3):
#		monmean = df['rainfall'][str(years[yC]):str(years[yC])].groupby(df['mon']).aggregate(np.sum)
#		monmean.plot(kind='bar', ax=axes[row,col], label=years[yC])
#		yC = yC + 1
fig, ax = plt.subplots()
for year in years:
	#ax.plot(pd.rolling_sum(df['rainfall'].ix[str(year):str(year)], 30), label=str(year))
	ax.plot(df['rainfall'].ix[str(year):str(year)].resample('W'), label=str(year))
ax.set_xlabel('Year')
ax.set_ylabel('Rainfall')
ax.legend(loc=1)
plt.show()
