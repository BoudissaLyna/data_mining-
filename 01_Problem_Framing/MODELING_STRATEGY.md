# 🎯 Laptop Price Prediction: Modeling Strategy
**Team:** Lyna, Aya, Leena, Abdallah  Mimoun  
**Framework:** 70% Training / 30% Testing Split

---

## 🗺️ The Four-Pronged Approach

This project will utilize all four core Data Mining techniques learned in class to provide a comprehensive analysis of the Algerian laptop market.

### 1. Classification (Lyna)
- **Goal:** Categorize laptops into price tiers.
- **Implementation:** Convert `PRICE` into categorical bins (e.g., `Budget (<80k)`, `Mid-Range (80k-150k)`, `Premium (>150k)`).
- **Target:** `Price_Tier`
- **Impact:** Provides a highly accurate "Buying Guide" classifier.

### 2. Clustering (Aya)
- **Goal:** Automatic Market Segmentation.
- **Implementation:** Use K-Means or DBSCAN on numeric features (`RAM_GB`, `TOTAL_PIXELS`, `PPI`).
- **Insight:** Discover if the market naturally groups into segments like "Gaming," "Ultrabooks," or "Old Office Tech" and how price varies within those clusters.

### 3. Association Rules (Leena)
- **Goal:** Pricing Patterns & Marketing Insights.
- **Implementation:** Use Apriori or FP-Growth algorithms on categorical features (`BRAND_TIER`, `CPU_TIER`, `STORAGE_TYPE`).
- **Insight:** Discover rules like `{GPU=RTX, RAM=16GB} => {Price=Premium}`. This explains the market logic.

### 4. Anomaly Detection (Abdallah & Mimoun)
- **Goal:** Identifying Scams and Fraudulent Listings.
- **Implementation:** Use Isolation Forest or Local Outlier Factor (LOF).
- **Insight:** Detect "Fraudulent" listings where the price is suspiciously low (scams) or unreasonably high (market manipulation) compared to the hardware specs. This acts as a "Trust Factor" for the platform.

---

## 📊 Evaluation & Validation (70/30 Split)

Every member will use the **same 70/30 split** to ensure the results are comparable.

| Technique | Primary Metric | Purpose |
| :--- | :--- | :--- |
| **Classification** | Accuracy / F1-Score | How well can we predict the tier? |
| **Clustering** | Silhouette Score | How "natural" are the market groups? |
| **Association Rules** | Confidence / Lift | How strong are the market patterns? |
| **Anomaly Detection** | Outlier Score | How many "weird" deals are in the data? |

---

## 🛠️ Data Preparation for Modeling
1. **One-Hot Encoding:** Categorical features (Tiers, Brands) need to be converted to dummy variables.
2. **Scaling:** Numeric features (`RAM_GB`, `PPI`, `PRICE`) must be scaled (StandardScaler) for Clustering and certain Classifiers.
3. **Imbalance Handling:** If there are few "Premium" laptops, we may use SMOTE to balance the classes.

---

## ✅ Expected Outcome
By the end of this phase, the team will not only have a **Price Predictor** but a complete **Market Intelligence System** for the Algerian laptop market.
