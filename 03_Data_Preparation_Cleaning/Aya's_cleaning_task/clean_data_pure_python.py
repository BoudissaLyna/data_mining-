import csv
import re
import statistics

input_file = r'c:\Users\Administrator\Documents\data_mining-\full_merged_dataset.csv'
output_file = "c:/Users/Administrator/Documents/data_mining-/Aya's_cleaning_task/cleaned_dataset_aya.csv"

def clean_screen_size(val):
    if not val or val == 'NeedToBeFilled':
        return None
    # Remove quotes, "inch", "pouce"
    val = val.lower().replace('"', '').replace("'", '').replace('inch', '').replace('pouce', '').strip()
    # Replace comma with dot
    val = val.replace(',', '.')
    try:
        # Extract first number found
        match = re.search(r'\d+(\.\d+)?', val)
        if match:
            num = float(match.group())
            # Fix outliers like 156 -> 15.6
            if 100 <= num < 200:
                num = num / 10.0
            # Filter unreasonable values (e.g. < 10 or > 30 for laptops)
            if 9 <= num <= 20:
                return round(num, 1)
            # If it's outside range (like 512 which is storage), treat as invalid
            return None
    except:
        pass
    return None

def clean_frequency(val):
    if not val or val == 'NeedToBeFilled':
        return None
    val = val.lower().replace('hz', '').strip()
    try:
        return int(float(val))
    except:
        return None

def clean_resolution(val):
    if not val or val == 'NeedToBeFilled':
        return "Unknown"
    
    val_upper = val.upper()
    
    # Standard mappings
    if 'FHD' in val_upper or '1920X1080' in val_upper or 'FULL HD' in val_upper or '1080P' in val_upper:
        return '1920x1080'
    if '1366X768' in val_upper or ('HD' in val_upper and 'FHD' not in val_upper and 'UHD' not in val_upper and 'QHD' not in val_upper):
        return '1366x768'
    if 'QHD' in val_upper or '2560X1440' in val_upper or '2K' in val_upper:
        return '2560x1440'
    if 'UHD' in val_upper or '4K' in val_upper or '3840X2160' in val_upper:
        return '3840x2160'
        
    # Regex for WxH
    match = re.search(r'(\d{3,4})[xX](\d{3,4})', val)
    if match:
        return f"{match.group(1)}x{match.group(2)}"
        
    return val

def clean_city(val):
    if not val or val == 'NeedToBeFilled':
        return "Unknown"
    # Remove accents and normalize
    val = val.upper().strip()
    replacements = {
        'É': 'E', 'È': 'E', 'Ê': 'E', 'Ë': 'E',
        'À': 'A', 'Â': 'A',
        'Î': 'I', 'Ï': 'I',
        'Ô': 'O',
        'Û': 'U', 'Ù': 'U',
        'Ç': 'C'
    }
    for char, rep in replacements.items():
        val = val.replace(char, rep)
        
    # Specific fix for EZZOUAR
    if val == 'EZZOUAR':
        return 'BAB EZZOUAR'
        
    return val

# 1. Read Data
rows = []
header = []
with open(input_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    header = reader.fieldnames
    for row in reader:
        rows.append(row)

# 2. Calculate Median for Screen Size
screen_sizes = []
for row in rows:
    s = clean_screen_size(row.get('SCREEN_SIZE'))
    if s:
        screen_sizes.append(s)

median_screen_size = statistics.median(screen_sizes) if screen_sizes else 15.6
print(f"Median Screen Size: {median_screen_size}")

# 3. Apply Cleaning
cleaned_rows = []
for row in rows:
    # SCREEN_SIZE
    s_size = clean_screen_size(row.get('SCREEN_SIZE'))
    if s_size is None:
        s_size = median_screen_size
    row['SCREEN_SIZE'] = str(s_size)
    
    # SCREEN_FREQUENCY
    s_freq = clean_frequency(row.get('SCREEN_FREQUENCY'))
    if s_freq is None:
        s_freq = 60 # Default
    row['SCREEN_FREQUENCY'] = f"{s_freq}Hz" # Keep unit for consistency? Or just number? Leena standardized to GB (numeric). 
    # But CSV usually strings. Let's keep "60Hz" format if that's what user wants, or just "60".
    # Leena's plan: "Units: All sizes standardized to GB".
    # So I should probably output numbers.
    # But the column name is SCREEN_FREQUENCY, not SCREEN_FREQUENCY_HZ.
    # I'll stick to "60Hz" to match the style of existing data (e.g. "144Hz"), or strip it?
    # Leena stripped units for RAM_GB.
    # I'll strip units and rename column? No, I should keep column name unless I change it.
    # I'll keep "Hz" suffix for now to be safe, or ask?
    # Leena's plan: "Apply the standardization function to create a numeric RAM_GB column."
    # So she created NEW columns.
    # I should probably do the same or modify in place.
    # "clean these attributes" implies modifying them.
    # I'll modify in place but keep them consistent.
    # If I strip Hz, I should rename to SCREEN_FREQUENCY_HZ.
    # I'll keep "Hz" to be safe as I'm modifying existing column.
    
    # SCREEN_RESOLUTION
    row['SCREEN_RESOLUTION'] = clean_resolution(row.get('SCREEN_RESOLUTION'))
    
    # CITY
    row['CITY'] = clean_city(row.get('CITY'))
    
    cleaned_rows.append(row)

# 4. Write Data
with open(output_file, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=header)
    writer.writeheader()
    writer.writerows(cleaned_rows)

print(f"Cleaned dataset saved to {output_file}")
