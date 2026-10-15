from pathlib import Path

import pandas as pd

# Load raw hardware data
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
INPUT_FILE = DATA_DIR / "google_machine_hardware_raw.csv"

df = pd.read_csv(INPUT_FILE)

print("Original shape:", df.shape)

# Validate required columns
required_columns = [
    "machine_id",
    "platform_id",
    "cpu_capacity",
    "memory_capacity",
    "event_time",
]

assert all(col in df.columns for col in required_columns)

# Check missing values
assert df[required_columns].notna().all().all(), "Missing values found"

# Check duplicate machines
assert not df["machine_id"].duplicated().any(), "Duplicate machine IDs found"

# Validate normalized hardware capacities
assert df["cpu_capacity"].between(0, 1).all(), "Invalid CPU capacity"
assert df["memory_capacity"].between(0, 1).all(), "Invalid memory capacity"

# Sort by machine ID
df = df.sort_values("machine_id").reset_index(drop=True)

# Save cleaned dataset
output_path = DATA_DIR / "google_machine_hardware_cleaned.csv"
df.to_csv(output_path, index=False)

print("Cleaned shape:", df.shape)
print("Unique machines:", df["machine_id"].nunique())
print("Unique platforms:", df["platform_id"].nunique())
print("Output:", output_path)
print("Validation completed successfully!")
