# Module 3 — Introduction to GitHub's products

Official Microsoft Learn module: <https://learn.microsoft.com/en-us/training/modules/github-introduction-products/>

This module maps **1:1 to all 9 official units**.

## Learning objectives

After this module you should be able to:

- distinguish GitHub account types from GitHub plans;
- explain Personal, Organization, and Enterprise accounts;
- distinguish GitHub Free, Pro, Team, and Enterprise plans at a conceptual level;
- explain the roles of GitHub Mobile and GitHub Desktop;
- understand subscriptions versus usage-based billing;
- recognize how Actions, Packages, Copilot, Marketplace, and other metered products affect billing;
- explain enterprise seat/license usage, including active seats and PAYG versus prepaid models;
- understand why automation/machine identities and peripheral services matter to cost and governance;
- interpret metered-usage reporting concepts.

---

## Unit 1 — Introduction

Official unit: <https://learn.microsoft.com/en-us/training/modules/github-introduction-products/1-introduction>

GitHub product decisions involve three distinct layers:

1. **account type** — who owns resources and how identity/administration is structured;
2. **plan** — which feature/support tier applies;
3. **metered products/usage** — consumption that can produce variable charges.

Do not treat account type and plan as synonyms.

---

## Unit 2 — GitHub accounts and plans

Official unit: <https://learn.microsoft.com/en-us/training/modules/github-introduction-products/2-what-are-github-products>

### Account types

#### Personal account

Every human user signs in with a personal account. The personal account is the user's identity and attribution surface on GitHub.

A personal account can own resources such as repositories, packages, and projects. Actions such as commits, issues, and reviews are attributed to the acting user.

Personal accounts use either GitHub Free or GitHub Pro.

#### Organization account

An organization is a shared ownership and collaboration boundary for multiple people and repositories.

Important differences from a personal account:

- you do **not** sign in as the organization;
- people sign in with their own identities and become organization members;
- organizations own repositories/packages/projects;
- access is managed through organization/repository roles and teams;
- owners and designated security/administrative roles manage policies and access.

A person can belong to multiple organizations.

#### Enterprise account

An enterprise account provides a higher-level administrative boundary over multiple organizations. It is used for centralized policy, identity, governance, and billing.

Enterprise administration can support organization-wide or enterprise-wide policies, consolidated billing, enterprise security controls, and InnerSource across organizations.

### Plans

The Microsoft Learn curriculum distinguishes these plan families:

- **GitHub Free** for personal accounts and organizations;
- **GitHub Pro** for personal accounts;
- **GitHub Team** for organizations needing additional collaboration/management capabilities;
- **GitHub Enterprise** for enterprise governance, security, identity, support, and centralized administration.

Plan features and prices evolve. For exam questions, focus on the **relative capability model** rather than memorizing a transient price.

Conceptually:

- Free provides core Git/GitHub collaboration;
- Pro enhances an individual developer's feature set;
- Team adds organization-oriented collaboration and repository-management controls;
- Enterprise adds centralized identity/governance, advanced auditing/security/support, and enterprise administration.

---

## Unit 3 — GitHub Mobile and GitHub Desktop

Official unit: <https://learn.microsoft.com/en-us/training/modules/github-introduction-products/3-mobile-versus-desktop>

### GitHub Desktop

GitHub Desktop is a graphical desktop application for common Git/GitHub workflows. Typical uses include:

- cloning repositories;
- viewing changed files and diffs;
- staging/committing changes;
- creating/switching branches;
- pushing/pulling;
- interacting with GitHub repositories without relying entirely on the CLI.

Desktop is primarily a **local development/version-control client**.

### GitHub Mobile

GitHub Mobile focuses on collaboration and repository activity while away from a desktop development environment. Typical activities include:

- reviewing notifications;
- reading/responding to Issues and PR conversations;
- reviewing pull requests;
- managing lightweight collaboration tasks;
- staying aware of repository/team activity.

Mobile is not a substitute for a full local build/test environment.

### Choosing between them

Use Desktop when the task is primarily local Git work and file/branch management. Use Mobile when the task is primarily review, triage, communication, or monitoring on a phone/tablet.

---

## Unit 4 — GitHub billing

Official unit: <https://learn.microsoft.com/en-us/training/modules/github-introduction-products/4-github-billing>

Billing is associated with the relevant personal, organization, or enterprise account.

A bill can combine:

### Fixed/subscription charges

Examples include:

- an account plan such as Pro or Team;
- GitHub Copilot seats/subscriptions;
- Marketplace app subscriptions;
- other fixed-price products.

### Usage-based charges

Examples include:

- GitHub Actions compute/runtime and related storage;
- Packages storage/data transfer;
- other metered services.

Plans often include quotas/allowances. Usage over included amounts can be controlled through budgets/spending limits and billing policies.

### Public vs private Actions usage

GitHub-hosted Actions usage for standard public repositories is generally provided without the same private-repository minute quota model. Private repositories consume included plan quotas and can incur additional usage depending on billing configuration.

