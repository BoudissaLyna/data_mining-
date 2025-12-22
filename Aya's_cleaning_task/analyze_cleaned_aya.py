import csv
import collections

file_path = "c:/Users/Administrator/Documents/data_mining-/Aya's_cleaning_task/cleaned_dataset_aya.csv"
target_cols = ['SCREEN_SIZE', 'SCREEN_FREQUENCY', 'SCREEN_RESOLUTION', 'CITY']

stats = {col: {'missing_ntbf': 0, 'missing_empty': 0, 'values': collections.Counter()} for col in target_cols}
total_rows = 0

with open(file_path, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        total_rows += 1
        for col in target_cols:
            val = row.get(col, '').strip()
            if val == 'NeedToBeFilled':
                stats[col]['missing_ntbf'] += 1
            elif val == '':
                stats[col]['missing_empty'] += 1
            else:
                stats[col]['values'][val] += 1

with open("Aya's_cleaning_task/analysis_results_cleaned.txt", 'w', encoding='utf-8') as f:
    f.write(f"Total rows: {total_rows}\n")
    
    for col in target_cols:
        f.write(f"\n--- {col} ---\n")
        s = stats[col]
        total_missing = s['missing_ntbf'] + s['missing_empty']
        f.write(f"Missing (NeedToBeFilled): {s['missing_ntbf']}\n")
        f.write(f"Missing (Empty): {s['missing_empty']}\n")
        f.write(f"Total Missing: {total_missing} ({total_missing/total_rows*100:.2f}%)\n")
        
        unique_vals = list(s['values'].keys())
        f.write(f"Unique values count: {len(unique_vals)}\n")
        
        # Sort by frequency
        most_common = s['values'].most_common(50)
        f.write(f"Most common values: {most_common}\n")
