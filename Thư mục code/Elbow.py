import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt

data = pd.read_csv('result.csv')

numeric_data = data.select_dtypes(include=['float64', 'int64'])

numeric_data = numeric_data.fillna(0)

if numeric_data.empty:
    print("Dữ liệu không hợp lệ hoặc không chứa dữ liệu số.")
else:
    X = numeric_data.values

numeric_data = numeric_data.dropna()

X = numeric_data.values

wcss = []
K_range = range(1, 11)
for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=0)
    kmeans.fit(X)
    wcss.append(kmeans.inertia_)

plt.figure(figsize=(8, 5))
plt.plot(K_range, wcss, marker='o', linestyle='-')
plt.xlabel('Số lượng cụm (k)')
plt.ylabel('WCSS')
plt.title('Phương pháp Elbow để xác định số cụm tối ưu')
plt.grid(True)
plt.show()


