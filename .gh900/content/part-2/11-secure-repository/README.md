# Module 11 — Maintain a secure repository by using GitHub best practices

Official Microsoft Learn module: <https://learn.microsoft.com/en-us/training/modules/maintain-secure-repository-github/>

This module maps **1:1 to all 6 official units**.

## Learning objectives

After this module you should be able to:

- explain secure-development and shift-left principles;
- identify repository security features in the Security tab;
- use `SECURITY.md`, security advisories, `.gitignore`, branch protections/rules, required reviews, and CODEOWNERS appropriately;
- explain dependency graphs, Dependabot alerts, Dependabot security/version updates, code scanning, and secret scanning;
- understand what to do when sensitive data is committed;
- distinguish removing a secret from the latest change from purging sensitive data from repository history;
- design basic supply-chain protections for a repository.

---

## Unit 1 — Introduction

Official unit: <https://learn.microsoft.com/en-us/training/modules/maintain-secure-repository-github/1-introduction>

Repository security is not a final deployment gate. Secure development integrates security into planning, coding, review, CI, dependency management, release, and maintenance.

A **shift-left** approach moves feedback earlier in the development lifecycle so developers can detect and remediate problems before they become expensive production incidents.

Security includes confidentiality, integrity, authentication, authorization, auditability, and compliance—not only vulnerability scanning.

---

## Unit 2 — How to maintain a secure GitHub repository

Official unit: <https://learn.microsoft.com/en-us/training/modules/maintain-secure-repository-github/2-how-to-maintain-secure-repository>

### Security strategy

A mature secure-development strategy accounts for:

- ongoing security education;
- secure architecture/design;
- secure implementation;
- review/testing;
- compliance requirements;
- repeatable automated controls;
- audit/history.

### Repository Security tab

Depending on repository/account features, the Security area can expose:

- security policy;
- security advisories;
- Dependabot alerts;
- code scanning;
- secret scanning;
- dependency information;
- security overview/context.

### SECURITY.md

A `SECURITY.md` policy tells people how to report vulnerabilities responsibly.

It should commonly explain:

- supported versions;
- how/where to report a vulnerability privately;
- what information to include;
- expected response process/timeline when appropriate;
- safe disclosure expectations.

Do not instruct researchers to publish an exploitable vulnerability as a normal public Issue before maintainers can address it.

### Repository security advisories

Security advisories let maintainers discuss and remediate vulnerabilities privately, coordinate fixes, and later publish disclosure information. Published advisories can integrate with vulnerability ecosystems such as CVE/GitHub Advisory Database processes where applicable.

### `.gitignore`

`.gitignore` prevents matching **untracked** files from being selected by normal Git add operations. Typical ignored content includes:

- build outputs;
- temporary files;
- local environment files;
- editor artifacts;
- generated dependencies/cache;
- local configuration that must not enter source control.

Important limitation: `.gitignore` is preventive convenience, not a security boundary. It does not remove already tracked files and a user can deliberately override it.

### If sensitive data is committed

Assume exposed credentials/secrets may be compromised.

Immediate response generally includes:

1. revoke/rotate the secret with the issuing provider;
2. stop further use;
3. remove it from the current code;
4. determine whether historical cleanup is required;
5. follow GitHub's sensitive-data removal guidance;
6. coordinate with collaborators because history rewrites affect clones/forks;
7. add preventive controls such as secret scanning/push protection and safer secret storage.

Simply adding a leaked file to `.gitignore` or deleting it in a later commit does **not** erase the value from old commits.

### Branch protection / rulesets

Repository rules can enforce workflows on important branches, including requirements such as:

- pull requests before merge;
- approving reviews;
- passing status checks;
- conversation resolution;
- signed commits or other supported constraints;
- restrictions on force pushes/deletions;
- code-owner review.

Rulesets are the modern policy framework; branch protection rules remain an important concept and may coexist depending on configuration.

### Required reviews

Required reviews establish independent scrutiny before merge. Options can include:

- a minimum number of approvals;
- dismissal of stale approvals after new changes;
- approval from someone other than the latest pusher;
- Code Owner approval.

### CODEOWNERS

`CODEOWNERS` assigns people/teams responsibility for paths.

Example:

```text
*.js        @org/javascript-team
/docs/      @org/docs-team
/security/  @org/security-team
```

