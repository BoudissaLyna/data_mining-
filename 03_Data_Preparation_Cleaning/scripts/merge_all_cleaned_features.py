# FINAL DATASET MERGER - IMPROVED VERSION
# Handles row count mismatches between datasets

import pandas as pd
import numpy as np

print("="*80)
print("MERGING ALL CLEANED FEATURES FROM THREE TASKS (IMPROVED)")
print("="*80)

# Load original dataset to use as index reference
print("\nLoading datasets...")
df_original = pd.read_csv('full_merged_dataset.csv')
df_your_clean = pd.read_csv('full_merged_dataset_CLEANED.csv')
df_leena_clean = pd.read_csv('Leena\'s_cleaning_task/cleaned_dataset_leena.csv')
df_aya_clean = pd.read_csv('Aya\'s_cleaning_task/cleaned_dataset_aya.csv')

print(f"Original dataset: {df_original.shape[0]} rows")
print(f"Your cleaned dataset: {df_your_clean.shape[0]} rows, {df_your_clean.shape[1]} columns")
print(f"Leena's cleaned dataset: {df_leena_clean.shape[0]} rows, {df_leena_clean.shape[1]} columns")
print(f"Aya's cleaned dataset: {df_aya_clean.shape[0]} rows, {df_aya_clean.shape[1]} columns")

# Define which features each person cleaned
your_features = ['PRICE', 'LAPTOP_CONDITION', 'LAPTOP_BRAND', 'LAPTOP_MODEL', 'POST_YEAR', 'POST_MONTH']
leena_features = ['RAM_SIZE', 'RAM_TYPE', 'SSD_SIZE', 'HDD_SIZE', 'STORAGE_SIZE', 'STORAGE_TYPE']
aya_features = ['SCREEN_SIZE', 'SCREEN_FREQUENCY', 'SCREEN_RESOLUTION', 'CITY']
uncleaned_features = ['DEDICATED_GPU', 'GPU_GENERAL', 'GPU_INTEGRATED', 'CPU']

print("\nFeature assignments:")
print(f" Your task (6 features): {', '.join(your_features)}")
print(f" Leena's task (6 features): {', '.join(leena_features)}")
print(f" Aya's task (4 features): {', '.join(aya_features)}")
print(f" Uncleaned (4 features): {', '.join(uncleaned_features)}")

# STRATEGY: Use your dataset as base (53,445 rows)
# For Leena's features: only use her cleaned rows, keep original for dropped rows
print("\nMerge Strategy:")
print(" - Using YOUR dataset as base (53,445 rows)")
print(" - Leena dropped rows with no storage -> we'll use original values for those rows")
print(" - Aya kept all rows -> direct replacement")

df_final = df_your_clean.copy()

# Merge Aya's features (same row count - direct replacement)
print("\nMerging Aya's cleaned features (direct replacement)...")
for feature in aya_features:
 if feature in df_aya_clean.columns:
 df_final[feature] = df_aya_clean[feature]
 print(f" Updated {feature} from Aya's work")

# Merge Leena's features (different row count - need matching strategy)
print("\nMerging Leena's cleaned features (with row matching)...")

# Check if Leena's dataset has a unique identifier we can use
# If not, we'll need to create one based on multiple columns
print(" Analyzing Leena's dataset structure...")

# Create a composite key for matching (using features that shouldn't change)
# We'll use PRICE + POST_YEAR + POST_MONTH + CITY as a composite key
key_cols = ['PRICE', 'POST_YEAR', 'POST_MONTH', 'CITY']

# Check if these columns exist in both datasets
if all(col in df_final.columns and col in df_leena_clean.columns for col in key_cols):
 print(f" Using composite key: {', '.join(key_cols)}")
 
 # Create composite key
 df_final['_merge_key'] = df_final[key_cols].astype(str).agg('_'.join, axis=1)
 df_leena_clean['_merge_key'] = df_leena_clean[key_cols].astype(str).agg('_'.join, axis=1)
 
 # For each of Leena's features, update matching rows
 for feature in leena_features:
 if feature in df_leena_clean.columns:
 # Create a mapping from merge_key to cleaned value
 leena_mapping = df_leena_clean.set_index('_merge_key')[feature].to_dict()
 
 # Update rows that exist in Leena's dataset
 matched_count = 0
 for idx, row in df_final.iterrows():
 merge_key = row['_merge_key']
 if merge_key in leena_mapping:
 df_final.at[idx, feature] = leena_mapping[merge_key]
 matched_count += 1
 
 print(f" Updated {feature}: {matched_count} rows matched from Leena's work")
 
 # Remove temporary merge key
 df_final.drop('_merge_key', axis=1, inplace=True)
