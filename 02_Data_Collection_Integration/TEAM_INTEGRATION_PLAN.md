#  Team Data Collection & Integration Plan

**Objective:** Consolidate 66,667 raw Ouedkniss listings into a single, high-quality dataset while preserving the unique contributions of each team member.

---

##  Member Contributions & Roles

Our integration strategy was built on a "Specialized Cleaning" model where each member was responsible for a specific technical domain:

### 1. Lyna: Core Market Identity
- **Features:** `PRICE`, `LAPTOP_BRAND`, `LAPTOP_MODEL`, `LAPTOP_CONDITION`
- **Goal:** Establish the target variable's integrity. Removed impossible prices (e.g., 1 DZD or 999M DZD) and standardized brand names to ensure no duplicates like 'DELL' vs 'dell'.

### 2. Aya: Visual & Display Metrics
- **Features:** `SCREEN_SIZE`, `SCREEN_RESOLUTION`, `SCREEN_FREQUENCY`
- **Goal:** Standardized display specs. Handled the complicated text-to-numeric conversion for resolutions (e.g., '1920x1080') and ensured screen sizes were within realistic bounds (11" - 18").

### 3. Leena: Storage & Memory Architecture
- **Features:** `RAM_GB`, `SSD_GB`, `HDD_GB`, `STORAGE_TYPE`
- **Goal:** Managed the core performance specs. Fixed inconsistent labeling (GB vs TB) and filled strategic missing values using market logic (e.g., Gaming laptops usually have SSDs).

### 4. Abdallah & Mimoun: Processing Power & Cross-Validation
- **Features:** `CPU`, `DEDICATED_GPU`, `GPU_INTEGRATED`
- **Goal:** The "Validation Unit". They ensured that the CPU and GPU combinations were logically consistent (e.g., preventing 'i3' laptops from claiming 'RTX 4090' GPUs) and handled the Tier classification.

---

##  The Integration Workflow

1.  **Raw Ingestion:** We pulled all raw scraps into a master CSV.
2.  **Specialized Passes:** Each member ran their cleaning logic on their assigned columns.
3.  **Cross-Validation:** We implemented scripts to check for "Inter-Feature Logic" (e.g., checking if price aligns with the CPU tier).
4.  **Final Merge:** All cleaned columns were unified, resulting in our **Final Master Dataset** of ~42,000 verified records.

---

##  Integration Results
- **Initial Count:** 66,667
- **Discarded (Noise/Outliers):** ~24,000
- **Final Validated Count:** 42,419
- 
