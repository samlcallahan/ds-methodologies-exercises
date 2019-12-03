import pandas as pd
import numpy as np
from acquire import get_zillow
from prepare import prep_zillow
import split_scale as ss
from sklearn.cluster import DBSCAN
import seaborn as sns

zillow = prep_zillow(get_zillow())
cluster = zillow[['sqft', 'beds']]
cluster = ss.scale(cluster)[1]

names = {0: 'sqft', 1: 'beds'}
cluster = cluster.rename(columns=names)

dbsc = DBSCAN(eps = .10, min_samples = 20).fit(cluster)
zillow['labels'] = dbsc.labels_

sns.scatterplot(x='sqft', y='beds', hue='labels' data=zillow)
plt.scatter(x='sqft', y='beds', c='labels', data=zillow, legend=True)
plt.legend()
plt.show()