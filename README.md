# GH-900 Interactive Foundations

A complete, autonomous, hands-on implementation of the official Microsoft Learn **GitHub Foundations Part 1 and Part 2** curriculum, cross-checked against the current **GH-900: GitHub Foundations** exam blueprint.

## What this repository contains

This is not a shortened study guide. It maps **2 learning paths, 16 official modules, and 106 official units**, with no unit intentionally omitted.

For every module, the repository provides:

- unit-by-unit theory in original wording;
- links back to the official Microsoft Learn/GitHub sources;
- real Git/GitHub practice where the feature can be exercised safely;
- faithful simulations where Enterprise/account-level features cannot be reproduced in a normal public repository;
- blind knowledge checks whose correct answers are not printed in the lesson;
- automated validation and progression through GitHub Actions.

The current GH-900 exam blueprint is audited separately so newer 2026 exam objectives are not lost when a Learn module gives them less emphasis.

See [`docs/COVERAGE.md`](docs/COVERAGE.md) and [`curriculum/official-curriculum.yml`](curriculum/official-curriculum.yml).

## How a learner uses the course

### 1. Fork this repository

Each learner should use **their own fork**. Course Issues, branches, Pull Requests, Actions runs, and progress then belong to that learner and do not interfere with anyone else.

### 2. Enable GitHub Actions in the fork

GitHub may require Actions to be enabled explicitly on a new fork. Open **Actions** and enable workflows if prompted.

### 3. Start Module 1

From **Actions**, open **GH-900 Module 1 Interactive Course** and choose **Run workflow** once.

The workflow creates a dedicated Issue and posts Step 1. Module 1 follows the GitHub Skills pattern: perform the requested Git/GitHub action, push the durable result, and the workflow posts the next checkpoint automatically.

### 4. Continue automatically through Modules 2–16

After Module 1 passes, a second Issue named:

```text
GH-900 Interactive Foundations — Full Course Progress
```

is created automatically and Module 2 is posted immediately.

For each later module:

1. read the module README;
2. create the exact lab branch shown by the course (`lab/module-02` through `lab/module-16`);
3. complete the real activities or documented simulations;
4. fill the module `submission.md` evidence fields;
5. mark `ACTIVITY_STATUS: COMPLETE` only when the activities are actually done;
6. answer the blind knowledge check;
7. commit and push.

`GH-900 Full Course Progress` validates the submission. If it fails, the progress Issue tells you what needs attention without revealing the correct answers. If it passes, the next module is posted automatically. Module 16 closes the progress Issue as completed.

## Course coverage

| Part | Modules | Units | Status |
|---|---:|---:|---|
| GitHub Foundations Part 1 | 8 | 57 | Implemented |
| GitHub Foundations Part 2 | 8 | 49 | Implemented |
| **Total** | **16** | **106** | **Implemented** |

The implementation includes Git fundamentals, GitHub Flow, repositories, products/plans, code scanning, Copilot, Codespaces, Projects, Markdown, open source, InnerSource, secure-repository practices, administration, authentication/authorization, Pull Requests, repository history/search, and Copilot with Python.

## Enterprise and paid-feature exercises

The course does **not** require a learner to buy GitHub Enterprise, alter billing, or expose real credentials merely to complete the curriculum. Where the official material covers features such as EMU, SAML/SCIM, team synchronization, organization-wide governance, billing/license reports, or paid security capabilities, the lesson combines official theory with read-only inspection and explicit interactive scenarios.

## Integrity of assessments

Module 1 uses a hashed validator and Modules 2–16 use a shared hashed answer map. The course reports which questions need review but does not print the answer key during normal use.

The repository is educational, not tamper-proof: a learner who deliberately reverse-engineers validators can defeat the blind-check design. For genuine exam preparation, do not inspect or modify answer-validation internals while taking a module assessment.

## Quality and completeness checks

`Course Quality` runs on Pull Requests and verifies:

- official curriculum inventory = **16 modules / 106 units**;
- every module README maps the exact number of official unit headings;
- every module has its interactive package;
- runtime catalog and validators are present;
- assessment hash coverage is complete;
- untouched learner submissions cannot pass by default.

## Sources of truth

- [Microsoft Learn — GitHub Foundations Part 1](https://learn.microsoft.com/en-us/training/paths/github-foundations/)
- [Microsoft Learn — GitHub Foundations Part 2](https://learn.microsoft.com/en-us/training/paths/github-foundations-2/)
- [Microsoft Learn — GH-900 Study Guide](https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/gh-900)
- [GitHub Skills](https://skills.github.com/)
- [GitHub Docs](https://docs.github.com/)
- [Git documentation](https://git-scm.com/doc)

> This repository maps and teaches the official curriculum but does not reproduce Microsoft Learn course text verbatim.
