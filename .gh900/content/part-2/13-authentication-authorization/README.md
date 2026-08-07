# Module 13 — Authenticate and authorize user identities on GitHub

Official Microsoft Learn module: <https://learn.microsoft.com/en-us/training/modules/authenticate-authorize-user-identities-github/>

This module maps **1:1 to all 7 official units**.

## Learning objectives

After this module you should be able to:

- distinguish identity, authentication, authorization, provisioning, and deprovisioning;
- explain GitHub authentication methods and organizational enforcement;
- explain OAuth Apps vs GitHub Apps at a foundational level;
- understand SAML SSO and its implications for users, PATs, SSH keys, and organization access;
- understand SCIM provisioning/deprovisioning and why SAML alone is not the same as account lifecycle management;
- explain fine-grained authorization, repository/team roles, IP allow lists, and application restrictions;
- explain team synchronization and Enterprise Managed Users.

---

## Unit 1 — Introduction

Official unit: <https://learn.microsoft.com/en-us/training/modules/authenticate-authorize-user-identities-github/1-introduction>

Identity and access management answers several separate questions:

- **Identity** — which user/service is this?
- **Authentication** — how does GitHub verify that identity?
- **Authorization** — what resources/actions can the identity access?
- **Provisioning** — how is access/account membership created?
- **Deprovisioning** — how is it reliably removed when no longer appropriate?

Keeping these concepts separate is important for GH-900 scenario questions.

---

## Unit 2 — User identity and access management

Official unit: <https://learn.microsoft.com/en-us/training/modules/authenticate-authorize-user-identities-github/2-user-identity-access-management>

### Personal identities

Normal GitHub users authenticate through their GitHub account and can belong to organizations/enterprises according to invitations, identity-provider integration, and policy.

### Enterprise identity patterns

An enterprise can choose identity architectures such as:

- personal GitHub accounts linked to enterprise/organization access through SAML SSO;
- **Enterprise Managed Users (EMU)**, where identities are provisioned and controlled by the enterprise identity provider.

### Identity providers

GitHub Enterprise Cloud supports integration with compatible SAML/SCIM identity providers. Common examples include Microsoft Entra ID, Okta, PingOne, OneLogin, AD FS, and other standards-compatible providers.

The durable concept is standards-based federation, not memorizing one vendor list.

### Enterprise Managed Users

EMU is designed for enterprises that need centrally controlled identities.

Core characteristics include:

- user lifecycle controlled by the enterprise/IdP;
- SCIM-based provisioning/deprovisioning in supported configurations;
- enterprise-focused namespaces/access;
- stronger central control over identity and membership;
- restrictions compared with ordinary personal GitHub accounts because managed users are intended for enterprise work.

### GitHub itself as identity system

For many non-enterprise scenarios GitHub remains the identity provider: users sign in to GitHub and organizations authorize their access through membership, teams, roles, and repository permissions.

---

## Unit 3 — User authentication

Official unit: <https://learn.microsoft.com/en-us/training/modules/authenticate-authorize-user-identities-github/3-user-authentication>

### Password and modern authentication

Passwords may be part of web account sign-in, but Git operations/API authentication no longer use an account password as the normal credential. Use supported tokens/SSH/application authentication instead.

### Two-factor authentication

2FA strengthens sign-in by requiring an additional factor. Supported methods can include authenticator apps, security keys/passkeys, GitHub Mobile, and recovery methods according to current GitHub capabilities.

Organizations/enterprises can enforce 2FA. Before enforcement, administrators should understand that noncompliant members can lose organization access according to GitHub's enforcement behavior.

### Passkeys

Passkeys use WebAuthn/FIDO mechanisms and can provide phishing-resistant authentication. They can authenticate with a trusted device/security key rather than relying only on reusable passwords.

### SAML SSO

SAML SSO delegates enterprise/organization authentication to an external identity provider.

Important concepts:

- an organization can require SAML SSO;
- enterprise-level SAML can centralize authentication across enterprise organizations;
- a user's GitHub identity can be linked to an IdP identity;
- organization resources can require an active SSO authorization session;
- credentials such as PATs or SSH keys may need explicit authorization for the SAML-protected organization.

### OAuth Apps vs GitHub Apps

Both can integrate external software with GitHub, but the models differ.

**OAuth App**:

- typically acts on behalf of a user;
- access is based on OAuth scopes/user authorization;
- historically can be broader at user scope.

**GitHub App**:

- purpose-built GitHub integration model;
- installed on selected accounts/repositories;
- uses fine-grained permissions and short-lived installation tokens;
- can act independently as the app or on behalf of a user in supported flows;
- usually preferred for new repository/org automation integrations when its model fits.

