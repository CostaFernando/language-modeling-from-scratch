# Language Modeling from Scratch

My implementations, experiments, and notes while studying [Stanford CS336: Language Modeling from Scratch](https://cs336.stanford.edu/).

This repository will document my work on the course assignments and related projects, from building a tokenizer and Transformer to optimizing training, preparing data, and exploring alignment.

## Assignment roadmap

Based on the [Spring 2026 course outline](https://cs336.stanford.edu/#coursework):

| Assignment | Focus | Status |
| --- | --- | --- |
| 1 — Basics | Tokenization, Transformer architecture, optimizers, and language model training | Not started |
| 2 — Systems | Profiling, efficient attention, and distributed training | Not started |
| 3 — Scaling | Transformer components and scaling laws | Not started |
| 4 — Data | Pretraining data preparation, filtering, and deduplication | Not started |
| 5 — Alignment and Reasoning RL | Supervised fine-tuning and reinforcement learning for reasoning | Not started |

## Getting started

```bash
git clone https://github.com/CostaFernando/language-modeling-from-scratch.git
cd language-modeling-from-scratch
```

The repository currently contains only this README and a `.gitignore`. Setup instructions, dependencies, and commands for running each assignment will be added alongside its implementation.

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
