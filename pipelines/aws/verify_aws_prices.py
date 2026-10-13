
import csv
import requests
from pathlib import Path

import pandas as pd

# Current AWS EC2 price list
URL = (
    "https://pricing.us-east-1.amazonaws.com"
    "/offers/v1.0/aws/AmazonEC2/current/us-east-1/index.csv"
)

TARGETS = {"c6i.large", "m6i.large", "r6i.large"}

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
df = pd.read_csv(DATA_DIR / "aws_ec2_pricing_cleaned.csv")

local_prices = dict(zip(
    df["instance_type"],
    df["hourly_price_usd"]
))

official_prices = {}

print("Checking current official AWS prices...")

with requests.get(URL, stream=True, timeout=(30, 180)) as response:
    response.raise_for_status()

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

    for row in reader:
        if row and row[0].strip() == "SKU":
            headers = row
            break
    else:
        raise ValueError("AWS header not found")

    for row in reader:
        if len(row) != len(headers):
            continue

        r = dict(zip(headers, row))
        instance = r.get("Instance Type", "")

        if instance not in TARGETS:
            continue

        if not all([
            r.get("Product Family") == "Compute Instance",
            r.get("TermType") == "OnDemand",
            r.get("Operating System") == "Linux",
            r.get("Tenancy") == "Shared",
            r.get("Region Code") == "us-east-1",
            r.get("Unit") == "Hrs",
            r.get("Currency") == "USD",
            r.get("CapacityStatus") in ("", "Used"),
            r.get("Pre Installed S/W") in ("", "NA"),
            r.get("MarketOption", "") in ("", "OnDemand"),
            r.get("License Model", "") in (
                "", "No License required"
            ),
        ]):
            continue

        price = float(r["PricePerUnit"])

        if price > 0:
            official_prices.setdefault(instance, set()).add(price)

print("\n=== AWS PRICE VERIFICATION ===")

for instance in sorted(TARGETS):
    local = local_prices.get(instance)
    prices = official_prices.get(instance, set())

    if local is None or len(prices) != 1:
        print(f"{instance}: REVIEW REQUIRED - {sorted(prices)}")
        continue

    official = next(iter(prices))
    status = "MATCH" if abs(local - official) < 0.000001 else "MISMATCH"

    print(
        f"{instance}: "
        f"Local=${local:.5f} | "
        f"AWS=${official:.5f} | "
        f"{status}"
    )
