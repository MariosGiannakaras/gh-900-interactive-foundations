# Coverage matrix

Verified against Microsoft Learn and the GH-900 study guide on **2026-08-06**.

Pinned Microsoft Learn source baseline: `MicrosoftDocs/learn@66ab07a355b38fb0f5a4cef8240eb2f765c839c8`.

## Completeness contract

This project is not a summary course. Completion requires all of the following:

1. Every official Microsoft Learn learning path is represented.
2. Every official module is represented.
3. Every official unit is represented, including introductions, exercises, assessments/knowledge checks, and summaries.
4. Concepts and operational details are covered in independently written wording rather than only naming learning objectives.
5. Every unit resolves to the pinned public Microsoft Learn source snapshot.
6. Practical units use real Git/GitHub work where safe; unavailable Enterprise/account/paid capabilities use explicit scenarios instead of pretending they were exercised.
7. Current GH-900 exam objectives are cross-checked separately.
8. Learner progression is unit-by-unit through one live course Issue.
9. The learner does not need to read internal source files to study or answer assessments.
10. Hands-on files/state are generated only for the current unit and cleaned afterward unless later learning genuinely requires persistence.
11. Source changes must pass inventory, semantic-depth, runtime-v2, workflow, validator, and repository-quality gates.

Canonical source inventory: [`curriculum/official-curriculum.yml`](../curriculum/official-curriculum.yml).  
Pinned source map: [`curriculum/microsoft-source-lock.json`](../curriculum/microsoft-source-lock.json).  
Packaged learner runtime: [`.gh900/`](../.gh900/).

## Microsoft Learn inventory

| # | Official module | Units | Part | Status |
|---:|---|---:|---:|---|
| 1 | Introduction to Git | 6 | 1 | Implemented |
| 2 | Introduction to GitHub | 8 | 1 | Implemented |
| 3 | Introduction to GitHub's products | 9 | 1 | Implemented |
| 4 | Configure code scanning on GitHub | 7 | 1 | Implemented |
| 5 | Introduction to GitHub Copilot | 7 | 1 | Implemented |
| 6 | Code with GitHub Codespaces | 7 | 1 | Implemented |
| 7 | Manage your work with GitHub Projects | 8 | 1 | Implemented |
| 8 | Communicate effectively on GitHub using Markdown | 5 | 1 | Implemented |
| **Part 1** | **8 modules** | **57** |  | **57/57** |
| 9 | Contribute to an open-source project on GitHub | 7 | 2 | Implemented |
| 10 | Manage an InnerSource program by using GitHub | 5 | 2 | Implemented |
| 11 | Maintain a secure repository by using GitHub best practices | 6 | 2 | Implemented |
| 12 | Introduction to GitHub administration | 7 | 2 | Implemented |
| 13 | Authenticate and authorize user identities on GitHub | 7 | 2 | Implemented |
| 14 | Manage repository changes by using pull requests on GitHub | 5 | 2 | Implemented |
| 15 | Search and organize repository history by using GitHub | 5 | 2 | Implemented |
| 16 | Using GitHub Copilot with Python | 7 | 2 | Implemented |
| **Part 2** | **8 modules** | **49** |  | **49/49** |
| **Total** | **16 modules** | **106** | **2 parts** | **106/106** |

## Learner runtime coverage

The normal learner experience follows a GitHub Skills-style flow while preserving the complete curriculum:

1. **Copy Exercise** creates a repository from the template.
2. `.github/workflows/00-start-course.yml` creates the live course Issue.
3. Step 0 removes source-maintenance material from the copied learner `main` and leaves the minimum self-contained runtime.
4. `.github/workflows/01-course-engine.yml` reads the hidden `mXX-uYY` state and presents one official unit at a time.
5. Reading and summary units advance with `/next`.
6. Assessments are displayed in the Issue and submitted with `/answer ...`; no answer worksheet is required.
7. Enterprise/account/UI-only application units use `/scenario ...`; no evidence worksheet is created.
8. Hands-on units receive isolated `sandbox/mXX-uYY` and `lab/mXX-uYY` branches plus only the current fixture.
9. Validators inspect direct repository/GitHub state rather than generic `submission.md` evidence files.
10. After validation, current temporary branches/artifacts are cleaned before progression is committed.
11. After `m16-u07`, the Issue closes as complete.

### Runtime mode inventory

The packaged 106-state runtime contains:

- **58** reading units;
- **12** repository/GitHub hands-on activities;
- **4** explicit scenario activities for capabilities that should not be faked in a personal learner repository;
- **16** assessments;
- **16** summaries.

