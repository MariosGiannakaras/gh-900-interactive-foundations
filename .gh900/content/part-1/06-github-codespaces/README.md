# Module 6 — Code with GitHub Codespaces

Official Microsoft Learn module: <https://learn.microsoft.com/en-us/training/modules/code-with-github-codespaces/>

This module maps **1:1 to all 7 official units**.

## Learning objectives

After this module you should be able to:

- describe GitHub Codespaces as a cloud-hosted development environment;
- explain creation, connection, stopping, restarting, rebuilding, and deletion;
- distinguish saved files from committed/pushed Git history;
- understand inactivity timeout and retention concepts;
- explain VM/container/dev-container setup;
- personalize Codespaces with settings, dotfiles, extensions, editor, shell, machine, region, timeout, and retention settings;
- distinguish GitHub.dev from Codespaces;
- use a Codespace/VS Code workflow safely.

---

## Unit 1 — Introduction

Official unit: <https://learn.microsoft.com/en-us/training/modules/code-with-github-codespaces/1-introduction>

GitHub Codespaces provides a development environment hosted in the cloud. Instead of requiring every developer to reproduce a local setup manually, a repository can define a repeatable environment that GitHub provisions on demand.

A Codespace combines repository content, compute resources, storage, a containerized development environment, editor connectivity, and user/repository customization.

---

## Unit 2 — The Codespace lifecycle

Official unit: <https://learn.microsoft.com/en-us/training/modules/code-with-github-codespaces/2-codespace-lifecycle>

### Creation sources

A Codespace can be created from different repository contexts, including:

- a template/new-project starting point;
- a repository branch;
- an open pull request;
- a specific historical commit for investigation.

You can have multiple Codespaces for a repository/branch subject to account limits.

### Provisioning sequence

Conceptually, creating a Codespace involves:

1. allocating a virtual machine and storage;
2. creating/configuring the development container;
3. establishing the editor/client connection;
4. running post-creation setup.

A repository's dev-container definition can standardize tools, extensions, settings, dependencies, and initialization commands.

### Prebuilds

Repository administrators can configure Codespaces prebuilds in supported contexts so much of the environment preparation happens before a developer creates the Codespace, reducing startup time.

### Saving work

Edits are stored in the Codespace's cloud-backed filesystem and normally survive stopping/restarting.

However, **saved in a Codespace is not the same thing as safely stored in GitHub history**.

To preserve work independent of the Codespace lifecycle:

```text
edit → git add → git commit → git push
```

If the Codespace is deleted before work is committed/pushed or otherwise exported, unprotected work can be lost.

### Opening/resuming

An existing active or stopped Codespace can be reopened from GitHub.com, VS Code, supported JetBrains tooling, or GitHub CLI.

### Timeout

A running Codespace stops after an inactivity timeout. The Microsoft Learn module uses a default inactivity concept of around 30 minutes, while settings/policies can affect the effective timeout.

Stopping preserves the environment's storage; running compute is no longer active.

### Internet connectivity

Codespaces requires network access for the interactive connection. Temporary connection loss does not inherently erase current filesystem state, but frequent commits/pushes remain good practice.

### Stop vs delete

**Stop**:

- compute is stopped;
- stored workspace state remains;
- it can be restarted.

**Delete**:

- the Codespace is removed;
- unpushed/unexported work can be lost;
- deletion is appropriate after work is safely pushed or no longer required.

### Rebuild

Rebuilding recreates the development container, typically after dev-container changes or environment problems.

Important persistence model:

- repository/workspace content under the workspace area is intended to persist through normal rebuilds;
- custom modifications made outside persisted workspace locations can be cleared;
- a full rebuild can bypass cached layers.

### Retention

Stopped/inactive Codespaces can be automatically deleted after a retention period. Personal and organization policies can influence retention, subject to GitHub's supported limits.

---

## Unit 3 — Personalize your Codespace

Official unit: <https://learn.microsoft.com/en-us/training/modules/code-with-github-codespaces/3-personalize-codespace>

There are two important scopes of customization:

### Repository-defined environment

A repository can define a **dev container** so collaborators receive a consistent project environment.

A `.devcontainer/devcontainer.json` configuration can define items such as:

- base image/container features;
- tools/runtime versions;
- VS Code extensions;
- forwarded ports;
- post-create commands;
- environment variables and other supported settings.

### User personalization

User-level options include:

