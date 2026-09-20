# Language Modeling from Scratch

My implementations, experiments, and notes while studying [Stanford CS336: Language Modeling from Scratch](https://cs336.stanford.edu/).

This repository will document my work on the course assignments and related projects, from building a tokenizer and Transformer to optimizing training, preparing data, and exploring alignment.

## Assignment roadmap

Based on the [Spring 2026 course outline](https://cs336.stanford.edu/#coursework):

| Assignment | Focus | Status |
| --- | --- | --- |
| [1 — Basics](assignment1-basics/SETUP.md) | Tokenization, Transformer architecture, optimizers, and language model training | Starter ready |
| 2 — Systems | Profiling, efficient attention, and distributed training | Not started |
| 3 — Scaling | Transformer components and scaling laws | Not started |
| 4 — Data | Pretraining data preparation, filtering, and deduplication | Not started |
| 5 — Alignment and Reasoning RL | Supervised fine-tuning and reinforcement learning for reasoning | Not started |

## Getting started

```bash
git clone https://github.com/CostaFernando/language-modeling-from-scratch.git
cd language-modeling-from-scratch
```

Assignment 1 is ready in [`assignment1-basics/`](assignment1-basics/). See its [local setup guide](assignment1-basics/SETUP.md) for environment setup, test commands, and file locations. Run assignment commands from that directory.

```bash
cd assignment1-basics
uv sync --locked --python 3.12
uv run --locked pytest --collect-only -q
```

## Repository conventions

- Keep assignment code, tests, and setup instructions together.
- Record experiment configurations and findings so results can be reproduced.
- Keep downloaded datasets, model checkpoints, and generated training outputs out of Git; document how to obtain or regenerate them.
- Commit dependency manifests and lockfiles when introducing project tooling.
- Use `.env.example` for configuration examples and keep local credentials in ignored `.env` files.

## References

- [Course website, lectures, and assignment links](https://cs336.stanford.edu/)
- [Previous offering: Spring 2025](https://stanford-cs336.github.io/spring2025/)

This is a personal study repository and is not affiliated with Stanford University. Course materials and starter code belong to their respective authors.
