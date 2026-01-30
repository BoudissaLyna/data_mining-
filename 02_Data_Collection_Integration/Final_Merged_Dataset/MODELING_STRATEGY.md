# MODELING STRATEGY FOR LAPTOP PRICE PREDICTION

## Problem Analysis

**Objective**: Predict laptop prices based on specifications and market data

**Available Techniques** (from your coursework):
1. Classification
2. Clustering
3. Decision Trees
4. Association Rules

---

## RECOMMENDED APPROACH: **DECISION TREES FOR REGRESSION**

### Why Decision Trees are PERFECT for this problem:

#### **1. Naturally Handles Price Prediction**
- Decision trees can do **regression** (predicting continuous values like price)
- They create rules like: "IF RAM >= 16GB AND SSD >= 512GB AND Brand = APPLE THEN Price = 150,000 DZD"
- This matches how laptop pricing actually works in the market!

#### **2. Interpretable Results**
- You can see EXACTLY why a laptop is priced at X DZD
- Example rule: "Gaming laptops (RTX GPU) with 16GB RAM cost 120,000-180,000 DZD"
- Perfect for explaining to stakeholders

#### **3. Handles Mixed Data Types**
- Categorical: BRAND, MODEL, CONDITION, STORAGE_TYPE
- Numerical: RAM_GB, SSD_GB, SCREEN_SIZE, PRICE
- Decision trees handle both naturally!

#### **4. Captures Non-Linear Relationships**
- Price doesn't increase linearly with RAM (4GB→8GB is bigger jump than 32GB→64GB)
- Decision trees capture this automatically

#### **5. No Need for Feature Scaling**
- Unlike other methods, you don't need to normalize/standardize
- Works directly with your cleaned data

---

## COMPLETE MODELING PLAN

### **Phase 1: Decision Tree Regression (PRIMARY)**

#### **Step 1: Data Preparation**
```python
# Features to use
X_features = [
 'RAM_GB', # Numerical
 'SSD_GB', # Numerical
 'HDD_GB', # Numerical
 'SCREEN_SIZE', # Numerical
 'SCREEN_FREQUENCY_NUM', # Numerical
 'LAPTOP_BRAND', # Categorical
 'LAPTOP_MODEL', # Categorical
 'LAPTOP_CONDITION', # Categorical
 'STORAGE_TYPE', # Categorical
 'SCREEN_RESOLUTION',# Categorical
 'POST_YEAR', # Numerical
 'CITY' # Categorical
]

y_target = 'PRICE'
```

#### **Step 2: Encode Categorical Variables**
```python
from sklearn.preprocessing import LabelEncoder

# Encode categorical features
for col in ['LAPTOP_BRAND', 'LAPTOP_MODEL', 'LAPTOP_CONDITION', 
 'STORAGE_TYPE', 'SCREEN_RESOLUTION', 'CITY']:
 le = LabelEncoder()
 df[col + '_encoded'] = le.fit_transform(df[col])
```

#### **Step 3: Train Decision Tree**
```python
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

# Split data
X_train, X_test, y_train, y_test = train_test_split(
 X, y, test_size=0.2, random_state=42
)

# Train model
dt_model = DecisionTreeRegressor(
 max_depth=10, # Prevent overfitting
 min_samples_split=50, # Require 50 samples to split
 min_samples_leaf=20, # Require 20 samples per leaf
 random_state=42
)

dt_model.fit(X_train, y_train)

# Predict
y_pred = dt_model.predict(X_test)

# Evaluate
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Absolute Error: {mae:,.0f} DZD")
print(f"R² Score: {r2:.3f}")
```

#### **Step 4: Extract Rules**
```python
from sklearn.tree import export_text

# Get human-readable rules
tree_rules = export_text(dt_model, feature_names=list(X.columns))
print(tree_rules)

# Example output:
# |--- RAM_GB <= 8.0
# | |--- SSD_GB <= 256.0
# | | |--- LAPTOP_BRAND_encoded <= 5.0
# | | | |--- value: [45000.0] # Budget laptop
# | |--- SSD_GB > 256.0
# | | |--- value: [65000.0] # Mid-range laptop
# |--- RAM_GB > 8.0
# | |--- LAPTOP_BRAND_encoded <= 2.0 # Apple
# | | |--- value: [180000.0] # Premium laptop
```

