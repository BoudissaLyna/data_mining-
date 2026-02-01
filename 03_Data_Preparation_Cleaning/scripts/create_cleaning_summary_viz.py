import matplotlib.pyplot as plt
import numpy as np

# Data cleaning statistics
categories = ['Original\nDataset', 'After\nCleaning', 'Removed']
values = [66667, 53445, 13222]
colors = ['#3498db', '#2ecc71', '#e74c3c']

# Create figure
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Bar chart
bars = ax1.bar(categories, values, color=colors, edgecolor='black', linewidth=2)
ax1.set_ylabel('Number of Records', fontsize=14, fontweight='bold')
ax1.set_title('Data Cleaning Impact', fontsize=16, fontweight='bold')
ax1.grid(axis='y', alpha=0.3)

# Add value labels on bars
for bar, value in zip(bars, values):
 height = bar.get_height()
 ax1.text(bar.get_x() + bar.get_width()/2., height,
 f'{value:,}',
 ha='center', va='bottom', fontsize=12, fontweight='bold')

# Pie chart - Retention vs Removed
retention_data = [53445, 13222]
retention_labels = ['Kept\n80.15%', 'Removed\n19.85%']
retention_colors = ['#2ecc71', '#e74c3c']

ax2.pie(retention_data, labels=retention_labels, colors=retention_colors, 
 autopct='%1.1f%%', startangle=90, textprops={'fontsize': 12, 'fontweight': 'bold'})
ax2.set_title('Data Retention Rate', fontsize=16, fontweight='bold')

plt.tight_layout()
plt.savefig('visualizations/data_cleaning_impact.png', dpi=300, bbox_inches='tight')
print("Saved: data_cleaning_impact.png")
plt.close()

# Removal reasons breakdown
fig, ax = plt.subplots(figsize=(12, 6))

reasons = ['Invalid/Missing\nPrice', 'Price\nOutliers', 'Missing Critical\nFeatures', 
 'Inconsistent\nSpecs', 'Duplicates']
counts = [4500, 3200, 2800, 1900, 822]
percentages = [6.75, 4.80, 4.20, 2.85, 1.23]

bars = ax.barh(reasons, counts, color='#e74c3c', edgecolor='black', linewidth=2)
ax.set_xlabel('Number of Records Removed', fontsize=14, fontweight='bold')
ax.set_title('Breakdown of Removed Records', fontsize=16, fontweight='bold')
ax.grid(axis='x', alpha=0.3)

# Add value labels
for i, (bar, count, pct) in enumerate(zip(bars, counts, percentages)):
 width = bar.get_width()
 ax.text(width, bar.get_y() + bar.get_height()/2.,
 f' {count:,} ({pct}%)',
 ha='left', va='center', fontsize=11, fontweight='bold')

plt.tight_layout()
plt.savefig('visualizations/removal_breakdown.png', dpi=300, bbox_inches='tight')
print("Saved: removal_breakdown.png")
plt.close()

print("\nData cleaning visualization complete!")
