
import pandas as pd
from pathlib import Path

# ============================================================
# SPECpower Dataset - Extraction, Cleaning, and Validation
# ============================================================
# Source: SPECpower_ssj2008 benchmark results
# Purpose:
# Extract server benchmark data, clean and validate the records,
# and prepare datasets for energy efficiency analysis.
# ============================================================


# Step 1: Data Extraction
# ------------------------------------------------------------
# Read the benchmark results table directly from the SPEC website.

url = "https://www.spec.org/power_ssj2008/results/power_ssj2008/"

tables = pd.read_html(url)
df = tables[0]


# Step 2: Initial Data Exploration
# ------------------------------------------------------------
# Examine the dataset structure before applying transformations.

# Display the total number of rows and columns.
print("Dataset Shape:", df.shape)

# Preview the first five records.
print("\nFirst 5 Rows:")
print(df.head())

# Inspect the original column names.
print("\nColumn Names:")
print(df.columns)

# Review column data types and non-null counts.
print("\nDataset Information:")
df.info()

# Identify missing values in the original dataset.
print("\nMissing Values:")
print(df.isnull().sum())

# Count fully duplicated rows before cleaning.
print("\nDuplicate Rows:")
print(df.duplicated().sum())


# Step 3: Remove Repeated Header Rows
# ------------------------------------------------------------
# The HTML table contains multi-level column headers and
# repeated header rows that are not actual benchmark records.

# Flatten MultiIndex columns into single-level column names.
df.columns = [
    "_".join(col).strip() if isinstance(col, tuple) else col
    for col in df.columns
]

# Identify the column used to detect repeated header rows.
header_column = (
    "Hardware Vendor Test Sponsor_"
    "Hardware Vendor Test Sponsor"
)

# Remove repeated headers while preserving actual records.
df_clean = df[
    df[header_column] != "Hardware Vendor Test Sponsor"
].copy()

# Reset the index after removing unnecessary rows.
df_clean.reset_index(drop=True, inplace=True)

# Compare dataset dimensions before and after cleaning.
print("\nBefore Cleaning:", df.shape)
print("\nAfter Cleaning:", df_clean.shape)
print("\nRows Removed:", len(df) - len(df_clean))


# Step 4: Data Quality Assessment
# ------------------------------------------------------------
# Check whether missing values or duplicates remain after
# removing repeated header rows.

print("\nMissing Values After Cleaning:")
print(df_clean.isnull().sum())

print("\nDuplicate Rows After Cleaning:")
print(df_clean.duplicated().sum())


# Step 5: Inspect Data Types and Column Names
# ------------------------------------------------------------
# Review the cleaned dataset structure before standardizing
# column names and converting numerical values.

print("\nCleaned Dataset Information:")
df_clean.info()

print("\nCleaned Column Names:")
print(df_clean.columns.tolist())


# Step 6: Standardize Column Names
# ------------------------------------------------------------
# Rename columns using snake_case to improve readability
# and compatibility with SQL, BigQuery, and dbt.

df_clean = df_clean.rename(columns={
    "Hardware Vendor Test Sponsor_Hardware Vendor Test Sponsor": "hardware_vendor",
    "System Enclosure (if applicable)_System Enclosure (if applicable)": "system_enclosure",
    "Nodes_Nodes": "nodes",
    "JVM Vendor_JVM Vendor": "jvm_vendor",
    "Processor_CPU Description": "cpu_description",
    "Processor_MHz": "cpu_mhz",
    "Processor_Chips": "cpu_chips",
    "Processor_Cores": "cpu_cores",
    "Processor_Total Threads": "cpu_threads",
    "Total Memory (GB)_Total Memory (GB)": "total_memory_gb",
    "Submeasurements_ssj_ops  @ 100%": "ssj_ops_100",
    "Submeasurements_avg. watts @ 100%": "avg_watts_100",
    "Submeasurements_avg. watts @ active idle": "avg_watts_idle",
    "Result (Overall ssj_ops/watt)_Result (Overall ssj_ops/watt)": "ssj_ops_per_watt"
})

print("\nRenamed Columns:")
print(df_clean.columns.tolist())


# Step 7: Convert Numeric Data Types
# ------------------------------------------------------------
# Numeric measurements are initially imported as strings.
# Convert them to numerical types for calculations and analysis.
#
# errors="coerce" converts non-numeric values, such as "NC",
# into NaN instead of raising an exception.

numeric_columns = [
    "nodes",
    "cpu_mhz",
    "cpu_chips",
    "cpu_cores",
    "cpu_threads",
    "total_memory_gb",
    "ssj_ops_100",
    "avg_watts_100",
    "avg_watts_idle",
    "ssj_ops_per_watt"
]

for col in numeric_columns:
    df_clean[col] = pd.to_numeric(
        df_clean[col],
        errors="coerce"
    )

# Verify the converted data types.
print("\nData Types After Conversion:")
print(df_clean.dtypes)

# Check missing values introduced by numeric conversion.
print("\nMissing Values After Conversion:")
print(df_clean[numeric_columns].isnull().sum())


# Step 8: Investigate Invalid Numeric Values
# ------------------------------------------------------------
# Inspect the original power measurements to identify values
# that cannot be converted into numbers.
#
# This check uses the original dataframe, so repeated HTML
# header values may also appear in the results.

