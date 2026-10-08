import json, sys
from pathlib import Path

trials = [json.loads(p.read_text()) for p in Path(sys.argv[1]).glob("*/result.json")]

cost = sum((t["agent_result"] or {}).get("cost_usd") or 0 for t in trials)
solved = sum(
    1 for t in trials
    if ((t["verifier_result"] or {}).get("rewards") or {}).get("reward") == 1
)
print(f"{len(trials)} trials, {solved} solved, ${cost:.2f} total")
print(f"${cost / max(solved, 1):.2f} per solved trial")
