import pandas as pd

hardware = pd.read_csv(
    "data/google_machine_hardware_cleaned.csv"
)

usage = pd.read_csv(
    "data/google_instance_usage_cleaned.csv"
)

# Validate one hardware record per machine
assert hardware["machine_id"].is_unique

# Join usage with hardware capacity
merged = usage.merge(
    hardware,
    on="machine_id",
    how="inner",
    validate="many_to_one"
)

# Check that no usage rows were multiplied
assert len(merged) <= len(usage)

# Calculate resource usage relative to machine capacity
merged["cpu_to_capacity_ratio"] = (
    merged["avg_cpu_usage"] / merged["cpu_capacity"]
)

merged["memory_to_capacity_ratio"] = (
    merged["avg_memory_usage"] / merged["memory_capacity"]
)

# Sort and save
merged = merged.sort_values(
    ["machine_id", "start_time"]
).reset_index(drop=True)

output_path = "data/google_hardware_workload_joined.csv"
merged.to_csv(output_path, index=False)

print("Joined rows:", len(merged))
print("Matched machines:", merged["machine_id"].nunique())
print("Columns:", merged.columns.tolist())
print("Output:", output_path)
print("Join completed successfully!")
