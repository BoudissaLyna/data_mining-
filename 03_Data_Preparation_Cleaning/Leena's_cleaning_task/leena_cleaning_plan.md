# 📋 Data Cleaning Strategy Plan

This document outlines the detailed step-by-step plan to clean the `full_merged_dataset.csv`. The goal is to maximize data accuracy for price prediction while dealing with significant missing values (~10% of rows have no storage info) and inconsistent formatting (French units like 'GO' and 'TO').

**Assigned Features:** `RAM_SIZE`, `RAM_TYPE`, `SSD_SIZE`, `HDD_SIZE`, `STORAGE_SIZE`, `STORAGE_TYPE`.

---

## 🔍 Phase 1: Diagnosis (What we found)
Before writing any code, we analyzed the dataset and found the following critical issues:
1.  **RAM_SIZE**: 4,080 rows (7.6%) are missing. Values include mixed units like `GB`, `GO` (Gigaoctet - French), `MO`, and `MB`.
2.  **RAM_TYPE**: 42,808 rows (80.1%) are missing (`NeedToBeFilled`). This is too high to impute safely.
3.  **Storage (SSD/HDD)**:
    *   `SSD_SIZE` is missing in 46% of rows.
    *   `HDD_SIZE` is missing in 95.7% of rows.
    *   **Critical Finding**: There is a `STORAGE_SIZE` column that contains data for 17,135 rows where SSD/HDD columns are empty. We can use this to "rescue" data.
4.  **"Dead" Data**: 5,811 rows (10.9%) have absolutely no information in `SSD_SIZE`, `HDD_SIZE`, or `STORAGE_SIZE`.

---

## 🛠️ Phase 2: Detailed Execution Plan

### Step 1: Standardization Helper
We need a robust function to parse size strings because the data is messy (e.g., `1TB`, `500 GO`, `512 MB`).
*   **Logic**:
    *   Regex to extract the number.
    *   Detect unit:
        *   `TB`, `TO` ➔ Multiply by 1024 (to get GB).
        *   `GB`, `GO` ➔ Keep as is.
        *   `MB`, `MO` ➔ Divide by 1024.
    *   Return a `float` value representing GB.

### Step 2: Processing `RAM_SIZE`
*   **Action**: Apply the standardization function to create a numeric `RAM_GB` column.
*   **Handling Missing Values**:
    *   **Reasoning**: Only 7.6% of data is missing. Dropping these is unnecessary data loss. Using the *Median* is safer than *Mean* because high-end outliers (e.g., 64GB) won't skew the value for standard laptops.
    *   **Decision**: Fill `NaN` with the **Median** of `RAM_GB`.

### Step 3: Processing `RAM_TYPE`
*   **Action**: Clean the text (uppercase, remove spaces).
*   **Handling Missing Values**:
    *   **Reasoning**: With 80% missing, any method to guess values (like checking CPU generation) is complex and prone to errors. Guessing wrong introduces bias.
    *   **Decision**: Fill all missing values with **"Unknown"**. This acknowledges the missing data without making false assumptions.

### Step 4: The Storage "Rescue Mission" (Recovering 17,000 Rows)
This is the most critical step. We have three columns `SSD_SIZE`, `HDD_SIZE`, and `STORAGE_SIZE` giving us clues.
*   **Step 4.1**: Clean `SSD_SIZE` and `HDD_SIZE` to numeric GB using our helper function.
*   **Step 4.2**: Backfill logic.
    *   Iterate through rows where both `SSD` and `HDD` are missing (NaN).
    *   Check `STORAGE_SIZE`.
    *   **Logic**:
        *   If `STORAGE_SIZE` is found, parse it.
        *   If the text contains "HDD" or "Hard Disk" ➔ Assign to `HDD`.
        *   Otherwise (Default) ➔ Assign to `SSD`.
    *   **Why Default to SSD?**: In the modern market (2024-2025), if a laptop lists "256GB" or "512GB" without specifying type, it is almost almost certainly an SSD. Assuming HDD would undervalue the laptop significantly.
*   **Step 4.3**: Finalizing Partial Missingness.
    *   If a row has `SSD` value but `HDD` is NaN ➔ Set `HDD = 0`.
    *   If a row has `HDD` value but `SSD` is NaN ➔ Set `SSD = 0`.

### Step 5: Engineering `STORAGE_TYPE`
*   **Action**: Drop the existing `STORAGE_TYPE` column (which is 68% missing) and create a fresh one based on our clean data.
*   **Logic**:
    *   If `SSD > 0` and `HDD > 0` ➔ **"Hybrid"**
    *   If `SSD > 0` and `HDD == 0` ➔ **"SSD"**
    *   If `HDD > 0` and `SSD == 0` ➔ **"HDD"**
    *   Else ➔ **"Unknown"** (These will be dropped in the next step).
*   **Reasoning**: This ensures 100% consistency between the storage size columns and the type column.

### Step 6: Dropping Irreparable Rows
*   **Action**: Filter out rows where `RAM_GB` is 0/NaN OR (`SSD_GB` == 0 AND `HDD_GB` == 0).
*   **Count**: This will remove approximately **5,811 rows**.
*   **Reasoning**: A laptop price prediction model cannot function without knowing the storage capacity. A valid row *must* have at least some RAM and some Storage. Keeping these "blind" rows adds noise that reduces the accuracy of the model on valid data.

---

## 📊 Summary of Expected Outcome
*   **Original Rows**: 53,445
*   **Rows with Storage Info Recovered**: ~17,135 (that would have otherwise been empty)
*   **Rows Dropped**: ~5,811 (~10%)
*   **Final Dataset Size**: ~47,600 Clean Rows
*   **Units**: All sizes standardized to **GB**.
