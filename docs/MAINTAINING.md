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

## Source vs learner copies

The upstream repository is intentionally content-rich because maintainers must be able to audit all 106 units. A learner copy is intentionally not.

`Step 0 - Start GH-900 Course` removes source-maintenance directories from a new learner copy and leaves only the small learner README, the internal `.gh900/` runtime package, and the workflows needed to continue the course.

Do not move source-only documentation or maintainer tooling into the learner-visible exercise baseline. Conversely, do not remove `.gh900/` from the template without replacing it with another self-contained runtime delivery mechanism; copied repositories must remain able to run the complete course without depending on later maintainer intervention.

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

These are source-maintenance preferences. Learner repositories may use different merge behavior because merge strategies themselves are course material.

## Protect `main`

Use a branch ruleset or branch-protection rule targeting `main` with the following baseline:

- require changes through a Pull Request;
- require the `Course Quality / validate` status check before merge;
- require conversation resolution before merge;
- block force pushes;
- block branch deletion;
- require linear history if squash-only merging is used.

For a single-maintainer educational project, a mandatory second human approval can be optional. The key invariant is that the automated quality gate cannot be skipped accidentally.

## GitHub Actions settings

Recommended Actions policy for the upstream source:

- allow the GitHub-authored Actions required by the repository;
- require full-length commit-SHA pinning when that repository setting is available;
- set the default `GITHUB_TOKEN` workflow permission to read-only;
- do not allow Actions to create or approve Pull Requests globally unless a future workflow explicitly needs it;
- require approval for workflows from untrusted fork contributors according to the contribution model.

The learner workflows request write permissions explicitly because the course creates and removes its own temporary `sandbox/mXX-uYY` and `lab/mXX-uYY` branches and updates the course Issue.

`Course Quality` is source-only and is removed from learner copies by Step 0.

## Learner runtime invariants

Changes to `.gh900/` or the learner workflows must preserve all of the following:

- Part 1 contains Modules 1–8 / 57 units;
- Part 2 contains Modules 9–16 / 49 units;
- total progression is exactly 106 units;
- all learner-visible lesson text is rendered into the course Issue;
- assessments use `/answer ...` rather than learner answer files;
- scenario-only work uses `/scenario ...` rather than evidence worksheets;
- a hands-on unit receives only the files required by that unit;
- generic `submission.md` files are not part of learner runtime;
- PR exercises target a temporary sandbox branch instead of `main`;
- temporary unit branches/files are cleaned after successful validation;
- `main` remains the clean learner baseline between exercises;
- internal setup pushes cannot accidentally advance the state machine.

`scripts/test_learner_runtime_v2.py` is the automated regression contract for these rules.

## Security and analysis

For the public upstream repository, enable the applicable GitHub security features in repository settings, including dependency alerts, secret detection/protection, private reporting, and code scanning where available.

The repository intentionally avoids adding source-maintenance automation that would create unrelated maintenance activity in every learner copy. External Action references are pinned and checked by `scripts/audit_public_repository.py`.

Never use a real credential as course exercise content.

## Community health

The source includes:

- `README.md`;
- `LICENSE`;
- `.github/CONTRIBUTING.md`;
- `.github/CODE_OF_CONDUCT.md`;
- `.github/SECURITY.md`.

Issue and Pull Request templates are intentionally omitted from the template baseline because the course includes hands-on creation of GitHub collaboration objects and copies would inherit those templates.

Root `SECURITY.md` and `.github/CODEOWNERS` are also not pre-created in the learner baseline because creating them is part of the security exercise. Runtime v2 creates neither in advance; the learner creates them on the temporary unit branch and cleanup removes that exercise branch afterward.

## Curriculum update procedure

When Microsoft Learn or the GH-900 study guide changes materially:

1. identify the new authoritative source commit;
2. compare the affected learning path, module, and unit ordering;
3. update `curriculum/microsoft-source-lock.json` and `curriculum/official-curriculum.yml` as required;
4. update independently written content in `modules/` / `unit-details/`;
5. update source fixture/question material under `labs/` when needed;
6. update the packaged equivalents under `.gh900/content/`, `.gh900/details/`, `.gh900/data/`, or `.gh900/templates/`;
7. update runtime behavior when the exercise model changed;
8. update `docs/COVERAGE.md` with the new baseline;
9. run the complete `Course Quality` gate before merge.

Do not update source authoring without updating the packaged learner runtime. The quality gate should detect divergence, but synchronized source/runtime changes remain a maintainer responsibility.

Do not silently move the Microsoft source baseline. The pinned commit is part of the reproducibility contract.

## Runtime dependency update procedure

When `actions/checkout` or another external Action is updated:

1. verify the release in the Action's official repository;
2. resolve the release tag to its exact 40-character commit SHA;
3. replace the workflow SHA and update the adjacent version comment;
4. let `scripts/audit_public_repository.py` confirm that no mutable Action reference remains;
5. verify both source CI and a fresh learner-copy startup before considering the change complete.

## Required end-to-end learner test

Before a major runtime release, create a fresh repository through **Copy Exercise** and verify at minimum:

1. Step 0 creates the course Issue without manual workflow dispatch;
2. the learner `main` is cleaned automatically;
3. reading units render fully in the Issue;
4. entering a hands-on unit creates only its expected temporary files/branches;
5. an invalid activity is rejected;
6. a valid activity advances and removes the old temporary state;
7. an assessment accepts `/answer ...` and reports wrong question numbers without revealing answers;
8. a scenario accepts `/scenario ...`;
9. the Part 1 → Part 2 transition is displayed correctly;
10. source-only `Course Quality` does not run in the learner copy.

## Release and archival posture

The maintained course currently follows `main` rather than versioned release trains. If historical certification baselines need to remain reproducible, use tags or Releases tied to the corresponding pinned Microsoft Learn snapshot rather than rewriting old tags.

If maintenance stops permanently, archive the repository rather than leaving curriculum claims and workflows appearing actively maintained.
