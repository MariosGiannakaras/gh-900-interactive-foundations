# Module 13 — Authenticate and authorize user identities: Interactive submission

Read `modules/13-authentication-authorization/README.md` first. Work on branch `lab/module-13`.

## Identity and access simulation

Create `labs/module-13/identity-scenarios.md` and solve these scenarios in your own words:

1. A human signs in to GitHub securely: compare password + 2FA, passkeys, and recovery considerations.
2. A command-line user needs repository access: compare HTTPS credentials/tokens and SSH authentication.
3. An application needs API access: distinguish OAuth apps, GitHub Apps, and personal access tokens at a foundational level.
4. An enterprise wants centralized authentication: explain SAML SSO.
5. An enterprise wants automated user provisioning/deprovisioning: explain SCIM.
6. An organization wants IdP groups reflected as GitHub teams: explain team synchronization.
7. Explain authentication (who are you?) versus authorization (what may you do?).

ACTIVITY_STATUS: INCOMPLETE
EVIDENCE_SCENARIO_FILE: REPLACE_ME
EVIDENCE_2FA_PASSKEY_NOTE: REPLACE_ME
EVIDENCE_SAML_SCIM_NOTE: REPLACE_ME
EVIDENCE_TEAM_SYNC_NOTE: REPLACE_ME

## Knowledge check

### Q1
What is the difference between authentication and authorization?
- [ ] A. Authentication chooses a Git branch; authorization creates commits.
- [ ] B. They are identical terms.
- [ ] C. Authentication verifies identity; authorization determines permitted actions/resources.

### Q2
What is the purpose of two-factor authentication?
- [ ] A. It gives every user administrator access.
- [ ] B. It adds another authentication factor so a password alone is not sufficient.
- [ ] C. It replaces repository permissions.

### Q3
What is SAML SSO primarily used for in enterprise GitHub access?
- [ ] A. Federated authentication through an organization's identity provider.
- [ ] B. Dependency updates.
- [ ] C. Git merge conflict resolution.

### Q4
What is SCIM used for?
- [ ] A. Formatting Markdown.
- [ ] B. Encrypting Git objects.
- [ ] C. Automating identity provisioning and deprovisioning between an identity system and supported services.

### Q5
What does team synchronization help accomplish?
- [ ] A. It replaces GitHub organizations.
- [ ] B. It maps/synchronizes identity-provider groups with GitHub teams so membership can follow central identity management.
- [ ] C. It automatically merges all Pull Requests.

### Q6
What is a strong general access-control practice?
- [ ] A. Use secure authentication and grant the minimum authorization needed, reviewing access over time.
- [ ] B. Share one token across the organization.
- [ ] C. Disable account recovery and auditability.
