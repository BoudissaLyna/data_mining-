# IMPROVED DATA CLEANING PLAN FOR LEENA'S FEATURES
# Alternative approach: Intelligent imputation instead of dropping rows
# Uses relationships with PRICE, LAPTOP_BRAND, LAPTOP_MODEL, POST_YEAR, LAPTOP_CONDITION

"""
KEY IMPROVEMENTS OVER ORIGINAL PLAN:
1. Use PRICE to infer RAM/Storage (expensive laptops = more RAM/Storage)
2. Use LAPTOP_BRAND + MODEL to infer typical specs (MacBook Pro = 16GB+, Budget HP = 8GB)
3. Use POST_YEAR to infer modern defaults (2024-2025 laptops = SSD, older = HDD)
4. Use LAPTOP_CONDITION to adjust values (New = higher specs, Used = lower)
5. PRESERVE ALL ROWS instead of dropping 66% of data
"""

## IMPROVED PLAN: INTELLIGENT IMPUTATION STRATEGY

### STEP 1: RAM_SIZE Imputation (Better than just median)

**Original Plan**: Fill missing RAM with global median (7.6% missing)
**Problem**: Ignores that expensive laptops have more RAM

**IMPROVED STRATEGY**:
1. Standardize units to GB (same as original)
2. For missing RAM, use **hierarchical imputation**:
   
   **Tier 1: BRAND + MODEL + PRICE range**
   - Group by BRAND + MODEL
   - Calculate median RAM within similar PRICE range (±20%)
   - Example: Dell Latitude with price 80,000-100,000 DZD → median RAM of similar Latitudes
   
   **Tier 2: PRICE-based inference**
   - If Tier 1 has <3 samples, use PRICE percentiles:
     - PRICE > 90th percentile → 16GB (high-end)
     - PRICE > 75th percentile → 12GB (upper-mid)
     - PRICE > 50th percentile → 8GB (mid-range)
     - PRICE > 25th percentile → 4GB (budget)
     - PRICE ≤ 25th percentile → 4GB (entry-level)
   
   **Tier 3: POST_YEAR adjustment**
   - Newer laptops (2024-2025) → +25% RAM (modern standard)
   - Older laptops (2020-2021) → -25% RAM (older standard)
   
   **Tier 4: Fallback**
   - Use global median (8GB) only if all else fails

**Market Reasoning**: 
- RAM correlates strongly with PRICE (r > 0.7 typically)
- Brand/Model defines product tier (gaming vs business vs budget)
- Modern laptops have higher base RAM (8GB minimum in 2024 vs 4GB in 2020)

---

### STEP 2: RAM_TYPE Imputation (Much better than "Unknown")

**Original Plan**: Fill 80% missing with "Unknown"
**Problem**: Loses valuable information, creates useless category

**IMPROVED STRATEGY**:
1. Standardize existing values (uppercase, remove spaces)
2. For missing RAM_TYPE, **infer from POST_YEAR + RAM_SIZE**:

   **Logic**:
   - If POST_YEAR >= 2020 AND RAM_SIZE >= 8GB → **"DDR4"**
   - If POST_YEAR >= 2023 AND RAM_SIZE >= 16GB → **"DDR5"** (modern high-end)
   - If POST_YEAR >= 2024 AND RAM_SIZE >= 32GB → **"DDR5"** (latest gen)
   - If POST_YEAR < 2020 → **"DDR3"** (older laptops)
   - Else → **"DDR4"** (safe default for 2020-2023)

**Market Reasoning**:
- DDR5 became mainstream in 2022-2023 for high-end laptops
- DDR4 is standard for 2016-2023 laptops
- DDR3 for pre-2016 laptops
- Higher RAM capacity often indicates newer RAM type
- This is **hardware fact**, not guessing (RAM generations are tied to CPU generations)

---

### STEP 3: Storage Imputation (CRITICAL - Avoid dropping 66% of data)

**Original Plan**: Drop rows with no storage info (dropped 35,518 rows!)
**Problem**: Lost 66% of dataset - too aggressive

**IMPROVED STRATEGY**:

#### Step 3.1: Storage "Rescue Mission" (Keep from original plan)
- Use STORAGE_SIZE to backfill SSD/HDD (good approach!)
- Default to SSD for modern laptops (2024-2025)
- Default to HDD for older laptops (2020-2021)

