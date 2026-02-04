import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, DBSCAN
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA

def main():
    # 1. Load Data
    try:
        df = pd.read_csv('../../D_RESULTS/training_dataset.csv')
    except FileNotFoundError:
        try:
            df = pd.read_csv('06_Model_Training_Evaluation/D_RESULTS/training_dataset.csv')
        except FileNotFoundError:
            print("Error: training_dataset.csv not found.")
            return

    print(f"Loaded training data with shape: {df.shape}")

    # 2. Select Features for Clustering
    # Goal: Automatic Market Segmentation
    # Features: RAM_GB, TOTAL_PIXELS, PPI
    
    features = ['RAM_GB', 'TOTAL_PIXELS', 'PPI']
    
    # Check if columns exist
    for f in features:
        if f not in df.columns:
            print(f"Error: Feature {f} not found in dataset.")
            return

    X = df[features].copy()
    
    # Handling missing values if any (though dataset should be cleaned)
    if X.isnull().sum().any():
        print("Warning: Missing values found. Dropping rows with missing values for clustering.")
        X = X.dropna()
        # Align df with X
        df = df.loc[X.index]

    print("Features selected for clustering:")
    print(X.head())

    # 3. Scaling
    # Numeric features must be scaled for distance-based algorithms like K-Means/DBSCAN
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # 4. K-Means Clustering
    # We'll try a few values of K to find the best Silhouette Score
    print("\n" + "="*50)
    print("Running K-Means Clustering...")
    
    best_k = 3
    best_score = -1
    best_model = None
    results = []

    # Testing K from 2 to 6
    for k in range(2, 7):
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = kmeans.fit_predict(X_scaled)
        score = silhouette_score(X_scaled, labels)
        print(f"K={k}, Silhouette Score: {score:.4f}")
        results.append({'K': k, 'Silhouette': score})
        
        if score > best_score:
            best_score = score
            best_k = k
            best_model = kmeans

    print(f"\nBest K selected: {best_k} with Silhouette Score: {best_score:.4f}")

    # 5. Apply Best K-Means
    final_labels = best_model.predict(X_scaled)
    df['Cluster'] = final_labels

    # 6. Cluster Analysis
    # Analyze how features and Price vary within clusters
    analysis_features = features + ['PRICE']
    cluster_stats = df.groupby('Cluster')[analysis_features].mean()
    cluster_counts = df['Cluster'].value_counts().rename("Count")
    
    cluster_summary = pd.concat([cluster_stats, cluster_counts], axis=1)
    
    print("\n" + "="*50)
    print("Cluster Analysis & Interpretation")
    print("="*50)
    print(cluster_summary)
    
    # Save Results to D_RESULTS
    cluster_summary.to_csv('../../D_RESULTS/Aya_Clustering_Summary.csv')
    print("\nAnalysis saved to '../../D_RESULTS/Aya_Clustering_Summary.csv'")

    # 7. Visualization (PCA)
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)
    
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=X_pca[:, 0], y=X_pca[:, 1], hue=df['Cluster'], palette='viridis', style=df['Cluster'], s=100)
    plt.title(f'Market Segmentation (K-Means, K={best_k})\nFeatures: RAM, Pixels, PPI')
    plt.xlabel('PCA Component 1')
    plt.ylabel('PCA Component 2')
    plt.legend(title='Cluster')
    plt.grid(True)
    
    plot_file = '../../D_RESULTS/Aya_Clustering_PCA_Plot.png'
    plt.savefig(plot_file)
    print(f"Cluster visualization saved to '{plot_file}'")
    
    # Interpretation Helper
    print("\nInterpretation Hints:")
    for cluster_id in cluster_summary.index:
        mb_ram = cluster_summary.loc[cluster_id, 'RAM_GB']
        avg_price = cluster_summary.loc[cluster_id, 'PRICE']
        
        label = "Unknown"
        if mb_ram >= 16 and avg_price > cluster_summary['PRICE'].median():
             label = "Potential High-End/Gaming"
        elif mb_ram <= 8:
            label = "Budget/Office"
        else:
            label = "Mainstream"
            
        print(f"Cluster {cluster_id}: Avg RAM={mb_ram:.1f}GB, Price={avg_price:.0f} DA -> {label}")

if __name__ == "__main__":
    main()
