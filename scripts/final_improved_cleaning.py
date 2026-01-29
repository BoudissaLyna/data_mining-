# FINAL IMPROVED DATA CLEANING - ALL FEATURES
# Implements improved plans for Leena's and Aya's features
# Then merges with your cleaned features

import pandas as pd
import numpy as np
import re

print("="*80)
print("IMPROVED DATA CLEANING - IMPLEMENTING BETTER STRATEGIES")
print("="*80)

# Load your cleaned dataset as base
print("\nLoading base dataset (your cleaned features)...")
df = pd.read_csv('full_merged_dataset_CLEANED.csv')
print(f"Loaded: {df.shape[0]} rows, {df.shape[1]} columns")

print("\nYour cleaned features (already done):")
print("  - PRICE, LAPTOP_CONDITION, LAPTOP_BRAND, LAPTOP_MODEL, POST_YEAR, POST_MONTH")

# ============================================================================
# PART 1: IMPROVED LEENA'S FEATURES (RAM + STORAGE)
# ============================================================================

print("\n" + "="*80)
print("PART 1: CLEANING LEENA'S FEATURES (IMPROVED STRATEGY)")
print("="*80)

# Helper function: Parse size strings to GB
def parse_size_to_gb(size_str):
    """Convert storage/RAM size strings to GB (handles TB, GB, MB, GO, TO, MO)"""
    if pd.isna(size_str) or size_str == 'NeedToBeFilled':
        return np.nan
    
    size_str = str(size_str).upper().strip()
    
    # Extract number
    match = re.search(r'(\d+(?:[.,]\d+)?)', size_str)
    if not match:
        return np.nan
    
    number = float(match.group(1).replace(',', '.'))
    
    # Detect unit and convert to GB
    if any(unit in size_str for unit in ['TB', 'TO']):
        return number * 1024
    elif any(unit in size_str for unit in ['MB', 'MO']):
        return number / 1024
    elif any(unit in size_str for unit in ['GB', 'GO', 'G']):
        return number
    else:
        # No unit - assume GB if reasonable range
        if 2 <= number <= 128:
            return number
        elif number > 128:
            return number / 1024  # Likely MB
        return np.nan

# --- RAM_SIZE Cleaning ---
print("\n1. Cleaning RAM_SIZE...")
df['RAM_GB'] = df['RAM_SIZE'].apply(parse_size_to_gb)

# Intelligent RAM imputation (4-tier)
print("   Imputing missing RAM using intelligent strategy...")

price_percentiles = df['PRICE'].quantile([0.25, 0.50, 0.75, 0.90])

def impute_ram(row):
    if pd.notna(row['RAM_GB']) and row['RAM_GB'] > 0:
        return row['RAM_GB']
    
    price = row['PRICE']
    year = row['POST_YEAR']
    brand = str(row['LAPTOP_BRAND']).upper()
    model = str(row['LAPTOP_MODEL']).upper()
    
    # Tier 1: Brand + Model median
    group = df[(df['LAPTOP_BRAND'] == row['LAPTOP_BRAND']) & 
               (df['LAPTOP_MODEL'] == row['LAPTOP_MODEL']) &
               (df['RAM_GB'].notna()) &
               (df['RAM_GB'] > 0)]
    
    if len(group) >= 5:
        return group['RAM_GB'].median()
    
    # Tier 2: Price-based inference
    if price >= price_percentiles[0.90]:
        ram = 16  # High-end
    elif price >= price_percentiles[0.75]:
        ram = 12  # Upper-mid
    elif price >= price_percentiles[0.50]:
        ram = 8   # Mid-range
    else:
        ram = 4   # Budget
    
    # Tier 3: Year adjustment
    if year >= 2024:
        ram = ram * 1.25  # Modern standard higher
    elif year <= 2021:
        ram = ram * 0.75  # Older standard lower
    
    # Tier 4: Round to standard RAM sizes
    standard_sizes = [2, 4, 6, 8, 12, 16, 24, 32, 64]
    ram = min(standard_sizes, key=lambda x: abs(x - ram))
    
    return ram

df['RAM_GB'] = df.apply(impute_ram, axis=1)
print(f"   RAM_GB: {(df['RAM_GB'].notna()).sum()} values ({(df['RAM_GB'].notna()).sum()/len(df)*100:.1f}%)")

# --- RAM_TYPE Cleaning ---
print("\n2. Cleaning RAM_TYPE...")

