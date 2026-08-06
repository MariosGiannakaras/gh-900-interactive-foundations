# Module 1 — Introduction to Git

Official Microsoft Learn module: <https://learn.microsoft.com/en-us/training/modules/intro-to-git/>

This module maps **1:1 to all 6 official units**. The explanations below are original wording; the practical layer adds a GitHub-hosted exercise that validates repository state as you work.

## Learning objectives

By the end of this module you should be able to:

- explain what version control is and why it is useful;
- distinguish centralized and distributed version control;
- distinguish Git from GitHub;
- use the core Git vocabulary correctly;
- configure a Git identity and work with a Git repository;
- stage, commit, and inspect changes;
- use branches to isolate experimental work;
- recognize the purpose of the most common basic Git commands.

---

## Unit 1 — Introduction

Official unit: <https://learn.microsoft.com/en-us/training/modules/intro-to-git/0-introduction>

Git is a version-control system used to record changes to files over time. Although it is strongly associated with software development, the same model works for documentation, configuration, data files, and other text-based projects.

The important mental model for this module is that Git lets you create a reliable history of a project, inspect that history, work on changes independently, and combine selected work later.

In the interactive lab you will use this repository itself as the project. You will work on a dedicated branch, make multiple commits, inspect history from a terminal, and let GitHub Actions validate the observable repository state.

---

## Unit 2 — What is version control?

Official unit: <https://learn.microsoft.com/en-us/training/modules/intro-to-git/1-what-is-vc>

### Version control systems

A **version control system (VCS)** tracks changes to a set of files. It gives a project a history instead of leaving you with unrelated copies such as `final`, `final-2`, and `really-final`.

Typical capabilities include:

- identifying what changed;
- identifying who made a change and when;
- attaching an explanation to a saved change;
- restoring an earlier version of one file or the whole project;
- creating isolated lines of development with branches;
- combining selected branch changes later;
- marking significant versions with tags, such as a release.

Version control is one practice within the broader discipline of **software configuration management (SCM)**. The terms are sometimes used loosely as if they were identical, but SCM covers more than version history alone.

### Centralized vs distributed version control

A centralized VCS stores authoritative history primarily on a central server. Examples historically include CVS, Subversion (SVN), and Perforce. Centralization can make the server a critical dependency.

Git is a **distributed version control system (DVCS)**. A normal Git clone contains project history locally, not just the current files. This means you can inspect history and create local commits without a network connection, then synchronize with another repository later.

Hosted services are still extremely useful, but Git itself does not require a permanent central server to record local history.

### Git

Git is a free and open-source distributed VCS created originally by Linus Torvalds. It is designed to be fast and scalable and is now used for projects of many sizes.

### Core terminology

#### Working tree

The project directories and files you are actively editing.

#### Repository

The Git data store that holds history and metadata. In a normal working repository, Git stores this information under the hidden `.git` directory at the root of the working tree.

A **bare repository** has repository data but no checked-out working tree. Bare repositories are commonly useful as shared or backup repositories.

#### Hash

Git identifies content and objects with cryptographic hashes. Historically Git uses SHA-1 object identifiers; modern Git also supports SHA-256 repositories. Because object identity derives from content, Git can determine whether content changed independently of a file's ordinary timestamp.

#### Git objects

The object model is important even at a foundational level:

- **blob** — stores file content;
- **tree** — represents a directory structure and points to names, permissions, and other objects;
- **commit** — represents a saved project state and connects history through parent commits;
- **annotated tag** — an object containing tag metadata that usually points to a commit.

Git also supports **lightweight tags**, which are references rather than full tag objects.

#### Commit

As a verb, **commit** means recording staged work as a new saved point in repository history. As a noun, a **commit** is that recorded history object.

A commit records metadata such as author identity, time, commit message, the project snapshot reference, and parent commit information. It can also contain a digital signature.

#### Branch, head, and HEAD

A **branch** is a named line of commits. Its newest commit is the branch's **head**.

`HEAD` is Git's reference to the currently checked-out position, normally the current branch. On GitHub, new repositories normally use `main` as the default branch unless configured otherwise.

Branches let separate changes proceed without immediately modifying the default branch.

#### Remote and origin

A **remote** is a named reference to another Git repository. After `git clone`, Git normally creates a remote named `origin` that points back to the repository you cloned.

#### Command, subcommand, option

In `git status`, `git` is the command and `status` is the subcommand. Options modify behavior, for example `git reset --hard`.

### Git command line vs graphical tools

Git can be used through graphical interfaces such as GitHub Desktop and through editor integrations such as Visual Studio Code. These tools can simplify routine work, but the Git command-line interface exposes the broadest set of Git capabilities and is consistent across operating systems.

For this reason, this module deliberately uses basic CLI commands even though later course modules also cover GitHub's graphical and web interfaces.

### Git vs GitHub

**Git** is the distributed version-control technology.

**GitHub** is a platform built around Git that hosts repositories and adds collaboration, automation, project-management, AI, and community features.

Examples of GitHub platform features include Issues, Discussions, Pull Requests, Notifications, Labels, Actions, Forks, Projects, Copilot, and Codespaces.

Git can exist without GitHub. GitHub repositories use Git for version history but provide much more than Git alone.

---

## Unit 3 — Exercise: Try out Git

