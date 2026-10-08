import csv, sys
OUT = "/app/out/customers_clean.csv"
try:
    with open(OUT, newline="") as f:
        header = next(csv.reader(f))
except FileNotFoundError:
    sys.exit(1)
sys.exit(0 if header == ["id", "name", "email", "signup_date"] else 1)