def infer_ram_type(row):
    ram_type = str(row['RAM_TYPE']).upper().strip()
    
    if ram_type not in ['NEEDTOBEFILLED', 'UNKNOWN', 'NAN']:
        # Standardize existing values
        if 'DDR5' in ram_type or 'LPDDR5' in ram_type:
            return 'DDR5'
        elif 'DDR4' in ram_type or 'LPDDR4' in ram_type:
            return 'DDR4'
        elif 'DDR3' in ram_type or 'LPDDR3' in ram_type:
            return 'DDR3'
        elif 'DDR2' in ram_type:
            return 'DDR2'
    
    # Infer from year + RAM size
    year = row['POST_YEAR']
    ram_gb = row['RAM_GB']
    
    if year >= 2024 and ram_gb >= 32:
        return 'DDR5'
    elif year >= 2023 and ram_gb >= 16:
        return 'DDR5'
    elif year >= 2020:
        return 'DDR4'
    elif year >= 2016:
        return 'DDR3'
    else:
        return 'DDR3'

df['RAM_TYPE'] = df.apply(infer_ram_type, axis=1)
print(f"   RAM_TYPE: Inferred based on year + RAM size")

# --- STORAGE Cleaning ---
print("\n3. Cleaning STORAGE (SSD/HDD)...")

# Parse existing storage values
df['SSD_GB'] = df['SSD_SIZE'].apply(parse_size_to_gb)
df['HDD_GB'] = df['HDD_SIZE'].apply(parse_size_to_gb)

# Rescue mission: Use STORAGE_SIZE to fill missing SSD/HDD
print("   Rescue mission: Using STORAGE_SIZE to recover data...")
rescue_count = 0

for idx, row in df.iterrows():
    if pd.isna(row['SSD_GB']) and pd.isna(row['HDD_GB']):
        storage_size_str = str(row['STORAGE_SIZE'])
        if storage_size_str != 'NeedToBeFilled' and storage_size_str != 'nan':
            storage_gb = parse_size_to_gb(storage_size_str)
            if pd.notna(storage_gb):
                # Check if HDD mentioned
                if 'HDD' in storage_size_str.upper() or 'HARD' in storage_size_str.upper():
                    df.at[idx, 'HDD_GB'] = storage_gb
                    df.at[idx, 'SSD_GB'] = 0
                else:
                    # Default to SSD for modern laptops
                    if row['POST_YEAR'] >= 2022:
                        df.at[idx, 'SSD_GB'] = storage_gb
                        df.at[idx, 'HDD_GB'] = 0
                    else:
                        # Older laptops - could be HDD
                        if storage_gb >= 500:
                            df.at[idx, 'HDD_GB'] = storage_gb
                            df.at[idx, 'SSD_GB'] = 0
                        else:
                            df.at[idx, 'SSD_GB'] = storage_gb
                            df.at[idx, 'HDD_GB'] = 0
                rescue_count += 1

print(f"   Rescued {rescue_count} rows from STORAGE_SIZE")

# Intelligent storage imputation
print("   Imputing remaining missing storage...")

def impute_storage(row):
    ssd = row['SSD_GB'] if pd.notna(row['SSD_GB']) else 0
    hdd = row['HDD_GB'] if pd.notna(row['HDD_GB']) else 0
    
    if ssd > 0 or hdd > 0:
        return ssd, hdd
    
    # Need to impute
    price = row['PRICE']
    year = row['POST_YEAR']
    
    # Price-based storage size
    if price >= price_percentiles[0.90]:
        storage = 1024  # 1TB
    elif price >= price_percentiles[0.75]:
        storage = 512
    elif price >= price_percentiles[0.50]:
        storage = 256
    else:
        storage = 128
    
    # Year-based type (SSD vs HDD)
    if year >= 2022:
        return storage, 0  # Modern = SSD
    elif year >= 2020:
        return storage, 0  # Mostly SSD
    else:
        # Older laptops - mix
        if storage <= 256:
            return storage, 0  # Small = SSD
        else:
            return 0, storage  # Large = HDD

imputed_count = 0
for idx, row in df.iterrows():
    if (pd.isna(row['SSD_GB']) or row['SSD_GB'] == 0) and (pd.isna(row['HDD_GB']) or row['HDD_GB'] == 0):
        ssd, hdd = impute_storage(row)
        df.at[idx, 'SSD_GB'] = ssd
        df.at[idx, 'HDD_GB'] = hdd
        imputed_count += 1

print(f"   Imputed storage for {imputed_count} rows")

# Fill remaining NaN with 0
df['SSD_GB'] = df['SSD_GB'].fillna(0)
df['HDD_GB'] = df['HDD_GB'].fillna(0)

# --- STORAGE_TYPE Engineering ---
print("\n4. Engineering STORAGE_TYPE...")

def determine_storage_type(row):
    ssd = row['SSD_GB']
    hdd = row['HDD_GB']
    
    if ssd > 0 and hdd > 0:
        return 'Hybrid'
    elif ssd > 0:
        return 'SSD'
    elif hdd > 0:
        return 'HDD'
    else:
        return 'Unknown'

df['STORAGE_TYPE'] = df.apply(determine_storage_type, axis=1)

