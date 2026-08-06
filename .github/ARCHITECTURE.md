# Architecture

## Purpose

GH-900 Interactive Foundations is a GitHub-native course engine. The maintained template contains the curriculum/runtime package, while each learner copy is converted automatically into a minimal exercise workspace.

## Trust boundary

The upstream repository is marked as a GitHub template.

- Source maintenance jobs run only when `github.event.repository.is_template` is true.
- Learner startup/progression runs only when it is false.
- Fork Pull Requests and public Issue comments are filtered before learner code is checked out or executed.
- External Actions are pinned to immutable commit SHAs.

## Persistent learner state

The permanent learner branch contains only the course shell:

- `README.md`;
- `.github/workflows/00-start-course.yml`;
- `.github/workflows/01-course-engine.yml`;
- `.gh900/`.

Progress itself is stored in the course Issue using a hidden `gh900-state` marker.

## Unit lifecycle

Non-practical units render directly into the course Issue.

For a practical unit the engine:

1. cleans any previous visible exercise state;
2. generates only the fixtures required for the new unit;
3. creates `sandbox/mXX-uYY` as the generated baseline;
4. creates `lab/mXX-uYY` for learner work;
5. validates the learner branch and, where relevant, GitHub Issues/PRs/reviews/metadata;
6. advances only after validation;
7. deletes temporary branches and disposable GitHub objects;
8. provisions the next unit.

A PR exercise merges `lab/...` into `sandbox/...`, never into learner `main`.

## Canonical source

`.gh900/` is the single course package:

- `content/part-1` and `content/part-2`: lesson source;
- `details/`: source-audited supplemental depth;
- `data/`: official inventory, Microsoft source lock, assessment hashes;
- `templates/`: exercise fixtures;
- `course_unit_state.py`: state model and Issue renderer;
- `workspace.py`: bootstrap, fixture creation, and visible cleanup;
- `validate_activity.py`: repository/GitHub state validation;
- `validate_assessment.py`: blind Issue-native assessment validation;
- `validate_scenario.py`: scenario response validation;
- `quality/`: upstream source and regression audits.

Parallel source trees are intentionally forbidden by CI.

## Curriculum boundary

The locked baseline contains:

- 2 learning paths;
- 16 modules;
- 106 units;
- Part 1: 57 units;
- Part 2: 49 units.

All units render in sequence. Enterprise-only or account-restricted operations use explicit scenarios when a normal personal learner repository cannot reproduce the actual administrative environment safely.

## Assessment integrity

Assessment questions are original course questions, displayed in the Issue. Correct answers are represented by hashes. The mechanism prevents accidental answer disclosure in normal feedback; it is not intended as DRM against a learner who owns their repository.

## Recovery

`/help` re-renders the current unit. `/check` revalidates the current hands-on unit. `workflow_dispatch` is reserved for recovery and does not replace the normal automatic progression path.
