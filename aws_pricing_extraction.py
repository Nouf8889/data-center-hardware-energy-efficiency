
import csv
import re
from collections import Counter
from pathlib import Path

import requests


# ============================================================
# STEP 1: CONFIGURATION
# ============================================================

BASE_URL = "https://pricing.us-east-1.amazonaws.com"

CSV_PATH = (
    "/offers/v1.0/aws/AmazonEC2/"
    "20261009203134/us-east-1/index.csv"
)

URL = BASE_URL + CSV_PATH

OUTPUT_FILE = Path("data/aws_ec2_pricing_cleaned.csv")
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

TARGET_FAMILIES = (
    "m6i.", "c6i.", "r6i.",
    "m7i.", "m7a.",
    "c7i.", "c7a.",
    "r7i.", "r7a."
)

COLUMNS = [
    "instance_type",
    "instance_family",
    "vcpu",
    "memory_gb",
    "physical_processor",
    "processor_architecture",
    "region",
    "operating_system",
    "tenancy",
    "pricing_type",
    "hourly_price_usd",
    "monthly_price_usd",
    "annual_price_usd"
]


# ============================================================
# STEP 2: DATA EXTRACTION & FILTERING
# ============================================================

print("Starting AWS EC2 extraction and cleaning...")
print("Reading AWS pricing data...")

filtered_rows = []
total_rows = 0
rejected = Counter()

with requests.get(
    URL,
    stream=True,
    timeout=(30, 180)
) as response:

    response.raise_for_status()

    # Read AWS CSV line by line
    lines = response.iter_lines(decode_unicode=True)

    reader = csv.reader(
        (
            line.decode("utf-8-sig")
            if isinstance(line, bytes)
            else line
            for line in lines
            if line
        )
    )

    # Find the real CSV header
    for row in reader:
        if row and row[0].strip() == "SKU":
            headers = row
            break
    else:
        raise ValueError("AWS CSV header not found.")

    required_columns = {
        "SKU",
        "Product Family",
        "Instance Type",
        "vCPU",
        "Memory",
        "Region Code",
        "Operating System",
        "Tenancy",
        "TermType",
        "Unit",
        "Currency",
        "PricePerUnit",
        "CapacityStatus",
        "Pre Installed S/W"
    }

    missing_columns = required_columns - set(headers)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    # Read rows while the connection is still open
    for row in reader:

        if len(row) != len(headers):
            rejected["malformed_row"] += 1
            continue

        total_rows += 1

        record = dict(zip(headers, row))
        instance_type = record["Instance Type"].strip()

        # Selected EC2 families only
        if not instance_type.startswith(TARGET_FAMILIES):
            continue

        # Standard EC2 compute instances
        if record["Product Family"] != "Compute Instance":
            continue

        # On-Demand pricing
        if record["TermType"] != "OnDemand":
            continue

        # Linux operating system
        if record["Operating System"] != "Linux":
            continue

        # Shared tenancy
        if record["Tenancy"] != "Shared":
            continue

        # AWS region: Northern Virginia
        if record["Region Code"] != "us-east-1":
            continue

        # Hourly prices in USD
        if record["Unit"] != "Hrs":
            continue

        if record["Currency"] != "USD":
            continue

        # Standard capacity
        if record["CapacityStatus"] not in ("", "Used"):
            continue

        # No additional pre-installed software
        if record["Pre Installed S/W"] not in ("", "NA"):
            continue

        # Exclude alternative market options
        if record.get("MarketOption", "") not in (
            "",
            "OnDemand"
        ):
            continue

        # Exclude additional software licenses
        if record.get("License Model", "") not in (
            "",
            "No License required"
        ):
            continue

        filtered_rows.append(record)


print(f"Total rows scanned: {total_rows:,}")
print(f"Rows after filtering: {len(filtered_rows):,}")


# ============================================================
# STEP 3: DATA CLEANING & TRANSFORMATION
# ============================================================

print("\nCleaning AWS EC2 data...")

cleaned_by_instance = {}
conflicting_records = []

