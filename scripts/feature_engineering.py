import pandas as pd
import numpy as np
import re

print("Starting Feature Engineering...")

# Load the master dataset
df = pd.read_csv('final_cleaned_dataset.csv')
print(f"Initial columns: {len(df.columns)}")

# 1. Pixel Extraction & PPI (Pixels Per Inch)
print("1. Calculating Screen Metrics (PPI)...")
def get_pixels(res_str):
    if pd.isna(res_str) or 'x' not in str(res_str):
        return 1920, 1080 # Default to FHD if missing
    try:
        parts = str(res_str).lower().split('x')
        return int(parts[0]), int(parts[1])
    except:
        return 1920, 1080

res_dims = df['SCREEN_RESOLUTION'].apply(get_pixels)
df['RES_WIDTH'] = [x[0] for x in res_dims]
df['RES_HEIGHT'] = [x[1] for x in res_dims]
df['TOTAL_PIXELS'] = df['RES_WIDTH'] * df['RES_HEIGHT']

# PPI Formula: sqrt(W^2 + H^2) / ScreenSize
df['PPI'] = np.sqrt(df['RES_WIDTH']**2 + df['RES_HEIGHT']**2) / df['SCREEN_SIZE']

# 2. Performance Scoring (Interaction Features)
print("2. Creating Performance Scores...")

# Total Storage
df['TOTAL_STORAGE_GB'] = df['SSD_GB'] + df['HDD_GB']

# RAM + SSD interaction (Usually high RAM laptops have high SSD)
df['RAM_STORAGE_RATIO'] = df['RAM_GB'] * df['SSD_GB']

# Gaming Flag (Interaction between GPU and Frequency)
def is_gaming(row):
    model = str(row['LAPTOP_MODEL']).upper()
    gpu = str(row['DEDICATED_GPU']).upper()
    gaming_brands = ['ROG', 'TUF', 'LEGION', 'OMEN', 'PREDATOR', 'ALIENWARE', 'MSI', 'VICTUS']
    
    if any(brand in model for brand in gaming_brands):
        return 1
    if any(card in gpu for card in ['RTX', 'GTX', 'RADEON RX']):
        return 1
    if row['SCREEN_FREQUENCY_NUM'] > 60:
        return 1
    return 0

df['IS_GAMING'] = df.apply(is_gaming, axis=1)

# 3. CPU/GPU Tiering (Categorical Interaction)
print("3. Categorizing CPU/GPU Tiers...")

def get_cpu_tier(cpu_str):
    cpu_str = str(cpu_str).upper()
    if any(x in cpu_str for x in ['I9', 'RYZEN 9', 'M1 MAX', 'M2 MAX', 'M3 MAX']):
        return 'Enthusiast'
    if any(x in cpu_str for x in ['I7', 'RYZEN 7', 'M1 PRO', 'M2 PRO', 'M3 PRO']):
        return 'High-End'
    if any(x in cpu_str for x in ['I5', 'RYZEN 5', 'M1', 'M2', 'M3']):
        return 'Mid-Range'
    if any(x in cpu_str for x in ['I3', 'RYZEN 3', 'CELERON', 'PENTIUM']):
        return 'Entry-Level'
    return 'Other'

df['CPU_TIER'] = df['CPU'].apply(get_cpu_tier)

# 4. Brand Premiumness (Interaction between Brand and Price)
# We calculate the mean price per brand in the training context (conceptually)
# But for feature engineering, we'll just group them by market position
def get_brand_tier(brand):
    brand = str(brand).upper()
    premium = ['APPLE', 'RAZER', 'MICROSOFT']
    mainstream = ['HP', 'DELL', 'LENOVO', 'ASUS', 'MSI']
    budget = ['ACER', 'GATEWAY', 'THOMSON', 'CHUWI']
    
    if brand in premium: return 'Premium'
    if brand in mainstream: return 'Mainstream'
    if brand in budget: return 'Budget'
    return 'Niche'

df['BRAND_TIER'] = df['LAPTOP_BRAND'].apply(get_brand_tier)

# 5. Storage Efficiency
# SSD usually adds more value than HDD. 
# We create a weighted storage score.
df['STORAGE_SCORE'] = (df['SSD_GB'] * 1.0) + (df['HDD_GB'] * 0.2)

# Save the final dataset with engineered features
df.to_csv('final_dataset_engineered.csv', index=False)
# Overwrite the main one for the next step
df.to_csv('final_cleaned_dataset.csv', index=False)

print(f"\nFeature Engineering Complete!")
print(f"New columns added: {['RES_WIDTH', 'RES_HEIGHT', 'TOTAL_PIXELS', 'PPI', 'TOTAL_STORAGE_GB', 'RAM_STORAGE_RATIO', 'IS_GAMING', 'CPU_TIER', 'BRAND_TIER', 'STORAGE_SCORE']}")
print(f"Final column count: {len(df.columns)}")
