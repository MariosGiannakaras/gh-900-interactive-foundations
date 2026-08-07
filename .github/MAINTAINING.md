# Maintaining the course

## Invariants

Every source change must preserve these contracts unless the verified upstream curriculum itself changes:

- 2 Microsoft Learn learning paths;
- 16 modules;
- 106 units;
- Part 1 = 57 units;
- Part 2 = 49 units;
- one ordered runtime state per official unit;
- lessons presented in the course Issue;
- no generic learner submission worksheets;
- practical files created only when required by the current unit;
- cleanup before the next unrelated unit;
- no exercise merges into learner `main`;
- no real credentials or secrets.

## Updating course content

The canonical lesson source lives under `.gh900/content/part-1` and `.gh900/content/part-2`. Supplemental unit depth lives under `.gh900/details`.

Do not create a second `modules/`, `course-content/`, or similar content tree.

When Microsoft Learn changes materially:

1. verify the new upstream unit inventory;
2. update `.gh900/data/official-curriculum.yml`;
3. update `.gh900/data/microsoft-source-lock.json` and the pinned commit;
4. update affected independent lesson text/detail;
5. update exercise behavior only where the learning objective changed;
6. run Course Quality;
7. review learner-visible rendering, not only source Markdown.

Never copy Microsoft Learn prose or its knowledge-check bank verbatim.

## Updating exercises

Prefer direct Git/GitHub evidence over evidence worksheets.

A new practical exercise should answer:

- What real Git/GitHub skill is being practiced?
- What is the minimum fixture required?
- Can the validator infer completion from repository/GitHub state?
- What needs cleanup?
- Does anything need to persist into the next unit?
- Can an untrusted public user trigger privileged course behavior?

If a capability requires Enterprise, organization, billing, SSO/IdP, or another unavailable administrative environment, use an explicit Issue-native scenario rather than simulating success deceptively.

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
- force pushes/deletion blocked;
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

1. Course Quality passes on the PR.
2. The PR diff contains no duplicate source trees.
3. A fresh repository is created with **Copy Exercise**.
4. Step 0 removes source-maintenance/community files from the learner copy.
5. The course Issue appears automatically.
6. At least one reading, assessment, scenario, file-edit activity, and PR activity are exercised.
7. Successful activities remove their temporary state.
8. Part transition and final course completion are verified.
