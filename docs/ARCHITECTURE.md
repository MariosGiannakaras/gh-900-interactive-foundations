# Architecture

## Two representations

GH-900 Interactive Foundations deliberately separates the maintained course source from the learner experience.

The **upstream template** keeps transparent source material for auditing and maintenance. A **learner copy** is automatically reduced to a small runtime workspace and receives only the files required by the current unit.

The live course Issue is the learner interface. Internal repository files are implementation details, not required reading.

## Source/template mode

When the repository itself is marked as a template:

- learner startup and progression remain inactive;
- the complete source curriculum remains reviewable;
- `Course Quality` validates curriculum coverage, rendering, runtime behavior, and repository quality.

Maintainable source areas include `modules/`, `unit-details/`, `labs/`, `curriculum/`, `scripts/`, and `docs/`.

## Learner bootstrap

A repository created from the template runs `.github/workflows/00-start-course.yml` on its initial `main` event.

Step 0:

1. creates **GH-900 Interactive Foundations — Course**;
2. initializes hidden state `m01-u01`;
3. runs `.gh900/workspace.py bootstrap`;
4. removes source-maintenance material that the learner does not need;
5. writes a small learner README;
6. commits the clean baseline to `main`;
7. renders the first unit directly in the Issue.

The learner therefore starts with a repository that is intentionally close to empty while retaining the internal automation required to continue the course.

## Packaged learner runtime

`.gh900/` contains the self-contained automation package copied with the template:

| Path | Purpose |
|---|---|
| `.gh900/content/part-1/` | Modules 1–8, 57 units |
| `.gh900/content/part-2/` | Modules 9–16, 49 units |
| `.gh900/details/` | Source-audited supplementary unit detail |
| `.gh900/data/` | Runtime inventory and validation data |
| `.gh900/templates/` | Internal exercise fixtures |
| `.gh900/course_unit_state.py` | Unit metadata, rendering, progression |
| `.gh900/workspace.py` | Bootstrap, per-unit preparation, cleanup |
| `.gh900/validate_activity.py` | Hands-on repository-state validation |
| `.gh900/validate_assessment.py` | Issue-native assessment validation |
| `.gh900/validate_scenario.py` | Issue-native scenario validation |

A learner does not need to inspect these files.

## State model

The course follows the Microsoft Learn structure explicitly:

```text
Part 1: m01-u01 → ... → m08-u05   (57 units)
Part 2: m09-u01 → ... → m16-u07   (49 units)
complete
```

The Issue body stores the authoritative hidden state marker. Every rendered unit shows Part, module, unit, and total-course progress.

Unit modes are:

- `read` — lesson in the Issue, then `/next`;
- `summary` — summary in the Issue, then `/next`;
- `activity` — temporary repository state plus automatic validation;
- `assessment` — questions in the Issue, submitted with `/answer ...`;
- `scenario` — applied response in the Issue, submitted with `/scenario ...`.

## Issue-first presentation

The complete learner-visible lesson is rendered into the course Issue. The learner is not asked to open a module README, curriculum file, assessment file, or validator to continue.

Assessments are rendered as normal Issue content rather than checkbox worksheets. Scenario-only exercises also remain in the Issue instead of creating evidence files.

## Per-unit workspace

Hands-on units use isolated temporary branches:

```text
main
  └─ sandbox/mXX-uYY
       └─ lab/mXX-uYY
```

The engine prepares `sandbox/mXX-uYY` from clean `main`, generates only the fixture needed by that unit, and then creates `lab/mXX-uYY` for learner work.

Pull Request exercises merge from the temporary learner branch into the temporary sandbox branch rather than into `main`. This preserves a real PR workflow without turning the permanent learner branch into a collection of completed exercises.

After successful validation, temporary branches and unit-specific temporary artifacts are removed. The next lesson starts from clean `main` unless persistent state is actually required by the next learning objective.

The lifecycle is therefore:

```text
clean workspace → prepare current unit → learn/practice → validate → cleanup → next unit
```

## Validation model

Generic learner `submission.md` worksheets are not part of runtime v2.

Where possible, validation uses repository or GitHub state directly, including commits, diffs, branches, Pull Requests, Issues, Markdown structure, configuration files, tags, and tests.

When a feature cannot reasonably be provisioned in a normal learner repository, the course uses an explicit Issue-native scenario rather than creating a fake evidence artifact.

## Source layout

| Path | Upstream responsibility |
|---|---|
| `.github/workflows/00-start-course.yml` | Learner initialization |
| `.github/workflows/01-course-engine.yml` | Progression and temporary exercise lifecycle |
| `.github/workflows/quality.yml` | Source-only quality gate |
| `.gh900/` | Packaged learner runtime |
| `modules/` | Maintainable unit content |
| `unit-details/` | Additional audited depth |
| `labs/` | Maintainer fixture/question source |
| `curriculum/` | Canonical curriculum/source mapping |
| `scripts/` | Source audits and regression tests |
| `docs/` | Maintainer/public documentation |

The previous duplicate `course/` and incomplete `course-content/` structures are intentionally removed.

## Quality layers

`Course Quality` independently validates:

1. the exact 2-path / 16-module / 106-unit inventory;
2. source-authoring completeness;
3. the packaged learner runtime and all 106 rendered states;
4. Part 1 = 57 units and Part 2 = 49 units;
5. all Issue-native assessments and scenario modes;
6. per-unit branch/workspace contracts;
7. source depth against the pinned Microsoft Learn baseline;
8. workflow syntax and Python compilation;
9. repository-level quality requirements.

This keeps the upstream source fully auditable while the learner workspace stays focused on one unit at a time.
