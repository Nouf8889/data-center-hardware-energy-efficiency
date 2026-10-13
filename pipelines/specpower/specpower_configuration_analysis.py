
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / 'data'

# Step 1: Load the prepared energy dataset
df = pd.read_csv(DATA_DIR / "specpower_energy.csv")

# Step 2: Define a minimum performance requirement
# Keep servers performing at or above the dataset's
# median full-load performance.

minimum_performance = df["ssj_ops_100"].median()

eligible_servers = df[
    (df["ssj_ops_100"] >= minimum_performance)
    & (df["ssj_ops_per_watt"] > 0)
].copy()

# Step 3: Rank eligible servers by overall energy efficiency
top_servers = eligible_servers.sort_values(
    by="ssj_ops_per_watt",
    ascending=False
).head(10)

# Step 4: Display hardware configurations and metrics
columns = [
    "hardware_vendor",
    "system_enclosure",
    "cpu_description",
    "cpu_cores",
    "total_memory_gb",
    "ssj_ops_100",
    "avg_watts_100",
    "ssj_ops_per_watt"
]

print("\nMinimum Required Performance:", minimum_performance)
print("Eligible Servers:", len(eligible_servers))

print("\nTop 10 Energy-Efficient Server Configurations:")
print(top_servers[columns].to_string(index=False))

# Step 5: Check repeated hardware configurations

configuration_columns = [
    "hardware_vendor",
    "cpu_description",
    "cpu_cores",
    "total_memory_gb"
]

print("\nUnique Hardware Configurations:")
print(
    eligible_servers[configuration_columns]
    .drop_duplicates()
    .shape[0]
)

print("\nRepeated Configuration Groups:")
print(
    eligible_servers
    .groupby(configuration_columns, dropna=False)
    .size()
    .sort_values(ascending=False)
    .head(10)
)


# Step 6: Rank distinct hardware configuration groups
# ------------------------------------------------------------
# Select the highest-efficiency benchmark result from each
# configuration group that meets the performance requirement.
#
# This is a best-observed-result ranking, not an average
# or a guarantee of real-world performance.

configuration_columns = [
    "hardware_vendor",
    "cpu_description",
    "cpu_cores",
    "total_memory_gb"
]

# Sort by overall energy efficiency, highest first.
ranked_servers = eligible_servers.sort_values(
    by="ssj_ops_per_watt",
    ascending=False
)

# Keep the best-performing benchmark record per group.
best_configurations = ranked_servers.drop_duplicates(
    subset=configuration_columns,
    keep="first"
)

# Display the top 10 configuration groups.
top_configurations = best_configurations.head(10)

print("\nTotal Distinct Configuration Groups:")
print(len(best_configurations))

print("\nTop 10 Configuration Groups by Energy Efficiency:")
print(top_configurations[
    [
        "hardware_vendor",
        "cpu_description",
        "cpu_cores",
        "total_memory_gb",
        "ssj_ops_100",
        "avg_watts_100",
        "ssj_ops_per_watt"
    ]
].to_string(index=False))


# Step 7: Extract Server Model
# ------------------------------------------------------------
# Remove report dates and HTML/Text link labels from
# the system_enclosure field for clearer comparisons.

df["server_model"] = (
    df["system_enclosure"]
    .astype("string")
    .str.replace(
        r"\s+[A-Z][a-z]{2}\s+\d{1,2},\s+\d{4}\s*\|\s*HTML\s*\|\s*Text.*$",
        "",
        regex=True
    )
    .str.strip()
)

print("\nServer Model Cleaning Check:")
print(
    df[["system_enclosure", "server_model"]]
    .head(10)
    .to_string(index=False)
)
# Step 8: Identify Configurations Including Server Model
# ------------------------------------------------------------
# Include the server model to distinguish hardware configurations
# that share the same CPU and memory specifications.

configuration_columns_detailed = [
    "hardware_vendor",
    "server_model",
    "cpu_description",
    "cpu_cores",
    "total_memory_gb"
]

# Apply the performance threshold to the dataset
# that already contains the cleaned server_model column.
eligible_servers_detailed = df[
    (df["ssj_ops_100"] >= minimum_performance)
    & (df["ssj_ops_per_watt"] > 0)
].copy()

# Select the highest-efficiency benchmark result
# from each detailed configuration group.
best_detailed_configurations = (
    eligible_servers_detailed
    .sort_values("ssj_ops_per_watt", ascending=False)
    .drop_duplicates(
        subset=configuration_columns_detailed,
        keep="first"
    )
)

print("\nDetailed Configuration Groups:")
print(len(best_detailed_configurations))

print("\nTop 10 Detailed Server Configurations:")
print(
    best_detailed_configurations[
        [
            "hardware_vendor",
            "server_model",
            "cpu_description",
            "cpu_cores",
            "total_memory_gb",
            "ssj_ops_100",
            "avg_watts_100",
            "ssj_ops_per_watt"
        ]
    ].head(10).to_string(index=False)
)


# Step 9: Performance-Constrained Server Recommendations
# ------------------------------------------------------------
# Filter all benchmark records by the required performance
# before selecting the most efficient result per configuration.

required_performance = 30_000_000

# Apply the performance requirement first.
performance_eligible = df[
    (df["ssj_ops_100"] >= required_performance)
    & (df["ssj_ops_per_watt"] > 0)
].copy()

# Rank eligible records by overall energy efficiency.
recommended_servers = (
    performance_eligible
    .sort_values("ssj_ops_per_watt", ascending=False)
    .drop_duplicates(
        subset=configuration_columns_detailed,
        keep="first"
    )
)

print("\nPerformance Requirement:", required_performance)
print("Matching Configuration Groups:", len(recommended_servers))

