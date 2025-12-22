# 📋 Data Cleaning Strategy Plan (Aya's Task)

This document outlines the detailed step-by-step plan to clean the `full_merged_dataset.csv` focusing on the attributes: `SCREEN_SIZE`, `SCREEN_FREQUENCY`, `SCREEN_RESOLUTION`, and `CITY`.

**Assigned Features:** `SCREEN_SIZE`, `SCREEN_FREQUENCY`, `SCREEN_RESOLUTION`, `CITY`.

---

## 🔍 Phase 1: Diagnosis

Based on the analysis of `full_merged_dataset.csv`:

1.  **SCREEN_SIZE**:
    *   15.5% missing.
    *   Values include "15.6", "14.0", "14 inch", "15.6 inch", etc.
    *   Some outliers/typos like "156" (likely 15.6).

2.  **SCREEN_FREQUENCY**:
    *   96% missing (Critical).
    *   Values include "144Hz", "60Hz", "120Hz".
    *   High missingness suggests most are standard 60Hz screens which don't advertise refresh rate.

3.  **SCREEN_RESOLUTION**:
    *   77% missing.
    *   Values are mixed: "FHD", "1920x1080", "HD", "4K", "QHD".
    *   Needs standardization to a consistent format (e.g., "1920x1080").

4.  **CITY**:
    *   30% missing.
    *   Values need normalization (case sensitivity, accents). "Bab ezzouar" vs "EZZOUAR".

---

## 🛠️ Phase 2: Detailed Execution Plan

### Step 1: Standardization Helper
We will create helper functions to parse and standardize these fields.

### Step 2: Processing `SCREEN_SIZE`
*   **Action**: Clean string to extract float number.
*   **Correction**: Fix common typos (e.g., values > 100 like "156" divided by 10).
*   **Handling Missing Values**:
    *   **Decision**: Fill `NaN` with the **Median** of `SCREEN_SIZE`.
    *   **Reasoning**: Screen sizes are standard (13, 14, 15.6). Median is robust.

### Step 3: Processing `SCREEN_FREQUENCY`
*   **Action**: Extract integer value (remove "Hz").
*   **Handling Missing Values**:
    *   **Decision**: Fill with **60**.
    *   **Reasoning**: 60Hz is the standard industry default. If it's not advertised, it's almost certainly 60Hz. Leaving it as NaN or "Unknown" would discard 96% of data or create a useless category.

### Step 4: Processing `SCREEN_RESOLUTION`
*   **Action**: Map common terms to resolution strings.
    *   "FHD", "Full HD", "1080p" ➔ "1920x1080"
    *   "HD" ➔ "1366x768" (Standard Laptop HD)
    *   "QHD", "2K" ➔ "2560x1440"
    *   "4K", "UHD" ➔ "3840x2160"
*   **Handling Missing Values**:
    *   **Decision**: Fill with **"1920x1080"** (Mode) or **"Unknown"**?
    *   Given 77% missing, filling with Mode (FHD) might be aggressive but "HD" (1366x768) is also common in older/cheaper models.
    *   **Refined Decision**: Fill with **"1920x1080"** as it is the most common *observed* value and the modern standard. However, to be safe and follow Leena's conservative approach for high missingness, we will use **"Unknown"** for completely missing values, but we will aggressively map text descriptions.

### Step 5: Processing `CITY`
*   **Action**: Convert to Uppercase. Remove accents. Trim whitespace.
*   **Handling Missing Values**:
    *   **Decision**: Fill with **"Unknown"**.
    *   **Reasoning**: City is categorical and 30% missing. Imputing mode (Bab Ezzouar) would bias the location data significantly.

---

## 📊 Summary of Expected Outcome
*   **SCREEN_SIZE**: 100% filled (Median imputation).
*   **SCREEN_FREQUENCY**: 100% filled (Default 60Hz).
*   **SCREEN_RESOLUTION**: Standardized format. Missing values marked "Unknown".
*   **CITY**: Normalized. Missing values marked "Unknown".
