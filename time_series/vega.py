from vega_datasets import data
import pandas as pd
import matplotlib.pyplot as plt

sf = data.sf_temps()
sf = sf.set_index('date').sort_index()

sf.resample('D').mean().plot()

sf.resample('D').max().plot()

sf.resample('D').min().plot()

sf.resample('M').mean().idxmin().temp.month

sf.resample('M').mean().idxmax().temp.month

extremes = sf.resample('D').agg(['min', 'max'])
extremes['diff'] = extremes.temp['max'] - extremes.temp['min']
extremes.resample('M').diff.mean().idxmax().month

plt.plot(sf.resample('D').mean())
plt.plot(sf.resample('D').min())
plt.plot(sf.resample('D').max())
plt.show()

seattle = data.seattle_weather().set_index('date').sort_index()
seattle.resample('M').precipitation.sum().idxmax()

seattle.resample('M').precipitation.sum().plot()

seattle.resample('W').wind.mean().plot()

seattle.resample('M').wind.mean().idxmax()

seattle['sunny'] = seattle['weather'] == 'sun'
seattle.resample('Y').sunny.sum().idxmax()

seattle.groupby(seattle.index.month).precipitation.sum().idxmax()

seattle['rained'] = seattle.precipitation > 0
seattle.groupby(seattle.index.month).rained.sum().idxmax()