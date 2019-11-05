from pydataset import data
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")
import matplotlib.pyplot as plt
from matplotlib import cm
import seaborn as sns
from sklearn.cluster import KMeans
from mpl_toolkits.mplot3d import Axes3D
from wrangle_zillow import get_db_url
from env import host, user, password

iris = data('iris')

iris.rename(columns={'Sepal.Length': 'sepal_length',
                     'Sepal.Width': 'sepal_width',
                     'Petal.Length': 'petal_length',
                     'Petal.Width': 'petal_width',
                     'Species': 'species'}, inplace=True)

X = iris[['sepal_length', 'petal_length', 'sepal_width']]

kmeans = KMeans(n_clusters=4)
kmeans.fit(X)

centers = pd.DataFrame(kmeans.cluster_centers_, columns=X.columns)

fig = plt.figure(figsize=(12, 9))
ax = Axes3D(fig)

ax.scatter(iris.sepal_length, iris.petal_length, iris.sepal_width, c=kmeans.labels_)
ax.scatter(centers.sepal_length, centers.petal_length, centers.sepal_width, c='pink', s=10000, alpha=.4)
ax.set(xlabel='sepal_length', ylabel='petal_length', zlabel='sepal_width')

# 3 is probably the optimal number of clusters since we have 3 different species
kmeans3 = KMeans(n_clusters=3)
kmeans3.fit(X)

centers = pd.DataFrame(kmeans3.cluster_centers_, columns=X.columns)

fig = plt.figure(figsize=(12, 9))
ax = Axes3D(fig)

ax.scatter(iris.sepal_length, iris.petal_length, iris.sepal_width, c=kmeans3.labels_)
ax.scatter(centers.sepal_length, centers.petal_length, centers.sepal_width, c='pink', s=10000, alpha=.4)
ax.set(xlabel='sepal_length', ylabel='petal_length', zlabel='sepal_width')

db_name = 'mall_customers'
query = 'select * from customers;'
url = get_db_url(user, host, password, db_name)
mall = pd.read_sql(query, url)

X = mall[['annual_income', 'spending_score']]

sns.scatterplot(x='spending_score', y='annual_income', data=mall)
plt.show()
# Probably 5 clusters

mallmeans = KMeans(n_clusters=5)
mallmeans.fit(X)

centers = pd.DataFrame(mallmeans.cluster_centers_, columns=X.columns)

mall['cluster'] = mallmeans.labels_
mall.groupby('cluster').age.mean()

fig = plt.figure(figsize=(12, 9))
ax = Axes3D(fig)

ax.scatter(mall.spending_score, mall.annual_income, mall.age, c=mallmeans.labels_)
ax.set(xlabel='spending_score', ylabel='annual_income', zlabel='age')
plt.show()

tips = data('tips')
tips.tip = tips.tip.astype('float')
X = tips[['tip', 'total_bill']]

tipmeans = KMeans(n_clusters=3)
tipmeans.fit(X)

centers = pd.DataFrame(tipmeans.cluster_centers_, columns=X.columns)

tips['cluster'] = tipmeans.labels_
tips.groupby('cluster')['size'].mean()

tips['smoker'] = tips.smoker.map({'Yes': 1, 'No': 0})
tips.groupby('cluster').smoker.mean()

tips['rate'] = tips.tip / tips.total_bill
tips.groupby('cluster').rate.mean()

fig = plt.figure(figsize=(12, 9))
ax = Axes3D(fig)

ax.scatter(tips.tip, tips.total_bill, tips['size'], c=tipmeans.labels_)
ax.set(xlabel='tip', ylabel='total_bill', zlabel='size')
plt.show()