Exact allowances/prices change over time; the course links to the live pricing/billing documentation rather than requiring stale price memorization.

### Organizational plan progression

At a conceptual level:

- Free: core repository/collaboration capabilities;
- Team: adds stronger team/repository management and collaboration controls;
- Enterprise: adds enterprise identity, auditing, governance, security, and enterprise support capabilities.

---

## Unit 5 — License Usage Stats

Official unit: <https://learn.microsoft.com/en-us/training/modules/github-introduction-products/5-license-usage-stats>

Enterprise administrators need to understand who consumes seats/licenses and where.

Common license-usage views include:

- total seats;
- active/used seats;
- pending invitations;
- available seats where the commercial model exposes a fixed pool;
- historical usage trends;
- usage by organization or enterprise.

### Prepaid vs PAYG

In a prepaid/subscription seat model, an administrator may see a fixed allocation and remaining/available seats.

In a **pay-as-you-go (PAYG)** model, cost is based on actual active usage rather than consuming from a prepaid pool; therefore an "available licenses" concept may not apply in the same way.

### Administrative/API access

Enterprise usage can be inspected through enterprise/organization billing interfaces and, where supported, APIs. The exam-level concept is that license reporting can be centralized and automated rather than manually counted repository by repository.

Use reporting to:

- optimize cost;
- identify inactive allocations;
- support compliance/audit work;
- forecast demand;
- detect unusual access patterns.

---

## Unit 6 — License Usage Stats in Machine and Peripheral Devices

Official unit: <https://learn.microsoft.com/en-us/training/modules/github-introduction-products/6-license-usage-machine>

### Machine accounts

A machine account is an account used primarily for automation or integration rather than interactive human work.

Examples include identities used by legacy automation, bots, CI systems, or third-party integration scripts.

A machine identity can create security and licensing consequences:

- unnecessary license/seat consumption;
- long-lived credentials;
- stale accounts with excessive privileges;
- unclear ownership/audit trails.

Prefer purpose-built GitHub Apps, scoped tokens, Actions identities, or other appropriate service authentication mechanisms when they solve the use case more safely than a full user account.

### Peripheral services

External services interacting with GitHub can include:

- CI/CD systems and runners;
- security scanners;
- issue/project integrations;
- chat/notification integrations;
- observability tools;
- API consumers.

Not every external service necessarily consumes a user seat, but all integrations should be inventoried for cost, permissions, credentials, and security impact.

### Governance principles

Administrators should periodically review:

- last activity;
- owner/purpose;
- granted permissions;
- token/application scopes;
- whether the integration is still needed;
- associated usage/cost.

---

## Unit 7 — Metered Usage Reports

Official unit: <https://learn.microsoft.com/en-us/training/modules/github-introduction-products/7-metered-usage-consumption-reports>

Metered reports help administrators understand variable consumption.

Common categories include:

- Actions compute/runtime and storage;
- Packages storage/data transfer;
- enterprise seats/licenses;
- Copilot seats/usage where applicable;
- GitHub Advanced Security or other metered advanced products where applicable.

Useful report dimensions can include:

- account/organization;
- repository;
- product/SKU;
- runner type;
- time period;
- quantity consumed;
- cost center or business unit in enterprise billing setups.

### Cost-control practices

For Actions:

- avoid unnecessary triggers;
- use caching appropriately;
- eliminate duplicate jobs;
- choose runner types intentionally;
- define budgets/spending controls.

For Packages/artifacts:

- establish retention/deletion policies;
- remove stale artifacts/packages;
- avoid needless duplication.

For licenses:

- remove stale members/invitations;
- audit automation identities;
- review assigned products periodically.

Do not memorize old per-minute prices from static training text as permanent truths; verify current pricing when making a real billing decision.

---

## Unit 8 — Module assessment

Official unit: <https://learn.microsoft.com/en-us/training/modules/github-introduction-products/8-knowledge-check>

The integrated assessment tests:

- account type vs plan;
- personal vs organization vs enterprise ownership;
- Desktop vs Mobile;
- subscription vs metered cost;
- Actions/Packages usage concepts;
- prepaid vs PAYG seats;
- machine-account governance;
- enterprise usage reporting.

---

## Unit 9 — Summary

Official unit: <https://learn.microsoft.com/en-us/training/modules/github-introduction-products/9-summary>

After this module you should be able to choose the correct account/plan concept for a scenario, identify the appropriate client surface, and explain how GitHub billing and enterprise usage reporting fit together.

## Hands-on/simulation layer

Because changing real paid plans or enterprise licensing solely for training would be inappropriate, this module uses an interactive **billing and account architecture simulation**. You will classify scenarios, inspect this public repository's current plan-independent features, and produce a small `account-plan-decisions.md` artifact that the course engine validates.

## Official references

- Microsoft Learn module: <https://learn.microsoft.com/en-us/training/modules/github-introduction-products/>
- GitHub plans: <https://github.com/pricing>
- GitHub billing docs: <https://docs.github.com/en/billing>
- GitHub Enterprise administration: <https://docs.github.com/en/enterprise-cloud@latest/admin>
