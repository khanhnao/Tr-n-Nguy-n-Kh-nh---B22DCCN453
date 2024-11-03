import pandas as pd
from sklearn.cluster import KMeans
import numpy as np

df = pd.read_csv('result.csv')
drop_cols = ['Name', 'Nation', 'Team', 'Position']
df = df.drop(columns = drop_cols)
df.head()


kmeans = KMeans(n_clusters=3, random_state=0)
df['cluster'] = kmeans.fit_predict(df[['Age', 'Minutes']])
centroids = kmeans.cluster_centers_

cen_x = [i[0] for i in centroids]
cen_y = [i[1] for i in centroids]

df['cen_x'] = df.cluster.map({0:cen_x[0], 1:cen_x[1], 2:cen_x[2]})
df['cen_y'] = df.cluster.map({0:cen_y[0], 1:cen_y[1], 2:cen_y[2]})
colors = ['#DF2020', '#81DF20', '#2095DF']
df['c'] = df.cluster.map({0:colors[0], 1:colors[1], 2:colors[2]})

import matplotlib.pyplot as plt
plt.scatter(df.Age, df.Minutes, c=df.c, alpha = 0.6, s=10)#s is size, c is color

plt.scatter(df.Age, df.Minutes, c=df.c, s=df.Minutes, alpha = 0.6)
plt.show()
