import pandas as pd
import numpy as np

file_path = r'c:\Users\amine\Downloads\data_mining-\full_merged_dataset.csv'
df = pd.read_csv(file_path)

target_cols = ['RAM_SIZE', 'RAM_TYPE', 'SSD_SIZE', 'HDD_SIZE', 'STORAGE_SIZE', 'STORAGE_TYPE']


with open('analysis_results.txt', 'w', encoding='utf-8') as f:
    f.write(f"Total rows: {len(df)}\n")

    for col in target_cols:
        f.write(f"\n--- {col} ---\n")
        missing_count = df[col].apply(lambda x: x == 'NeedToBeFilled').sum()
        f.write(f"Missing (NeedToBeFilled): {missing_count} ({missing_count/len(df)*100:.2f}%)\n")
        
        # Get unique values excluding NeedToBeFilled
        unique_vals = df[df[col] != 'NeedToBeFilled'][col].unique()
        f.write(f"Unique values count: {len(unique_vals)}\n")
        f.write(f"Sample values: {unique_vals[:20]}\n")

    # Check relationship between storage columns
    f.write("\n--- Storage Logic Check ---\n")
    # Count rows where SSD and HDD are both NeedToBeFilled
    both_missing = df[(df['SSD_SIZE'] == 'NeedToBeFilled') & (df['HDD_SIZE'] == 'NeedToBeFilled')]
    f.write(f"Rows with both SSD and HDD missing: {len(both_missing)}\n")

    # Count rows where STORAGE_SIZE is present
    storage_present = df[df['STORAGE_SIZE'] != 'NeedToBeFilled']
    f.write(f"Rows with STORAGE_SIZE present: {len(storage_present)}\n")

    # Check overlap
    intersection = both_missing[both_missing['STORAGE_SIZE'] != 'NeedToBeFilled']
    f.write(f"Rows with both SSD/HDD missing but STORAGE_SIZE present: {len(intersection)}\n")
