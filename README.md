# GH-900 Interactive Foundations

A self-contained, hands-on transformation of the official Microsoft Learn **GitHub Foundations Part 1 + Part 2** curriculum, cross-checked against the current **GH-900: GitHub Foundations** blueprint.

[![Copy Exercise](https://img.shields.io/badge/Copy%20Exercise-%E2%86%92-1f883d?style=for-the-badge&logo=github)](https://github.com/new?template_owner=MariosGiannakaras&template_name=gh-900-interactive-foundations&owner=%40me&name=gh-900-interactive-foundations-course&description=My%20interactive%20GH-900%20GitHub%20Foundations%20course&visibility=public)

> **Learners:** use **Copy Exercise**. Do not do the course in this source repository.

## What this course guarantees

This is not a shortened exam cram guide. Its curriculum contract is:

- **2/2** official Microsoft Learn learning paths;
- **16/16** official modules;
- **106/106** official units in their Microsoft sequence;
- concepts/details taught by every unit in independently written wording;
- hands-on Git/GitHub activity when the capability can be exercised safely;
- explicit simulations/read-only inspection when Enterprise, organization, billing, paid-product, or identity-provider access cannot reasonably be reproduced in a learner repository;
- original blind assessments rather than copied Microsoft assessment questions;
- automatic validation, feedback, and progression.

The course is source-audited against the pinned public `MicrosoftDocs/learn` snapshot:

```text
66ab07a355b38fb0f5a4cef8240eb2f765c839c8
2026-08-06
```

This gives the repository an exact curriculum baseline. The current GH-900 exam blueprint is checked separately so newer exam objectives can be covered even when a Learn unit gives them less emphasis.

See [`docs/COVERAGE.md`](docs/COVERAGE.md), [`curriculum/official-curriculum.yml`](curriculum/official-curriculum.yml), and [`curriculum/microsoft-source-lock.json`](curriculum/microsoft-source-lock.json).

## Start — like GitHub Skills

### 1. Select **Copy Exercise**

The button opens GitHub's **Create a new repository from template** screen with a suggested learner-repository name. Create the repository under your own account. Public visibility is recommended for the course so standard GitHub-hosted Actions usage is straightforward.

### 2. Open the new repository

There is no normal **Actions → Run workflow** setup step.

The initial `main` creation triggers **Step 0 - Start GH-900 Course** automatically. Step 0 creates one Issue:

```text
GH-900 Interactive Foundations — Course
```

That Issue is the live course interface.

### 3. Follow the latest unit in the Issue

The engine progresses through the official curriculum **unit by unit**, not merely module by module:

```text
M01 U01 → M01 U02 → ... → M16 U07 → Course complete
```

There are **106 official unit checkpoints**.

- **Theory / summary unit:** the complete local lesson for that unit is posted in the course Issue. When understood, comment exactly `/next`.
- **Hands-on unit:** GitHub tells you the branch/activity to perform. Your push triggers validation automatically. If the state is incomplete, the Issue tells you what still needs attention.
- **Assessment unit:** answer the original blind questions on the specified lab branch and push. Validation identifies questions to review without revealing correct answers.
- Comment `/help` at any time to show the current unit again.

A `workflow_dispatch` entry remains only as a recovery/support mechanism. It is **not** the normal learner start flow.

## What changes while you learn

The course intentionally uses real repository state. Depending on the unit, a learner will create or inspect items such as:

- branches, commits, diffs, staging/unstaging, merges, remotes;
- Issues, Pull Requests, links, reviews, status checks and repository collaboration features;
- Markdown/GFM artifacts;
- repository community/security files such as `SECURITY.md` and `CODEOWNERS`;
- GitHub Actions/code-scanning configuration concepts and safe SARIF scenarios;
- Projects planning/automation evidence;
- open-source and InnerSource contribution artifacts;
- administration/permission and identity scenarios for features that require organization/enterprise access;
- Python code/tests for the Copilot-with-Python exercise.

The course never asks a learner to expose a real secret, purchase Enterprise, or change billing solely to prove an exercise.

## Course coverage

| Part | Modules | Units | Interactive status |
|---|---:|---:|---|
| GitHub Foundations Part 1 | 8 | 57 | Implemented |
| GitHub Foundations Part 2 | 8 | 49 | Implemented |
| **Total** | **16** | **106** | **Implemented** |

Topics include Git fundamentals, GitHub Flow, repositories, GitHub products/plans and consumption, code scanning/SARIF, Copilot, Codespaces/dev containers/github.dev, Projects, Markdown/GFM, open source, InnerSource, secure-repository practices, administration, authentication/authorization/SAML/SCIM/EMU/team sync, Pull Requests, repository history/search, and Copilot with Python.

## Enterprise and paid-feature units

Some official material cannot be faithfully provisioned in a normal public learner repository—for example EMU, enterprise SAML/SCIM, team synchronization, organization-wide Copilot policy, enterprise billing/license reports, or some paid security capabilities.

Those units are **not skipped**. They use full theory plus scenario/read-only exercises so the learner still has to apply the correct role, policy, identity, product, or security concept without pretending that a personal repository is an Enterprise tenant.

## Assessment integrity

Correct answers are stored as hashes rather than printed beside the questions. The workflow reports which questions require review but does not reveal the answer key during normal use.

This is educational protection, not DRM: a learner can deliberately inspect/reverse-engineer validators. For genuine exam preparation, do not read or modify answer-validation internals while taking an assessment.

## Quality and completeness gates

`Course Quality` validates the course itself on changes. It checks:

- exact official inventory: **16 modules / 106 units**;
- the sequential **106-unit state machine** (`m01-u01` through `m16-u07`);
- every unit against the pinned Microsoft Learn source tree;
- learner-visible semantic depth so a heading/objective-only placeholder cannot count as coverage;
- 16 interactive module packages;
- automatic Step 0 + event-driven course engine presence;
- workflow YAML parsing;
- Python validator compilation;
- that untouched hands-on submissions cannot pass;
- that untouched assessments cannot pass.

The semantic-depth gate is a mechanical guardrail, not a claim that software can prove semantic equivalence. The source-pinned unit audit plus manual content review are the stronger completeness controls.

## Sources of truth

- [Microsoft Learn — GitHub Foundations Part 1](https://learn.microsoft.com/en-us/training/paths/github-foundations/)
- [Microsoft Learn — GitHub Foundations Part 2](https://learn.microsoft.com/en-us/training/paths/github-foundations-2/)
- [Microsoft Learn — GH-900 Study Guide](https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/gh-900)
- [GitHub Skills](https://skills.github.com/)
- [GitHub Docs](https://docs.github.com/)
- [Git documentation](https://git-scm.com/doc)

> This repository maps and teaches the official curriculum but does not reproduce Microsoft Learn course text verbatim.

## Maintainer requirement

For the **Copy Exercise** button to use GitHub's native template flow, the source repository must have **Settings → General → Template repository** enabled. The course workflows are written so the source repository itself does not create learner progress; a copied learner repository starts automatically on its initial `main` event.
