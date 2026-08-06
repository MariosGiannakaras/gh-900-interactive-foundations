# Module 11 — Maintain a secure repository: Interactive submission

Read `modules/11-secure-repository/README.md` first. Work on branch `lab/module-11`.

## Hands-on activities

1. Create or review a `SECURITY.md` policy explaining how vulnerabilities should be reported.
2. Create/review `.github/CODEOWNERS` and map at least one path to an owner placeholder or your username.
3. Review branch/ruleset protection concepts: required PRs, reviews, status checks, signed commits where appropriate, and restrictions.
4. Inspect Dependabot alerts/settings and a `.github/dependabot.yml` example; enable only features appropriate for your fork.
5. Inspect secret scanning/push protection and dependency review concepts; do not commit real secrets for testing.
6. Record how least privilege, protected branches/rulesets, automated dependency/security checks, and secure disclosure work together.

ACTIVITY_STATUS: INCOMPLETE
EVIDENCE_SECURITY_POLICY: REPLACE_ME
EVIDENCE_CODEOWNERS: REPLACE_ME
EVIDENCE_RULESET_NOTE: REPLACE_ME
EVIDENCE_DEPENDABOT_NOTE: REPLACE_ME
EVIDENCE_SECRET_SCANNING_NOTE: REPLACE_ME

## Knowledge check

### Q1
What is the safest way to test secret-scanning concepts?
- [ ] A. Commit a real cloud API key and delete it later.
- [ ] B. Disable all repository history.
- [ ] C. Use documentation/test patterns and never place real credentials in the repository.

### Q2
What is the purpose of `SECURITY.md`?
- [ ] A. It configures Git remotes.
- [ ] B. It documents the project's security policy and preferred vulnerability-reporting process.
- [ ] C. It creates a Codespace.

### Q3
What does CODEOWNERS help automate?
- [ ] A. Identifying responsible owners/reviewers for paths and supporting required review workflows.
- [ ] B. Subscription billing.
- [ ] C. Git object garbage collection.

### Q4
Why use branch protection or repository rulesets?
- [ ] A. To make every repository public.
- [ ] B. To prevent all branching.
- [ ] C. To enforce controls such as PR review, checks, restrictions, and other repository policies before protected refs change.

### Q5
What does Dependabot help with?
- [ ] A. Generating Git commit hashes.
- [ ] B. Dependency vulnerability awareness and, depending on configuration, automated update Pull Requests.
- [ ] C. Managing SAML identities.

### Q6
What principle should guide repository permissions?
- [ ] A. Least privilege: grant only the access needed for the role/task.
- [ ] B. Give every contributor admin access.
- [ ] C. Share one administrator account across the team.
