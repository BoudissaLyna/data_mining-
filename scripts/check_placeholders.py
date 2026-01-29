import pandas as pd

df = pd.read_csv('final_cleaned_dataset.csv')
print(f"Dataset shape: {df.shape}")

print("\nValue counts for 'NeedToBeFilled':")
for col in df.columns:
    count = df[col].astype(str).str.contains('NeedToBeFilled', case=False, na=False).sum()
    if count > 0:
        print(f"{col}: {count} ({count/len(df)*100:.2f}%)")

# Let's also check for other placeholders like 'Unknown'
print("\nValue counts for 'Unknown':")
for col in df.columns:
    count = df[col].astype(str).str.contains('Unknown', case=False, na=False).sum()
    if count > 0:
        print(f"{col}: {count} ({count/len(df)*100:.2f}%)")
