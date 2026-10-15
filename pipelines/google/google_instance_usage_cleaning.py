from pathlib import Path

import pandas as pd

# Load raw data
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
INPUT_FILE = DATA_DIR / "google_instance_usage_raw.csv"

df = pd.read_csv(INPUT_FILE)

print("Original shape:", df.shape)

# Validate required columns
required_columns = [
    "machine_id",
    "start_time",
    "end_time",
    "avg_cpu_usage",
    "avg_memory_usage",
]

assert all(col in df.columns for col in required_columns)

# Check missing values and duplicates
assert df[required_columns].notna().all().all(), "Missing values found"
assert not df.duplicated().any(), "Duplicate rows found"

# Validate time intervals
assert (df["end_time"] > df["start_time"]).all(), "Invalid time intervals"

# Calculate interval duration in minutes
df["duration_minutes"] = (
    df["end_time"] - df["start_time"]
) / 60_000_000

# Validate usage values
assert df["avg_cpu_usage"].between(0, 1).all(), "Invalid CPU usage"
assert df["avg_memory_usage"].between(0, 1).all(), "Invalid memory usage"

# Sort data
df = df.sort_values(
    ["machine_id", "start_time"]
).reset_index(drop=True)

# Save cleaned data
output_path = DATA_DIR / "google_instance_usage_cleaned.csv"
df.to_csv(output_path, index=False)

print("Cleaned shape:", df.shape)
print("Unique machines:", df["machine_id"].nunique())
print("Interval durations:", df["duration_minutes"].value_counts().to_dict())
print("Output:", output_path)
print("Validation completed successfully!")