#### **Step 5: Feature Importance**
```python
import matplotlib.pyplot as plt

# Get feature importance
importances = dt_model.feature_importances_
feature_names = X.columns

# Plot
plt.figure(figsize=(10, 6))
plt.barh(feature_names, importances)
plt.xlabel('Importance')
plt.title('Feature Importance for Price Prediction')
plt.tight_layout()
plt.savefig('feature_importance.png')

# Expected top features:
# 1. RAM_GB (most important)
# 2. LAPTOP_BRAND
# 3. SSD_GB
# 4. LAPTOP_MODEL
# 5. LAPTOP_CONDITION
```

---

### **Phase 2: Clustering (SECONDARY - for Market Segmentation)**

#### **Purpose**: Group laptops into market segments
- Budget laptops (30,000-60,000 DZD)
- Mid-range laptops (60,000-120,000 DZD)
- Premium laptops (120,000-250,000 DZD)
- Ultra-premium (250,000+ DZD)

#### **Method**: K-Means Clustering
```python
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Select features for clustering
cluster_features = ['RAM_GB', 'SSD_GB', 'SCREEN_SIZE', 'PRICE']
X_cluster = df[cluster_features]

# Normalize (required for K-Means)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_cluster)

# Find optimal clusters (Elbow method)
inertias = []
for k in range(2, 11):
 kmeans = KMeans(n_clusters=k, random_state=42)
 kmeans.fit(X_scaled)
 inertias.append(kmeans.inertia_)

# Train with optimal K (likely 4-5)
kmeans = KMeans(n_clusters=4, random_state=42)
df['Market_Segment'] = kmeans.fit_predict(X_scaled)

# Analyze segments
print(df.groupby('Market_Segment').agg({
 'PRICE': ['mean', 'min', 'max'],
 'RAM_GB': 'mean',
 'SSD_GB': 'mean',
 'LAPTOP_BRAND': lambda x: x.mode()[0]
}))

# Expected output:
# Segment 0: Budget (avg 45K, 4-8GB RAM, 128-256GB SSD)
# Segment 1: Mid-range (avg 85K, 8-12GB RAM, 256-512GB SSD)
# Segment 2: Premium (avg 160K, 16GB+ RAM, 512GB-1TB SSD)
# Segment 3: Ultra-premium (avg 280K, 32GB+ RAM, 1TB+ SSD, Apple/Gaming)
```

#### **Use Case**: 
- Understand market structure
- Identify pricing anomalies (laptops in wrong segment)
- Marketing strategy (target specific segments)

---

### **Phase 3: Classification (TERTIARY - for Price Range Prediction)**

#### **Purpose**: Classify laptops into price categories
- Instead of predicting exact price, predict price range

#### **Method**: Decision Tree Classifier
```python
from sklearn.tree import DecisionTreeClassifier

# Create price categories
def categorize_price(price):
 if price < 60000:
 return 'Budget'
 elif price < 120000:
 return 'Mid-Range'
 elif price < 250000:
 return 'Premium'
 else:
 return 'Ultra-Premium'

df['Price_Category'] = df['PRICE'].apply(categorize_price)

# Train classifier
X = df[feature_columns]
y = df['Price_Category']

dt_classifier = DecisionTreeClassifier(max_depth=8, random_state=42)
dt_classifier.fit(X_train, y_train)

# Predict
y_pred = dt_classifier.predict(X_test)

# Evaluate
from sklearn.metrics import classification_report, confusion_matrix

print(classification_report(y_test, y_pred))
print(confusion_matrix(y_test, y_pred))

# Expected accuracy: 85-90%
```

#### **Use Case**:
- Quick price range estimation
- Easier to interpret than exact price
- Good for initial screening

---

### **Phase 4: Association Rules (BONUS - for Market Insights)**

#### **Purpose**: Find interesting patterns in laptop configurations
- "Laptops with RTX 4090 → Usually have 32GB RAM (confidence: 95%)"
- "MacBook Pro → Usually has 16GB+ RAM AND 512GB+ SSD (confidence: 92%)"