for record in filtered_rows:

    instance_type = record["Instance Type"].strip()

    try:
        vcpu = int(record["vCPU"].strip())

        memory_text = record["Memory"].strip()

        memory_match = re.fullmatch(
            r"([\d,]+(?:\.\d+)?)\s+GiB",
            memory_text
        )

        if memory_match is None:
            rejected["invalid_memory_format"] += 1
            continue

        memory_gb = float(
            memory_match.group(1).replace(",", "")
        )

        hourly_price = float(
            record["PricePerUnit"]
        )

    except (ValueError, TypeError, KeyError):
        rejected["invalid_numeric_value"] += 1
        continue

    # Reject invalid values
    if vcpu <= 0 or memory_gb <= 0 or hourly_price <= 0:
        rejected["non_positive_value"] += 1
        continue

    cleaned_record = {
        "instance_type": instance_type,
        "instance_family": instance_type.split(".")[0],
        "vcpu": vcpu,
        "memory_gb": memory_gb,
        "physical_processor": record.get(
            "Physical Processor", ""
        ).strip(),
        "processor_architecture": record.get(
            "Processor Architecture", ""
        ).strip(),
        "region": record["Region Code"],
        "operating_system": record["Operating System"],
        "tenancy": record["Tenancy"],
        "pricing_type": record["TermType"],
        "hourly_price_usd": round(hourly_price, 6),
        "monthly_price_usd": round(
            hourly_price * 720, 2
        ),
        "annual_price_usd": round(
            hourly_price * 8760, 2
        )
    }

    # Detect duplicate or conflicting records
    if instance_type in cleaned_by_instance:

        previous = cleaned_by_instance[instance_type]

        if previous != cleaned_record:
            conflicting_records.append({
                "instance_type": instance_type,
                "sku": record.get("SKU", ""),
                "rate_code": record.get("RateCode", ""),
                "usage_type": record.get("usageType", ""),
                "operation": record.get("operation", ""),
                "previous_price": previous[
                    "hourly_price_usd"
                ],
                "new_price": hourly_price
            })
        else:
            rejected["identical_duplicate"] += 1

        continue

    cleaned_by_instance[instance_type] = cleaned_record


# ============================================================
# STEP 4: DATA VALIDATION
# ============================================================

print("Validating AWS EC2 data...")

if conflicting_records:

    print("\nWARNING: Conflicting pricing records found!")

    for conflict in conflicting_records[:10]:
        print(conflict)

    raise ValueError(
        f"Found {len(conflicting_records)} "
        "conflicting records. "
        "Review pricing dimensions before exporting."
    )

cleaned_rows = sorted(
    cleaned_by_instance.values(),
    key=lambda row: (
        row["instance_family"],
        row["vcpu"],
        row["instance_type"]
    )
)

if not cleaned_rows:
    raise ValueError("No valid EC2 records found.")

instance_types = [
    row["instance_type"]
    for row in cleaned_rows
]

assert len(instance_types) == len(set(instance_types))

assert all(
    row["vcpu"] > 0
    for row in cleaned_rows
)

assert all(
    row["memory_gb"] > 0
    for row in cleaned_rows
)

assert all(
    row["hourly_price_usd"] > 0
    for row in cleaned_rows
)


# ============================================================
# STEP 5: SAVE CLEANED DATA
# ============================================================

with OUTPUT_FILE.open(
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.DictWriter(
        file,
        fieldnames=COLUMNS
    )

    writer.writeheader()
    writer.writerows(cleaned_rows)


# ============================================================
# STEP 6: SUMMARY REPORT
# ============================================================

print("\n========== AWS CLEANING SUMMARY ==========")

print(f"Cleaned rows: {len(cleaned_rows):,}")
print(f"Total columns: {len(COLUMNS)}")
print("Duplicate instance types: 0")
print("Conflicting pricing records: 0")
print(f"Saved to: {OUTPUT_FILE}")

print("\nInstances by family:")

family_counts = Counter(
    row["instance_family"]
    for row in cleaned_rows
)

for family, count in sorted(family_counts.items()):
    print(f"  {family}: {count}")

print("\nRejected rows:")

for reason, count in sorted(rejected.items()):
    print(f"  {reason}: {count}")

print("\nAWS EC2 cleaning completed successfully!")
