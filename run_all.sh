#!/usr/bin/env bash
# Reproduce every run from the post. Needs Docker and Harbor (pip install harbor).
# No model or API key is used. Takes about 20 minutes on a small machine.
set -uo pipefail
cd "$(dirname "$0")"
export PYTHONPATH=.
J=jobs

run() { echo; echo "== $*"; harbor run -o "$J" -y "$@"; }

# Check 1 and 2: oracle and nop, with the broken and the fixed verifier
run -p csv-dedupe-buggy -a oracle --job-name buggy-oracle
run -p csv-dedupe-buggy -a nop    --job-name buggy-nop      # RewardFileNotFoundError
run -p csv-dedupe       -a oracle --job-name fixed-oracle
run -p csv-dedupe       -a nop    --job-name fixed-nop      # a real 0

# Check 3: three baselines against the strong and the weak verifier
for t in csv-dedupe csv-dedupe-weak; do
  run -p "$t" -a oracle                       --job-name "$t-oracle-baseline"
  run -p "$t" -a nop                          --job-name "$t-nop-baseline"
  run -p "$t" -a agents.lazy:LazyCopyAgent    --job-name "$t-lazy-baseline"
done

# Check 4: an agent that solves the task, then hangs past a 6-second timeout
run -p csv-dedupe -a agents.hang:SolveThenHangAgent \
    --agent-timeout-multiplier 0.05 --job-name timeout-test

# Check 5: variance and pass@k on 20 tasks with a 60% coin-flip agent
python3 scripts/make_dedupe20.py
for i in 1 2 3 4 5; do
  run -p dedupe-20 -a agents.flaky:CoinFlipAgent --job-name "coin-k1-run$i"
done
run -p dedupe-20 -a agents.flaky:CoinFlipAgent -k 5 --job-name coin-k5

# Harness overhead at different concurrency levels
for n in 1 4 8; do
  run -p dedupe-20 -a oracle -n "$n" --job-name "overhead-n$n"
done

echo; echo "== triage"
for d in "$J"/*/; do echo "$d"; python3 scripts/triage.py "$d"; done
echo; python3 scripts/always.py "$J/coin-k5"
