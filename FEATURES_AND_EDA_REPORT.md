# 📊 Features Dictionary & EDA Insights Report
**Project:** Algerian Laptop Market Analysis  
**Dataset Version:** Master Cleaned (v2.0 - 42,419 rows)  
**Date:** January 29, 2026

---

## 📝 Part 1: Feature Glossary (35 Features)

This dataset contains **35 features** structured to provide a 360-degree view of the laptop market. We have categorized them into **Original Features** and **Engineered Features**.

### 🔹 Original Features (25)
These were cleaned and standardized by the team (Lyna, Aya, Leena, Abdallah & Mimoun).

| Feature | Type | Description |
| :--- | :--- | :--- |
| `PRICE` | Numeric | **Target Variable.** Price in Algerian Dinars (DZD). Range: 5k - 800k. |
| `LAPTOP_CONDITION` | Categorical | Condition: *New, Used, Refurbished*. |
| `LAPTOP_BRAND` | Categorical | Manufacturer (HP, Dell, Apple, etc.). Standardized for variations. |
| `LAPTOP_MODEL` | Categorical | Specific model series (e.g., Latitude, XPS, Pavilion). |
| `CPU` | Categorical | Raw processor string (e.g., "Intel Core i7 12th Gen"). |
| `DEDICATED_GPU` | Categorical | Discrete graphics model (NVIDIA/AMD) or "None". |
| `GPU_INTEGRATED` | Categorical | Built-in graphics (Intel UHD, Vega, etc.). |
| `GPU_GENERAL` | Categorical | High-level GPU description. |
| `RAM_SIZE` | String | Capacity as text (e.g., "16GB"). |
| `RAM_GB` | Numeric | Capacity as a number (4, 8, 16, 32, etc.). |
| `RAM_TYPE` | Categorical | Technology (DDR3, DDR4, DDR5). |
| `SSD_SIZE` | String | SSD capacity as text. |
| `SSD_GB` | Numeric | SSD capacity as a number. |
| `HDD_SIZE` | String | HDD capacity as text. |
| `HDD_GB` | Numeric | HDD capacity as a number. |
| `STORAGE_SIZE` | String | Combined storage text. |
| `STORAGE_TYPE` | Categorical | Configuration: *SSD, HDD, or Hybrid*. |
| `SCREEN_SIZE` | Numeric | Physical diagonal size in inches (e.g., 15.6). |
| `SCREEN_RESOLUTION` | String | Standardized resolution (e.g., "1920x1080"). |
| `SCREEN_RESOLUTION_CLEAN`| String | Pure resolution string (sparsely populated). |
| `SCREEN_FREQUENCY` | String | Refresh rate as text (e.g., "144Hz"). |
| `SCREEN_FREQUENCY_NUM` | Numeric | Numeric refresh rate (60, 120, 144, 240). |
| `CITY` | Categorical | Listing location (Algiers, Oran, etc.). |
| `POST_YEAR` | Numeric | Year the listing was posted. |
| `POST_MONTH` | Numeric | Month the listing was posted. |

### 🛠️ Engineered Features (10)
These were created to help the models (Decision Trees, Clustering) understand complex relationships.

| Feature | Goal | Logic |
| :--- | :--- | :--- |
| `RES_WIDTH` | Math | Numeric width extracted from resolution (e.g., 1920). |
| `RES_HEIGHT` | Math | Numeric height extracted from resolution (e.g., 1080). |
| `TOTAL_PIXELS` | Quality | `Width x Height`. Higher values = Premium High-Def screens. |
| `PPI` | Precision | **Pixels Per Inch.** Measures pixel density (Sharpness). |
| `TOTAL_STORAGE_GB` | Capacity | `SSD_GB + HDD_GB`. The total space available. |
| `RAM_STORAGE_RATIO` | Power | `RAM_GB * SSD_GB`. High scores = High-performance Workstations. |
| `IS_GAMING` | Split | **Flag (1/0).** Identified by GPU (RTX/GTX) or Brand (ROG/TUF/Legion). |
| `CPU_TIER` | Simplicity | Groups messy CPU names into: *Entry, Mid, High, Enthusiast*. |
| `BRAND_TIER` | Simplicity | Groups brands by pricing: *Budget, Mainstream, Premium*. |
| `STORAGE_SCORE` | Market | `(SSD * 1.0) + (HDD * 0.2)`. Values SSD 5x more than HDD. |

---

## 📈 Part 2: Key EDA Findings & Visualization Notes

From our analysis of the 9 generated charts and the `EDA_and_insights.ipynb` notebook, here are the critical takeaways for your report:

### 1. Price Distribution (The Target)
- **Insight:** Most laptops cluster between **50,000 DZD and 150,000 DZD**.
- **Outliers:** The tail goes up to 800,000 DZD. These are purely high-end gaming laptops or Apple MacBooks.
- **Action:** Models need to handle this "skewness" by focusing on the majority but allowing growth in the premium segment.

### 2. Brand Trends
- **Market Leaders:** HP and Dell dominate the Algerian used and new market.
- **Premium Leaders:** Apple and Razer have the highest median prices. 
- **Note:** `BRAND_TIER` (Premium vs Budget) shows a massive price gap, confirming brand value is a major price driver in Algeria.

### 3. Specs vs. Price Relationship
- **RAM is King:** Moving from 8GB to 16GB RAM creates the most consistent price jump across all brands.
- **The SSD Revolution:** Laptops with even a small SSD (256GB) are priced significantly higher than those with only 1TB HDD. Our `STORAGE_SCORE` captured this perfectly.
- **Gaming Premium:** Laptops flagged as `IS_GAMING=1` have a price distribution that starts where normal office laptops end.

### 4. Correlation Highlights
- **Strongest Positive Correlations:** `RAM_GB`, `STORAGE_SCORE`, `IS_GAMING`, and `TOTAL_PIXELS`.
- **Unexpected Find:** `SCREEN_SIZE` has a relatively low correlation with price. This is because many expensive 13-inch MacBooks exist, while cheap 15.6-inch office laptops are common. This proves **specs matter more than size.**

### 5. Data Cleaning Impact
- **Trust Factor:** By removing "NeedToBeFilled" and illegal outliers, our accuracy potential increased. We sacrificed quantity (removing ~36% of data) to ensure **High Quality** results.

---

## 🛠️ Part 3: Why This Helps Your Modeling

- **For Lyna (Classification):** Using `CPU_TIER` and `BRAND_TIER` instead of raw names will make your Decision Tree much "cleaner" and easier to read (Shorter trees, higher accuracy).
- **For Aya (Clustering):** Use `PPI` and `STORAGE_SCORE` to find the clusters. You will likely see a "Premium Sharp Screen" cluster vs an "Old Office" cluster.
- **For Leena (Association Rules):** Look for rules involving `IS_GAMING`. You'll find high-confidence rules like `{IS_GAMING=1} => {Price=Premium}`.
- **For Abdallah & Mimoun (Anomaly):** Use `RAM_STORAGE_RATIO`. If someone lists a laptop with high RAM and high SSD (High Ratio) for a very low Price, it’s a **guaranteed scam/anomaly.**

---

**Summary:** This dataset is now a "Professional Grade" data mining source. You have the raw physical details, the engineered market logic, and clear visual evidence to support your final report.
