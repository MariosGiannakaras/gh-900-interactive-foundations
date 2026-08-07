# Maintaining the course

## Invariants

Every source change must preserve these contracts unless the verified upstream curriculum itself changes:

- 2 Microsoft Learn learning paths;
- 16 modules;
- 106 units;
- Part 1 = 57 units;
- Part 2 = 49 units;
- one ordered runtime state per official unit;
- lessons presented in the course Issue with a stable `gh900-unit` marker;
- no official Microsoft Learn unit titled **Exercise** reduced to reading-only mode;
- no generic learner submission/evidence worksheets;
- practical files created only when required by the current unit;
- account/entitlement-dependent exercises provide an honest real path plus explicit fallback;
- Enterprise/paid scenarios use structured decisions instead of fake infrastructure;
- learner evidence is scoped to the unit where it was submitted;
- state/render transitions are recoverable and `/help` always restores authoritative state;
- cleanup before the next unrelated unit;
- no exercise merges into learner `main`;
- no real credentials or secrets.

## Updating course content

The canonical lesson source lives under `.gh900/content/part-1` and `.gh900/content/part-2`. Supplemental unit depth lives under `.gh900/details`.

Do not create a second `modules/`, `course-content/`, or similar content tree. Do not leave obsolete implementation descriptions in canonical lesson source merely because the renderer happens to strip them.

When Microsoft Learn changes materially:

1. verify the new upstream unit inventory;
2. update `.gh900/data/official-curriculum.yml`;
3. update `.gh900/data/microsoft-source-lock.json` and the pinned commit used by Course Quality;
4. update affected independent lesson text/detail;
5. update `.gh900/data/concept-coverage.json` for changed required concepts;
6. update exercise/checkpoint/scenario behavior where the learning objective changed;
7. run Course Quality;
8. review learner-visible rendering, not only source Markdown.

Never copy Microsoft Learn prose or its knowledge-check bank verbatim.

## Updating GH-900 exam coverage

Microsoft Learn curriculum coverage and GH-900 certification-objective coverage are separate contracts.

When the official GH-900 study guide changes:

1. review every changed exam domain/objective;
2. update `.gh900/data/gh900-objectives.json`;
3. map each objective to the smallest set of learner-visible units that actually teach it;
4. update the lesson content if an objective has no adequate coverage;
5. run `.gh900/quality/exam_coverage.py` through Course Quality.

Do not satisfy an exam objective by mapping it to a unit that merely has a related title. The required terms/concepts must be visible in the actual rendered lesson.

## Quality layers

The quality scripts intentionally answer different questions:

- `audit.py` — is the public/runtime structure valid and complete?
- `fixture_contracts.py` — can every generated exercise obtain the files it requires?
- `semantic.py` — do all pinned Microsoft units resolve and is local rendered depth substantial? This is **not semantic equivalence**.
- `concept_coverage.py` — does every one of the 106 learner-visible units contain its curated required concept groups?
- `exam_coverage.py` — does every current GH-900 exam objective map to learner-visible coverage?
- `simulate_runtime.py` — does the complete 106-state protocol remain internally consistent, including stale-response and checkpoint contracts?

A green length/depth gate must never be used as the sole proof that a concept is covered.

## Updating exercises

Prefer direct Git/GitHub evidence over evidence worksheets.

A new practical exercise should answer:

- What real Git/GitHub skill is being practiced?
- What is the minimum fixture required?
- Can the validator infer completion from repository/GitHub state?
- What needs cleanup?
- Does anything need to persist into the next unit?
- Can an untrusted public user trigger privileged course behavior?
- Does the exercise depend on an entitlement or private product telemetry that Actions cannot honestly prove?

For an entitlement-dependent official exercise, use this order:

1. real action/inspection where the learner has access;
2. preserve the official Microsoft Learn unit link in the lesson;
3. provide a structured `/checkpoint` fallback when access is unavailable.

If a capability requires Enterprise, organization, billing, SSO/IdP, or another administrative environment that a personal repository cannot safely reproduce, use a structured `/scenario` response with explicit required fields/relationships. Do not create a worksheet that merely claims the real configuration occurred.

## Runtime/recovery changes

The `gh900-state` marker is the authoritative state. Every rendered lesson must begin with `<!-- gh900-unit:mXX-uYY -->`.

Changes to comment handling must preserve:

- duplicate/stale command rejection;
- `/reflection` and `/investigation` scoped to their preceding lesson marker;
- `/help` bypassing stale-command checks and rendering current authoritative state;
- transcript reconciliation when state exists but the corresponding lesson marker is missing;
- full pagination for long course Issues;
- serialization of course events;
- timeouts around learner-controlled validation and Git/GitHub network operations.

Update `runtime_protocol.py` and `quality/simulate_runtime.py` together when the protocol changes.

## Repository settings

Recommended source-repository settings:

- public template repository;
- Issues enabled;
- Wiki disabled unless it gains a distinct maintenance purpose;
- squash merge enabled;
- merge commits/rebase disabled for normal maintenance;
- automatic head-branch deletion enabled;
- `main` protected by a ruleset;
- Course Quality required before merge;
- CodeQL/code-scanning results required where available;
- force pushes/deletion blocked;
- review conversations resolved before merge where the account UI supports the rule;
- Actions default token read-only;
- **Allow GitHub Actions to create and approve pull requests** disabled — learner PR creation is intentionally user-owned;
- fork workflows require approval for external contributors;
- private vulnerability reporting enabled;
- Dependabot/security scanning features enabled where available.

Do not add learner-owned exercise artifacts such as root `SECURITY.md` or `.github/CODEOWNERS` to the permanent template shell; those are generated/created only when their lesson requires them.

## Dependency / Action updates

External Actions must use a full 40-character commit SHA. Update the explanatory version comment at the same time.

Test Action-version changes against both:

- source Course Quality; and
- learner startup/progression semantics.

## Release checklist

Before considering the template ready:

1. Course Quality passes on the PR, including structural, fixture, concept, exam-objective, and 106-state runtime simulation gates.
2. CodeQL passes on the same head SHA.
3. The PR diff contains no duplicate source trees or obsolete implementation documentation.
4. A fresh repository is created with **Copy Exercise**.
5. Step 0 removes source-maintenance/community files from the learner copy and leaves only the intended shell.
6. The course Issue appears automatically.
7. Reading, assessment, structured scenario, account-aware checkpoint, file-edit activity, and PR activity paths are exercised.
8. Duplicate/stale command behavior and `/help` recovery are exercised.
9. Successful activities remove their temporary state.
10. Part transition and final course completion are represented by the deterministic 106-state simulation; representative real GitHub-hosted E2E paths are also verified before release.
