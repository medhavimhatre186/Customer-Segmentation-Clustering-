import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score

# ==========================
# Load Dataset
# ==========================
df = pd.read_csv("data/Mall_Customers.csv")

print("\nFirst 5 Rows:")
print(df.head())

# ==========================
# Feature Selection
# ==========================
X = df[['Annual Income (k$)', 'Spending Score (1-100)']]

# ==========================
# Feature Scaling
# ==========================
scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)

print("\nFeature Scaling Applied Successfully!")

# ==========================
# K-Means Clustering
# ==========================
kmeans = KMeans(
    n_clusters=5,
    random_state=42,
    n_init=10
)

df['Cluster'] = kmeans.fit_predict(X_scaled)

# ==========================
# Silhouette Score
# ==========================
score = silhouette_score(X_scaled, df['Cluster'])

print("\nSilhouette Score:")
print(round(score, 4))

# ==========================
# Cluster Summary
# ==========================
print("\nCluster Summary:")

summary = df.groupby('Cluster').agg({
    'Age': 'mean',
    'Annual Income (k$)': 'mean',
    'Spending Score (1-100)': 'mean'
}).round(2)

print(summary)

# ==========================
# Save Segmented Dataset
# ==========================
df.to_csv(
    "data/customer_segments.csv",
    index=False
)

print("\nSegmented Dataset Saved!")
print("File: data/customer_segments.csv")

# ==========================
# Visualization
# ==========================
plt.figure(figsize=(10,7))

sns.scatterplot(
    data=df,
    x='Annual Income (k$)',
    y='Spending Score (1-100)',
    hue='Cluster',
    palette='Set1',
    s=100
)

# Convert centroids back to original scale
centroids = scaler.inverse_transform(
    kmeans.cluster_centers_
)

plt.scatter(
    centroids[:,0],
    centroids[:,1],
    c='black',
    s=350,
    marker='X',
    label='Centroids'
)

plt.title("Customer Segmentation using K-Means")
plt.xlabel("Annual Income (k$)")
plt.ylabel("Spending Score (1-100)")
plt.legend()

# Save Graph
plt.savefig(
    "visuals/customer_segments.png"
)

print("\nGraph Saved!")
print("File: visuals/customer_segments.png")

plt.show()