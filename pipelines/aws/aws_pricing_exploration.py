import csv
import requests

INDEX_URL = (
    "https://pricing.us-east-1.amazonaws.com"
    "/offers/v1.0/aws/AmazonEC2/current/region_index.json"
)

print("Connecting to AWS Pricing Data...")

index_response = requests.get(INDEX_URL, timeout=30)
index_response.raise_for_status()

regions = index_response.json()["regions"]
region = regions["us-east-1"]

csv_url = (
    "https://pricing.us-east-1.amazonaws.com"
    + region["currentVersionUrl"].replace("/index.json", "/index.csv")
)

print("Connection successful!")
print("Region: us-east-1")
print("Counting AWS CSV rows and columns...")

rows = 0
columns = None

with requests.get(
    csv_url,
    stream=True,
    timeout=(30, 300)
) as response:
    response.raise_for_status()

    # Read the CSV line by line without saving it
    lines = (
        line.decode("utf-8-sig")
        for line in response.iter_lines()
    )

    reader = csv.reader(lines)

    # Skip metadata until the actual header
    for row in reader:
        if row and row[0] == "SKU":
            columns = len(row)
            print(f"Total Columns: {columns}")
            print("Column Names:", row)
            break

    if columns is None:
        raise ValueError("CSV header not found")

    for row in reader:
        if row and any(row):
            rows += 1

print(f"Total Rows: {rows:,}")
print(f"Total Columns: {columns}")
print("Done!")