original_column = "Submeasurements_avg. watts @ 100%"

invalid_values = df[
    ~pd.to_numeric(
        df[original_column],
        errors="coerce"
    ).notna()
]

print("\nInvalid Power Values:")
print(invalid_values[original_column].value_counts(dropna=False))


# Step 9: Inspect Missing Power Measurements
# ------------------------------------------------------------
# Identify records where full-load power consumption is missing.
# These records may still contain useful hardware information.

missing_power = df_clean[
    df_clean["avg_watts_100"].isna()
]

print("\nRows with Missing Power Values:")
print(missing_power[
    [
        "hardware_vendor",
        "system_enclosure",
        "ssj_ops_100",
        "avg_watts_100",
        "avg_watts_idle",
        "ssj_ops_per_watt"
    ]
].head(10))

print("\nTotal Rows with Missing Power:")
print(len(missing_power))


# Step 10: Prepare the Energy Analysis Dataset
# ------------------------------------------------------------
# Create a separate dataset containing complete energy metrics.
#
# Keep all records in df_clean for traceability.
# Exclude incomplete energy records only from df_energy.

energy_columns = [
    "ssj_ops_100",
    "avg_watts_100",
    "avg_watts_idle",
    "ssj_ops_per_watt"
]

df_energy = df_clean.dropna(
    subset=energy_columns
).copy()

print("\nTotal Cleaned Rows:", len(df_clean))
print("Rows Ready for Energy Analysis:", len(df_energy))
print(
    "Rows Excluded from Energy Analysis:",
    len(df_clean) - len(df_energy)
)


# Step 11: Validate Energy Data Quality
# ------------------------------------------------------------
# Verify that the analysis dataset contains valid energy
# measurements and no fully duplicated records.

print("\nEnergy Data Validation:")

# Check completeness of the required energy columns.
print("Missing Energy Values:")
print(df_energy[energy_columns].isnull().sum())

# Check for duplicate records.
print("\nDuplicate Rows:")
print(df_energy.duplicated().sum())

# Power consumption should be greater than zero.
print("\nInvalid Power Values:")
print((df_energy["avg_watts_100"] <= 0).sum())

# Overall efficiency should be greater than zero.
print("\nInvalid Efficiency Values:")
print((df_energy["ssj_ops_per_watt"] <= 0).sum())

# Review descriptive statistics to identify unusual values.
print("\nEnergy Statistics:")
print(df_energy[energy_columns].describe())


# Step 12: Validate Power Consistency
# ------------------------------------------------------------
# Full-load power is generally expected to be greater than
# or equal to active idle power.
#
# Flag records where idle power exceeds full-load power
# for further investigation.

invalid_power_relationship = df_energy[
    df_energy["avg_watts_idle"] > df_energy["avg_watts_100"]
]

print("\nPower Consistency Check:")
print(
    "Rows where idle power exceeds full-load power:",
    len(invalid_power_relationship)
)

print("\nSample Invalid Rows:")
print(invalid_power_relationship[
    [
        "hardware_vendor",
        "system_enclosure",
        "avg_watts_100",
        "avg_watts_idle"
    ]
].head())



# Step 13: Calculate and Compare Efficiency Metrics
# ------------------------------------------------------------
# Calculate energy efficiency at 100% workload.
# This metric is different from the official SPECpower overall
# efficiency, which includes multiple workload levels.

df_energy["efficiency_100"] = (
    df_energy["ssj_ops_100"] /
    df_energy["avg_watts_100"]
)

# Calculate the percentage difference between the two metrics.
# This is a descriptive comparison, not a data quality failure.

df_energy["efficiency_difference_pct"] = (
    (
        df_energy["efficiency_100"]
        - df_energy["ssj_ops_per_watt"]
    ).abs()
    / df_energy["ssj_ops_per_watt"]
) * 100

print("\nEfficiency Consistency Check:")
print(df_energy[
    [
        "ssj_ops_100",
        "avg_watts_100",
        "efficiency_100",
        "ssj_ops_per_watt",
        "efficiency_difference_pct"
    ]
].head(10))

print("\nEfficiency Difference Statistics:")
print(df_energy["efficiency_difference_pct"].describe())

print("\nInvalid Calculated Efficiency:")
print((df_energy["efficiency_100"] <= 0).sum())


# Step 14: Export Final Datasets
# ------------------------------------------------------------
# Save the cleaned dataset and the final energy analysis dataset.
# Each CSV file is exported only once.

from pathlib import Path

# Create the output directory if it does not exist.
output_dir = Path("data")
output_dir.mkdir(exist_ok=True)

# Export all cleaned benchmark records (14 columns).
df_clean.to_csv(
    output_dir / "specpower_cleaned.csv",
    index=False
)

# Export energy analysis records with calculated metrics (16 columns).
df_energy.to_csv(
    output_dir / "specpower_energy.csv",
    index=False
)

print("\nDatasets Exported Successfully!")
print("Cleaned Dataset:", df_clean.shape)
print("Energy Dataset:", df_energy.shape)

print("\nFinal Energy Columns:")
print(df_energy.columns.tolist())
