# Assignment 1 workspace

This directory contains the official student starter for CS336 Assignment 1. No assignment solutions have been added.

## Source and version

- Upstream: <https://github.com/stanford-cs336/assignment1-basics>
- Imported commit: `a158843b20107949f1a8d7df1b05cd33b9166712`
- Imported on: September 20, 2026
- Handout: Spring 2026, version 26.0.3; identical to the supplied PDF.
- Handout SHA-256: `cf402d1c6d3c66da035bdf33b3e2c1bbc4bb92a78b006ee36577e925a265e328`

The upstream README and submission script still contain Spring 2025 labels. All upstream files are preserved as supplied, including the MIT license, agent guidelines, dependency lockfile, and test fixtures. This is a snapshot inside the course repository, not a nested Git repository; pulling this repository does not fetch upstream assignment updates.

## Environment

Run these commands from this directory:

```bash
cd assignment1-basics # if currently at the course repository root
uv sync --locked --python 3.12
uv run --locked pytest --collect-only -q
```

The upstream project supports Python 3.12 and 3.13. The command above selects Python 3.12 and creates an ignored `.venv/` using the committed lockfile. Select `assignment1-basics/.venv/bin/python` as your editor interpreter.

To run the assignment tests:

```bash
uv run --locked pytest
# Run a focused group while working on tokenization:
uv run --locked pytest tests/test_train_bpe.py
```

Test collection should succeed. Tests that call unfinished adapters will fail with `NotImplementedError` until you implement the components and connect them to the adapters.

## Where to work

| Path | Purpose |
| --- | --- |
| `cs336_assignment1_basics.pdf` | Assignment requirements and written questions |
| `cs336_basics/` | Your implementations; includes the official pretokenization example |
| `tests/adapters.py` | Hooks connecting your implementation to the official tests |
| `tests/test_*.py` | Official tests |
| `tests/fixtures/`, `tests/_snapshots/` | Required reference inputs and expected outputs |
| `data/` | Downloaded datasets; contents are ignored except `.gitkeep` |
| `pyproject.toml`, `uv.lock` | Official dependencies and reproducible environment |
| `make_submission.sh` | Official submission packaging helper |

Follow the dataset download instructions in the [upstream README](README.md#download-data) when needed. Full training datasets are not included; the small official test fixtures are included. Store generated checkpoints in `checkpoints/` and experiment outputs in `outputs/`, both ignored by the root repository.

The handout asks for a typeset `writeup.pdf` and a code archive. Add your writeup source here when you begin answering the written questions. Run the packaging helper from this directory; review its exclusions before packaging large datasets or checkpoints. It currently produces `cs336-spring2025-assignment-1-submission.zip` despite the 2026 handout.