else:
 print(" WARNING: Cannot create composite key - keeping original Leena features")

# Preserve uncleaned features
print("\nPreserving uncleaned features (as-is from original)...")
for feature in uncleaned_features:
 if feature in df_your_clean.columns:
 print(f" Kept {feature} uncleaned")

# Generate comprehensive report
print("\n" + "="*80)
print("FINAL MERGED DATASET REPORT")
print("="*80)

print(f"\nDataset Dimensions:")
print(f" Total rows: {df_final.shape[0]:,}")
print(f" Total columns: {df_final.shape[1]}")

print(f"\nCleaned Features Summary:")
print(f" Your cleaned features: {len(your_features)}")
print(f" Leena's cleaned features: {len(leena_features)}")
print(f" Aya's cleaned features: {len(aya_features)}")
print(f" Total cleaned: {len(your_features) + len(leena_features) + len(aya_features)}")
print(f" Uncleaned (preserved): {len(uncleaned_features)}")

# Check for missing values in cleaned features
print(f"\nMissing Value Check (Cleaned Features Only):")
all_cleaned_features = your_features + leena_features + aya_features

for feature in all_cleaned_features:
 if feature in df_final.columns:
 missing_count = df_final[feature].isna().sum()
 missing_pct = (missing_count / len(df_final)) * 100
 
 # Also check for placeholder values
 if df_final[feature].dtype == 'object':
 placeholder_count = df_final[feature].isin(['NeedToBeFilled', 'Unknown', 'NEEDTOBEFILLED', 'UNKNOWN']).sum()
 total_missing = missing_count + placeholder_count
 total_pct = (total_missing / len(df_final)) * 100
 
 if total_missing > 0:
 status = "OK" if total_pct < 5 else ("WARNING" if total_pct < 20 else "HIGH")
 print(f" [{status}] {feature}: {missing_count} NaN + {placeholder_count} placeholders = {total_missing} ({total_pct:.2f}%)")
 else:
 print(f" [OK] {feature}: 0 missing (0.00%)")
 else:
 status = "OK" if missing_count == 0 else ("WARNING" if missing_pct < 20 else "HIGH")
 print(f" [{status}] {feature}: {missing_count} missing ({missing_pct:.2f}%)")

# Check uncleaned features
print(f"\nUncleaned Features Status:")
for feature in uncleaned_features:
 if feature in df_final.columns:
 missing_count = df_final[feature].isna().sum()
 missing_pct = (missing_count / len(df_final)) * 100
 
 if df_final[feature].dtype == 'object':
 placeholder_count = df_final[feature].isin(['NeedToBeFilled', 'Unknown', 'NEEDTOBEFILLED']).sum()
 total_missing = missing_count + placeholder_count
 print(f" {feature}: {total_missing} total missing ({(total_missing/len(df_final))*100:.2f}%)")
 else:
 print(f" {feature}: {missing_count} missing ({missing_pct:.2f}%)")

# Show sample of final dataset
print(f"\nSample of Final Merged Dataset (first 5 rows):")
print("="*80)
display_cols = your_features[:3] + leena_features[:2] + aya_features[:2] + uncleaned_features[:1]
print(df_final[display_cols].head())

# Export final merged dataset
output_filename = 'FINAL_MERGED_CLEANED_DATASET.csv'
df_final.to_csv(output_filename, index=False)

print("\n" + "="*80)
print("EXPORT COMPLETED")
print("="*80)
print(f"\nFinal merged dataset saved as: {output_filename}")
print(f"Total rows: {len(df_final):,}")
print(f"Total columns: {len(df_final.columns)}")
print(f"\nDataset breakdown:")
print(f" Cleaned by you: {len(your_features)} features")
print(f" Cleaned by Leena: {len(leena_features)} features (with row matching)")
print(f" Cleaned by Aya: {len(aya_features)} features")
print(f" Uncleaned (preserved): {len(uncleaned_features)} features")
print(f" Total features: {len(df_final.columns)}")

print(f"\nNext steps:")
print(f" 1. Review the merged dataset: {output_filename}")
print(f" 2. Optionally clean the 4 uncleaned GPU/CPU features")
print(f" 3. Proceed with feature engineering and modeling")

print("\n" + "="*80)
print("MERGE COMPLETED SUCCESSFULLY!")
print("="*80)
