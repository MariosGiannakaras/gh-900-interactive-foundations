# Security Policy

## Supported version

Security fixes are maintained on the current `main` branch. Historical course snapshots are not maintained as separate supported release lines.

## What to report

Security reports are appropriate for issues such as:

- a workflow path that could give untrusted code or users unintended write access;
- command/script injection in course automation;
- a way to expose repository or Actions credentials;
- unsafe handling of Pull Request, Issue, or comment input;
- a validator or automation flaw with a meaningful security impact;
- a dependency or workflow-action compromise affecting the maintained source.

Factual course-content errors, broken links, assessment disagreements, and ordinary validation bugs can be reported as normal Issues unless they also create a security risk.

## How to report privately

Do **not** publish exploit details, tokens, credentials, private keys, or other sensitive information in a public Issue.

Use GitHub's private vulnerability-reporting / repository security-advisory flow from the repository **Security** area when it is available. If private reporting is not available, open a minimal public Issue titled **Security contact requested** without exploit details or secrets so a private channel can be arranged.

A useful private report includes:

- the affected workflow, script, or path;
- the security impact;
- minimal reproduction steps;
- any conditions required for exploitation;
- a suggested mitigation, if known.

## Course credentials

The course does not require real secrets to be committed. Never use production credentials, personal access tokens, SSH private keys, cloud keys, passwords, or other live secrets as exercise data.

If a real credential is accidentally committed to a public learner repository, revoke or rotate it immediately. Removing the file in a later commit does not make the exposed credential safe.

## Disclosure

Please allow maintainers a reasonable opportunity to validate and remediate a vulnerability before public disclosure. Security advisories may be used to coordinate a fix and communicate impact when appropriate.
