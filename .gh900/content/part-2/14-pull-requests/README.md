# Module 14 — Manage repository changes by using pull requests on GitHub

Official Microsoft Learn module: <https://learn.microsoft.com/en-us/training/modules/manage-changes-pull-requests-github/>

This module maps **1:1 to all 5 official units**.

## Learning objectives

After this module you should be able to:

- explain why branches are essential to pull-request workflows;
- distinguish base and compare/head branches;
- create a pull request and a draft pull request;
- recognize draft, open, closed, and merged PR states;
- request reviewers and work with reviews/comments;
- understand required reviews and status checks;
- compare merge commit, squash merge, and rebase merge;
- understand branch cleanup, stars, keyboard shortcuts, and the GitHub command palette where covered by the official module.

---

## Unit 1 — Introduction

Official unit: <https://learn.microsoft.com/en-us/training/modules/manage-changes-pull-requests-github/1-introduction>

Pull requests are GitHub's primary collaboration surface for proposing, reviewing, discussing, validating, and merging branch changes.

A pull request does not replace Git branches. It adds collaboration and policy around the relationship between branches.

---

## Unit 2 — What are pull requests?

Official unit: <https://learn.microsoft.com/en-us/training/modules/manage-changes-pull-requests-github/2-what-are-pull-requests>

### Branches and PRs

Branches isolate work so multiple developers can make independent commits without immediately changing the shared/default branch.

A PR becomes useful when that isolated work is ready to be compared with and potentially integrated into another branch.

### Base and compare branches

A pull request compares:

- **base branch** — the destination branch that should receive the change;
- **compare/head branch** — the source branch containing the proposed commits.

The default branch is often `main`, but a PR can target another branch when the workflow requires it.

### Creating a pull request

A normal creation flow is:

1. create a branch;
2. make/commit/push changes;
3. choose **Compare & pull request** or open the Pull Requests tab;
4. select base and compare branches;
5. write a clear title and description;
6. create as ready-for-review or draft.

A useful description explains purpose, related work, testing, risks, and anything reviewers need to understand.

### Pull-request states

#### Draft

A draft PR communicates that work is incomplete/not ready for formal merge. Draft PRs cannot be merged until marked ready for review. Code Owners are not automatically requested in the same way as a ready-for-review PR.

#### Open

The PR is active and unmerged. New commits pushed to its source branch automatically update the PR.

#### Closed

The PR was closed without merging. This is useful when the change is no longer wanted, superseded, or abandoned.

#### Merged

The source changes have been integrated into the base branch through one of the repository's enabled merge methods.

### Reviewers

A PR can request review from eligible collaborators/teams. Reviewers inspect the diff, comment, approve, or request changes.

Repository rules can require a number of approving reviews and/or Code Owner approval before merge.

### Status checks and CI

PRs can run checks from GitHub Actions or external CI systems. Typical checks include:

- unit/integration tests;
- formatting/linting;
- build verification;
- security scanning.

When a required check fails, merge is blocked until the branch satisfies the configured rule.

### Merge methods

#### Merge commit

Preserves the source branch's commits and creates a merge commit tying histories together. Useful when explicit branch history is desired.

#### Squash and merge

Combines the source branch commits into one commit on the base branch. Useful for a concise base-branch history.

#### Rebase and merge

Replays source commits onto the base branch without creating a merge commit, producing a linear history while preserving individual commits.

The repository controls which methods are available.

No merge strategy is universally best; choose based on traceability, history style, and team policy.

### Branch cleanup

After merge, a short-lived feature branch can normally be deleted because its work is now represented in the base branch history. Repository settings can automatically delete merged branches in supported configurations.

### Stars

Starring a repository saves it to your personal starred list and is also a lightweight signal of interest/appreciation. Stars do not grant permissions or subscribe you to all notifications.

### Keyboard shortcuts

Press `?` on GitHub.com to see available keyboard shortcuts. Shortcuts vary by page/context.

### Command palette

GitHub's command palette can be opened with `Ctrl+K` on Windows/Linux or `⌘+K` on macOS in supported contexts. It helps navigate repositories/pages and invoke common actions without manually traversing menus.

---

## Unit 3 — Exercise: Reviewing pull requests

Official unit: <https://learn.microsoft.com/en-us/training/modules/manage-changes-pull-requests-github/3-review-pull-requests>

The interactive course creates a real, isolated review workflow using `lab/m14-u03` → `sandbox/m14-u03`; the exercise never targets learner `main`.

The learner:

1. makes multiple commits while fixing the intentional defect in `exercise/review_fixture.py` and keeping `exercise/test_review_fixture.py` passing;
2. opens the Pull Request from `lab/m14-u03` into `sandbox/m14-u03` as a **draft**;
3. inspects **Conversation**, **Commits**, **Checks**, and **Files changed**;
4. marks the PR **Ready for review**;
5. adds an inline review comment on the changed code/intentional defect;
6. pushes a follow-up update resolving the review point and inspects the updated diff/check state;
7. posts a unit-scoped `/reflection ...` comparing merge-commit, squash, and rebase implications for history;
8. merges the temporary training PR using an allowed merge method.

The engine records draft/ready transitions, verifies the real PR/review/commit/test state, and cleans the temporary branches after successful validation. No merge-strategy worksheet is created.

---

## Unit 4 — Module assessment

Official unit: <https://learn.microsoft.com/en-us/training/modules/manage-changes-pull-requests-github/4-knowledge-check>

Assessment coverage includes:

- branches and PR purpose;
- base vs compare branch;
- draft/open/closed/merged states;
- reviewers;
- required reviews/status checks;
- merge methods;
- branch cleanup;
- stars, shortcuts, and command palette concepts covered by Microsoft Learn.

---

## Unit 5 — Summary

Official unit: <https://learn.microsoft.com/en-us/training/modules/manage-changes-pull-requests-github/5-summary>

After this module you should be able to take a branch change through proposal, review, CI, update, and merge while understanding the resulting Git history.

## Official references

- Microsoft Learn module: <https://learn.microsoft.com/en-us/training/modules/manage-changes-pull-requests-github/>
- GitHub Docs — Pull requests: <https://docs.github.com/en/pull-requests>
- GitHub Docs — Merge methods: <https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges>
