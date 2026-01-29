import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path

# Create visualizations directory
Path("visualizations").mkdir(exist_ok=True)

# Load dataset
print("Loading dataset...")
df = pd.read_csv('final_cleaned_dataset.csv')
print(f"Dataset shape: {df.shape}")

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)

# 1. Price Distribution
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
axes[0, 0].hist(df['PRICE'], bins=50, color='steelblue', edgecolor='black')
axes[0, 0].set_title('Price Distribution', fontsize=14, fontweight='bold')
axes[0, 0].set_xlabel('Price (DZD)')
axes[0, 0].set_ylabel('Frequency')

# 2. Price by Brand
top_brands = df['LAPTOP_BRAND'].value_counts().head(10).index
df_top = df[df['LAPTOP_BRAND'].isin(top_brands)]
df_top.boxplot(column='PRICE', by='LAPTOP_BRAND', ax=axes[0, 1])
axes[0, 1].set_title('Price by Top 10 Brands', fontsize=14, fontweight='bold')
axes[0, 1].set_xlabel('Brand')
axes[0, 1].set_ylabel('Price (DZD)')
plt.sca(axes[0, 1])
plt.xticks(rotation=45)

# 3. Price by Condition
df.boxplot(column='PRICE', by='LAPTOP_CONDITION', ax=axes[1, 0])
axes[1, 0].set_title('Price by Condition', fontsize=14, fontweight='bold')
axes[1, 0].set_xlabel('Condition')
axes[1, 0].set_ylabel('Price (DZD)')

# 4. RAM Distribution
ram_counts = df['RAM_GB'].value_counts().sort_index()
axes[1, 1].bar(ram_counts.index, ram_counts.values, color='coral', edgecolor='black')
axes[1, 1].set_title('RAM Distribution', fontsize=14, fontweight='bold')
axes[1, 1].set_xlabel('RAM (GB)')
axes[1, 1].set_ylabel('Count')

plt.tight_layout()
plt.savefig('visualizations/overview_analysis.png', dpi=300, bbox_inches='tight')
print("Saved: overview_analysis.png")
plt.close()

# 5. Correlation Heatmap
numeric_cols = ['PRICE', 'RAM_GB', 'SSD_GB', 'HDD_GB', 'SCREEN_SIZE', 'SCREEN_FREQUENCY_NUM', 'POST_YEAR']
corr = df[numeric_cols].corr()
plt.figure(figsize=(10, 8))
sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', center=0, square=True)
plt.title('Feature Correlation Heatmap', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('visualizations/correlation_heatmap.png', dpi=300, bbox_inches='tight')
print("Saved: correlation_heatmap.png")
plt.close()

# 6. Price vs RAM
plt.figure(figsize=(12, 6))
sns.scatterplot(data=df, x='RAM_GB', y='PRICE', hue='LAPTOP_CONDITION', alpha=0.6, s=50)
plt.title('Price vs RAM by Condition', fontsize=16, fontweight='bold')
plt.xlabel('RAM (GB)')
plt.ylabel('Price (DZD)')
plt.legend(title='Condition')
plt.tight_layout()
plt.savefig('visualizations/price_vs_ram.png', dpi=300, bbox_inches='tight')
print("Saved: price_vs_ram.png")
plt.close()

# 7. Storage Analysis
fig, axes = plt.subplots(1, 2, figsize=(16, 6))
storage_counts = df['STORAGE_TYPE'].value_counts()
axes[0].pie(storage_counts.values, labels=storage_counts.index, autopct='%1.1f%%', startangle=90)
axes[0].set_title('Storage Type Distribution', fontsize=14, fontweight='bold')

df.boxplot(column='PRICE', by='STORAGE_TYPE', ax=axes[1])
axes[1].set_title('Price by Storage Type', fontsize=14, fontweight='bold')
axes[1].set_xlabel('Storage Type')
axes[1].set_ylabel('Price (DZD)')

plt.tight_layout()
plt.savefig('visualizations/storage_analysis.png', dpi=300, bbox_inches='tight')
print("Saved: storage_analysis.png")
plt.close()

# 8. Brand Distribution
brand_counts = df['LAPTOP_BRAND'].value_counts().head(15)
plt.figure(figsize=(14, 6))
brand_counts.plot(kind='bar', color='teal', edgecolor='black')
plt.title('Top 15 Laptop Brands', fontsize=16, fontweight='bold')
plt.xlabel('Brand')
plt.ylabel('Count')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('visualizations/brand_distribution.png', dpi=300, bbox_inches='tight')
print("Saved: brand_distribution.png")
plt.close()

# 9. Temporal Analysis
temporal = df.groupby(['POST_YEAR', 'POST_MONTH']).size().reset_index(name='count')
plt.figure(figsize=(14, 6))
plt.plot(range(len(temporal)), temporal['count'], marker='o', linewidth=2, markersize=6)
plt.title('Listings Over Time', fontsize=16, fontweight='bold')
plt.xlabel('Time Period')
plt.ylabel('Number of Listings')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('visualizations/temporal_trends.png', dpi=300, bbox_inches='tight')
print("Saved: temporal_trends.png")
plt.close()

# 10. Screen Size Analysis
plt.figure(figsize=(12, 6))
screen_counts = df['SCREEN_SIZE'].value_counts().sort_index()
plt.bar(screen_counts.index, screen_counts.values, color='purple', edgecolor='black', alpha=0.7)
plt.title('Screen Size Distribution', fontsize=16, fontweight='bold')
plt.xlabel('Screen Size (inches)')
plt.ylabel('Count')
plt.tight_layout()
plt.savefig('visualizations/screen_size_distribution.png', dpi=300, bbox_inches='tight')
print("Saved: screen_size_distribution.png")
plt.close()

print("\nAll visualizations created successfully!")
print(f"Total visualizations: 10")
print(f"Location: visualizations/")
