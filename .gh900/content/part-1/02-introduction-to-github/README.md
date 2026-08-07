# Module 2 — Introduction to GitHub

Official Microsoft Learn module: <https://learn.microsoft.com/en-us/training/modules/introduction-to-github/>

This module maps **1:1 to all 8 official units** and preserves the official exercise objectives while adding repo-native practice.

## Learning objectives

By the end of this module you should be able to:

- identify the fundamental features of GitHub;
- manage repositories and understand repository visibility;
- explain and use branches, commits, pull requests, and GitHub Flow;
- distinguish GitHub Flow from Git flow;
- use Issues and Discussions appropriately;
- manage notifications, subscriptions, and mentions;
- recognize Gists, Wikis, Pages, feature previews, and repository-level collaboration features;
- complete the guided GitHub workflow of branch → commit → pull request → review/merge.

---

## Unit 1 — Introduction

Official unit: <https://learn.microsoft.com/en-us/training/modules/introduction-to-github/1-introduction>

GitHub is a cloud platform built around Git. Git provides distributed version control; GitHub adds hosted repositories, web and command-line interfaces, collaboration, automation, security, AI-assisted development, project management, and community features.

This module focuses on the GitHub platform rather than on Git internals.

---

## Unit 2 — What is GitHub?

Official unit: <https://learn.microsoft.com/en-us/training/modules/introduction-to-github/2-what-is-github>

### GitHub Enterprise platform pillars

Microsoft Learn frames the GitHub platform around five broad capabilities:

- **AI** — Copilot, Copilot Chat/agents, AI-assisted collaboration, and AI-enhanced security feedback;
- **Collaboration** — repositories, issues, pull requests, reviews, discussions, and shared workflows;
- **Productivity** — automation and CI/CD with GitHub Actions and integrated developer tooling;
- **Security** — CodeQL, secret scanning, Dependabot, security overview, and security controls integrated into development;
- **Scale** — a large developer ecosystem and extensible platform supporting individuals through enterprises.

### Repositories

A repository contains project files plus their revision history and related GitHub collaboration metadata. Repositories can belong to a personal account or an organization.

When creating a repository you normally choose:

- an owner;
- repository name;
- optional description;
- visibility;
- optional initialization files such as README, `.gitignore`, and license.

Visibility basics:

- **Public** — content is visible on the internet;
- **Private** — access is limited to explicitly authorized users and applicable organization members;
- Enterprise environments can also expose additional visibility options such as internal repositories where applicable.

### Cloning

Cloning creates a local Git copy including repository history. GitHub exposes HTTPS, SSH, and GitHub CLI clone options. A normal CLI clone is:

```bash
git clone <repository-url>
```

The resulting clone normally configures the GitHub repository as the remote named `origin`.

### Adding files on GitHub.com

With sufficient repository permissions, files can be created or uploaded from the web interface. A web edit is still a Git change: GitHub asks for a commit message and can commit directly to the current branch or create a new branch and propose the change through a pull request.

For shared/default branches, creating a branch and pull request is usually safer than committing directly.

### Gists

A Gist is a lightweight Git-backed way to share snippets, notes, scripts, examples, or small collections of files.

Important properties:

- public Gists are discoverable;
- secret Gists are unlisted but **not private** — anyone with the URL can access them;
- Gists have revision history;
- they can be cloned and forked;
- Markdown is supported;
- Gists can be embedded in other pages.

Never treat a secret Gist as a secure place for passwords, API keys, tokens, or confidential data.

### Wikis

Repository wikis provide long-form documentation beyond the quick orientation usually placed in a README. A wiki has its own Git-backed history. Private repository wiki visibility follows repository access.

Typical uses include:

- design documentation;
- user guides;
- architecture notes;
- project principles;
- extended documentation that would make the main README unwieldy.

### GitHub Pages

GitHub Pages hosts static websites sourced from a GitHub repository. Typical sources include a branch root or a `/docs` directory, with optional build workflows. Pages is commonly used for project sites, documentation, portfolios, and organization/user sites.

### Feature previews

GitHub may expose experimental or preview functionality through feature-preview controls. Preview features can change and should not be treated as stable platform contracts.

---

## Unit 3 — Components of the GitHub flow

Official unit: <https://learn.microsoft.com/en-us/training/modules/introduction-to-github/3-components-of-github-flow>

### Branches

A branch provides an isolated line of work. Creating feature or fix branches allows changes to progress without immediately affecting the default branch.

### Commits

A commit records one or more staged changes and provides an auditable point in history. GitHub tracks commit identifiers, timestamps, authors/contributors, and commit messages.

File states you should recognize:

- **untracked** — Git is not yet tracking the file;
- **tracked/unmodified** — tracked and unchanged since the relevant commit;
- **modified** — changed in the working tree;
- **staged** — selected for the next commit;
- **committed** — stored in repository history.

### Pull requests

A pull request (PR) proposes merging the commits from a compare/head branch into a base branch. PRs provide a collaboration surface for:

- reviewing changed files;
- comments and threaded discussion;
- requested changes and approvals;
- automated checks;
- linked issues;
- merge readiness.

A **draft pull request** communicates that work is visible but not yet ready for formal review/merge.

### GitHub Flow

GitHub Flow is a lightweight branch-based workflow:

