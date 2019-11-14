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

flights = data.flights_20k().set_index('date').sort_index()

flights['delay'] = flights.delay.apply(lambda x: 0 if x < 0 else x)

flights.groupby(flights.index.hour).delay.mean().idxmax()

flights.groupby(flights.index.weekday_name).delay.mean() # Yes, Friday > Thursday > Wednesday > Sunday > Tuesday > Saturday > Monday

flights.groupby(flights.index.month).delay.mean() # Kind of but not really. I'd say it doesn't because the difference in mean times is a minute or so

iowa = data.iowa_electricity().set_index('year').sort_index()

totals = iowa.resample('Y').sum()

sf['desc'] = pd.qcut(x=sf.temp, q=4, labels=['cold', 'cool', 'warm', 'hot'])