print("\nTop 10 Recommended Server Configurations:")
print(
    recommended_servers[
        [
            "hardware_vendor",
            "server_model",
            "cpu_description",
            "cpu_cores",
            "total_memory_gb",
            "ssj_ops_100",
            "avg_watts_100",
            "ssj_ops_per_watt"
        ]
    ].head(10).to_string(index=False)
)
# Step 10: Export Server Configuration Recommendations
# ------------------------------------------------------------
# Save performance-qualified configuration groups for
# downstream analysis and dashboard development.



output_dir = DATA_DIR
output_dir.mkdir(exist_ok=True)

recommended_servers.to_csv(
    output_dir / "specpower_recommendations.csv",
    index=False
)

print("\nRecommendations exported successfully!")
print("Exported Configurations:", len(recommended_servers))

# Step 11: Inspect CPU Description Variations

print("\nUnique CPU Descriptions:")
print(df["cpu_description"].nunique())

print("\nMost Common CPU Descriptions:")
print(df["cpu_description"].value_counts().head(20))

# Step 12: Standardize CPU Model Names
# ------------------------------------
# Remove clock-speed information while preserving
# the original CPU description.

df["cpu_model"] = (
    df["cpu_description"]
    .astype("string")
    .str.replace(
        r"\s*@?\s*\(?\d+(?:\.\d+)?\s*GHz\b.*$",
        "",
        regex=True,
        case=False
    )
    .str.strip()
    .str.rstrip(" ,")
)

print("\nUnique CPU Models:", df["cpu_model"].nunique())

print("\nCPU Models Ending with an Opening Parenthesis:")
print(
    df.loc[
        df["cpu_model"].str.endswith("(", na=False),
        ["cpu_description", "cpu_model"]
    ]
    .drop_duplicates()
    .to_string(index=False)
)
# Step 13: Validate CPU Model Standardization
# -------------------------------------------
# Identify CPU models mapped from multiple original descriptions.

cpu_variations = (
    df.groupby("cpu_model")["cpu_description"]
    .nunique()
    .sort_values(ascending=False)
)

print("\nCPU Models with Multiple Descriptions:")
print(cpu_variations[cpu_variations > 1].head(15))

print("\nOriginal Descriptions for AMD EPYC 9845:")
print(
    df.loc[
        df["cpu_model"] == "AMD EPYC 9845",
        "cpu_description"
    ]
    .drop_duplicates()
    .to_string(index=False)
)

# Step 14: Investigate Incomplete CPU Model Names
# ------------------------------------------------------------
# Inspect original descriptions that produced an incomplete model.

problematic_models = df[
    df["cpu_model"].str.contains(
        r"\($",
        regex=True,
        na=False
    )
]

print("\nCPU Models Ending with an Opening Parenthesis:")
print(
    problematic_models[
        ["cpu_description", "cpu_model"]
    ]
    .drop_duplicates()
    .to_string(index=False)
)

print("\nTotal Affected Records:", len(problematic_models))

# Step 15: Test Recommendations with Standardized CPU Models
# ------------------------------------------------------------

updated_configuration_columns = [
    "hardware_vendor",
    "server_model",
    "cpu_model",
    "cpu_cores",
    "total_memory_gb"
]

updated_recommendations = (
    df[
        (df["ssj_ops_100"] >= 30_000_000)
        & (df["ssj_ops_per_watt"] > 0)
    ]
    .sort_values("ssj_ops_per_watt", ascending=False)
    .drop_duplicates(
        subset=updated_configuration_columns,
        keep="first"
    )
)

print("\nPrevious Recommendation Groups:", len(recommended_servers))
print("Updated Recommendation Groups:", len(updated_recommendations))

print("\nTop 10 Updated Recommendations:")
print(
    updated_recommendations[
        [
            "hardware_vendor",
            "server_model",
            "cpu_model",
            "cpu_cores",
            "total_memory_gb",
            "ssj_ops_100",
            "avg_watts_100",
            "ssj_ops_per_watt"
        ]
    ].head(10).to_string(index=False)
)

# Step 16: Validate Hardware Configuration Grouping
# ------------------------------------------------------------
# Check whether grouped configurations contain different
# CPU chip counts or thread counts.

configuration_variations = (
    df[
        (df["ssj_ops_100"] >= 30_000_000)
        & (df["ssj_ops_per_watt"] > 0)
    ]
    .groupby(updated_configuration_columns, dropna=False)
    .agg(
        unique_cpu_chips=("cpu_chips", "nunique"),
        unique_cpu_threads=("cpu_threads", "nunique"),
        benchmark_records=("ssj_ops_100", "size")
    )
    .reset_index()
)

inconsistent_groups = configuration_variations[
    (configuration_variations["unique_cpu_chips"] > 1)
    | (configuration_variations["unique_cpu_threads"] > 1)
]

print("\nGroups with Different CPU Chips or Threads:")
print(len(inconsistent_groups))

print("\nExamples:")
print(inconsistent_groups.head(10).to_string(index=False))

# Step 17: Export Updated Server Recommendations
# ------------------------------------------------------------
# Export recommendations using standardized CPU models
# and validated configuration grouping.

updated_recommendations.to_csv(
    DATA_DIR / "specpower_recommendations.csv",
    index=False
)

print("\nUpdated recommendations exported successfully!")
print("Total Configuration Groups:", len(updated_recommendations))

print("\nExported Columns:")
print(updated_recommendations.columns.tolist())

# Step 18: Export Enriched Energy Dataset

df.to_csv(
    DATA_DIR / "specpower_energy.csv",
    index=False
)

print("\nEnergy dataset updated successfully!")
print("Total Rows:", len(df))
print("Total Columns:", len(df.columns))
print("Columns:", df.columns.tolist())