1. create a branch;
2. make changes and commits;
3. open a pull request;
4. discuss/review and update the branch;
5. pass required checks/approvals;
6. merge to the base/default branch;
7. delete the completed branch when appropriate.

It works particularly well with continuous integration and continuous delivery.

### Git flow

Git flow is a more structured branching strategy used by some release-driven projects. Common branch roles include:

- `master`/production branch;
- `develop` for integration work;
- `feature/*`;
- `release/*`;
- `hotfix/*`.

It can be useful for scheduled releases, multiple maintained versions, or slower regulated release cycles, but it is more heavyweight than GitHub Flow. Traditional Git flow also relies on merge structure, so aggressive rebasing/squashing can undermine the historical model it expects.

Do not confuse **Git flow** (the branching model) with **GitHub Flow** (the simpler GitHub-oriented workflow).

---

## Unit 4 — GitHub is a collaborative platform

Official unit: <https://learn.microsoft.com/en-us/training/modules/introduction-to-github/4-collaborative-platform>

### Issues

Issues can track:

- bugs;
- tasks;
- ideas;
- feature requests;
- feedback;
- follow-up work.

Issues can originate from the Issues tab, task lists, project notes/items, comments, selected code lines, and other GitHub surfaces.

Issue collaboration features include:

- assignees;
- labels;
- milestones;
- projects;
- mentions;
- reactions;
- links to commits and PRs;
- issue templates and structured issue forms.

Templates/forms improve consistency by prompting contributors for the information maintainers need.

### Discussions

Discussions are better suited to conversations that are not yet concrete tracked work, such as:

- Q&A;
- announcements;
- general community conversation;
- ideas;
- polls;
- show-and-tell.

A repository owner or user with appropriate access can enable Discussions. Discussions inherit repository visibility.

Common default categories include Announcements, General, Ideas, Polls, Q&A, and Show and tell. Maintainers can customize categories.

Useful capabilities include:

- marking a reply as the answer in Q&A discussions;
- pinning important discussions;
- referencing or converting a discussion into a new issue when conversation turns into actionable work.

### Choosing Issues vs Discussions

Use an **Issue** when work needs to be tracked and closed.

Use a **Discussion** when the primary goal is an open conversation, question, announcement, or idea exploration.

---

## Unit 5 — GitHub platform management

Official unit: <https://learn.microsoft.com/en-us/training/modules/introduction-to-github/5-platform-management>

### Notifications and subscriptions

GitHub notifications help you follow relevant activity without watching everything.

You may receive or configure notifications for:

- issues;
- pull requests;
- Gists;
- releases;
- discussions;
- GitHub Actions workflow activity;
- repository activity generally.

You can become subscribed automatically by participating, being assigned, opening an item, or being mentioned, and you can manually subscribe/unsubscribe.

Repository watch levels include concepts such as:

- **Watching** — broadly notify about activity;
- **Not watching** — usually notify only for participation/mentions;
- **Ignore** — suppress repository notifications;
- **Custom** — choose specific event categories.

Notification delivery can be configured for web, email, and mobile where supported.

### Mentions and search

`@username` mentions bring users into a conversation. Search qualifiers can locate related work, for example:

```text
mentions:<username>
```

### Pages

GitHub Pages is a static-hosting capability using files stored in a GitHub repository. Static HTML/CSS/JavaScript can be published directly or generated through a build process.

---

## Unit 6 — Exercise: A guided tour of GitHub

Official unit: <https://learn.microsoft.com/en-us/training/modules/introduction-to-github/6-guided-tour-of-github>

The official exercise validates the core GitHub workflow. Our integrated lab reproduces the same durable GitHub actions in this repository.

You will:

1. create the module branch `lab/module-02-github`;
2. create/edit the module lab file;
3. commit the change;
4. create an Issue used to track the exercise;
5. open a pull request from the module branch;
6. link the PR and Issue;
7. inspect the Files changed and Conversation tabs;
8. merge the PR when the automated course instructs you;
9. observe the linked Issue/PR state and branch history.

The course engine validates the branch, commits, Issue/PR metadata, and completion marker where GitHub exposes the state safely to Actions.

---

## Unit 7 — Module assessment

Official unit: <https://learn.microsoft.com/en-us/training/modules/introduction-to-github/7-knowledge-check>

The repository uses original GH-900-style questions covering:

- Git vs GitHub;
- repositories and visibility;
- Gists, Wikis, and Pages;
- GitHub Flow vs Git flow;
- file states;
- issues vs discussions;
- notifications/subscriptions;
- pull requests and draft pull requests.

Answers are validated without exposing the answer key before submission.

---

## Unit 8 — Summary

Official unit: <https://learn.microsoft.com/en-us/training/modules/introduction-to-github/8-summary>

After completing the module you should be able to explain and demonstrate the basic GitHub collaboration lifecycle and choose the correct GitHub feature for common collaboration scenarios.

## Official references

- Microsoft Learn module: <https://learn.microsoft.com/en-us/training/modules/introduction-to-github/>
- GitHub Docs — Get started: <https://docs.github.com/en/get-started>
- GitHub Docs — Issues: <https://docs.github.com/en/issues>
- GitHub Docs — Pull requests: <https://docs.github.com/en/pull-requests>
- GitHub Docs — Discussions: <https://docs.github.com/en/discussions>
- GitHub Docs — Notifications: <https://docs.github.com/en/account-and-profile/managing-subscriptions-and-notifications-on-github>
