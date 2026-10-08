import json, sys
from collections import Counter
from pathlib import Path

VERIFIER_BROKEN = {"RewardFileNotFoundError", "RewardFileEmptyError",
                   "VerifierOutputParseError", "VerifierTimeoutError"}

def bucket(r: dict) -> str:
    exc = (r.get("exception_info") or {}).get("exception_type")
    rewards = (r.get("verifier_result") or {}).get("rewards")
    if rewards is None:
        return "verifier broken" if exc in VERIFIER_BROKEN else f"infra: {exc}"
    passed = next(iter(rewards.values())) == 1
    if exc == "AgentTimeoutError":
        return "timed out, passed" if passed else "timed out, failed"
    return "passed" if passed else "failed"

job = Path(sys.argv[1])
counts = Counter(bucket(json.loads(p.read_text()))
                 for p in job.glob("*/result.json"))
for name, n in counts.most_common():
    print(f"{n:4d}  {name}")