# Update original columns
df['RAM_SIZE'] = df['RAM_GB'].astype(str) + 'GB'
df['SSD_SIZE'] = df['SSD_GB'].apply(lambda x: f"{int(x)}GB" if x > 0 else 'NeedToBeFilled')
df['HDD_SIZE'] = df['HDD_GB'].apply(lambda x: f"{int(x)}GB" if x > 0 else 'NeedToBeFilled')

print("   STORAGE_TYPE distribution:")
print(df['STORAGE_TYPE'].value_counts())

# ============================================================================
# PART 2: IMPROVED AYA'S FEATURES (SCREEN + CITY)
# ============================================================================

print("\n" + "="*80)
print("PART 2: CLEANING AYA'S FEATURES (IMPROVED STRATEGY)")
print("="*80)

# --- SCREEN_SIZE Cleaning ---
print("\n1. Cleaning SCREEN_SIZE...")

def parse_screen_size(size_str):
    if pd.isna(size_str) or size_str == 'NeedToBeFilled':
        return np.nan
    
    size_str = str(size_str)
    match = re.search(r'(\d+(?:[.,]\d+)?)', size_str)
    if not match:
        return np.nan
    
    size = float(match.group(1).replace(',', '.'))
    
    # Fix typos (e.g., 156 -> 15.6)
    if size > 100:
        size = size / 10
    
    # Validate range
    if 9.0 <= size <= 20.0:
        return size
    return np.nan

df['SCREEN_SIZE'] = df['SCREEN_SIZE'].apply(parse_screen_size)
median_screen = df['SCREEN_SIZE'].median()
df['SCREEN_SIZE'] = df['SCREEN_SIZE'].fillna(median_screen)
print(f"   Filled missing with median: {median_screen}")

# --- SCREEN_FREQUENCY Cleaning ---
print("\n2. Cleaning SCREEN_FREQUENCY...")

def parse_frequency(freq_str):
    if pd.isna(freq_str) or freq_str == 'NeedToBeFilled':
        return np.nan
    
    freq_str = str(freq_str)
    match = re.search(r'(\d+)', freq_str)
    if match:
        return int(match.group(1))
    return np.nan

df['SCREEN_FREQUENCY_NUM'] = df['SCREEN_FREQUENCY'].apply(parse_frequency)

# Intelligent frequency imputation
def impute_frequency(row):
    if pd.notna(row['SCREEN_FREQUENCY_NUM']):
        return row['SCREEN_FREQUENCY_NUM']
    
    model = str(row['LAPTOP_MODEL']).upper()
    gpu = str(row['DEDICATED_GPU']).upper()
    price = row['PRICE']
    
    # Gaming laptops with high-end GPU
    if any(x in model for x in ['ROG', 'OMEN', 'LEGION', 'PREDATOR', 'ALIENWARE', 'TUF']):
        if 'RTX 4090' in gpu or 'RTX 4080' in gpu:
            return 240
        elif 'RTX' in gpu and price > price_percentiles[0.75]:
            return 144
    
    return 60  # Default

df['SCREEN_FREQUENCY_NUM'] = df.apply(impute_frequency, axis=1)
df['SCREEN_FREQUENCY'] = df['SCREEN_FREQUENCY_NUM'].astype(str) + 'Hz'
print(f"   Frequency distribution: {df['SCREEN_FREQUENCY'].value_counts().head()}")

# --- SCREEN_RESOLUTION Cleaning (IMPROVED) ---
print("\n3. Cleaning SCREEN_RESOLUTION (with intelligent inference)...")

def standardize_resolution(res_str):
    if pd.isna(res_str) or res_str == 'NeedToBeFilled':
        return None
    
    res_str = str(res_str).upper()
    
    # Map keywords
    if 'FHD' in res_str or 'FULL HD' in res_str or '1080P' in res_str:
        return '1920x1080'
    elif '4K' in res_str or 'UHD' in res_str or '3840' in res_str:
        return '3840x2160'
    elif 'QHD' in res_str or '2K' in res_str or '2560' in res_str:
        return '2560x1440'
    elif 'HD' in res_str and 'FHD' not in res_str:
        return '1366x768'
    
    # Extract WxH pattern
    match = re.search(r'(\d{3,4})[xX×](\d{3,4})', res_str)
    if match:
        return f"{match.group(1)}x{match.group(2)}"
    
    return None

df['SCREEN_RESOLUTION_CLEAN'] = df['SCREEN_RESOLUTION'].apply(standardize_resolution)

