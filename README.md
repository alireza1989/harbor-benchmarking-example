# harbor-benchmarking-example

Companion code for the blog post
[Your Agent Benchmark Is Only as Honest as Its Verifier](https://alidarbehani.com)
on alidarbehani.com.

A tiny CSV dedupe task for [Harbor](https://github.com/harbor-framework/harbor),
broken on purpose in a few ways, plus baseline agents that never call a model.
Everything runs locally with Docker. No API keys.

## Run it

Clone the repo and run everything from its root folder:

```bash
git clone https://github.com/alireza1989/harbor-benchmarking-example
cd harbor-benchmarking-example
```

Then:

```bash
pip install harbor        # tested with harbor 0.24.0
./run_all.sh              # every run from the post, about 20 minutes
harbor view jobs          # browse trajectories and verifier output
```

Or run a single check, for example:

```bash
harbor run -p csv-dedupe-buggy -a nop        # Check 2: RewardFileNotFoundError
PYTHONPATH=. harbor run -p csv-dedupe-weak -a agents.lazy:LazyCopyAgent   # Check 3
```

## What's here

| Path | What it is |
| --- | --- |
| `csv-dedupe/` | The task, with a verifier that writes 0 on failure |
| `csv-dedupe-buggy/` | Same task with the `set -e` verifier that crashes instead of scoring 0 |
| `csv-dedupe-weak/` | Same task with a weak verifier that only checks the header |
| `agents/lazy.py` | Copies the input to the output path and ignores the instruction |
| `agents/hang.py` | Solves the task, then hangs past the agent timeout |
| `agents/flaky.py` | Solves each task with probability 0.6, otherwise does nothing |
| `scripts/make_dedupe20.py` | Generates the 20-task dataset used for the variance runs (seeded) |
| `scripts/triage.py` | Sorts a job's trials into passed, failed, timed out, verifier broken, infra |
| `scripts/always.py` | Counts tasks solved in every attempt (pass^k) |
| `scripts/cost.py` | Total cost and cost per solved trial from `result.json` files |

Usage for the scripts: `python3 scripts/triage.py jobs/<job-name>`.

## Results from the post

Harbor 0.24.0, on a 2-vCPU Linux VM.

- Coin-flip agent (true rate 0.60), five single-attempt runs on 20 tasks:
  0.50, 0.45, 0.65, 0.50, 0.65
- Same agent with `-k 5` (100 trials): mean 0.56, Pass@2 0.805, Pass@4 0.93,
  Pass@5 0.95, tasks solved in all five attempts: 0 of 20
- Oracle on 20 tasks: 4 min 37 s at `-n 1`, 1 min 22 s at `-n 4`, 1 min 3 s at `-n 8`

The coin-flip numbers are random, so your runs will differ. That's the point.

## License

MIT
