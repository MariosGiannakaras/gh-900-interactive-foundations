# Maintaining the public repository

This document describes the intended upstream repository posture. Settings here apply to the maintained source repository; GitHub template copies do not automatically inherit every repository setting.

## Repository identity

Recommended repository metadata:

- **Description:** `Interactive GH-900 GitHub Foundations course covering all 16 Microsoft Learn modules and 106 units with automated validation and progression.`
- **Visibility:** Public
- **Template repository:** Enabled
- **Default branch:** `main`
- **Topics:** `github`, `git`, `gh-900`, `github-foundations`, `microsoft-learn`, `github-actions`, `github-skills`, `interactive-learning`, `certification`, `education`

A social-preview image is recommended for links shared outside GitHub. It should identify the project as an independent interactive GH-900/GitHub Foundations course and should not imply Microsoft or GitHub endorsement.

## General feature settings

Recommended source-repository settings:

- **Issues:** Enabled — used for project feedback and source maintenance.
- **Discussions:** Optional; keep disabled unless a support/community discussion surface is actively maintained.
- **Wiki:** Disable — maintained documentation lives under `docs/` and duplicating it creates a second stale source of truth.
- **Projects:** Optional for upstream project management; not required by the course runtime.
- **Template repository:** Keep enabled. Learner runtime depends on a template copy being a non-template repository.

## Pull Request and merge settings

For the upstream source, prefer a predictable linear history:

- allow **squash merge**;
- disable merge commits and rebase merging unless a specific maintenance need appears;
- enable automatic deletion of merged head branches;
- optionally allow contributors to update PR branches when base changes.

These are source-maintenance preferences. Learner repositories may use different merge behavior because merge strategies themselves are part of Git/GitHub learning.

## Protect `main`

Use a branch ruleset or branch-protection rule targeting `main` with the following baseline:

- require changes through a Pull Request;
- require the `Course Quality / validate` status check before merge;
- require conversation resolution before merge;
- block force pushes;
- block branch deletion;
- require linear history if squash-only merging is used.

For a single-maintainer educational project, a mandatory second human approval can be optional; the important invariant is that the automated quality gate cannot be skipped accidentally. If additional maintainers join, requiring at least one approving review becomes appropriate.

Do not configure ambiguous duplicate status-check job names across workflows.

## GitHub Actions settings

Recommended Actions policy for the upstream source:

- allow GitHub-authored Actions required by the repository;
- require Actions to be pinned to a full-length commit SHA when the repository setting is available;
- set the default `GITHUB_TOKEN` workflow permission to read-only;
- do not allow GitHub Actions to create or approve Pull Requests unless a future workflow explicitly needs that capability;
- require approval for workflows from untrusted fork contributors according to the repository's contribution model.

The workflows themselves declare explicit permissions and use immutable Action SHAs. `Course Quality` is source-only; learner copies use only the lightweight course runtime.

## Security and analysis

For the public upstream repository, enable the applicable GitHub security features:

- dependency graph;
- Dependabot alerts;
- Dependabot security updates where a supported dependency ecosystem is detected;
- secret scanning;
- push protection;
- private vulnerability reporting / repository security advisories;
- code scanning default setup, including GitHub Actions workflow analysis when available.

The repository intentionally avoids adding a `dependabot.yml` solely for GitHub Actions because template copies would inherit it and receive maintenance PRs unrelated to the learner course. Action references are instead pinned and protected by `scripts/audit_public_repository.py`; upstream dependency automation can be enabled at the repository-settings level when appropriate.

Never store course credentials in Actions secrets when a workflow can use the scoped `GITHUB_TOKEN` instead.

## Community health

The source includes:

- `README.md`;
- `LICENSE`;
- `.github/CONTRIBUTING.md`;
- `.github/CODE_OF_CONDUCT.md`;
- `.github/SECURITY.md`.

Issue and Pull Request templates are intentionally omitted from the template baseline because the course includes hands-on creation of GitHub collaboration objects. A source-only issue form would be useful for maintainers, but GitHub templates copy `.github/ISSUE_TEMPLATE` into learner repositories and could alter the learner exercise UX.

Similarly, do not pre-create root `SECURITY.md` or `.github/CODEOWNERS`: those are explicit learner deliverables in Module 11.

## Curriculum update procedure

When Microsoft Learn or the GH-900 study guide changes materially:

1. identify the new authoritative source commit;
2. compare the affected Learn modules and unit ordering;
3. update `curriculum/microsoft-source-lock.json` and the canonical curriculum inventory if required;
4. update independently written local lesson coverage;
5. update hands-on/simulation behavior when the capability changed;
6. update `docs/COVERAGE.md` with the new baseline date/commit;
7. run the complete quality gate before merge.

Do not silently move the source baseline. The pinned commit is part of the repository's reproducibility contract.

## Action dependency update procedure

When `actions/checkout` or another external Action is updated:

1. verify the release in the Action's official repository;
2. resolve the release tag to its exact 40-character commit SHA;
3. replace the workflow SHA and update the adjacent version comment;
4. let `scripts/audit_public_repository.py` confirm that no mutable Action reference remains;
5. merge only after `Course Quality` passes.

## Release and archival posture

The course currently follows the maintained `main` branch rather than versioned release trains. If historical certification baselines need to remain reproducible, create signed/annotated tags or GitHub Releases tied to the corresponding pinned Microsoft Learn snapshot rather than rewriting old tags.

If the project is ever discontinued, archive the repository rather than leaving workflows and curriculum claims appearing actively maintained.
