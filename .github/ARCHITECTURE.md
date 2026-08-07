# Architecture

## Purpose

GH-900 Interactive Foundations is a GitHub-native course engine. The maintained template contains the curriculum/runtime package, while each learner copy is converted automatically into a minimal exercise workspace.

## Trust boundary

The upstream repository is marked as a GitHub template.

- Source maintenance jobs run only when `github.event.repository.is_template` is true.
- Learner startup/progression runs only when it is false.
- Issue-comment jobs are limited to the exact course Issue and trusted repository collaborators.
- PR jobs are limited to trusted same-repository `lab/...` → `sandbox/...` training PRs.
- Fork Pull Requests and unrelated public Issue comments are rejected before course execution.
- External Actions are pinned to immutable commit SHAs.

## Persistent learner state

The permanent learner branch contains only the course shell:

- `README.md`;
- `LICENSE`;
- `.github/workflows/00-start-course.yml`;
- `.github/workflows/01-course-engine.yml`;
- `.gh900/`.

Progress itself is stored in the course Issue using a hidden `gh900-state` marker.

Every rendered lesson also begins with a stable transcript marker:

```html
<!-- gh900-unit:m05-u03 -->
```

The state marker identifies the authoritative current unit; lesson markers identify which unit a visible comment/learner response belonged to.

## Unit lifecycle

Reading/summary, assessment, structured scenario, and account-aware checkpoint units render directly into the course Issue without creating unnecessary repository files.

For a repository practical unit the engine:

1. cleans any previous visible exercise state;
2. generates only the fixtures required for the new unit;
3. creates `sandbox/mXX-uYY` as the generated baseline;
4. creates `lab/mXX-uYY` for learner work;
5. validates the learner branch and, where relevant, GitHub Issues/PRs/reviews/metadata;
6. advances only after validation;
7. persists the next state;
8. deletes temporary branches and disposable GitHub objects;
9. renders the next unit with explicit previous-checkpoint feedback.

A PR exercise merges `lab/...` into `sandbox/...`, never into learner `main`.

## Interaction modes

The state model supports:

- `read` — theory/understanding unit, `/next`;
- `summary` — summary unit, `/next`;
- `assessment` — Issue-native original questions, `/answer ...`;
- `activity` — generated Git/GitHub workspace with durable-state validation;
- `scenario` — structured `key=value` decisions for paid/Enterprise/account-scoped concepts that cannot safely be provisioned;
- `checkpoint` — account/entitlement-aware guided checkpoint for an official exercise whose private editor/product telemetry cannot be proven from Actions.

An official Microsoft Learn unit whose title is an **Exercise** must not silently fall back to `read` mode. Where the exact product is unavailable, the lesson keeps the official exercise link visible and uses an explicit structured fallback.

## Response scoping

`/next`, `/answer`, `/scenario`, `/checkpoint`, `/reflection`, `/investigation`, and `/check` belong to the `gh900-unit` marker that was in force when the learner posted the comment.

The engine uses this to reject queued duplicate/stale progression commands. Activity validators use the same protocol to retrieve only `/reflection` or `/investigation` evidence submitted for the current unit. Older responses cannot satisfy later checkpoints merely because they contain similar words.

`/help` is intentionally different: it is a recovery command and always renders the authoritative `gh900-state`, even if the learner's visible transcript is stale.

## Self-healing transitions

The engine provisions the next activity before state mutation so provisioning failures leave the previous validated unit recoverable. Once the next state is stored, cleanup is safe and best-effort.

A final Issue-comment API failure can otherwise leave the state ahead of the visible transcript. Every engine run therefore performs reconciliation:

1. read the authoritative `gh900-state`;
2. inspect the paginated course transcript for `<!-- gh900-unit:<state> -->`;
3. if that lesson marker is absent, re-render the current lesson idempotently;
4. continue event processing only after the transcript is recoverable.

Temporary course-owned branches are also re-scanned on later transitions, so a transient cleanup failure does not permanently accumulate `lab/`, `sandbox/`, or `fixture/` branches.

## Canonical source

`.gh900/` is the single course package:

- `content/part-1` and `content/part-2`: lesson source;
- `details/`: independently written supplemental depth;
- `data/official-curriculum.yml`: canonical 106-unit order;
- `data/microsoft-source-lock.json`: pinned Microsoft Learn source snapshot;
- `data/concept-coverage.json`: required concept groups for every official unit;
- `data/gh900-objectives.json`: January-2026 GH-900 exam-objective → unit mapping;
- `data/assessment-hashes.json`: blind assessment answer data;
- `templates/`: exercise fixtures;
- `course_unit_state.py`: state model and Issue renderer;
- `runtime_protocol.py`: stable lesson-marker and response-scoping protocol;
- `workspace.py`: bootstrap, fixture creation, and visible cleanup;
- `validate_activity.py`: repository/GitHub state validation and unit-scoped evidence;
- `validate_assessment.py`: blind Issue-native assessment validation;
- `validate_checkpoint.py`: account-aware external/product setup validation;
- `validate_scenario.py`: structured scenario validation;
- `quality/`: source, concept, exam, fixture, runtime, and regression audits.

Parallel source trees are intentionally forbidden by CI.

## Curriculum and exam boundaries

The locked Microsoft Learn baseline contains:

- 2 learning paths;
- 16 modules;
- 106 units;
- Part 1: 57 units;
- Part 2: 49 units.

Three different checks deliberately prove different things:

1. `semantic.py` resolves the pinned upstream unit and prevents a learner-visible unit from becoming only a title/objective-sized placeholder. It is a **source/depth gate**, not semantic equivalence.
2. `concept_coverage.py` enforces curated required concept groups against the actual Issue rendering for **all 106 units**.
3. `exam_coverage.py` independently maps the January-2026 **GH-900 study-guide objectives** to learner-visible course units.

This separation avoids treating text length as proof of conceptual or exam coverage.

## Runtime verification

`quality/simulate_runtime.py` walks the complete 106-state chain and verifies:

- exact transition order;
- stable lesson markers;
- mode/continuation contracts;
- branch/sandbox ownership for activities;
- no official exercise is reading-only;
- stale-command rejection;
- unit-scoped evidence selection;
- structured scenario acceptance/rejection;
- both available and unavailable paths for the M16-U03 account-aware checkpoint.

This deterministic simulation complements, but does not falsely claim to replace, a GitHub-hosted learner E2E test of real Issues, PRs, Actions, and API behavior.

## Assessment integrity

Assessment questions are original course questions, displayed in the Issue. Correct answers are represented by hashes. The mechanism prevents accidental answer disclosure in normal feedback; it is not intended as DRM against a learner who owns their repository.

## Recovery

`/help` always re-renders the authoritative current unit. `/check` revalidates the current hands-on unit. `workflow_dispatch` is reserved for recovery and does not replace the normal automatic progression path. Validators and network/Git operations have explicit timeouts so a non-terminating learner test or transient command cannot hold a runner indefinitely.
