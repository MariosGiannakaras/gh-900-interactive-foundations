# GH-900 Interactive Foundations

An interactive, hands-on implementation of the official Microsoft Learn **GitHub Foundations Part 1 and Part 2** curriculum, cross-checked against the current **GH-900: GitHub Foundations** exam blueprint.

## Course contract

This is not a shortened study guide. The target is **2 learning paths, 16 official modules, and 106 official units**, with no unit omitted.

For each unit the repository provides, as applicable:

- complete concept coverage in original wording;
- links to the official Microsoft Learn and GitHub sources;
- real Git/GitHub practice when the feature can be exercised safely;
- an interactive scenario when an Enterprise/account feature cannot be reproduced in this repository;
- automatic validation of durable GitHub state where possible;
- original knowledge checks without exposing answers before submission.

The separate GH-900 exam blueprint is also audited so newer exam objectives are not lost if a Learn module has not emphasized them sufficiently.

See [`docs/COVERAGE.md`](docs/COVERAGE.md) and [`curriculum/official-curriculum.yml`](curriculum/official-curriculum.yml).

## Current implementation

### Module 1 — Introduction to Git

Implemented coverage:

- all 6 Microsoft Learn units;
- the linked official GitHub Skills **Introduction to Git** exercise;
- CLI and VS Code Source Control practice;
- Git identity and privacy considerations;
- init/clone, status, staging, commits, history and checkout;
- diffs and unstaging;
- branches and merge strategies;
- remotes and basic collaboration concepts;
- 12-question blind assessment with automatic validation.

### Starting the interactive course

After Module 1 is installed on `main`, a GitHub Actions workflow creates a course Issue named:

```text
GH-900 Interactive Course - Module 1: Introduction to Git
```

Follow the latest instruction posted in that Issue. The first activity is to create the exact branch `lab/module-01-git`. Later steps unlock according to the durable repository state produced by your work.

Do not read or modify the validator to discover answers while taking the assessment; use it as an exam-style blind check.

## Sources of truth

- [Microsoft Learn — GitHub Foundations Part 1](https://learn.microsoft.com/en-us/training/paths/github-foundations/)
- [Microsoft Learn — GitHub Foundations Part 2](https://learn.microsoft.com/en-us/training/paths/github-foundations-2/)
- [Microsoft Learn — GH-900 Study Guide](https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/gh-900)
- [GitHub Skills](https://skills.github.com/)
- [Git documentation](https://git-scm.com/doc)

> The repository maps and teaches the official material but does not reproduce Microsoft Learn course text verbatim.
