# Module 6 — Code with GitHub Codespaces: Interactive submission

Read `modules/06-github-codespaces/README.md` first. Work on branch `lab/module-06`.

## Hands-on activities

1. Create/open a Codespace for your copied course repository and identify the repository, branch, terminal, forwarded ports, and source-control controls.
2. Stop and restart the Codespace so you understand the lifecycle and the difference between stop and delete.
3. Open `.devcontainer/devcontainer.json`. Replace the `TODO customize` name and make at least one meaningful, valid dev-container customization (for example an editor setting or supported feature). Keep valid JSON.
4. Rebuild or inspect how a rebuild would apply the dev-container configuration, and understand which workspace data is preserved.
5. Open the same repository with `github.dev` and compare what is available there versus a full Codespace.
6. Record how secrets, dotfiles/Settings Sync, machine configuration, timeouts/retention, and prebuilds can affect Codespaces.

ACTIVITY_STATUS: INCOMPLETE
EVIDENCE_CODESPACE_NOTE: REPLACE_ME
EVIDENCE_LIFECYCLE_NOTE: REPLACE_ME
EVIDENCE_DEVCONTAINER_NOTE: REPLACE_ME
EVIDENCE_GITHUB_DEV_COMPARISON: REPLACE_ME

## Knowledge check

### Q1
What is a GitHub Codespace?
- [ ] A. A repository label.
- [ ] B. A cloud-hosted development environment associated with a repository/configuration.
- [ ] C. A replacement for Pull Requests.

### Q2
What generally happens when you stop a Codespace?
- [ ] A. Compute stops while the Codespace can later be resumed, subject to retention policies.
- [ ] B. The repository is permanently deleted.
- [ ] C. Every commit is squashed automatically.

### Q3
What is a dev container configuration used for?
- [ ] A. Setting GitHub billing currency.
- [ ] B. Defining repository visibility.
- [ ] C. Describing a repeatable development environment, tools, features, settings, and related configuration.

### Q4
What is a key difference between `github.dev` and Codespaces?
- [ ] A. `github.dev` always provides a full remote VM and terminal.
- [ ] B. Codespaces provides a full compute-backed development environment, while `github.dev` is a lightweight browser editor without the same compute environment.
- [ ] C. Codespaces cannot edit repository files.

### Q5
Why can prebuilds be useful?
- [ ] A. They can prepare common environment setup ahead of time to reduce Codespace startup/setup time.
- [ ] B. They convert private repos to public.
- [ ] C. They replace branch protection.

### Q6
How should sensitive values be handled in Codespaces?
- [ ] A. Hard-code them into the repository.
- [ ] B. Put them in README screenshots.
- [ ] C. Use supported secret mechanisms and avoid committing credentials to source control.
