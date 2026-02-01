import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.tree import DecisionTreeClassifier, plot_tree, export_text
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix

print("Starting Decision Tree Classification (Lyna's Task)...")

# 1. Load Datasets
train_df = pd.read_csv('training_dataset.csv')
test_df = pd.read_csv('testing_dataset.csv')

# 2. Target Preprocessing: Convert Price into Categorical Bins
# We define 4 logical tiers for the Algerian market
def categorize_price(price):
 if price < 75000: return 'Budget'
 if price < 130000: return 'Mainstream'
 if price < 200000: return 'High-End'
 return 'Ultimate'

train_df['PRICE_TIER'] = train_df['PRICE'].apply(categorize_price)
test_df['PRICE_TIER'] = test_df['PRICE'].apply(categorize_price)

# 3. Feature Selection
# We use the most powerful engineered and original features
features = ['BRAND_TIER', 'CPU_TIER', 'RAM_GB', 'STORAGE_SCORE', 'IS_GAMING', 'PPI', 'LAPTOP_CONDITION']

X_train = train_df[features].copy()
y_train = train_df['PRICE_TIER']
X_test = test_df[features].copy()
y_test = test_df['PRICE_TIER']

# 4. Encoding Categorical Features
# Simple Label Encoding is efficient for Decision Trees
le_map = {}
for col in ['BRAND_TIER', 'CPU_TIER', 'LAPTOP_CONDITION']:
 le = LabelEncoder()
 X_train[col] = le.fit_transform(X_train[col].astype(str))
 X_test[col] = le.transform(X_test[col].astype(str))
 le_map[col] = le

# 5. Build Decision Tree Model
# We use 'entropy' for Information Gain or 'gini' for Gini Index
print("Training model using Information Gain (Entropy)...")
clf = DecisionTreeClassifier(
 criterion='entropy', 
 max_depth=5, # Limited depth to prevent overfitting and stay readable
 min_samples_split=20, 
 random_state=42
)

clf.fit(X_train, y_train)

# 6. Evaluation
y_pred = clf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print("\n" + "="*40)
print(f"MODEL ACCURACY: {accuracy:.2f}%")
print("="*40)
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# 7. Analyze Information Gain (Feature Importance)
importances = pd.DataFrame({
 'Feature': features,
 'Importance': clf.feature_importances_
}).sort_values(by='Importance', ascending=False)

print("\nFeature Importance (Information Gain):")
print(importances)

# 8. Visualize the Logic
plt.figure(figsize=(20, 10))
plot_tree(clf, feature_names=features, class_names=clf.classes_, filled=True, rounded=True, fontsize=10)
plt.title("Decision Tree Structure for Price Prediction")
plt.savefig('visualizations/decision_tree_structure.png', dpi=300, bbox_inches='tight')
print("\nSaved structure to: visualizations/decision_tree_structure.png")

# 9. Textual representation of the first few splits
tree_rules = export_text(clf, feature_names=features)
with open('scripts/decision_tree_rules.txt', 'w') as f:
 f.write(tree_rules)
print("Saved tree rules to: scripts/decision_tree_rules.txt")

print("\nTask Complete! Lyna, you have a working predictor.")
