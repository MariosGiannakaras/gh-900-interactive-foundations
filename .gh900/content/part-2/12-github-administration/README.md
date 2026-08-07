# Module 12 — Introduction to GitHub administration

Official Microsoft Learn module: <https://learn.microsoft.com/en-us/training/modules/github-introduction-administration/>

This module maps **1:1 to all 7 official units**.

## Learning objectives

After this module you should be able to:

- explain GitHub administration at team, organization, and enterprise scope;
- distinguish member, owner, maintainer, moderator, billing/security, outside-collaborator, and enterprise roles at a conceptual level;
- understand repository permission levels and least privilege;
- explain supported authentication technologies such as passkeys, 2FA, PATs, SSH keys, deploy keys, and SAML SSO;
- explain team synchronization and directory-service integration;
- understand organization design, base permissions, custom roles, and repository access;
- explain Enterprise Managed Users (EMU), enterprise governance, audit/policy, and centralized billing at a foundational level.

---

## Unit 1 — Introduction

Official unit: <https://learn.microsoft.com/en-us/training/modules/github-introduction-administration/1-introduction>

GitHub administration is the set of tasks used to manage identity, access, policy, security, repositories, organizations, and enterprises.

Administration exists at several scopes. A repository administrator has different responsibilities from an organization owner, and an enterprise owner governs a broader boundary than either.

The central security principle is **least privilege**: grant the minimum access necessary for the task and review that access periodically.

---

## Unit 2 — What is GitHub administration?

Official unit: <https://learn.microsoft.com/en-us/training/modules/github-introduction-administration/2-what-is-github-administration>

### Team-level administration

Teams are groups of organization members. Teams simplify access management because repository permissions and review responsibilities can be assigned to a group instead of repeatedly to individual users.

Useful team concepts include:

- parent and nested teams;
- team maintainers;
- team visibility;
- repository access assigned to a team;
- Code Owner/team review requests;
- review-request load balancing where supported;
- scheduled review reminders where supported;
- synchronization with an identity-provider group in supported enterprise configurations.

Nested teams can reflect organizational structure, but excessive nesting can make access hard to reason about.

### Organization-level administration

Organization owners can manage areas such as:

- membership and invitations;
- teams;
- outside collaborators;
- repository creation/visibility policies;
- default/base repository permissions;
- security features and policies;
- integrations/apps;
- billing and product access;
- audit and compliance configuration.

A common design recommendation is to avoid creating many organizations without a genuine governance need. Extra organizations create additional policy, application, membership, billing, and discoverability overhead.

### Outside collaborators

An outside collaborator can be granted access to selected organization repositories without becoming a full organization member. This is useful for vendors or temporary contributors who should not receive broad organization membership.

Use the least repository permission necessary and remove access when the engagement ends.

### Enterprise-level administration

An enterprise account can centrally govern multiple organizations. Enterprise administration can include:

- organization membership/governance policy;
- authentication policy and SAML SSO;
- Enterprise Managed Users where configured;
- enterprise-wide security and repository policy;
- audit visibility;
- centralized billing/product allocation;
- enterprise settings shared across organizations;
- GitHub Connect or other GitHub Enterprise integrations where applicable.

---

## Unit 3 — How does GitHub authentication work?

Official unit: <https://learn.microsoft.com/en-us/training/modules/github-introduction-administration/3-how-github-authentication-works>

Authentication answers: **Who are you?**

Authorization answers: **What are you allowed to do?**

Do not confuse the two.

### Web authentication

A user normally signs in to GitHub with their account credentials and, where enabled/required, an additional authentication factor.

### Two-factor authentication (2FA)

2FA adds a second factor beyond the account password. GitHub supports secure approaches such as authenticator apps, security keys/passkeys, GitHub Mobile, and recovery mechanisms according to current account capabilities.

Organizations and enterprises can require 2FA for eligible users. Administrators must understand the impact on members who are not compliant before enforcement.

### Passkeys

Passkeys use WebAuthn/FIDO-based authentication and can provide phishing-resistant sign-in. They can simplify secure authentication by using a trusted device/security key rather than a reusable password.

### Personal access tokens (PATs)

PATs authenticate API/Git operations over HTTPS where token authentication is appropriate.

Prefer **fine-grained PATs** when supported because they can be restricted by:

- resource owner;
- selected repositories;
- specific permissions;
- expiration.

Classic PATs exist for compatibility but can provide broader access and should be scoped carefully.

Never commit PATs to a repository.

### SSH keys

SSH keys authenticate Git operations over SSH. A user's SSH key is associated with the user account and can be protected with a passphrase.

### Deploy keys

A deploy key is an SSH key attached directly to a single repository. It is often used by a server or automation that needs repository-specific access.

Deploy keys are distinct from a user's general SSH key and should be used only when the repository-scoped model is appropriate.

### SAML SSO

Organizations/enterprises can integrate with an identity provider using SAML single sign-on. SAML provides federated authentication and can centralize sign-in policy.

SAML authentication alone should not be confused with automatic user provisioning/deprovisioning; SCIM handles lifecycle provisioning in supported setups.

