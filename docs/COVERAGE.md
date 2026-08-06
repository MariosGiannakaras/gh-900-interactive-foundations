# Coverage matrix

Verified against Microsoft Learn and the GH-900 study guide on **2026-08-06**.

## Completeness contract

This project is not a summary course. Completion requires all of the following:

1. Every official Microsoft Learn learning path is represented.
2. Every official module is represented.
3. Every official unit is represented, including introductions, exercises, assessments, and summaries.
4. The concepts and learning objectives taught by each unit are covered in original wording.
5. Where an official unit is practical, the course provides a hands-on equivalent; where an account/Enterprise feature cannot be reproduced safely, the course provides an explicit interactive simulation.
6. Current GH-900 exam objectives are cross-checked separately so a newer objective is not lost merely because a Learn path gives it less emphasis.
7. A module counts as implemented only when theory, practical/simulated activity, assessment, source links, runtime integration, and completeness audit are present.

Canonical official inventory: [`curriculum/official-curriculum.yml`](../curriculum/official-curriculum.yml).
Runtime module catalog: [`curriculum/course-catalog.json`](../curriculum/course-catalog.json).

## Microsoft Learn inventory

| # | Official module | Units | Interactive implementation |
|---:|---|---:|---|
| 1 | Introduction to Git | 6 | Implemented — multi-step GitHub Skills-style workflow |
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
| **Total** | **16 modules** | **106 units** | **106/106 units mapped; 16/16 interactive packages** |

## Runtime coverage

- Module 1: dedicated `GH-900 Module 1 Interactive Course` workflow with durable step-by-step state checks.
- Modules 2–16: `GH-900 Full Course Progress` workflow with automatic validation and next-module progression.
- Modules 2–16: shared validator checks evidence placeholders, activity completion, blind knowledge checks, and module-specific required artifacts.
- Module 8: Markdown artifact structure is checked automatically.
- Module 10: InnerSource program artifact is required.
- Module 11: `SECURITY.md` and `.github/CODEOWNERS` are required.
- Module 12: administration matrix is required.
- Module 13: identity-scenarios artifact is required.
- Module 16: Python implementation must pass included tests.
- `scripts/audit_complete_course.py`: verifies 16 modules, 106 unit headings, 16 lab packages, answer-hash coverage, and runtime files.

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

The implementation explicitly includes the current areas most likely to be missed by older GH-900 material:

- Copilot agents, Agent Mode, and multi-model concepts;
- passkeys;
- Enterprise Managed Users (EMU);
- organization-wide governance/Copilot policy concepts;
- `github.dev` versus Codespaces;
- current repository management/security practices and dependency insights.

## Source links

- [Microsoft Learn — GitHub Foundations Part 1](https://learn.microsoft.com/en-us/training/paths/github-foundations/)
- [Microsoft Learn — GitHub Foundations Part 2](https://learn.microsoft.com/en-us/training/paths/github-foundations-2/)
- [Microsoft Learn — GH-900 Study Guide](https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/gh-900)
- [GitHub Skills](https://skills.github.com/)
- [GitHub Docs](https://docs.github.com/)

## Automated gate

The `Course Quality` workflow must pass before changes are merged. The completeness audit rejects missing module READMEs, missing unit mappings, missing labs, incomplete assessment-hash coverage, or missing runtime components.
