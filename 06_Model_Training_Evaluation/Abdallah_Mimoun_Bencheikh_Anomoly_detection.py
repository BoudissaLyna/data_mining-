import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
import os
import matplotlib.pyplot as plt

# Locate the cleaned data
dataset_path = '../06_Model_Training_Evaluation/final_cleaned_dataset.csv'
if not os.path.exists(dataset_path):
    dataset_path = 'final_cleaned_dataset.csv'  # Fallback if running from root

# Load dataset
X = pd.read_csv(dataset_path)
print(f"Loaded {len(X)} records with {len(X.columns)} initial columns.")

# ---- SELECT ONLY NUMERIC FEATURES ----
numeric_cols = X.select_dtypes(include=[np.number])

if numeric_cols.empty:
    raise ValueError("No numeric columns found. Isolation Forest requires numeric features.")

# ---- SCALE DATA ----
scaler = StandardScaler()
X_scaled = scaler.fit_transform(numeric_cols)

# ---- ISOLATION FOREST MODEL ----
model = IsolationForest(
    n_estimators=200,
    contamination=0.05,
    random_state=42
)

# Fit and predict
X['anomaly_label'] = model.fit_predict(X_scaled)   # -1 = anomaly, 1 = normal
X['anomaly_score'] = model.decision_function(X_scaled)

# ---- TRUST SCORE (0 → low trust, 1 → high trust) ----
scores = X['anomaly_score']
X['trust_score'] = (scores - scores.min()) / (scores.max() - scores.min())

print(X[['anomaly_label', 'trust_score']].head(20))

print(X['anomaly_label'].value_counts())


# ---------- TRUST SCORE DISTRIBUTION ----------
plt.figure()
plt.hist(X['trust_score'], bins=50)
plt.xlabel('Trust Score')
plt.ylabel('Number of Listings')
plt.title('Distribution of Trust Scores')
plt.show()

# ---------- PRICE VS TRUST SCORE ----------
plt.figure()
plt.scatter(X['PRICE'], X['trust_score'], alpha=0.4)
plt.xlabel('PRICE')
plt.ylabel('Trust Score')
plt.title('PRICE vs Trust Score')
plt.show()

# ---------- SUSPICIOUS LISTINGS ONLY ----------
anomalies = X[X['anomaly_label'] == -1]

plt.figure()
plt.scatter(anomalies['PRICE'], anomalies['trust_score'], alpha=0.6)
plt.xlabel('PRICE')
plt.ylabel('Trust Score')
plt.title('Suspicious Laptop Listings')
plt.show()

# ---------- NORMAL VS ANOMALY COMPARISON ----------
normal = X[X['anomaly_label'] == 1]

plt.figure()
plt.scatter(normal['PRICE'], normal['trust_score'], alpha=0.3, label='Normal')
plt.scatter(anomalies['PRICE'], anomalies['trust_score'], alpha=0.7, label='Anomaly')
plt.xlabel('PRICE')
plt.ylabel('Trust Score')
plt.title('Normal vs Suspicious Listings')
plt.legend()
plt.show()


suspicious = X[X['anomaly_label'] == -1]
print(suspicious)