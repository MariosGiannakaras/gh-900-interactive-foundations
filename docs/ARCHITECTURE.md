# Architecture

## Purpose

GH-900 Interactive Foundations is both a maintained **source template** and a **learner runtime**. The same repository contents behave differently depending on whether the repository is itself marked as a GitHub template.

The design goal is to keep the upstream source inert for learner progress while allowing a repository created from the template to start the course automatically.

## Source/template mode

When `github.event.repository.is_template` is `true`:

- learner startup does not run;
- learner progression does not run;
- `Course Quality` is allowed to run for source maintenance;
- curriculum, runtime, workflow, security, and public-repository audits protect `main`.

This keeps the canonical template free of learner progress Issues and lab state.

## Learner-copy mode

A repository created from the template is not a template by default. In that repository:

1. the initial `main` event runs `.github/workflows/00-start-course.yml`;
2. Step 0 creates the single live course Issue;
3. the Issue begins at hidden state `m01-u01`;
4. `.github/workflows/01-course-engine.yml` reacts to authorized course comments, lab-branch pushes, and relevant Pull Request updates;
5. validated checkpoints advance the hidden state one unit at a time;
6. after `m16-u07`, the state becomes `complete` and the course Issue closes.

The source-maintenance `Course Quality` job is disabled in learner copies so learners do not pay the runtime and UI cost of re-auditing the full upstream curriculum.

## State model

The runtime catalog defines an ordered chain of 106 states:

```text
m01-u01 → m01-u02 → ... → m16-u07 → complete
```

`scripts/course_unit_state.py` resolves each state to learner-visible content, mode, module, and expected lab branch.

Checkpoint modes are:

- `read` / `summary` — progression uses `/next`;
- `activity` — progression requires repository state validated by `scripts/validate_unit_activity.py`;
- `assessment` — progression requires the module assessment validator.

The Issue body contains the authoritative hidden state marker. Workflow comments are presentation/output, not the source of truth for progression.

## Trust boundaries

### GitHub Actions token

Each workflow declares explicit permissions. Learner workflows receive only the repository permissions required for checkout, Issue updates, and the Pull Request evidence used by validators. No course workflow requires a repository secret.

### Public Issue comments

The course engine authorizes `OWNER`, `MEMBER`, and `COLLABORATOR` associations at the **job condition** before a runner is allocated. Bot comments are rejected there as well. The Bash runtime repeats the check as defense in depth.

### Pull Requests

Drive-by Pull Requests are rejected at the job condition before checkout. Authorized learner/collaborator PRs may be inspected because the exercise intentionally validates repository state.

The workflows do not use `pull_request_target`, avoiding the privileged base-repository token model for untrusted fork code.

### External Actions

External GitHub Actions are referenced by immutable 40-character commit SHAs rather than mutable tags. The human-readable release version is kept as a comment beside the SHA.

### External curriculum source

`Course Quality` checks out Microsoft Learn only at the commit recorded in `curriculum/microsoft-source-lock.json`. Sparse checkout limits the external source tree to the 16 relevant modules.

The external source is used for auditing and comparison. It is not executed as learner code.

## Repository layout

| Path | Responsibility |
|---|---|
| `.github/workflows/00-start-course.yml` | One-time learner bootstrap |
| `.github/workflows/01-course-engine.yml` | Learner progression and validation events |
| `.github/workflows/quality.yml` | Upstream/source-only merge gate |
| `curriculum/` | Canonical inventory, source lock, runtime catalog, assessment hashes |
| `modules/` | Module lesson content |
| `unit-details/` | Additional source-audited lesson depth |
| `labs/` | Learner-editable artifacts and assessments |
| `scripts/` | Runtime, validators, audits |
| `docs/COVERAGE.md` | Curriculum completeness contract |

## Exercise baseline protection

Some files are intentionally **absent** from the template because creating them is part of the curriculum. In particular, Module 11 expects learners to create:

- root `SECURITY.md`;
- `.github/CODEOWNERS`.

The upstream public security policy therefore lives at `.github/SECURITY.md`, a GitHub-supported community-health location that does not pre-complete the learner's required root artifact.

`scripts/audit_public_repository.py` protects this distinction so future repository hardening cannot accidentally seed learner answers.

## Quality layers

The maintained source uses independent gates rather than one monolithic test:

1. official curriculum inventory validation;
2. complete-course structural audit;
3. public-repository/security audit;
4. 106-state runtime-chain validation;
5. semantic-depth audit against the pinned Microsoft Learn source;
6. workflow YAML/Bash parsing;
7. Python compilation;
8. negative tests proving untouched activities and assessments do not pass.

This provides defense in depth: a content change can be structurally valid yet still fail source coverage, runtime, security, or negative-validation checks.