#### **Method**: Apriori Algorithm
```python
from mlxtend.frequent_patterns import apriori, association_rules

# Create binary features
df_binary = pd.DataFrame()
df_binary['High_RAM'] = (df['RAM_GB'] >= 16).astype(int)
df_binary['Large_SSD'] = (df['SSD_GB'] >= 512).astype(int)
df_binary['High_Refresh'] = (df['SCREEN_FREQUENCY_NUM'] >= 144).astype(int)
df_binary['Premium_Brand'] = df['LAPTOP_BRAND'].isin(['APPLE', 'MICROSOFT', 'RAZER']).astype(int)
df_binary['Gaming_GPU'] = df['DEDICATED_GPU'].str.contains('RTX', na=False).astype(int)
df_binary['High_Price'] = (df['PRICE'] >= 120000).astype(int)

# Find frequent itemsets
frequent_itemsets = apriori(df_binary, min_support=0.05, use_colnames=True)

# Generate rules
rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.7)

# Sort by lift
rules_sorted = rules.sort_values('lift', ascending=False)

print(rules_sorted[['antecedents', 'consequents', 'support', 'confidence', 'lift']].head(10))

# Expected insights:
# Gaming_GPU → High_RAM (confidence: 0.92, lift: 3.5)
# Premium_Brand → Large_SSD (confidence: 0.88, lift: 2.8)
# High_Refresh → Gaming_GPU (confidence: 0.95, lift: 4.2)
```

#### **Use Case**:
- Validate market assumptions
- Find unusual configurations
- Recommend specs for new laptops

---

## RECOMMENDED IMPLEMENTATION ORDER

### **Week 1: Decision Tree Regression (PRIMARY)**
**Priority**: (HIGHEST)

**Why**: This directly solves your problem (price prediction)

**Deliverables**:
1. Trained decision tree model
2. Price predictions with MAE and R² scores
3. Feature importance chart
4. Extracted pricing rules

**Expected Results**:
- MAE: 8,000-12,000 DZD (±10% of average price)
- R²: 0.85-0.92 (very good fit)

---

### **Week 2: Clustering (SECONDARY)**
**Priority**: (HIGH)

**Why**: Provides market insights and validates pricing

**Deliverables**:
1. Market segments (Budget, Mid, Premium, Ultra)
2. Segment characteristics
3. Pricing anomaly detection

**Expected Results**:
- 4-5 clear market segments
- Identify 5-10% of laptops as mispriced

---

### **Week 3: Classification (OPTIONAL)**
**Priority**: (MEDIUM)

**Why**: Alternative approach, easier interpretation

**Deliverables**:
1. Price category classifier
2. Confusion matrix
3. Classification rules

**Expected Results**:
- Accuracy: 85-90%
- Good for quick estimates

---

### **Week 4: Association Rules (BONUS)**
**Priority**: (LOW)

**Why**: Interesting insights but not core to price prediction

**Deliverables**:
1. Configuration patterns
2. Market insights
3. Spec recommendations

**Expected Results**:
- 20-30 interesting rules
- Validate market assumptions

---

## EVALUATION METRICS

### **For Regression (Decision Tree)**:
1. **Mean Absolute Error (MAE)**: Average price difference
 - Target: < 10,000 DZD
2. **R² Score**: How well model explains variance
 - Target: > 0.85
3. **Mean Absolute Percentage Error (MAPE)**: Percentage error
 - Target: < 12%

### **For Classification**:
1. **Accuracy**: Overall correctness
 - Target: > 85%
2. **Precision/Recall**: Per-category performance
 - Target: > 80% for all categories
3. **Confusion Matrix**: Where errors occur

### **For Clustering**:
1. **Silhouette Score**: Cluster quality
 - Target: > 0.5
2. **Within-cluster variance**: Compactness
 - Lower is better
3. **Business validation**: Do segments make sense?

---

## FINAL RECOMMENDATION

### **PRIMARY METHOD: Decision Tree Regression**

**Reasons**:
1. Directly predicts price (your goal)
2. Interpretable rules (explain why)
3. Handles your data types naturally
4. No complex preprocessing needed
5. You've studied this in class

**Expected Performance**:
- Predict prices within ±10,000 DZD
- R² score of 0.85-0.92
- Clear, explainable rules

**Bonus**: Add clustering for market segmentation insights!

