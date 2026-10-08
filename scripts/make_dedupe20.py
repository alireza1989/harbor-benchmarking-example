"""Generate dedupe-20/: 20 copies of csv-dedupe with different data (seeded)."""
import csv, io, random, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC, OUT = ROOT / "csv-dedupe", ROOT / "dedupe-20"
NAMES = ["Maya", "Omar", "Lina", "Theo", "Ava", "Noah", "Zara", "Ilya",
         "Sofia", "Ken", "Priya", "Luis", "Hana", "Ezra", "Nia"]

random.seed(7)
shutil.rmtree(OUT, ignore_errors=True)
OUT.mkdir()
for i in range(1, 21):
    task = OUT / f"dedupe-{i:02d}"
    shutil.copytree(SRC, task)
    toml = task / "task.toml"
    toml.write_text(toml.read_text().replace('name = "demo/csv-dedupe"',
                                              f'name = "demo/dedupe-{i:02d}"'))
    people = random.sample(NAMES, 6)
    rows, expected, seen = [], [], set()
    for rid in range(1, 10):
        name = random.choice(people)
        email = f"{name.lower()}@example.com"
        variant = random.choice([email, email.upper(), " " + email, email + " ",
                                 name.capitalize() + "@example.com"])
        rows.append([str(rid), name, variant,
                     f"2026-0{random.randint(1, 9)}-1{random.randint(0, 9)}"])
        key = variant.strip().lower()
        if key not in seen:
            seen.add(key)
            expected.append(str(rid))
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(["id", "name", "email", "signup_date"])
    w.writerows(rows)
    (task / "environment/data/customers.csv").write_text(buf.getvalue())
    test = task / "tests/test_outputs.py"
    test.write_text(test.read_text().replace('EXPECTED_IDS = ["1", "2", "4", "6"]',
                                             f"EXPECTED_IDS = {expected!r}"))
print(f"wrote {OUT}")
