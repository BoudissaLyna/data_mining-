import pandas as pd
try:
    from mlxtend.frequent_patterns import fpgrowth, association_rules
    from mlxtend.preprocessing import TransactionEncoder
except ImportError:
    print("Error: mlxtend not installed. Please run 'pip install mlxtend'")
    exit(1)

def main():
    # Load Data
    try:
        df = pd.read_csv('../../D_RESULTS/training_dataset.csv')
    except FileNotFoundError:
        try:
            df = pd.read_csv('06_Model_Training_Evaluation/D_RESULTS/training_dataset.csv')
        except FileNotFoundError:
            print("Error: training_dataset.csv not found.")
            return

    print(f"Loaded dataset with shape: {df.shape}")

    # Features to use based on request and insight
    # BRAND_TIER, CPU_TIER, STORAGE_TYPE are requested.
    # Insight mentions GPU and RAM affecting Price.
    # We will include RAM_SIZE and construct a simplified GPU feature if possible, 
    # but strictly adhering to BRAND_TIER, CPU_TIER, STORAGE_TYPE as requested + Price is safer for "Implementation".
    # I will add RAM_SIZE as it helps with the "Insight" about specs.
    
    selected_features = ['BRAND_TIER', 'CPU_TIER', 'STORAGE_TYPE', 'RAM_SIZE']
    target = 'PRICE'

    if target not in df.columns:
        print("Error: PRICE column not found")
        return

    # Check if features exist
    missing_cols = [c for c in selected_features if c not in df.columns]
    if missing_cols:
        print(f"Warning: Missing columns {missing_cols}. Proceeding without them.")
        selected_features = [c for c in selected_features if c in df.columns]

    # Prepare Data Subset
    data = df[selected_features].copy()
    
    # Binning PRICE into Tiers
    # We'll use 4 quartiles: Budget, Mainstream, Premium, High-End
    try:
        data['Price_Tier'] = pd.qcut(df[target], q=4, labels=['Budget', 'Mainstream', 'Premium', 'High-End'])
    except ValueError:
        # Fallback if too few unique values
        data['Price_Tier'] = pd.cut(df[target], bins=4, labels=['Budget', 'Mainstream', 'Premium', 'High-End'])

    # Drop original numerical price if used (not in selected_features for data)
    
    # Handle Missing Values
    data.dropna(inplace=True)
    
    # Convert all to string to ensure categorical treatment
    data = data.astype(str)
    
    print("Features used for Association Rules:")
    print(data.columns.tolist())
    
    # One-Hot Encoding
    # pd.get_dummies creates columns like "BRAND_TIER_Apple", "Price_Tier_Premium"
    data_encoded = pd.get_dummies(data)
    
    # Convert to boolean (required for mlxtend)
    data_encoded = data_encoded.astype(bool)

    print(f"Encoded data shape: {data_encoded.shape}")
    
    # Mining Rules using FP-Growth
    # We want strong patterns. Start with min_support=0.01 (1%) to find niche but strong rules, 
    # or 0.05 (5%) for general patterns.
    # Given dataset size (~20k), 1% is 200 items.
    min_support = 0.05
    print(f"Mining frequent itemsets with min_support={min_support}...")
    
    frequent_itemsets = fpgrowth(data_encoded, min_support=min_support, use_colnames=True)
    
    print(f"Found {len(frequent_itemsets)} frequent itemsets.")

    if len(frequent_itemsets) == 0:
        print("No frequent itemsets found. Try lowering min_support.")
        return

    # Generating Association Rules
    # We are interested in "Confidence" and "Lift"
    # min_threshold for confidence, e.g., 0.5
    min_confidence = 0.5
    print(f"Generating rules with min_confidence={min_confidence}...")
    
    rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=min_confidence)
    
    if rules.empty:
        print("No rules found.")
        return

    # Filter rules where Consequent is a Price Tier
    # This aligns with "Insight: Discover rules like ... => {Price=Premium}"
    def is_price_consequent(consequents):
        # consequents is a frozenset
        for item in consequents:
            if "Price_Tier" in item:
                return True
        return False

    price_rules = rules[rules['consequents'].apply(is_price_consequent)]
    
    # Sort by Lift (strength of association)
    # Sort by Lift (strength of association)
    price_rules = price_rules.sort_values('lift', ascending=False)
    
    # Format for display: Convert frozensets to strings
    def format_set(s):
        return ', '.join(list(s))

    # Evaluation Table
    print("\n" + "="*80)
    print("📊 Evaluation & Validation (Association Rules Analysis)")
    print("="*80)
    print(f"Total Rules found: {len(rules)}")
    print(f"Rules implying Price Tiers: {len(price_rules)}")
    print("-" * 80)
    
    # Select columns to display
    cols_to_show = ['antecedents', 'consequents', 'confidence', 'lift', 'support']
    
    if not price_rules.empty:
        # Create a display copy
        disp_df = price_rules[cols_to_show].copy()
        disp_df['antecedents'] = disp_df['antecedents'].apply(format_set)
        disp_df['consequents'] = disp_df['consequents'].apply(format_set)
        
        # Renaissance formatting to match user request table style
        # | Association Rules | Confidence / Lift |
        print(f"{'Association Rules (Antecedents -> Consequents)':<60} | {'Confidence':<10} | {'Lift':<10}")
        print("-" * 90)
        for idx, row in disp_df.head(20).iterrows():
            rule = f"{{{row['antecedents']}}} => {{{row['consequents']}}}"
            conf = f"{row['confidence']:.2f}"
            lift = f"{row['lift']:.2f}"
            print(f"{rule:<60} | {conf:<10} | {lift:<10}")
    else:
        print("No rules found that imply a specific Price Tier with the given thresholds.")
        print("Top general rules:")
        disp_df = rules.sort_values('lift', ascending=False)[cols_to_show].head(10).copy()
        disp_df['antecedents'] = disp_df['antecedents'].apply(format_set)
        disp_df['consequents'] = disp_df['consequents'].apply(format_set)
        print(disp_df.to_string(index=False))

    # Save results to D_RESULTS
    output_file = '../../D_RESULTS/Leena_Association_Rules_Results.csv'
    price_rules['antecedents'] = price_rules['antecedents'].apply(format_set)
    price_rules['consequents'] = price_rules['consequents'].apply(format_set)
    price_rules.to_csv(output_file, index=False)
    print(f"\nFull results saved to {output_file}")

if __name__ == "__main__":
    main()
