import pandas as pd
from sklearn.model_selection import train_test_split

print("Starting Dataset Split (70% Train / 30% Test)...")

# Load the master engineered dataset
df = pd.read_csv('final_cleaned_dataset.csv')
print(f"Total rows in master dataset: {len(df)}")

# Splitting the data
# We use random_state=42 so that everyone in your group gets the EXACT same split
train_df, test_df = train_test_split(df, test_size=0.30, random_state=42)

# Save to files
train_df.to_csv('training_dataset.csv', index=False)
test_df.to_csv('testing_dataset.csv', index=False)

print("\nFiles Created Successfully:")
print(f"1. training_dataset.csv: {len(train_df)} rows (70%)")
print(f"2. testing_dataset.csv: {len(test_df)} rows (30%)")

print("\nReady for modeling phase!")
