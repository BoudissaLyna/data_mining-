# 📊 Laptop Price Prediction - Data Mining Project

**Team Members:** Lyna Boudissa, Aya, Leena, Abdallah & Mimoun  
**Course:** Data Mining  
**Institution:** ENSIA  
**Date:** January 2026

---

## 🎯 Project Overview

This project analyzes the Algerian laptop market to build a price prediction model. We cleaned and processed **66,667 laptop listings** to create a high-quality dataset of **53,445 records** (80.15% retention rate).

---

## 📁 Project Structure

```
data_mining-/
├── final_cleaned_dataset.csv              ← MAIN DATASET (53,445 records, 25 features)
├── TEAM_DATA_CLEANING_PLAN.md             ← Complete documentation
├── comprehensive_visualizations.py         ← Visualization script
├── visualizations/                         ← All charts and graphs
│   ├── overview_analysis.png
│   ├── correlation_heatmap.png
│   ├── price_vs_ram.png
│   ├── storage_analysis.png
│   ├── brand_distribution.png
│   ├── temporal_trends.png
│   └── screen_size_distribution.png
│
├── Lyna_cleaning_task/                    ← Lyna's work
├── Aya's_cleaning_task/                   ← Aya's work
├── Leena's_cleaning_task/                 ← Leena's work
└── Abdallah_Mimoun's_cleaning_task/       ← Abdallah & Mimoun's work
```

---

## 📊 Dataset Summary

### Final Dataset: `final_cleaned_dataset.csv`

- **Records:** 53,445 laptop listings
- **Features:** 25 columns
- **Missing Values:** 0 (in critical features)
- **Data Quality:** Production-ready ✓

### Key Features

**Target Variable:**
- `PRICE` - Laptop price in DZD (10,000 - 500,000)

**Categorical Features:**
- `LAPTOP_BRAND` - Manufacturer (HP, Dell, Lenovo, Asus, etc.)
- `LAPTOP_CONDITION` - New, Used, or Refurbished
- `LAPTOP_MODEL` - Model name
- `CPU` - Processor information
- `DEDICATED_GPU` - Discrete graphics card
- `GPU_INTEGRATED` - Integrated graphics
- `RAM_TYPE` - Memory type (DDR3, DDR4, DDR5)
- `STORAGE_TYPE` - SSD, HDD, or Hybrid
- `CITY` - Location in Algeria

**Numeric Features:**
- `RAM_GB` - RAM capacity (4, 8, 16, 32+ GB)
- `SSD_GB` - SSD capacity
- `HDD_GB` - HDD capacity
- `SCREEN_SIZE` - Display size (11"-17.3")
- `SCREEN_FREQUENCY_NUM` - Refresh rate (60-240 Hz)
- `POST_YEAR` - Listing year
- `POST_MONTH` - Listing month

---

## 👥 Team Contributions

### Lyna Boudissa
**Features:** PRICE, LAPTOP_CONDITION, LAPTOP_BRAND, LAPTOP_MODEL, POST_YEAR, POST_MONTH  
**Impact:** Established foundation for price prediction with clean target variable

### Aya
**Features:** SCREEN_SIZE, SCREEN_FREQUENCY, SCREEN_RESOLUTION  
**Impact:** Enabled display quality analysis

### Leena
**Features:** RAM_SIZE, RAM_TYPE, SSD_SIZE, HDD_SIZE, STORAGE_SIZE, STORAGE_TYPE  
**Impact:** Provided critical performance indicators

### Abdallah & Mimoun
**Features:** CPU, DEDICATED_GPU, GPU_INTEGRATED, GPU_GENERAL  
**Impact:** Ensured dataset integrity through cross-feature validation

---

## 📈 Data Cleaning Results

### Data Retention
- **Original Records:** 66,667
- **Final Records:** 53,445
- **Retention Rate:** 80.15%
- **Records Removed:** 13,222 (19.85%)

### Removal Breakdown
| Reason | Count | % |
|--------|-------|---|
| Invalid/Missing Price | ~4,500 | 6.75% |
| Price Outliers | ~3,200 | 4.80% |
| Missing Critical Features | ~2,800 | 4.20% |
| Inconsistent Specs | ~1,900 | 2.85% |
| Duplicates | ~822 | 1.23% |

---

## 📊 Visualizations

Run the visualization script to generate all charts:

```bash
python comprehensive_visualizations.py
```

### Generated Visualizations

1. **overview_analysis.png** - Price distribution, price by brand, price by condition, RAM distribution
2. **correlation_heatmap.png** - Feature correlations
3. **price_vs_ram.png** - Price vs RAM scatter plot
4. **storage_analysis.png** - Storage type distribution and pricing
5. **brand_distribution.png** - Top 15 laptop brands
6. **temporal_trends.png** - Listings over time
7. **screen_size_distribution.png** - Screen size frequencies

---

## 🔍 Key Insights

### Price Distribution
- **Mean Price:** ~125,000 DZD
- **Median Price:** ~110,000 DZD
- **Price Range:** 10,000 - 500,000 DZD

### Market Composition
- **Top Brands:** HP (18%), Dell (16%), Lenovo (15%), Asus (14%), Acer (12%)
- **Condition:** New (45%), Used (48%), Refurbished (7%)
- **RAM:** 8GB most common (45%), followed by 16GB (32%)
- **Storage:** Hybrid SSD+HDD (40%), SSD only (35%), HDD only (25%)

### Correlations
- Strong correlation between RAM and Price
- Storage type significantly impacts pricing
- Screen size moderately correlated with price
- Brand has significant influence on pricing

---

## 🚀 Next Steps

### For Analysis
1. Explore visualizations to understand patterns
2. Perform feature importance analysis
3. Identify key price drivers

### For Modeling
1. Feature selection and engineering
2. Train regression models (Decision Tree, Random Forest, XGBoost)
3. Evaluate and compare models
4. Deploy best model for price prediction

---

## 📖 Documentation

For complete details on data cleaning methodology, team contributions, and quality metrics, see:
- **TEAM_DATA_CLEANING_PLAN.md** - Comprehensive documentation

---

## 🛠️ Requirements

```bash
pip install pandas numpy matplotlib seaborn scikit-learn
```

---

## 📞 Contact

For questions about specific features or cleaning decisions:
- **Lyna:** Core features (Price, Brand, Model, Condition, Dates)
- **Aya:** Display features (Screen Size, Resolution, Frequency)
- **Leena:** Storage features (RAM, SSD, HDD, Storage Type)
- **Abdallah & Mimoun:** Processing features (CPU, GPU) + Cross-validation

---

## ✅ Project Status

- [x] Data collection and merging
- [x] Individual feature cleaning
- [x] Cross-feature validation
- [x] Final dataset creation
- [x] Comprehensive visualizations
- [x] Documentation
- [ ] Exploratory Data Analysis
- [ ] Model development
- [ ] Model evaluation
- [ ] Deployment

---

**Dataset Quality:** Production-ready ✓  
**Documentation:** Complete ✓  
**Ready for Modeling:** Yes ✓

*Last Updated: January 29, 2026*
