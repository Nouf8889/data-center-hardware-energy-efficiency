import pandas as pd

INPUT_FILE = "data/google_power_cella_pdu10_raw.csv"
OUTPUT_FILE = "data/google_power_cella_pdu10_cleaned.csv"

df = pd.read_csv(INPUT_FILE)

required_columns = [
    "time",
    "cell",
    "pdu",
    "measured_power_util",
    "production_power_util",
    "bad_measurement_data",
    "bad_production_power_data",
]

assert all(col in df.columns for col in required_columns)
assert df[required_columns].isna().sum().sum() == 0

df = df.sort_values("time").reset_index(drop=True)

assert not df["time"].duplicated().any()

for col in ["measured_power_util", "production_power_util"]:
    assert df[col].between(0, 1).all()

assert (df["time"].diff().dropna() == 300_000_000).all()

# Relative hours from the first observation
df["hours_from_start"] = (
    (df["time"] - df["time"].min()) / 3_600_000_000
)

# Preserve original quality flags without filtering
df.to_csv(OUTPUT_FILE, index=False)

print("=== GOOGLE POWER CLEANING SUMMARY ===")
print("Rows:", len(df))
print("Columns:", len(df.columns))
print("Missing values:", df.isna().sum().sum())
print("Duplicate timestamps:", df["time"].duplicated().sum())
print("Output:", OUTPUT_FILE)
print("\nQuality flags:")
print(df[
    ["bad_measurement_data", "bad_production_power_data"]
].value_counts())
