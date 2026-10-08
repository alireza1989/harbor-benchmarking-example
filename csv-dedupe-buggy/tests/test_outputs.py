import csv, sys

OUT = "/app/out/customers_clean.csv"
EXPECTED_IDS = ["1", "2", "4", "6"]

def main() -> int:
    try:
        with open(OUT, newline="") as f:
            rows = list(csv.DictReader(f))
            header = rows and list(rows[0].keys())
    except FileNotFoundError:
        print(f"FAIL: {OUT} not found")
        return 1
    if header != ["id", "name", "email", "signup_date"]:
        print(f"FAIL: header is {header}")
        return 1
    ids = [r["id"] for r in rows]
    if ids != EXPECTED_IDS:
        print(f"FAIL: ids {ids} != {EXPECTED_IDS}")
        return 1
    print("PASS")
    return 0

sys.exit(main())