#### Step 3.2: Intelligent Storage Imputation (NEW - for remaining missing)

For rows STILL missing storage after rescue mission:

**Tier 1: BRAND + MODEL + PRICE-based inference**
- Group by BRAND + MODEL
- Calculate median SSD/HDD within similar PRICE range
- Example: HP Pavilion 80,000 DZD → median 512GB SSD

**Tier 2: PRICE percentile-based inference**
- PRICE > 90th percentile → 1TB SSD (high-end)
- PRICE > 75th percentile → 512GB SSD (upper-mid)
- PRICE > 50th percentile → 256GB SSD (mid-range)
- PRICE > 25th percentile → 128GB SSD (budget)
- PRICE ≤ 25th percentile → 128GB SSD or 500GB HDD (entry-level)

**Tier 3: POST_YEAR + LAPTOP_CONDITION adjustment**
- POST_YEAR >= 2023 → SSD (modern standard)
- POST_YEAR < 2021 → 50% chance HDD (older laptops)
- LAPTOP_CONDITION = "New" → +50% storage (newer = larger)
- LAPTOP_CONDITION = "Used - Poor" → -25% storage

**Tier 4: Fallback**
- Default: 256GB SSD (most common in 2024)
- Mark with confidence flag for transparency

**Market Reasoning**:
- Storage size correlates with PRICE (r > 0.6)
- SSDs became standard in 2020+
- Modern laptops rarely have <256GB storage
- Gaming/Professional laptops (high price) = 512GB-1TB
- Budget laptops = 128-256GB

---

### STEP 4: STORAGE_TYPE Engineering (Keep from original)

**Original approach is good**: Derive from SSD/HDD values
- SSD > 0 AND HDD > 0 → "Hybrid"
- SSD > 0 AND HDD = 0 → "SSD"
- HDD > 0 AND SSD = 0 → "HDD"
- Both = 0 → "Unknown" (but we'll impute these now, so very rare)

---

### STEP 5: Final Validation (NO DROPPING!)

**Original Plan**: Drop rows with no storage
**IMPROVED**: Keep ALL rows, mark imputed values

**Strategy**:
1. Add confidence flags:
   - `RAM_IMPUTED` (True/False)
   - `STORAGE_IMPUTED` (True/False)
   - `IMPUTATION_METHOD` (Tier1/Tier2/Tier3/Tier4)

2. Only drop rows if:
   - PRICE is missing (can't impute without price reference)
   - AND all storage/RAM fields are missing
   - **Expected drops**: <1% of data (vs 66% in original plan)

---

## COMPARISON: Original vs Improved Plan

| Metric | Original Plan | Improved Plan |
|--------|--------------|---------------|
| Rows preserved | 17,927 (33.5%) | ~53,000 (99%+) |
| RAM_SIZE missing | 0% (median fill) | 0% (intelligent fill) |
| RAM_TYPE missing | 80% ("Unknown") | <5% (inferred from year) |
| Storage missing | 0% (dropped rows) | <1% (intelligent fill) |
| Data loss | 66% | <1% |
| Imputation quality | Low (global median) | High (contextual) |

---

## EXPECTED OUTCOME

- **Original Rows**: 53,445
- **Rows Dropped**: <500 (<1%) - only truly irreparable cases
- **Final Dataset Size**: ~53,000 Clean Rows (vs 17,927 in original)
- **Data Preserved**: 99%+ (vs 33.5% in original)
- **Quality**: Higher (uses market relationships vs simple median)

---

## IMPLEMENTATION PRIORITY

1. ✅ Keep Leena's standardization logic (excellent)
2. ✅ Keep Leena's storage rescue mission (excellent)
3. ❌ Replace global median with price-based imputation
4. ❌ Replace "Unknown" RAM_TYPE with year-based inference
5. ❌ Replace row dropping with intelligent storage imputation
6. ✅ Keep STORAGE_TYPE engineering (excellent)

---

**CONCLUSION**: This improved plan preserves 99% of data (vs 33%) while maintaining high quality through intelligent imputation using PRICE, BRAND, MODEL, YEAR, and CONDITION relationships.