---

## Unit 4 — How does GitHub organization and permissions work?

Official unit: <https://learn.microsoft.com/en-us/training/modules/github-introduction-administration/4-how-github-organization-permissions-work>

### Repository roles

The standard organization-repository permission levels are:

- **Read** — view and participate without write access;
- **Triage** — manage Issues/PRs without changing repository code/settings;
- **Write** — push/contribute code and perform normal collaboration tasks;
- **Maintain** — manage repository operational settings without the full sensitive/destructive Admin capability;
- **Admin** — full repository administration.

Enterprise organizations can support **custom repository roles** based on an existing base role with additional selected permissions.

### Base permissions

An organization can configure a base/default repository permission for members. More specific team/user grants can then provide additional access to particular repositories.

Keep base permission conservative; do not rely on a permissive default if only a subset of users need write access.

### Teams

Teams provide scalable permission assignment and review ownership. A user can inherit repository access from one or more teams and may also have direct grants.

When troubleshooting access, consider all possible sources:

- organization base permission;
- team membership;
- direct repository access;
- outside-collaborator grant;
- enterprise policy restrictions.

### Fork permissions

Fork behavior depends on repository visibility and organization/enterprise policy.

Private/internal repository forks are not equivalent to independent public forks. Their visibility and access remain constrained by the upstream repository/network and applicable enterprise policy.

### Least privilege and periodic review

Access should be reviewed when:

- roles change;
- a project ends;
- a contractor leaves;
- a team is reorganized;
- an integration is no longer needed.

---

## Unit 5 — Managing enterprise access, permissions, and governance

Official unit: <https://learn.microsoft.com/en-us/training/modules/github-introduction-administration/5-manage-enterprise-access-permissions-governance>

### Organization roles

Important organization-level roles include:

- **Owner** — broad organization administration;
- **Member** — normal organization membership;
- **Moderator** — community interaction/moderation responsibilities where supported;
- **Billing manager** — billing access without broad repository administration;
- **Security manager** — organization-wide security-management capability without making the user an owner;
- **Outside collaborator** — repository-specific access without full membership.

Exact role capabilities can evolve; the exam-level principle is separation of duties.

### Enterprise roles

Important enterprise roles include:

- **Enterprise owner** — enterprise-wide administration and policy;
- **Enterprise member** — member within the enterprise boundary;
- **Billing manager** — enterprise billing access where configured;
- **Guest collaborator** in Enterprise Managed Users environments for restricted collaboration use cases.

### Enterprise Managed Users (EMU)

With EMU, user accounts are provisioned and controlled through the enterprise's identity system rather than independently managed personal identities for enterprise work.

Key concepts:

- enterprise controls identity lifecycle;
- users authenticate according to configured identity-provider requirements;
- SCIM can provision/deprovision users/groups;
- managed users primarily operate within the enterprise context;
- enterprise policy can control repository/org access centrally.

Do not assume EMU is simply "SAML SSO turned on". It is a managed-identity model with different account lifecycle characteristics.

### Governance

Enterprise governance can enforce policies such as:

- organization creation/management constraints;
- repository visibility/creation policies;
- authentication requirements;
- 2FA/SSO policies;
- application access restrictions;
- security settings;
- audit/logging requirements;
- Copilot/product policies;
- billing controls.

Policy should be applied at the highest appropriate scope to reduce inconsistent organization-by-organization configuration.

### Audit and accountability

Administration should preserve clear attribution and reviewable history. Prefer named users, GitHub Apps, Actions identities, and scoped service authentication over shared human credentials.

The interactive adaptation for this unit is a structured `/scenario` decision. Learners with suitable organization/enterprise access may inspect the corresponding settings in the UI, while everyone can complete the same scope/role/least-privilege reasoning without buying Enterprise or changing a real company's policy. No role matrix or governance worksheet is generated.

---

## Unit 6 — Module assessment

Official unit: <https://learn.microsoft.com/en-us/training/modules/github-introduction-administration/6-knowledge-check>

The assessment covers:

- team/org/enterprise scope;
- nested teams and IdP group synchronization;
- owners vs outside collaborators;
- authentication vs authorization;
- 2FA/passkeys;
- PATs/SSH/deploy keys;
- repository roles and base permissions;
- organization and enterprise roles;
- SAML/SCIM/EMU concepts;
- least privilege and governance.

---

## Unit 7 — Summary

Official unit: <https://learn.microsoft.com/en-us/training/modules/github-introduction-administration/7-summary>

After this module you should be able to design a basic GitHub administrative model for a team, organization, or enterprise and choose appropriate identity/access controls.

## Official references

- Microsoft Learn module: <https://learn.microsoft.com/en-us/training/modules/github-introduction-administration/>
- GitHub Docs — Organizations: <https://docs.github.com/en/organizations>
- GitHub Docs — Enterprise administration: <https://docs.github.com/en/enterprise-cloud@latest/admin>
- Repository roles: <https://docs.github.com/en/organizations/managing-user-access-to-your-organizations-repositories/repository-roles-for-an-organization>
- Authentication: <https://docs.github.com/en/authentication>
