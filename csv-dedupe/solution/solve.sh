#!/bin/bash
set -euo pipefail
mkdir -p /app/out
python3 - <<'PY'
import csv
seen = set()
with open("/app/data/customers.csv", newline="") as f, \
     open("/app/out/customers_clean.csv", "w", newline="") as out:
    reader = csv.DictReader(f)
    writer = csv.DictWriter(out, fieldnames=reader.fieldnames)
    writer.writeheader()
    for row in reader:
        key = row["email"].strip().lower()
        if key not in seen:
            seen.add(key)
            writer.writerow(row)
PY
