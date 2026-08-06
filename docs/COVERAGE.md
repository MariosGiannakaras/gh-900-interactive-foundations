# Coverage matrix

Verified against Microsoft Learn and the GH-900 study guide on **2026-08-06**.

## Completeness contract

This project is not a summary course. Completion requires all of the following:

1. Every official Microsoft Learn learning path is represented.
2. Every official module is represented.
3. Every official unit is represented, including introductions, exercises, assessments, and summaries.
4. The concepts and learning objectives taught by each unit are covered in original wording.
5. Where an official unit is practical, the local course provides a hands-on equivalent or a documented reason why only a simulation is possible.
6. Current GH-900 exam objectives are cross-checked separately so an exam objective is not lost merely because the Learn paths lag behind the exam blueprint.
7. A module is marked `complete` only after theory, hands-on activity/simulation, assessment, source links, and coverage audit all pass.

Canonical machine-readable inventory: [`curriculum/official-curriculum.yml`](../curriculum/official-curriculum.yml).

## Microsoft Learn inventory

| # | Official module | Units | Interactive implementation |
|---:|---|---:|---|
| 1 | Introduction to Git | 6 | Implemented in bootstrap checkpoint |
| 2 | Introduction to GitHub | 8 | Planned |
| 3 | Introduction to GitHub's products | 9 | Planned |
| 4 | Configure code scanning on GitHub | 7 | Planned |
| 5 | Introduction to GitHub Copilot | 7 | Planned |
| 6 | Code with GitHub Codespaces | 7 | Planned |
| 7 | Manage your work with GitHub Projects | 8 | Planned |
| 8 | Communicate effectively on GitHub using Markdown | 5 | Planned |
| 9 | Contribute to an open-source project on GitHub | 7 | Planned |
| 10 | Manage an InnerSource program by using GitHub | 5 | Planned |
| 11 | Maintain a secure repository by using GitHub best practices | 6 | Planned |
| 12 | Introduction to GitHub administration | 7 | Planned |
| 13 | Authenticate and authorize user identities on GitHub | 7 | Planned |
| 14 | Manage repository changes by using pull requests on GitHub | 5 | Planned |
| 15 | Search and organize repository history by using GitHub | 5 | Planned |
| 16 | Using GitHub Copilot with Python | 7 | Planned |
| **Total** | **16 modules** | **106 units** | **6/106 units implemented** |

## Current GH-900 exam blueprint cross-check

The January 2026 GH-900 blueprint has seven domains. Each domain remains an independent completeness gate even after all 106 Learn units are implemented.

| GH-900 domain | Weight | Required coverage areas |
|---|---:|---|
| Understand Git and GitHub basics | 25–30% | version control; Git vs GitHub; repositories, commits, branches; accounts/organizations/enterprise; GitHub Flow; Markdown; Desktop; Mobile |
| Work with GitHub repositories | 10–15% | README, LICENSE, CONTRIBUTING, CODEOWNERS, SECURITY; templates; branches; files; insights; stars; feature previews; metrics; dependency insights; maintenance practices |
| Collaborate using GitHub | 10–15% | issues; pull requests; discussions; linked work; templates; filters; assignments; notifications; Gists; Wikis; Pages |
| Apply modern development practices | 10–15% | Actions; Copilot suggestions; agents; Agent Mode; multi-model support; Copilot plan differences; Codespaces; dev containers; github.dev |
| Manage projects with GitHub | 5–10% | Projects; layouts; labels; milestones; workflows; saved replies; assignees; project insights |
| Privacy, security, and administration | 10–15% | 2FA; passkeys; repository/org roles; EMUs; organization-wide Copilot policy; visibility; branch protection; organizations; teams; roles |
| Explore the GitHub community | 5–10% | open source; Sponsors; following; Marketplace; InnerSource; forks; templates; discoverability |

### Blueprint-only / freshness watch

The exam guide changed significantly in January 2026. During implementation, the following current objectives must be explicitly checked even if an older Learn unit does not emphasize them enough:

- Copilot agents, Agent Mode, and multi-model support.
- Passkeys.
- Enterprise Managed Users (EMUs).
- Organization-wide Copilot policy management.
- `github.dev` versus Codespaces.
- Repository metrics/dependency insights and current repository-management features.

## Source links

- [Microsoft Learn — GitHub Foundations Part 1](https://learn.microsoft.com/en-us/training/paths/github-foundations/)
- [Microsoft Learn — GitHub Foundations Part 2](https://learn.microsoft.com/en-us/training/paths/github-foundations-2/)
- [Microsoft Learn — GH-900 Study Guide](https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/gh-900)
- [GitHub Skills](https://skills.github.com/)

## Status rule

Do not increase the implemented count merely because a placeholder file exists. A unit counts only when its instructional content, practical layer or justified simulation, validation, and assessment linkage are present and reviewed.
