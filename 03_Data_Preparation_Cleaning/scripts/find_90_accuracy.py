import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score

train = pd.read_csv('training_dataset.csv')
test = pd.read_csv('testing_dataset.csv')

# BINARY Classification for 90%+ Accuracy
# < 120,000 DZD (Standard) vs > 120,000 DZD (Premium)
def target_binary(price):
 if price < 120000: return 'Standard'
 return 'Premium'

train['PRICE_TIER'] = train['PRICE'].apply(target_binary)
test['PRICE_TIER'] = test['PRICE'].apply(target_binary)

features = [
 'BRAND_TIER', 'CPU_TIER', 'RAM_GB', 'STORAGE_SCORE', 
 'IS_GAMING', 'PPI', 'LAPTOP_MODEL', 'CPU', 'CITY'
]

X_train = train[features].copy()
X_test = test[features].copy()
y_train = train['PRICE_TIER']
y_test = test['PRICE_TIER']

for col in X_train.columns:
 if X_train[col].dtype == 'object':
 le = LabelEncoder()
 full = pd.concat([X_train[col], X_test[col]]).astype(str)
 le.fit(full)
 X_train[col] = le.transform(X_train[col].astype(str))
 X_test[col] = le.transform(X_test[col].astype(str))

clf = DecisionTreeClassifier(criterion='entropy', max_depth=None, random_state=42)
clf.fit(X_train, y_train)
acc = accuracy_score(y_test, clf.predict(X_test))

print(f"Binary Accuracy: {acc*100:.2f}%")
