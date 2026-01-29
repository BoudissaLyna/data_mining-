import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score

train = pd.read_csv('training_dataset.csv')
test = pd.read_csv('testing_dataset.csv')

def categorize_price(price):
    if price < 75000: return 'Budget'
    if price < 130000: return 'Mainstream'
    if price < 200000: return 'High-End'
    return 'Ultimate'

train['PRICE_TIER'] = train['PRICE'].apply(categorize_price)
test['PRICE_TIER'] = test['PRICE'].apply(categorize_price)

# Using HIGH CARDINALITY features like MODEL to push accuracy higher
features = [
    'BRAND_TIER', 'CPU_TIER', 'RAM_GB', 'STORAGE_SCORE', 
    'IS_GAMING', 'PPI', 'LAPTOP_CONDITION', 'TOTAL_PIXELS', 
    'SCREEN_SIZE', 'SSD_GB', 'TOTAL_STORAGE_GB', 'LAPTOP_BRAND', 
    'LAPTOP_MODEL', 'CPU', 'CITY', 'POST_MONTH'
]

X_train = train[features].copy()
y_train = train['PRICE_TIER']
X_test = test[features].copy()
y_test = test['PRICE_TIER']

# Encoding everything
for col in X_train.select_dtypes(include=['object']).columns:
    le = LabelEncoder()
    full_data = pd.concat([X_train[col], X_test[col]]).astype(str)
    le.fit(full_data)
    X_train[col] = le.transform(X_train[col].astype(str))
    X_test[col] = le.transform(X_test[col].astype(str))

# Deep tree to maximize learning
clf = DecisionTreeClassifier(
    criterion='entropy', 
    max_depth=None, # Allow infinite depth
    min_samples_leaf=1, 
    random_state=42
)

clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)
print(f"Final High-Performance Accuracy: {accuracy_score(y_test, y_pred)*100:.2f}%")