Supported locations include the repository root, `.github/`, or `docs/`. With appropriate branch/rules configuration, Code Owner review can be required.

---

## Unit 3 — Automated security

Official unit: <https://learn.microsoft.com/en-us/training/modules/maintain-secure-repository-github/3-security-automation>

### Dependency graph

GitHub can parse supported package manifests/lock files to build a dependency graph, including transitive dependency relationships where supported.

The dependency graph enables other supply-chain features.

### Dependabot alerts

Dependabot compares dependency versions against known vulnerability data and alerts repository maintainers when vulnerable dependencies are detected.

An alert identifies a vulnerable dependency/version and usually provides advisory/remediation information.

### Dependabot security updates

Dependabot can automatically propose pull requests that update vulnerable dependencies to a remediated version when possible.

A generated PR still needs normal validation—tests, compatibility checks, review, and merge policy.

### Dependabot version updates

Version-update configuration in `.github/dependabot.yml` can proactively open PRs to keep dependencies current even when there is not a known vulnerability.

Do not confuse:

- **alerts** — tell you a dependency is vulnerable;
- **security updates** — propose a fix for vulnerable dependencies;
- **version updates** — proactively keep dependencies updated on a schedule/configuration.

### Code scanning

Code scanning analyzes source code for security/correctness problems. CodeQL is GitHub's primary semantic analysis engine, but third-party SARIF-producing tools can integrate too.

### Secret scanning and push protection

Secret scanning searches for known credential/token patterns. On supported repositories/configurations, **push protection** can block a secret before it enters Git history.

Public repositories receive broad secret-scanning protections, while private/internal availability and advanced controls depend on plan/security configuration.

A secret-scanning alert should trigger credential-provider remediation (for example revoke/rotate), not merely deletion from a file.

---

## Unit 4 — Exercise: Secure your repository's supply chain

Official unit: <https://learn.microsoft.com/en-us/training/modules/maintain-secure-repository-github/4-exercise-secure-repository-supply-chain>

The interactive exercise creates a temporary security workspace on `lab/m11-u04`. The learner must:

1. create root `SECURITY.md` with a responsible vulnerability-disclosure process;
2. create `.gitignore` protecting the supplied fake local-secret path;
3. create `.github/dependabot.yml` for the supplied npm/package manifest;
4. create `.github/CODEOWNERS` with ownership for `exercise/sensitive/`;
5. inspect the supplied `package.json` as dependency-graph/Dependabot input;
6. post a unit-scoped `/reflection ...` that designs repository rules requiring PRs, checks, and meaningful review and explains secret remediation using **revocation/rotation plus appropriate history handling**;
7. where available, inspect Dependabot, code-scanning, and secret-scanning surfaces under **Security**;
8. commit and push the temporary configuration.

The validator checks the real generated configuration plus the unit-scoped governance/remediation reflection. The exercise deliberately uses fake training data only; never paste a real credential into the repository. Root `SECURITY.md` and `.github/CODEOWNERS` are intentionally created only for this lesson and disappear with the temporary branches after completion.

---

## Unit 5 — Module assessment

Official unit: <https://learn.microsoft.com/en-us/training/modules/maintain-secure-repository-github/5-knowledge-check>

Assessment coverage includes:

- shift-left security;
- Security tab features;
- SECURITY.md/advisories;
- `.gitignore` limitations;
- secret compromise response;
- branch rules/reviews/CODEOWNERS;
- dependency graph;
- Dependabot alerts/security updates/version updates;
- code scanning;
- secret scanning/push protection.

---

## Unit 6 — Summary

Official unit: <https://learn.microsoft.com/en-us/training/modules/maintain-secure-repository-github/6-summary>

After this module you should be able to layer repository governance, automated scanning, dependency management, and disclosure practices into a coherent security strategy.

## Official references

- Microsoft Learn module: <https://learn.microsoft.com/en-us/training/modules/maintain-secure-repository-github/>
- GitHub Docs — Code security: <https://docs.github.com/en/code-security>
- GitHub Docs — Security policy: <https://docs.github.com/en/code-security/getting-started/adding-a-security-policy-to-your-repository>
- GitHub Docs — Dependabot: <https://docs.github.com/en/code-security/dependabot>
- GitHub Docs — Removing sensitive data: <https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository>