`script/test_learner_runtime_v2.py` verifies the exact packaged chain, modes, rendering, Part 1/Part 2 counts, assessment rendering, branch isolation, and cleanup contracts.

### Direct hands-on validation

Examples include:

- Git commits, diffs, and merge history;
- real temporary Issues and Pull Requests;
- Markdown structure;
- code-scanning configuration concepts;
- dev-container JSON;
- InnerSource program design;
- `SECURITY.md` and `.github/CODEOWNERS` created only during the relevant temporary exercise;
- repository tags/history;
- Python implementation and tests.

The learner `main` is not used as a permanent dumping ground for completed exercise fixtures.

## Microsoft-source coverage controls

`Course Quality` fetches the pinned `MicrosoftDocs/learn` source tree and resolves all **106/106 units** from the 16 relevant modules.

`scripts/audit_microsoft_semantic_depth.py` compares learner-visible local coverage with the size/depth of the source so a title/objective-only placeholder cannot satisfy the gate. This is a mechanical guardrail, not a claim that text length proves semantic equivalence.

`modules/` contains maintainable independently written source lessons. `unit-details/` contains source-audited additions where extra depth is required. Runtime v2 packages these under `.gh900/content/` and `.gh900/details/` for Issue rendering in learner copies.

The repository does **not** copy Microsoft's knowledge-check question bank. Assessments are original questions covering equivalent concepts and are validated using hidden hashes.

## Current GH-900 exam blueprint cross-check

The January 2026 GH-900 blueprint has seven domains. These remain a separate completeness gate on top of the 106 Learn units.

| GH-900 domain | Weight | Coverage areas |
|---|---:|---|
| Understand Git and GitHub basics | 25–30% | version control; Git vs GitHub; repositories, commits, branches; accounts/organizations/enterprise; GitHub Flow; Markdown; Desktop; Mobile |
| Work with GitHub repositories | 10–15% | README, LICENSE, CONTRIBUTING, CODEOWNERS, SECURITY; templates; branches; files; insights; stars; feature previews; dependency/maintenance concepts |
| Collaborate using GitHub | 10–15% | Issues; Pull Requests; Discussions; linked work; templates; filters; assignments; notifications; Gists; Wikis; Pages |
| Apply modern development practices | 10–15% | Actions; Copilot suggestions; agents; Agent Mode; multi-model support; Copilot plan differences; Codespaces; dev containers; github.dev |
| Manage projects with GitHub | 5–10% | Projects; layouts/views; labels; milestones; workflows; saved replies; assignees; insights |
| Privacy, security, and administration | 10–15% | 2FA; passkeys; repository/org roles; EMU; organization-wide Copilot policy; visibility; branch protection/rulesets; organizations; teams; roles |
| Explore the GitHub community | 5–10% | open source; Sponsors; following; Marketplace; InnerSource; forks; templates; discoverability |

### Freshness items explicitly included

- Copilot agents, Agent Mode, and multi-model concepts;
- passkeys and WebAuthn concepts;
- Enterprise Managed Users (EMU);
- organization-wide governance/Copilot policy concepts;
- `github.dev` versus Codespaces;
- repository insights/dependency concepts;
- current repository-security/ruleset practices.

Time-sensitive prices, quotas, limits, or feature packaging remain source-snapshot facts and should be verified against current GitHub documentation before real purchasing/administration decisions.

## Automated merge gate

`Course Quality` rejects changes when any of these contracts break:

- inventory is not 2 paths / 16 modules / 106 units;
- Part 1 is not 57 units or Part 2 is not 49;
- the learner runtime is not exactly 106 sequential states;
- a learner-visible unit cannot render fully in the Issue;
- an assessment falls back to a learner answer file;
- a hands-on unit does not use isolated per-unit state;
- packaged runtime/source-maintenance components disappear;
- an upstream source unit cannot be resolved at the pinned commit;
- learner-visible coverage is materially too thin;
- workflow YAML/Bash fails to parse;
- Python runtime/source validators fail to compile;
- public-repository requirements fail.

## Sources

- [Microsoft Learn — GitHub Foundations Part 1](https://learn.microsoft.com/en-us/training/paths/github-foundations/)
- [Microsoft Learn — GitHub Foundations Part 2](https://learn.microsoft.com/en-us/training/paths/github-foundations-2/)
- [Microsoft Learn — GH-900 Study Guide](https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/gh-900)
- [GitHub Skills](https://skills.github.com/)
- [GitHub Docs](https://docs.github.com/)
