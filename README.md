# GH-900 Interactive Foundations

[![Course Quality](https://github.com/MariosGiannakaras/gh-900-interactive-foundations/actions/workflows/quality.yml/badge.svg?branch=main)](https://github.com/MariosGiannakaras/gh-900-interactive-foundations/actions/workflows/quality.yml)
![Curriculum](https://img.shields.io/badge/curriculum-16%20modules%20%7C%20106%20units-0969da)
![Template](https://img.shields.io/badge/GitHub-template-8250df?logo=github)
[![License: MIT](https://img.shields.io/badge/license-MIT-2da44e)](LICENSE)

A self-contained, interactive GitHub Foundations course that maps **all 16 Microsoft Learn modules and all 106 official units** from GitHub Foundations Part 1 and Part 2, with hands-on repository work, original assessments, automated validation, and unit-by-unit progression.

The course is independently written and cross-checked against the current **GH-900: GitHub Foundations** study guide. It is not an official Microsoft or GitHub product and is not affiliated with or endorsed by Microsoft or GitHub.

[![Copy Exercise](https://img.shields.io/badge/Copy%20Exercise-%E2%86%92-1f883d?style=for-the-badge&logo=github)](https://github.com/new?template_owner=MariosGiannakaras&template_name=gh-900-interactive-foundations&owner=%40me&name=gh-900-interactive-foundations-course&description=Interactive%20GH-900%20GitHub%20Foundations%20course&visibility=public)

> **Course use:** create a repository with **Copy Exercise** and complete the course in that repository. The upstream template is the maintained course source, not a learner workspace.

## Quick start

1. Select **Copy Exercise** and create a repository under a GitHub account.
2. Open the new repository. Its initial `main` event automatically starts **Step 0 - Start GH-900 Course**.
3. Open the Issue named **GH-900 Interactive Foundations — Course** and follow only the latest instruction.

There is no normal **Actions → Run workflow** setup step. `workflow_dispatch` exists only as a recovery mechanism.

Public visibility provides the simplest course experience and includes standard GitHub-hosted runner usage for public repositories. A private copy can behave differently because plan, billing, fork, and security-feature availability may differ.

## Course at a glance

| Item | Coverage |
|---|---:|
| Microsoft Learn learning paths | **2 / 2** |
| Microsoft Learn modules | **16 / 16** |
| Official units | **106 / 106** |
| Interactive module packages | **16 / 16** |
| Progression | **Unit by unit** |
| Assessments | **Original blind questions** |
| Validation | **Automatic** |

The curriculum is intentionally not an exam-cram summary. Every official unit is represented in sequence and taught in independently written wording. Practical capabilities use repository-based exercises when they can be exercised safely; Enterprise, organization, billing, identity-provider, or paid-feature material uses explicit scenario/read-only exercises instead of pretending that a personal repository has enterprise access.

See [`docs/COVERAGE.md`](docs/COVERAGE.md) for the full curriculum contract and module inventory.

## How the course works

The live course Issue contains one active unit at a time:

```text
M01 U01 → M01 U02 → ... → M16 U07 → Course complete
```

Each checkpoint has one of three modes:

- **Reading / summary:** read the complete local lesson and comment exactly `/next` when ready.
- **Hands-on activity:** perform the requested Git/GitHub change on the specified lab branch. A relevant push or Pull Request update triggers validation automatically.
- **Assessment:** answer the original blind questions on the specified branch and push. Validation identifies questions to review without revealing the answer key.

Useful recovery commands in the course Issue:

- `/help` — show the current unit again.
- `/check` — re-run the current repository-state checkpoint when an automatic event was missed.

## What changes while learning

The exercises intentionally use real repository state. Depending on the unit, learners create or inspect branches, commits, diffs, merges, remotes, Issues, Pull Requests, reviews, status checks, Markdown/GFM, Projects evidence, community/security artifacts, Codespaces/dev-container configuration, code-scanning scenarios, repository administration/identity scenarios, and Python code/tests.

The course never requires a real secret to be committed, an Enterprise subscription to be purchased, or billing to be changed solely to satisfy an exercise.

## Source baseline and traceability

The Microsoft Learn curriculum is pinned to a specific public source snapshot:

```text
MicrosoftDocs/learn@66ab07a355b38fb0f5a4cef8240eb2f765c839c8
Baseline date: 2026-08-06
```

This gives the repository a reproducible curriculum baseline. The GH-900 study guide is cross-checked separately so current exam objectives can be represented even when a Learn unit gives them less emphasis.

Primary traceability files:

- [`curriculum/official-curriculum.yml`](curriculum/official-curriculum.yml) — canonical 16-module / 106-unit inventory.
- [`curriculum/microsoft-source-lock.json`](curriculum/microsoft-source-lock.json) — pinned Microsoft Learn source map.
- [`curriculum/course-catalog.json`](curriculum/course-catalog.json) — runtime module catalog.
- [`docs/COVERAGE.md`](docs/COVERAGE.md) — completeness and blueprint cross-check.

This repository maps and teaches the curriculum but does **not** reproduce Microsoft Learn prose or its knowledge-check question bank verbatim.

## Assessment integrity

Correct assessment answers are stored as hashes rather than printed beside the questions. Normal validation reports which questions require review without revealing correct answers.

This is an educational integrity measure, not DRM. Repository owners can inspect the validation implementation. For realistic exam preparation, avoid reading or modifying assessment-validation internals while taking an assessment.

## Repository structure

| Path | Purpose |
|---|---|
| `modules/` | Independent module lessons mapped to official units |
| `unit-details/` | Source-audited detail used where a unit needs additional depth |
| `labs/` | Hands-on and assessment artifacts |
| `curriculum/` | Canonical inventory, runtime catalog, source lock, assessment hashes |
| `course/` | Course/runtime metadata |
| `scripts/` | State engine, validators, completeness/security audits |
| `.github/workflows/` | Template startup, learner course engine, source quality gate |
| `docs/` | Coverage, architecture, and maintainer documentation |

See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for the runtime and trust model.

## Quality gates

The upstream template runs **Course Quality** before course changes are accepted. The gate verifies, among other things:

- the exact **16-module / 106-unit** official inventory;
- the complete 106-state progression chain;
- source resolution against the pinned Microsoft Learn commit;
- learner-visible semantic depth;
- workflow YAML and Bash syntax;
- Python validator compilation;
- rejection of untouched hands-on and assessment submissions;
- public-repository/community file requirements;
- immutable full-SHA references for external GitHub Actions;
- source-template and learner-runtime isolation.

`Course Quality` is a **source-maintenance** workflow. Template copies use the lightweight learner engine instead of re-running the upstream curriculum audit.

## Security model

The repository is designed so that course automation follows least-privilege principles:

- the upstream template remains inert for learner progression;
- learner startup and progression activate only in non-template copies;
- the source-only quality gate activates only in the template repository;
- workflow permissions are declared explicitly;
- public drive-by Issue comments and Pull Requests are filtered before learner jobs execute;
- third-party workflow dependencies are pinned to immutable commit SHAs;
- no course workflow requires a repository secret.

Security reports should follow [`.github/SECURITY.md`](.github/SECURITY.md). Do not place credentials, tokens, private keys, or exploit details in a public Issue.

## Contributing

Contributions are welcome for factual corrections, accessibility, course-engine reliability, security, validation quality, and independently written curriculum improvements. Curriculum changes must preserve source traceability and the 16-module / 106-unit contract.

Read [`.github/CONTRIBUTING.md`](.github/CONTRIBUTING.md) before opening a Pull Request. Community participation is covered by [`.github/CODE_OF_CONDUCT.md`](.github/CODE_OF_CONDUCT.md).

## License and attribution

Original material and code in this repository are available under the [MIT License](LICENSE), except where a file explicitly states otherwise. Microsoft, GitHub, Microsoft Learn, GH-900, and related names or marks belong to their respective owners.

Reference sources:

- [Microsoft Learn — GitHub Foundations Part 1](https://learn.microsoft.com/en-us/training/paths/github-foundations/)
- [Microsoft Learn — GitHub Foundations Part 2](https://learn.microsoft.com/en-us/training/paths/github-foundations-2/)
- [Microsoft Learn — GH-900 Study Guide](https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/gh-900)
- [GitHub Skills](https://skills.github.com/)
- [GitHub Docs](https://docs.github.com/)
- [Git documentation](https://git-scm.com/doc)

## Maintainer documentation

Repository architecture and operational maintenance are documented in:

- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)
- [`docs/MAINTAINING.md`](docs/MAINTAINING.md)
- [`docs/COVERAGE.md`](docs/COVERAGE.md)