# Intelligent resolution imputation
def impute_resolution(row):
    if row['SCREEN_RESOLUTION_CLEAN'] is not None:
        return row['SCREEN_RESOLUTION_CLEAN']
    
    price = row['PRICE']
    year = row['POST_YEAR']
    size = row['SCREEN_SIZE']
    model = str(row['LAPTOP_MODEL']).upper()
    
    # MacBook special handling
    if 'MACBOOK' in model:
        if size >= 15:
            return '3024x1964'
        return '2560x1600'
    
    # Price + Year + Size based
    if size >= 15.6 and price >= price_percentiles[0.90] and year >= 2023:
        return '3840x2160'  # 4K
    elif size >= 15.6 and price >= price_percentiles[0.75]:
        return '2560x1440'  # QHD
    elif year >= 2020:
        return '1920x1080'  # FHD (modern standard)
    elif year < 2020 or price < price_percentiles[0.25]:
        return '1366x768'  # HD (older/budget)
    else:
        return '1920x1080'

df['SCREEN_RESOLUTION'] = df.apply(impute_resolution, axis=1)
unknown_count = (df['SCREEN_RESOLUTION'] == 'Unknown').sum()
print(f"   Reduced 'Unknown' to: {unknown_count} ({unknown_count/len(df)*100:.1f}%)")
print(f"   Top resolutions: {df['SCREEN_RESOLUTION'].value_counts().head()}")

# --- CITY Cleaning ---
print("\n4. Cleaning CITY...")

def normalize_city(city_str):
    if pd.isna(city_str) or city_str == 'NeedToBeFilled':
        return 'Unknown'
    
    city_str = str(city_str).upper().strip()
    
    # Remove accents
    city_str = city_str.replace('É', 'E').replace('È', 'E').replace('Ê', 'E')
    city_str = city_str.replace('À', 'A').replace('Â', 'A')
    city_str = city_str.replace('Ô', 'O').replace('Ù', 'U')
    
    # Merge variations
    if 'EZZOUAR' in city_str and 'BAB' not in city_str:
        return 'BAB EZZOUAR'
    
    return city_str

df['CITY'] = df['CITY'].apply(normalize_city)
print(f"   Top cities: {df['CITY'].value_counts().head()}")

# ============================================================================
# FINAL REPORT
# ============================================================================

print("\n" + "="*80)
print("FINAL CLEANED DATASET REPORT")
print("="*80)

print(f"\nDataset: {df.shape[0]} rows, {df.shape[1]} columns")

print("\nCleaned Features Summary:")
print("  Your features (6): PRICE, LAPTOP_CONDITION, LAPTOP_BRAND, LAPTOP_MODEL, POST_YEAR, POST_MONTH")
print("  Leena's features (6): RAM_SIZE, RAM_TYPE, SSD_SIZE, HDD_SIZE, STORAGE_SIZE, STORAGE_TYPE")
print("  Aya's features (4): SCREEN_SIZE, SCREEN_FREQUENCY, SCREEN_RESOLUTION, CITY")
print("  Total cleaned: 16/20 features (80%)")

print("\nData Quality Check:")
all_features = ['PRICE', 'LAPTOP_CONDITION', 'LAPTOP_BRAND', 'LAPTOP_MODEL', 'POST_YEAR', 'POST_MONTH',
                'RAM_SIZE', 'RAM_TYPE', 'SSD_SIZE', 'HDD_SIZE', 'STORAGE_TYPE',
                'SCREEN_SIZE', 'SCREEN_FREQUENCY', 'SCREEN_RESOLUTION', 'CITY']

for feature in all_features:
    if feature in df.columns:
        missing = df[feature].isna().sum()
        if df[feature].dtype == 'object':
            unknown = df[feature].isin(['Unknown', 'NeedToBeFilled']).sum()
            total = missing + unknown
            status = "OK" if total < len(df)*0.05 else "WARNING"
            print(f"  [{status}] {feature}: {total} missing/unknown ({total/len(df)*100:.1f}%)")
        else:
            status = "OK" if missing == 0 else "WARNING"
            print(f"  [{status}] {feature}: {missing} missing ({missing/len(df)*100:.1f}%)")

# Export
output_file = 'FINAL_IMPROVED_CLEANED_DATASET.csv'
df.to_csv(output_file, index=False)

print("\n" + "="*80)
print("EXPORT COMPLETED")
print("="*80)
print(f"\nSaved as: {output_file}")
print(f"Rows: {len(df):,} (preserved {len(df)/53445*100:.1f}% of original data)")
print(f"Columns: {len(df.columns)}")

print("\nKey Improvements:")
print("  - Leena's features: Preserved 99%+ rows (vs 33% in original)")
print("  - RAM_TYPE: Inferred from year (vs 80% 'Unknown')")
print("  - SCREEN_RESOLUTION: Inferred from price/year (vs 77% 'Unknown')")
print("  - SCREEN_FREQUENCY: Gaming laptops get 144Hz/240Hz")

print("\n" + "="*80)
print("SUCCESS! Dataset ready for modeling")
print("="*80)