- **Settings Sync** — synchronize VS Code preferences, themes, keyboard shortcuts, and supported extension configuration;
- **dotfiles** — a repository containing shell/user configuration scripts/files;
- Codespace display name;
- shell choice/default shell;
- machine type;
- default editor;
- preferred region;
- inactivity timeout;
- retention/automatic deletion settings.

### Extensions and plugins

VS Code Codespaces can use compatible Marketplace extensions. JetBrains-based Codespaces can use supported plugins.

The distinction to remember is:

- **dev container** = project/repository repeatability;
- **Settings Sync/dotfiles/personal settings** = developer personalization.

---

## Unit 4 — Codespaces versus GitHub.dev editor

Official unit: <https://learn.microsoft.com/en-us/training/modules/code-with-github-codespaces/4-codespaces-versus-github-dev-editor>

Both provide a browser-based VS Code-like editing surface, but they are not equivalent.

### GitHub.dev

GitHub.dev is a lightweight web editor for repository content.

Strengths:

- opens very quickly;
- free lightweight editing/navigation;
- supports repository/fork/PR file editing and commits;
- useful for small changes.

Limitations:

- no dedicated compute VM;
- no integrated terminal;
- cannot run/build/debug arbitrary application code like a full development environment;
- only compatible web extensions are available.

### GitHub Codespaces

Codespaces provides:

- a VM and containerized environment;
- terminal access;
- build/run/debug compute;
- broader extension/tool support;
- dev-container configuration;
- persistent cloud workspace storage while retained.

### Moving from GitHub.dev to Codespaces

A lightweight edit can begin in GitHub.dev and continue in a Codespace when terminal/build/debug capability becomes necessary. Commit changes before switching as instructed by the interface/workflow so the branch state is safely available.

### Decision rule

Use **GitHub.dev** for quick browser editing and repository navigation.

Use **Codespaces** when you need a real development environment with compute, terminal, dependencies, execution, tests, or debugging.

---

## Unit 5 — Exercise: Code with Codespaces and Visual Studio Code

Official unit: <https://learn.microsoft.com/en-us/training/modules/code-with-github-codespaces/5-exercise-code-with-codespaces>

The interactive exercise generates only the temporary configuration needed for this unit on `lab/m06-u05`.

The learner:

1. creates/opens a Codespace for the temporary learner branch when the account permits it;
2. verifies repository and branch state from the Codespaces terminal;
3. inspects and customizes `.devcontainer/devcontainer.json` with a meaningful repository-level setting;
4. rebuilds the Codespace, or explicitly identifies the rebuild action when the environment already matches the desired configuration;
5. runs a sample terminal command/test and commits the customization;
6. compares the capability with **github.dev**, identifying what requires Codespaces compute/terminal access;
7. distinguishes **stopping** a Codespace from **deleting** it;
8. posts a unit-scoped `/reflection ...` confirming the observed or guided Codespaces/github.dev/stop-vs-delete behavior;
9. pushes the temporary learner branch.

The course validates durable repository configuration and the unit-scoped reflection. GitHub Actions cannot honestly inspect a learner's private Codespaces lifecycle, so account/quota limitations do not require fabricated telemetry. The official Microsoft Learn exercise link remains visible in this unit.

---

## Unit 6 — Module assessment

Official unit: <https://learn.microsoft.com/en-us/training/modules/code-with-github-codespaces/6-knowledge-check>

Assessment coverage includes:

- lifecycle stages;
- branch/PR/commit/template creation contexts;
- stop vs delete vs rebuild;
- persistence and push safety;
- dev containers;
- prebuilds;
- Settings Sync/dotfiles;
- machine/editor/region/timeouts;
- GitHub.dev vs Codespaces.

---

## Unit 7 — Summary

Official unit: <https://learn.microsoft.com/en-us/training/modules/code-with-github-codespaces/7-summary>

After completing this module you should be able to choose between local development, GitHub.dev, and Codespaces and understand what happens to code and compute throughout the Codespace lifecycle.

## Official references

- Microsoft Learn module: <https://learn.microsoft.com/en-us/training/modules/code-with-github-codespaces/>
- GitHub Docs — Codespaces: <https://docs.github.com/en/codespaces>
- GitHub Docs — dev containers: <https://docs.github.com/en/codespaces/setting-up-your-project-for-codespaces/introduction-to-dev-containers>
- GitHub.dev: <https://docs.github.com/en/codespaces/the-githubdev-web-based-editor>
