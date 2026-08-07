# Module 12 — Introduction to GitHub administration: Interactive submission

Read `modules/12-github-administration/README.md` first. Work on branch `lab/module-12`.

## Administration simulation

Create `labs/module-12/admin-matrix.md` and complete a table for these scopes: repository, organization, enterprise. For each scope include typical roles, what they can administer, and one least-privilege example.

Then complete scenarios for:
- personal accounts vs organization-owned resources;
- repository roles and organization roles;
- enterprise owners and governance;
- authentication choices and SSO concepts;
- Enterprise Managed Users (EMU) versus ordinary personal GitHub accounts;
- policy inheritance/central governance.

Inspect your own repository/organization settings in read-only mode where available; do not create an Enterprise account solely for this exercise.

ACTIVITY_STATUS: INCOMPLETE
EVIDENCE_ADMIN_MATRIX: REPLACE_ME
EVIDENCE_ROLE_NOTE: REPLACE_ME
EVIDENCE_EMU_NOTE: REPLACE_ME
EVIDENCE_GOVERNANCE_NOTE: REPLACE_ME

## Knowledge check

### Q1
What is a central goal of GitHub administration?
- [ ] A. Replacing Git commits with billing records.
- [ ] B. Managing identities, access, policies, organizations/repositories, security, and governance at the appropriate scope.
- [ ] C. Preventing all collaboration.

### Q2
Why are GitHub organizations useful?
- [ ] A. They remove repository permissions.
- [ ] B. They are required for every personal repository.
- [ ] C. They provide shared ownership, teams, roles, policies, and administration for collaborative resources.

### Q3
What is the best general rule when assigning repository or organization roles?
- [ ] A. Use the least-privileged role that still permits the required work.
- [ ] B. Make every member an owner.
- [ ] C. Share an owner credential.

### Q4
What is an enterprise account used for?
- [ ] A. Editing local Git config only.
- [ ] B. Central governance across organizations and enterprise-level policies/features.
- [ ] C. Replacing branches with folders.

### Q5
What distinguishes Enterprise Managed Users (EMU) conceptually?
- [ ] A. EMU accounts are ordinary unmanaged personal accounts with no enterprise control.
- [ ] B. EMU only changes Markdown rendering.
- [ ] C. User identities and lifecycle are controlled through the enterprise's identity-management model rather than ordinary self-managed personal accounts.

### Q6
Why should administrators understand scope inheritance and policy precedence?
- [ ] A. Settings at enterprise/organization/repository scopes can constrain or shape lower-level behavior and access.
- [ ] B. Git ignores all organization settings.
- [ ] C. Scope only affects repository names.
