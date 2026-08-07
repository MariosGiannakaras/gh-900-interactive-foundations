# Module 14 — Manage repository changes with Pull Requests: Interactive submission

Read `modules/14-pull-requests/README.md` first. Work on branch `lab/module-14`.

## Hands-on activities

1. Create a small Issue describing the documentation change you will make.
2. Make that documentation change on `lab/module-14` and open a Pull Request to `main`.
3. Write a clear PR title/body and reference the related Issue in the PR body (`Closes #...`, `Fixes #...`, or another explicit `#...` reference appropriate to your scenario).
4. Inspect **Files changed** and add at least one review-style comment to your own diff if GitHub allows it; otherwise document the exact review action you would take on another contributor's PR.
5. Compare approve, comment, and request-changes review outcomes.
6. Inspect merge commit, squash merge, and rebase merge options and explain when each affects history differently.
7. Inspect branch protection/ruleset settings that can require reviews/status checks before merge.

ACTIVITY_STATUS: INCOMPLETE
EVIDENCE_ISSUE: REPLACE_ME
EVIDENCE_PR: REPLACE_ME
EVIDENCE_REVIEW_NOTE: REPLACE_ME
EVIDENCE_MERGE_STRATEGY_NOTE: REPLACE_ME
EVIDENCE_PROTECTION_NOTE: REPLACE_ME

## Knowledge check

### Q1
What is a Pull Request?
- [ ] A. A request to download a repository locally.
- [ ] B. A reviewable proposal to merge a set of branch changes into another branch.
- [ ] C. A GitHub billing object.

### Q2
What is the main purpose of the Files changed tab?
- [ ] A. Review the diff and discuss specific changed lines/files.
- [ ] B. Change account passwords.
- [ ] C. Configure enterprise SSO.

### Q3
What does a request-changes review communicate?
- [ ] A. The PR is automatically merged.
- [ ] B. The branch is deleted.
- [ ] C. The reviewer believes changes are required before the PR should be accepted.

### Q4
Why use squash merge?
- [ ] A. To preserve every feature-branch commit as separate commits on the target.
- [ ] B. To combine the PR's changes into a single target-branch commit, simplifying target history.
- [ ] C. To disable review.

### Q5
What can required status checks do?
- [ ] A. Prevent merge/update of protected refs until specified automated checks pass.
- [ ] B. Change GitHub plan automatically.
- [ ] C. Replace authentication.

### Q6
What makes a PR easier to review?
- [ ] A. Mixing many unrelated features.
- [ ] B. Hiding test results.
- [ ] C. Focused scope, useful description/context, understandable commits/diff, and relevant tests/checks.