Official unit: <https://learn.microsoft.com/en-us/training/modules/intro-to-git/2-exercise-configure-git>

The official exercise checks version-control concepts, identity configuration, repository creation and commits, history, branches, and basic collaboration. Our exercise preserves those objectives while using this course repository as the managed training environment.

### Interactive lab objectives

You will:

1. create the required training branch;
2. open a GitHub Codespace or use a local clone;
3. inspect and, if necessary, configure your Git identity;
4. inspect repository status;
5. edit the lab file;
6. stage the file;
7. create a commit with a meaningful message;
8. inspect commit history;
9. make a second change and commit so history contains multiple snapshots;
10. push the branch so GitHub Actions can validate the result;
11. complete an original knowledge check covering the same learning objectives.

### Identity configuration

Inspect the identity Git will attach to commits:

```bash
git config user.name
git config user.email
```

If the values are not set for this repository, set them locally:

```bash
git config user.name "Your Name"
git config user.email "your-email@example.com"
```

`--global` stores a value in your user-level Git configuration and therefore affects other repositories for that user. For a disposable training environment, repository-local configuration is sufficient and avoids unintentionally changing unrelated repositories.

### Repository creation vs cloning

A new local Git repository can be created with:

```bash
git init
```

For this course, you are already working with an existing GitHub repository, so you normally **clone** it or open it in Codespaces instead of running `git init` inside it.

A local clone can be created with:

```bash
git clone <repository-url>
```

A clone normally creates the `origin` remote automatically.

### Branch work

The automated course will ask you to create:

```text
lab/module-01-git
```

From a terminal, a typical equivalent is:

```bash
git switch -c lab/module-01-git
```

`git switch` changes the checked-out branch. `-c` creates the named branch first.

---

## Unit 4 — Basic Git commands

Official unit: <https://learn.microsoft.com/en-us/training/modules/intro-to-git/3-basic-git-commands>

A useful model is:

**working tree → staging area → commit history**

You edit in the working tree, select the content intended for the next commit by staging it, then save that staged state as a commit.

### `git status`

```bash
git status
```

Shows the state of the working tree and staging area. It helps distinguish untracked, modified, and staged changes and usually tells you what Git expects next.

### `git add`

```bash
git add <path>
```

Places the current content for the chosen path into the **staging area** (also called the index). Staging does not create a commit. It selects content for a future commit.

The same command is used both for newly tracked files and for later modifications to already tracked files.

### `git commit`

```bash
git commit -m "Describe the change"
```

Creates a new commit from the staged content. A useful commit message explains the intent of the saved change rather than merely restating a filename.

### `git log`

```bash
git log
```

Displays commit history, including information such as commit identifiers, authorship, timestamps, and messages.

For a compact graph view you can also experiment with:

```bash
git log --oneline --graph --decorate
```

### `git help`

```bash
git help
```

Provides Git help. A specific command's manual can be requested with:

```bash
git <subcommand> --help
```

For example:

```bash
git commit --help
```

### Synchronization commands you should recognize

Although the official basic-command unit focuses on status/add/commit/log/help, the surrounding version-control vocabulary expects you to recognize these terms:

- `git push` sends local refs/commits to a remote repository;
- `git pull` integrates changes obtained from a remote tracking branch;
- `git fetch` downloads remote refs/objects without automatically integrating them into your current branch.

Detailed collaboration behavior is covered later in the course.

---

## Unit 5 — Module assessment

Official unit: <https://learn.microsoft.com/en-us/training/modules/intro-to-git/4-knowledge-check>

The repository uses **original questions**, not copied Microsoft Learn assessment items. The assessment checks the same knowledge areas:

- appropriate use cases for version control;
- relationship between VCS and SCM terminology;
- Git vs GitHub;
- basic command purposes;
- distributed version-control behavior;
- working tree, staging area, commit, branch, remote, and `HEAD`.

The interactive workflow will not reveal the answer key before you submit the assessment.

---

## Unit 6 — Summary

Official unit: <https://learn.microsoft.com/en-us/training/modules/intro-to-git/5-summary>

After completing the module, you should be able to explain and demonstrate:

- what a VCS provides;
- why Git is distributed;
- essential Git terminology;
- the distinction between Git and GitHub;
- Git identity configuration;
- the working-tree/staging/commit model;
- `git status`, `git add`, `git commit`, `git log`, and `git help`;
- basic branch-based isolation of work.

### Further official references

- Git documentation: <https://git-scm.com/doc>
- GitHub Git learning resources: <https://docs.github.com/en/get-started/using-git/about-git>
- Microsoft Learn module: <https://learn.microsoft.com/en-us/training/modules/intro-to-git/>

---

## Interactive course flow

When the course workflow is active, the course issue guides you through these validated checkpoints:

1. **Create branch** `lab/module-01-git`.
2. **First snapshot**: edit `labs/module-01/version-control-notes.md`, stage it, commit, and push.
3. **History checkpoint**: make a second meaningful commit to the same file and push it.
4. **Assessment**: complete `labs/module-01/assessment.md` without changing the question text.
5. **Completion**: automatic validation records Module 1 as completed and points to Module 2.

Not every terminal command can be observed remotely by GitHub Actions (for example, simply running `git help`). Those commands remain required hands-on steps, while the validator checks the durable repository evidence that can be verified safely.
