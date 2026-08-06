# Coverage matrix

Verified against Microsoft Learn and the GH-900 study guide on **2026-08-06**.

Pinned Microsoft Learn source baseline: `MicrosoftDocs/learn@66ab07a355b38fb0f5a4cef8240eb2f765c839c8`.

## Completeness contract

This project is not a summary course. Completion requires all of the following:

1. Every official Microsoft Learn learning path is represented.
2. Every official module is represented.
3. Every official unit is represented, including introductions, exercises, assessments/knowledge checks, and summaries.
4. The concepts and operational details taught by each unit are covered in independently written wording rather than only naming its learning objective.
5. Every unit resolves to its source YAML/Markdown in the pinned public Microsoft Learn snapshot.
6. Where a unit is practical, the course provides a real hands-on equivalent. Where an account/organization/Enterprise/paid feature cannot be reproduced safely, the course provides an explicit scenario or read-only activity rather than pretending the feature was exercised.
7. Current GH-900 exam objectives are cross-checked separately so a newer exam objective is not lost merely because a Learn path gives it less emphasis.
8. Learner progression is unit-by-unit through the same live course Issue; a module is not considered covered merely because a README contains headings.
9. Course changes must pass source-depth, state-machine, workflow, validator, and untouched-submission gates before merge.

Canonical inventory: [`curriculum/official-curriculum.yml`](../curriculum/official-curriculum.yml).  
Pinned source map: [`curriculum/microsoft-source-lock.json`](../curriculum/microsoft-source-lock.json).  
Runtime catalog: [`curriculum/course-catalog.json`](../curriculum/course-catalog.json).

## Microsoft Learn inventory

| # | Official module | Units | Status |
|---:|---|---:|---|
| 1 | Introduction to Git | 6 | Implemented |
| 2 | Introduction to GitHub | 8 | Implemented |
| 3 | Introduction to GitHub's products | 9 | Implemented |
| 4 | Configure code scanning on GitHub | 7 | Implemented |
| 5 | Introduction to GitHub Copilot | 7 | Implemented |
| 6 | Code with GitHub Codespaces | 7 | Implemented |
| 7 | Manage your work with GitHub Projects | 8 | Implemented |
| 8 | Communicate effectively on GitHub using Markdown | 5 | Implemented |
| 9 | Contribute to an open-source project on GitHub | 7 | Implemented |
| 10 | Manage an InnerSource program by using GitHub | 5 | Implemented |
| 11 | Maintain a secure repository by using GitHub best practices | 6 | Implemented |
| 12 | Introduction to GitHub administration | 7 | Implemented |
| 13 | Authenticate and authorize user identities on GitHub | 7 | Implemented |
| 14 | Manage repository changes by using pull requests on GitHub | 5 | Implemented |
| 15 | Search and organize repository history by using GitHub | 5 | Implemented |
| 16 | Using GitHub Copilot with Python | 7 | Implemented |
| **Total** | **16 modules** | **106 units** | **106/106 source-resolved; 106-step runtime; 16/16 lab packages** |

## Runtime coverage

The normal learner experience mirrors GitHub Skills rather than asking the learner to orchestrate workflows manually:

1. **Copy Exercise** creates a repository from the course template.
2. `.github/workflows/00-start-course.yml` runs on the copied repository's initial `main` event and creates the live course Issue.
3. `.github/workflows/01-course-engine.yml` reads the hidden `mXX-uYY` state marker and presents exactly one official unit at a time.
4. Reading/summary units advance with `/next`.
5. Activity units advance only after the required lab branch/state passes `scripts/validate_unit_activity.py`.
6. Assessment units advance only after the appropriate blind assessment validator passes.
7. After the last unit (`m16-u07`), the course Issue is closed as completed.

Module-specific durable validation includes:

- Module 1: CLI/VS Code commits, changed Git fixtures, visible merge commit, recorded SHAs, remote push state;
- Module 2: real Issue and Pull Request references are checked in the learner repository;
- Module 8: Markdown artifact structure;
- Module 10: InnerSource program artifact;
- Module 11: `SECURITY.md` and `.github/CODEOWNERS`;
- Module 12: administration scenario matrix;
- Module 13: identity scenarios;
- Module 16: Python implementation/tests.

Other Enterprise/UI/account-only activities use explicit evidence/scenario checks because a public learner repository cannot expose an enterprise tenant, IdP, billing console, or paid plan on demand.

## Microsoft-source coverage controls

`Course Quality` performs a sparse checkout of the pinned `MicrosoftDocs/learn` source tree and resolves all **106/106 units** from their module indexes. `scripts/audit_microsoft_semantic_depth.py` compares learner-visible local coverage with the size/depth of the official source so a title/objective-only placeholder cannot satisfy the gate.

The depth check is intentionally a guardrail rather than a claim that string length proves semantic equivalence. For units whose base text was too compressed, [`unit-details/`](../unit-details/) contains source-audited additions that are rendered directly into the live learner step. Manual source review remains part of the completeness process.

The repository does **not** copy Microsoft's knowledge-check question bank. Assessments are original questions that test equivalent concepts and are validated with hidden hashes.

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

Time-sensitive plan prices, quotas, limits, or feature packaging are identified as source-snapshot facts where they appear and should be verified against current GitHub documentation for real purchasing/administration decisions.

## Automated merge gate

The `Course Quality` workflow rejects changes when any of these contracts break:

- source inventory is not 16 modules / 106 units;
- the unit engine is not exactly 106 sequential states;
- an upstream source unit cannot be resolved at the pinned commit;
- learner-visible coverage is materially too thin relative to the source;
- a module/lab/runtime component disappears;
- a workflow YAML file does not parse;
- Python validators do not compile;
- untouched activities or assessments can pass.

## Sources

- [Microsoft Learn — GitHub Foundations Part 1](https://learn.microsoft.com/en-us/training/paths/github-foundations/)
- [Microsoft Learn — GitHub Foundations Part 2](https://learn.microsoft.com/en-us/training/paths/github-foundations-2/)
- [Microsoft Learn — GH-900 Study Guide](https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/gh-900)
- [GitHub Skills](https://skills.github.com/)
- [GitHub Docs](https://docs.github.com/)
