# GH-900 Interactive Foundations

[![Course Quality](https://github.com/MariosGiannakaras/gh-900-interactive-foundations/actions/workflows/quality.yml/badge.svg?branch=main)](https://github.com/MariosGiannakaras/gh-900-interactive-foundations/actions/workflows/quality.yml)
![Curriculum](https://img.shields.io/badge/curriculum-16%20modules%20%7C%20106%20units-0969da)
![Template](https://img.shields.io/badge/GitHub-template-8250df?logo=github)
[![License: MIT](https://img.shields.io/badge/license-MIT-2da44e)](LICENSE)

A self-contained, interactive **GH-900: GitHub Foundations** course covering **2 / 2 Microsoft Learn learning paths, 16 / 16 modules, and 106 / 106 official units** in sequence.

The learner experience is designed around GitHub itself: lessons, assessments, progress, validation, and feedback appear in one live course Issue. Temporary repository files and branches are created only when the current unit requires them and are cleaned after validation.

This project is independently written and is not an official Microsoft or GitHub product. Microsoft Learn is used as the public curriculum/source baseline; Microsoft and GitHub trademarks belong to their respective owners.

[![Copy Exercise](https://img.shields.io/badge/Copy%20Exercise-%E2%86%92-1f883d?style=for-the-badge&logo=github)](https://github.com/new?template_owner=MariosGiannakaras&template_name=gh-900-interactive-foundations&owner=%40me&name=gh-900-interactive-foundations-course&description=Interactive%20GH-900%20GitHub%20Foundations%20course&visibility=public)

> **To take the course:** select **Copy Exercise**, create a repository from the template, then open the course Issue that starts automatically.

## Quick start

1. Select **Copy Exercise**.
2. Create a repository under your GitHub account.
3. Open the new repository.
4. Wait for **Step 0 - Start GH-900 Course** to initialize the learner workspace.
5. Open **GH-900 Interactive Foundations — Course** under Issues.
6. Follow only the latest instruction in that Issue.

There is no normal **Actions → Run workflow** setup step. `workflow_dispatch` exists only as a recovery mechanism.

## What the learner sees

The course is intentionally **Issue-first**, not file-first.

A normal unit is presented directly in the course Issue with:

- Part, module, unit, and total-course progress;
- the complete independently written lesson for that unit;
- source-audited detail where needed;
- the current hands-on task or assessment;
- automatic feedback and the exact next action.

Learners do **not** need to browse `modules/`, `curriculum/`, `labs/`, or internal validator files to study. Those are source-maintenance assets in the upstream template.

Files appear in the learner repository only when editing a file is itself part of the current exercise.

## Clean per-unit workspace

A copied learner repository is automatically reduced to the minimum course runtime. Source-maintenance directories are removed from the learner's `main` branch.

For a hands-on unit, the engine creates an isolated temporary workspace:

```text
main
  └─ sandbox/mXX-uYY       ← generated baseline for this unit
       └─ lab/mXX-uYY      ← learner work
```

Only the artifacts required by that unit are generated. Examples include:

- a small Git practice fixture;
- one Markdown file;
- a temporary `.devcontainer/devcontainer.json`;
- a Python file and tests;
- `SECURITY.md` and `CODEOWNERS` when creating those files is the lesson itself.

After successful validation, the course removes the temporary lab/sandbox branches and temporary exercise state. The next lesson therefore starts from a clean workspace unless prior repository state is genuinely necessary for that lesson.

The goal is effectively:

```text
clean workspace → current lesson → validate → cleanup → next lesson
```

## Microsoft Learn structure

The learner sees the same high-level separation as the Microsoft Learn curriculum.

### Part 1 of 2

**Modules 1–8 · 57 units**

1. Introduction to Git
2. Introduction to GitHub
3. Introduction to GitHub's products
4. Configure code scanning on GitHub
5. Introduction to GitHub Copilot
6. Code with GitHub Codespaces
7. Manage your work with GitHub Projects
8. Communicate effectively on GitHub using Markdown

After Module 8 the course explicitly marks **Part 1 complete**.

### Part 2 of 2

**Modules 9–16 · 49 units**

9. Contribute to an open-source project on GitHub
10. Manage an InnerSource program by using GitHub
11. Maintain a secure repository by using GitHub best practices
12. Introduction to GitHub administration
13. Authenticate and authorize user identities on GitHub
14. Manage repository changes by using pull requests on GitHub
15. Search and organize repository history by using GitHub
16. Using GitHub Copilot with Python

Total: **16 modules / 106 units**.

## Course interaction

The live state advances one official unit at a time:

```text
Part 1: M01 U01 → ... → M08 U05
Part 2: M09 U01 → ... → M16 U07
Course complete
```

Unit modes are intentionally different depending on what can be demonstrated safely.

### Reading and summary

Read the lesson in the Issue and comment:

```text
/next
```

### Hands-on activity

The engine creates only the required temporary branch/files. Perform the task and push the requested changes. Validation runs from repository/GitHub state rather than from a generic answer worksheet.

For Pull Request exercises, the PR is opened between temporary course branches rather than into `main`, so completing the exercise does not pollute the learner's permanent workspace.

### Assessment

Questions are displayed directly in the Issue. No assessment file needs to be opened or edited.

Submit answers in order, for example:

```text
/answer B C A B A C
```

The validator identifies only the questions that need review; it does not reveal the correct answer key.

### Scenario / Enterprise-only activity

When a real personal repository cannot safely reproduce an Enterprise, identity-provider, billing, or organization-level feature, the course presents the scenario directly in the Issue.

Respond with:

```text
/scenario <reasoned answer>
```

The response is checked for the required concepts without creating a worksheet file.

### Recovery commands

- `/help` — show the current unit again.
- `/check` — manually re-run the current hands-on state validation when needed.

## Course at a glance

| Item | Coverage |
|---|---:|
| Microsoft Learn learning paths | **2 / 2** |
| Microsoft Learn modules | **16 / 16** |
| Official units | **106 / 106** |
| Part 1 | **8 modules / 57 units** |
| Part 2 | **8 modules / 49 units** |
| Progression | **Unit by unit** |
| Lessons | **Displayed in the Issue** |
| Assessments | **Issue-native, original blind questions** |
| Hands-on state | **Generated on demand** |
| Cleanup | **Automatic after validation** |

The curriculum is not an exam-cram summary. Every official unit is represented in sequence and covered in independently written wording. Where a feature cannot reasonably be provisioned in a personal learner repository, the course uses a transparent scenario/read-only equivalent instead of pretending the feature was exercised.

See [`docs/COVERAGE.md`](docs/COVERAGE.md) for the full completeness contract.

## Source baseline and traceability

The curriculum is audited against the pinned public Microsoft Learn source snapshot:

```text
MicrosoftDocs/learn@66ab07a355b38fb0f5a4cef8240eb2f765c839c8
Baseline date: 2026-08-06
```

Source-maintenance files include:

- [`curriculum/official-curriculum.yml`](curriculum/official-curriculum.yml) — canonical 2-path / 16-module / 106-unit inventory;
- [`curriculum/microsoft-source-lock.json`](curriculum/microsoft-source-lock.json) — pinned Microsoft Learn source map;
- [`docs/COVERAGE.md`](docs/COVERAGE.md) — completeness and GH-900 blueprint cross-check;
- `modules/` and `unit-details/` — maintainable independently written source content;
- `.gh900/` — generated/packaged learner runtime content, templates, and validators.

These source-maintenance directories exist in the upstream template so the course can be audited and maintained. **Step 0 removes the source-only material from learner copies.**

This repository does not reproduce Microsoft Learn prose or Microsoft's knowledge-check question bank verbatim.

## Repository structure

The upstream source is intentionally different from a learner copy.

| Path | Upstream responsibility |
|---|---|
| `modules/` | Maintainable unit-by-unit lesson source |
| `unit-details/` | Additional source-audited depth |
| `labs/` | Internal fixture/question source used to build temporary exercises |
| `curriculum/` | Canonical inventory and source traceability |
| `.gh900/` | Packaged learner runtime, Part 1/Part 2 content, templates, validators |
| `.github/workflows/` | Automatic startup, course engine, source quality gate |
| `scripts/` | Source audits and regression tests |
| `docs/` | Coverage, architecture, and maintenance documentation |

The former duplicate `course/` and incomplete `course-content/` structures are not part of the runtime architecture.

See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).

## Quality gates

The upstream template runs **Course Quality** for source changes. It verifies, among other things:

- exact **2 / 2 paths, 16 / 16 modules, 106 / 106 units**;
- Part 1 = 57 units and Part 2 = 49 units;
- the full source-authoring and packaged learner state chains;
- successful rendering of every learner-visible unit;
- all 16 assessments rendered directly in the Issue;
- isolated per-unit branch naming and cleanup contracts;
- source resolution against the pinned Microsoft Learn commit;
- learner-visible semantic depth;
- workflow YAML and Bash syntax;
- Python validator compilation;
- rejection of untouched source fixtures;
- public-repository/community requirements;
- immutable full-SHA references for external Actions.

`Course Quality` is source-maintenance CI only. A learner copy does not re-run the full upstream curriculum audit.

## Security model

Course automation follows explicit trust boundaries and least privilege:

- the upstream template does not create learner progress;
- learner runtime activates only in non-template copies;
- source quality activates only in the template repository;
- workflow permissions are declared explicitly;
- public drive-by comments and Pull Requests are filtered before learner jobs execute;
- Pull Request exercises use temporary sandbox branches rather than merging exercise content into `main`;
- temporary branches and exercise artifacts are deleted after validation;
- external Actions are pinned to immutable commit SHAs;
- no learner exercise requires committing a real secret.

Security reports should follow [`.github/SECURITY.md`](.github/SECURITY.md). Never place credentials, tokens, private keys, or exploit details in a public Issue.

## Assessment integrity

Correct answers are stored as hashes rather than printed beside the questions. Normal validation reports only the questions requiring review.

Because a learner owns their copied repository, this is an educational integrity mechanism rather than DRM. For realistic exam preparation, avoid inspecting or modifying `.gh900/` while taking assessments.

## Contributing

Contributions are welcome for factual corrections, accessibility, course-engine reliability, security, validation quality, and independently written curriculum improvements. Changes must preserve the 2-path / 16-module / 106-unit contract and source traceability.

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

- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)
- [`docs/MAINTAINING.md`](docs/MAINTAINING.md)
- [`docs/COVERAGE.md`](docs/COVERAGE.md)
