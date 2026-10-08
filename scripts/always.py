import json, sys
from collections import defaultdict
from pathlib import Path

by_task = defaultdict(list)
for p in Path(sys.argv[1]).glob("*/result.json"):
    r = json.loads(p.read_text())
    rewards = (r["verifier_result"] or {}).get("rewards") or {}
    by_task[r["task_name"]].append(rewards.get("reward", 0))

always = sum(all(x == 1 for x in v) for v in by_task.values())
print(f"solved every time: {always}/{len(by_task)}")
