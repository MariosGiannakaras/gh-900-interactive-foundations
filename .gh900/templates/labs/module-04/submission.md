# Module 4 — Configure code scanning: Interactive submission

Read `modules/04-code-scanning/README.md` first. Work on branch `lab/module-04`.

## Hands-on activities

1. Inspect the repository Security tab and the code-scanning area available to your copied course repository.
2. Review how default setup differs from advanced workflow configuration.
3. Review a CodeQL workflow and identify initialization, build/autobuild, and analysis stages.
4. Review how third-party SARIF-producing tools can upload results to GitHub code scanning.
5. Complete every `TODO` in `labs/module-04/code-scanning-simulation.yml`. The file is deliberately outside `.github/workflows`, so the configuration exercise cannot execute arbitrary workflow code.
6. If code scanning is available in your repository, enable/configure it and inspect a result. If it is unavailable, the completed simulation artifact is the durable hands-on equivalent; record why the live setup was unavailable.

ACTIVITY_STATUS: INCOMPLETE
EVIDENCE_SECURITY_TAB: REPLACE_ME
EVIDENCE_SETUP_MODE: REPLACE_ME
EVIDENCE_CODEQL_STAGE_NOTE: REPLACE_ME
EVIDENCE_SARIF_NOTE: REPLACE_ME
EVIDENCE_SIMULATION_FILE: REPLACE_ME

## Knowledge check

### Q1
What is the purpose of GitHub code scanning?
- [ ] A. To replace source control.
- [ ] B. To find security vulnerabilities and coding errors by analyzing repository code.
- [ ] C. To calculate GitHub billing totals.

### Q2
What is CodeQL in the context of GitHub code scanning?
- [ ] A. A semantic code-analysis engine/query technology used to identify security and quality problems.
- [ ] B. A repository visibility level.
- [ ] C. A Git merge strategy.

### Q3
How can a supported third-party scanner integrate with GitHub code scanning?
- [ ] A. By rewriting Git commit IDs.
- [ ] B. By disabling the Security tab.
- [ ] C. By producing/uploading compatible analysis results such as SARIF.

### Q4
Why would you use an advanced code-scanning workflow instead of default setup?
- [ ] A. To remove all scanning configuration choices.
- [ ] B. To customize languages, build steps, queries, triggers, or other workflow behavior.
- [ ] C. To make a private repository public automatically.

### Q5
Where are code-scanning alerts normally reviewed?
- [ ] A. In the repository security/code-scanning experience and related pull-request annotations when applicable.
- [ ] B. Only in local `.git/config`.
- [ ] C. Only in GitHub Desktop settings.

### Q6
What is the best response when a training account does not expose a paid/enterprise scanning option?
- [ ] A. Skip the concept entirely.
- [ ] B. Buy an unrelated subscription.
- [ ] C. Use the supported public/free path when available or complete a faithful configuration simulation and learn the decision model.
