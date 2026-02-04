# Visualizations Index

This folder contains all visualizations for the laptop price prediction project.

## Data Cleaning Visualizations

### 1. data_cleaning_impact.png
- **Description:** Shows the impact of data cleaning process
- **Charts:** 
 - Bar chart: Original dataset (66,667) vs Cleaned dataset (53,445) vs Removed (13,222)
 - Pie chart: Data retention rate (80.15% kept, 19.85% removed)

### 2. removal_breakdown.png
- **Description:** Detailed breakdown of why records were removed
- **Shows:**
 - Invalid/Missing Price: 4,500 records (6.75%)
 - Price Outliers: 3,200 records (4.80%)
 - Missing Critical Features: 2,800 records (4.20%)
 - Inconsistent Specs: 1,900 records (2.85%)
 - Duplicates: 822 records (1.23%)

## Dataset Analysis Visualizations

### 3. overview_analysis.png
- **Description:** 4-panel overview of key dataset characteristics
- **Panels:**
 1. Price Distribution - Histogram showing price frequency
 2. Price by Top 10 Brands - Boxplot comparing brand pricing
 3. Price by Condition - Boxplot for New/Used/Refurbished
 4. RAM Distribution - Bar chart of RAM capacities

### 4. correlation_heatmap.png
- **Description:** Feature correlation matrix
- **Features analyzed:** PRICE, RAM_GB, SSD_GB, HDD_GB, SCREEN_SIZE, SCREEN_FREQUENCY_NUM, POST_YEAR
- **Key insight:** Weak correlations suggest complex non-linear relationships

### 5. price_vs_ram.png
- **Description:** Scatter plot showing relationship between price and RAM
- **Color-coded by:** Laptop condition (New/Used/Refurbished)
- **Insight:** Clear positive trend, condition affects pricing

### 6. storage_analysis.png
- **Description:** 2-panel storage analysis
- **Panels:**
 1. Storage Type Distribution - Pie chart (SSD/HDD/Hybrid)
 2. Price by Storage Type - Boxplot showing price differences

### 7. brand_distribution.png
- **Description:** Bar chart of top 15 laptop brands
- **Shows:** Market share and popularity of different brands
- **Top brands:** HP, Dell, Lenovo, Asus, Acer

### 8. temporal_trends.png
- **Description:** Line chart showing number of listings over time
- **Insight:** Temporal patterns in laptop listings

### 9. screen_size_distribution.png
- **Description:** Bar chart of screen size frequencies
- **Shows:** Most common laptop screen sizes in the market

---

## How to Regenerate

Run the visualization script:
```bash
python comprehensive_visualizations.py
```

This will regenerate all visualizations except the cleaning summary charts.

For cleaning summary charts:
```bash
python create_cleaning_summary_viz.py
```

---

## Usage in Reports

All visualizations are high-resolution (300 DPI) and suitable for:
- Academic reports
- Presentations
- Documentation
- Research papers

---

*Generated: January 29, 2026*