Do not use a shared human PAT when a GitHub App or Actions identity provides a safer, auditable integration model.

---

## Unit 4 — User authorization

Official unit: <https://learn.microsoft.com/en-us/training/modules/authenticate-authorize-user-identities-github/4-user-authorization>

### Repository authorization

Access can derive from:

- organization base permissions;
- team permissions;
- direct repository grants;
- organization/enterprise roles;
- outside-collaborator access;
- app/token permission scopes;
- enterprise policy constraints.

The effective result is determined by all applicable grants and restrictions.

### Fine-grained PATs

Fine-grained personal access tokens can be limited by:

- resource owner;
- repository selection;
- individual permission categories;
- expiration.

Organizations can apply policies around token access. Use the smallest useful permission set and a reasonable expiration.

### SAML-authorized credentials

When an organization uses SAML SSO, credentials such as classic PATs or SSH keys may require SSO authorization before they can access organization resources. The exact behavior depends on credential type and current GitHub policy.

### IP allow lists

Organizations/enterprises can use IP allow lists in supported plans to limit access to allowed network addresses. This is an additional access restriction, not a replacement for authentication.

### OAuth/GitHub App policy

Administrators can restrict or approve applications to prevent users from granting unreviewed third-party applications access to organization data.

### Custom repository roles

Enterprise organizations can define custom repository roles by extending a base permission level with selected additional permissions. This supports separation of duties beyond the standard five roles.

---

## Unit 5 — Team synchronization

Official unit: <https://learn.microsoft.com/en-us/training/modules/authenticate-authorize-user-identities-github/5-team-synchronization>

### Team sync

Team synchronization maps identity-provider groups to GitHub teams in supported enterprise setups.

Benefits include:

- automatic onboarding when someone joins an IdP group;
- movement between teams as corporate group membership changes;
- automatic removal when group membership is removed;
- less manual GitHub membership drift.

### SAML vs SCIM vs team sync

These mechanisms solve different problems:

- **SAML SSO** — authenticates/federates identity;
- **SCIM** — provisions and deprovisions user identities/membership through an API standard;
- **Team sync** — maps IdP groups to GitHub team membership.

SAML by itself does not guarantee automatic account deprovisioning when an employee leaves. SCIM is the lifecycle mechanism in supported configurations.

### SCIM

SCIM can automate:

- creating/provisioning users;
- updating identity attributes;
- suspending/deprovisioning access;
- synchronizing group membership according to the provider/integration.

This is important for reliable offboarding.

### EMU and lifecycle management

Enterprise Managed Users relies heavily on enterprise-controlled provisioning and identity policy. Managed user accounts should not be treated like normal personal accounts that the employee independently controls.

The interactive adaptation is the structured `/scenario` checkpoint in this unit. A real corporate IdP is optional: learners with appropriate enterprise access can inspect the corresponding identity/team settings, while everyone must explicitly distinguish the IdP/group, GitHub team, team synchronization, SAML authentication, and SCIM provisioning. No identity worksheet or fake tenant is created.

---

## Unit 6 — Module assessment

Official unit: <https://learn.microsoft.com/en-us/training/modules/authenticate-authorize-user-identities-github/6-knowledge-check>

The integrated assessment covers:

- authentication vs authorization vs provisioning;
- personal account vs EMU identity models;
- 2FA/passkeys;
- SAML SSO;
- PAT/SSH SSO authorization;
- OAuth Apps vs GitHub Apps;
- fine-grained PATs;
- IP allow lists and app restrictions;
- SAML vs SCIM vs team sync;
- deprovisioning scenarios.

---

## Unit 7 — Summary

Official unit: <https://learn.microsoft.com/en-us/training/modules/authenticate-authorize-user-identities-github/7-summary>

After this module you should be able to trace a user from identity creation through authentication, authorization, team assignment, and eventual deprovisioning.

## Official references

- Microsoft Learn module: <https://learn.microsoft.com/en-us/training/modules/authenticate-authorize-user-identities-github/>
- GitHub authentication docs: <https://docs.github.com/en/authentication>
- SAML SSO: <https://docs.github.com/en/enterprise-cloud@latest/organizations/managing-saml-single-sign-on-for-your-organization>
- SCIM: <https://docs.github.com/en/enterprise-cloud@latest/organizations/managing-saml-single-sign-on-for-your-organization/about-scim-for-organizations>
- Enterprise Managed Users: <https://docs.github.com/en/enterprise-cloud@latest/admin/managing-iam/understanding-iam-for-enterprises/about-enterprise-managed-users>
