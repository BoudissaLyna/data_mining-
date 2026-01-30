import pandas as pd
import numpy as np

print("Starting Master Dataset Cleaning...")

# Load the dataset
df = pd.read_csv('final_cleaned_dataset.csv')
initial_shape = df.shape
print(f"Initial shape: {initial_shape}")

# 1. Handle "NeedToBeFilled" in critical columns
# If we don't know the Brand or CPU, and Model is also unknown, it's trash.
critical_placeholder = 'NeedToBeFilled'

# Check if Brand or CPU is NeedToBeFilled
mask_trash_brand = df['LAPTOP_BRAND'].astype(str).str.contains(critical_placeholder, case=False, na=False)
mask_trash_cpu = df['CPU'].astype(str).str.contains(critical_placeholder, case=False, na=False)
mask_unknown_model = df['LAPTOP_MODEL'].astype(str).str.contains('UNKNOWN', case=False, na=False)

# Drop rows where we don't have enough basic info
# We drop if (Brand is NTBF AND Model is UNKNOWN) OR (CPU is NTBF AND Model is UNKNOWN)
to_drop = (mask_trash_brand & mask_unknown_model) | (mask_trash_cpu & mask_unknown_model)
df = df[~to_drop]
print(f"Dropped {initial_shape[0] - df.shape[0]} rows with missing Brand/CPU and Unknown Model.")

# 2. Fix placeholders in non-critical columns
print("Standardizing labels in non-critical columns...")

# GPU
# If it's NeedToBeFilled, it likely means no dedicated/integrated gpu was specified.
# For DEDICATED_GPU, it should be 'None' if missing.
df['DEDICATED_GPU'] = df['DEDICATED_GPU'].astype(str).replace(r'(?i)NeedToBeFilled', 'None', regex=True)
df['GPU_INTEGRATED'] = df['GPU_INTEGRATED'].astype(str).replace(r'(?i)NeedToBeFilled', 'Integrated', regex=True)
df['GPU_GENERAL'] = df['GPU_GENERAL'].astype(str).replace(r'(?i)NeedToBeFilled', 'Standard Graphics', regex=True)

# Storage
# If SSD_SIZE or HDD_SIZE is NeedToBeFilled, check the numeric columns
# If SSD_GB is 0, then SSD_SIZE should be 'None' or '0GB'
mask_ssd_0 = df['SSD_GB'] == 0
df.loc[mask_ssd_0, 'SSD_SIZE'] = 'None'
df['SSD_SIZE'] = df['SSD_SIZE'].astype(str).replace(r'(?i)NeedToBeFilled', '0GB', regex=True)

mask_hdd_0 = df['HDD_GB'] == 0
df.loc[mask_hdd_0, 'HDD_SIZE'] = 'None'
df['HDD_SIZE'] = df['HDD_SIZE'].astype(str).replace(r'(?i)NeedToBeFilled', '0GB', regex=True)

# STORAGE_SIZE
df['STORAGE_SIZE'] = df['STORAGE_SIZE'].astype(str).replace(r'(?i)NeedToBeFilled', 'Not Specified', regex=True)

# 3. Handle 'Unknown' in other columns
print("Handling 'Unknown' and 'nan' values...")
df['LAPTOP_MODEL'] = df['LAPTOP_MODEL'].astype(str).replace(r'(?i)UNKNOWN', 'Not Specified', regex=True)
df['CITY'] = df['CITY'].astype(str).replace(r'(?i)Unknown', 'Not Specified', regex=True)
df['CITY'] = df['CITY'].astype(str).replace(r'(?i)nan', 'Not Specified', regex=True)

# 4. Rigorous Price Cleaning
# Removing ultra-outliers (anything above 1,000,000 DZD is likely a car or a mistake, or currency error)
# High end gaming laptops in DZ are up to 600k-800k max.
upper_bound = 800000 
lower_bound = 5000 # Anything below 5k DZD is unlikely for a working laptop

price_mask = (df['PRICE'] >= lower_bound) & (df['PRICE'] <= upper_bound)
rows_before_price = df.shape[0]
df = df[price_mask]
print(f"Dropped {rows_before_price - df.shape[0]} rows with unrealistic prices (below 5k or above 800k).")

# 5. Final quality check - Drop any remaining "NeedToBeFilled" in critical columns if they exist
# Actually, let's just replace them with 'Generic' if we decide to keep them, or drop them.
# Given the user's strong reaction, let's just remove them.
for col in ['LAPTOP_BRAND', 'CPU', 'LAPTOP_CONDITION']:
 mask = df[col].astype(str).str.contains(critical_placeholder, case=False, na=False)
 df = df[~mask]

# Final result
final_shape = df.shape
print(f"\nFinal dataset shape: {final_shape}")
print(f"Total data kept: {final_shape[0]/initial_shape[0]*100:.2f}% of previous cleaned dataset")
print(f"Total data kept relative to original (estimated): {final_shape[0]/66667*100:.2f}%")

# Save final dataset
df.to_csv('final_dataset_v2.csv', index=False)
# Overwrite the main one
df.to_csv('final_cleaned_dataset.csv', index=False)

print("\nDone! Dataset is now clean of placeholders.")
