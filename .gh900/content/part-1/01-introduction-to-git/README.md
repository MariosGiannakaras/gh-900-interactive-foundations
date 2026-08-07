# Module 1 — Introduction to Git

Official Microsoft Learn module: <https://learn.microsoft.com/en-us/training/modules/intro-to-git/>

Official hands-on exercise linked by Microsoft Learn: <https://github.com/skills/introduction-to-git>

This module maps **1:1 to all 6 Microsoft Learn units** and also preserves the concepts and activities taught by the linked official GitHub Skills exercise. The wording here is original; the practical work is adapted to this repository so progress can be validated automatically.

## Learning objectives

By the end of this module you should be able to:

- explain what version control is and the problems it solves;
- distinguish centralized and distributed version control;
- distinguish Git from GitHub;
- use essential Git vocabulary correctly;
- configure Git identity safely;
- initialize or clone a repository;
- work with the working directory, staging area, and repository history;
- stage and commit changes with useful messages;
- inspect history and temporarily view older states;
- compare working, staged, and committed states with diffs;
- create, switch, merge, and delete branches;
- distinguish fast-forward, merge-commit, and squash merge strategies;
- recognize basic collaboration concepts such as clone, push, pull, and pull request.

---

## Unit 1 — Introduction

Official unit: <https://learn.microsoft.com/en-us/training/modules/intro-to-git/0-introduction>

Git is a version-control system used to record changes to files over time. Although most examples involve source code, version control also works for documentation, configuration, tutorials, and other projects whose files benefit from history and collaboration.

The module's core mental model is that Git lets you build a reliable history, inspect or recover earlier states, experiment without immediately disturbing trusted work, compare changes before saving them, and combine selected work later.

The official exercise assumes Git is already installed. If you need Git on your own computer, use the installation guidance at <https://git-scm.com/> rather than relying on a platform-specific shortcut.

The interactive exercise can be completed in a GitHub Codespace or a local clone. Codespaces provides Git and VS Code in a browser, while a local clone lets you use the same Git commands on your own machine.

---

## Unit 2 — What is version control?

Official unit: <https://learn.microsoft.com/en-us/training/modules/intro-to-git/1-what-is-vc>

### What a VCS solves

A **version control system (VCS)** tracks changes to a set of files. It replaces fragile practices such as duplicated folders, emailed copies, manually numbered ZIP files, or a single shared file that becomes locked while somebody else edits it.

The official material highlights problems such as:

- backup and recovery;
- safe/sandboxed experimentation;
- parallel development;
- locked files;
- duplicate copies;
- conflicting changes;
- team collaboration.

With a VCS you can:

- see what changed, when, and by whom;
- attach a message explaining the reason for a change;
- retrieve an earlier version of one file or an entire project;
- use branches for isolated features, fixes, or experiments;
- merge selected branch work later;
- attach tags to important versions, such as releases.

Version control is one practice within **software configuration management (SCM)**. The terms are sometimes used loosely as synonyms, but SCM is broader than version history alone. Git's official documentation is hosted at `git-scm.com`.

### Centralized vs distributed version control

Centralized systems such as CVS, Subversion (SVN), and Perforce traditionally rely on a central server for project history. That architecture can make the server a critical dependency or single point of failure.

Git is a **distributed version control system (DVCS)**. A normal clone contains repository history locally. You can therefore inspect history, compare versions, create commits, and perform many other operations without a network connection. Changes can later be synchronized with another repository. A Git repository can technically be shared by many mechanisms; in modern practice teams normally use a hosted remote service.

Distributed copies also improve resilience and allow developers to choose workflows and tools that suit their work.

### Git

Git is a fast, scalable, free, open-source DVCS originally created by Linus Torvalds, who also created Linux.

### Core terminology

#### Working tree / working directory

The directories and files currently checked out for you to edit.

#### Repository

The Git data store containing project history and metadata. In a normal working repository, Git stores its internal data in the hidden `.git` directory at the top of the working tree.

A **bare repository** contains repository data but no checked-out working tree. Bare repositories are useful for sharing or backup.

#### Staging area / index

A preparation area between your working files and the next commit. Staging allows you to choose exactly which current changes will become part of the next saved snapshot.

#### Hash

Git identifies objects using cryptographic hashes. Git traditionally uses SHA-1 identifiers; modern Git also supports SHA-256 repositories. Because identity comes from content, a timestamp change alone does not imply that Git file content changed.

#### Git objects

A repository contains four fundamental object types:

- **blob** — file content;
- **tree** — directory structure, including names, permissions, and object references;
- **commit** — a saved project state plus history metadata and parent links;
- **annotated tag** — tag metadata that normally points to a commit.

Git also has **lightweight tags**, which are references rather than separate tag objects.

#### Commit

As a verb, committing means recording staged work in history. As a noun, a commit is that recorded history object.

Commit metadata can include the author name/email, timestamp, commit message, optional digital signature, reference to the saved project state, and parent commit or commits.

Good commit messages are concise but descriptive. Generic messages make history harder to understand and make later debugging harder.

#### Branch, head, and `HEAD`

A **branch** is a lightweight named pointer associated with a line of linked commits. The newest commit on a branch is its **head**.

`HEAD` identifies your current position in repository history, normally the currently checked-out branch. GitHub normally uses `main` as the default branch name for new repositories; older repositories and documentation may use the historical name `master`.

A feature branch gives you an isolated place to develop without immediately changing the trusted default branch.

#### Remote and `origin`

A **remote** is a named reference to another Git repository. After `git clone`, Git normally creates a remote called `origin` that points back to the repository you cloned.

#### Commands, subcommands, and options

In `git status`, `git` is the command and `status` is the subcommand. Options change behavior, for example `git merge --no-ff` or `git reset --hard`.

### Ways to use Git

The official exercise demonstrates that Git can be accessed through several categories of tooling:

- **CLI** — the original interface and the route to Git's full command set;
- **code editors/IDEs** — for example VS Code, JetBrains IDEs, Xcode, Emacs, and Vim;
- **Git hosting services** — for example GitHub, GitLab, Gitea, Azure DevOps, AWS CodeCommit, and Bitbucket;
- **desktop Git clients** — for example GitHub Desktop, Sourcetree, TortoiseGit, GitKraken, and GitButler.

Graphical tools are useful, but they differ in features and limitations. The command line remains important because it exposes Git operations consistently across operating systems and helps when a GUI cannot express or recover from a particular state.

### Git vs GitHub

**Git** is the distributed version-control system.

**GitHub** is a platform built around Git that hosts repositories and adds collaboration, automation, project-management, AI, and community capabilities.

GitHub features include Issues, Discussions, Pull Requests, Notifications, Labels, Actions, Forks, Projects, Copilot, and Codespaces.

Git works without GitHub. GitHub uses Git as its version-history foundation but adds much more than Git alone.

---

## Unit 3 — Exercise: Try out Git

Official unit: <https://learn.microsoft.com/en-us/training/modules/intro-to-git/2-exercise-configure-git>

The Microsoft Learn page sends learners to the official GitHub Skills **Introduction to Git** exercise. That exercise is part of our coverage target, not an optional extra.

### A. Verify Git and open help

In the terminal:

```bash
git --version
git --help
```

The first confirms Git is installed. The second opens general help. A subcommand's detailed help is available through `git <subcommand> --help`.

### B. Configure your Git identity

Git stores author identity in commits, and that information is visible to anyone who can view the repository history. GitHub offers a `noreply` email option if you do not want a personal email address exposed in commits.

The official exercise demonstrates global configuration:

```bash
git config --global user.name "Your Name"
git config --global user.email "your-address-or-noreply-address"
git config --global --list
```

Global settings affect repositories for that user. You can instead use repository-local configuration for a particular project:

```bash
git config --local user.name "Your Name"
git config --local user.email "your-address-or-noreply-address"
```

The course recommends local settings so the training exercise does not unintentionally change unrelated repositories.

### C. Create vs clone a repository

To turn an ordinary directory into a new Git repository:

```bash
git init
```

To obtain an existing repository and its history:

```bash
git clone <repository-url>
```

Because this course already exists on GitHub, you normally clone it or open it in Codespaces rather than running `git init` inside the existing repository.

### D. The basic Git workflow

The three core areas are:

```text
Working directory  --git add-->  Staging area/index  --git commit-->  Repository history
```

`git checkout` (and newer commands such as `git switch`/`git restore` for more specific tasks) can change what is checked out into the working tree.

Typical first-repository sequence:

```bash
git init
git status
git add <file-or-path>
git status
git commit -m "Initial commit"
git status
```

Before the first commit, status can report that there are no commits yet. After staging new files, status identifies them as new files. After committing all current work, status can report a **clean working tree**, meaning the checked-out files match the recorded/staged state with no pending changes.

You can stage several explicit files or use a path pattern when appropriate. If you staged something by mistake, remove it from the staging area without discarding the working-file edit using:

```bash
git restore --staged <filename>
```

VS Code's **Source Control** view exposes the same basic states: Changes, Staged Changes, commit messages, commit actions, and history/graph views.

### E. Explore history

Important commit information includes:

- unique commit hash/ID;
- parent commit reference(s);
- author information;
- timestamp;
- commit message.

Useful commands:

```bash
git log
git log --oneline
git log --graph --oneline
git log --all --graph --oneline
```

You can temporarily inspect an older commit:

```bash
git checkout <commit-id>
```

Then return to your branch:

```bash
git checkout <branch-name>
```

Checking out a commit directly places you at that historical position rather than on the normal tip of a branch. For this learning exercise, inspect the state and then return to your branch before continuing work.

VS Code can also display a source-control graph. Expanding a commit shows which files changed in that commit.

### F. Compare changes with diffs

Diff output typically marks added lines with `+` and removed lines with `-` and commonly uses green/red coloring.

The official exercise distinguishes three comparisons:

```bash
git diff                 # working directory vs staging area
git diff --staged        # staging area vs last commit
git diff HEAD~1          # current commit vs its previous commit
```

A path can be supplied to narrow the comparison.

After you stage a working-file change, plain `git diff` can become empty because the working version now matches the staging area; `git diff --staged` then shows what is prepared for the next commit.

Git diff colors can be configured. The official exercise gives examples such as:

```bash
git config --global color.diff.old yellow
git config --global color.diff.new blue
```

VS Code provides a graphical diff view for both unstaged and staged changes. The working-file side can be edited; a staged snapshot represents what is currently prepared for commit.

If Git opens long output in a pager, `q` exits the pager.

### G. Work with branches

Branches are lightweight pointers that support safe parallel work.

Common branch commands demonstrated in the official exercise include:

```bash
git branch <new-branch>
git checkout <branch>
git branch --list
git merge <branch>
git branch --delete <branch>
```

Git 2.23 introduced `git switch` as a clearer command for switching and creating branches:

```bash
git switch --create <new-branch>
git switch <branch>
```

A branch can be renamed if necessary:

```bash
git branch --move old-name new-name
```

Deleting a merged branch name removes the pointer used to reference that branch; it does not magically erase commits that remain reachable through merged history.

### H. Merge strategies you must distinguish

#### Fast-forward

If the target branch has not diverged, Git can simply advance its branch pointer to the newer commit. No separate merge commit is required.

#### Merge commit

Git can preserve the two-parent relationship by creating a new merge commit. The official exercise deliberately demonstrates a non-fast-forward merge:

```bash
git merge --no-ff <feature-branch> -m "Merge message"
```

This makes the branch structure visible in history.

#### Squash merge

A squash takes the net changes from a branch and records them as one new commit on the target branch rather than preserving each branch commit as part of the target branch's history.

These strategies trade off history shape, traceability, and compactness. Later GitHub modules revisit merging in pull-request workflows.

### I. Collaboration concepts

A common collaboration sequence is:

1. **clone** a repository to obtain a local copy and history;
2. create branches and make commits locally;
3. **push** commits/branches to a remote repository others can access;
4. obtain and integrate shared work from a remote, commonly using **pull**;
5. use a **pull request** to propose that another repository/branch review and integrate your work.

Git is distributed, so collaboration means synchronizing work between repository copies. Git hosting platforms make that synchronization and review much easier.

The course turns this official exercise into a temporary `lab/m01-u03` workspace. Durable repository evidence—changed fixtures, multiple commits, and a visible merge commit—is validated automatically. Display-only actions such as opening `git help` or reading `git log` remain explicit required steps because repository automation cannot honestly prove private terminal viewing without intrusive telemetry.

---

## Unit 4 — Basic Git commands

Official unit: <https://learn.microsoft.com/en-us/training/modules/intro-to-git/3-basic-git-commands>

The Microsoft unit specifically emphasizes these commands:

### `git status`

```bash
git status
```

Shows the state of the working tree and staging area, including untracked, modified, and staged content.

### `git add`

```bash
git add <path>
```

Places the selected current content into the staging area. It is used both for newly tracked files and later modifications.

### `git commit`

```bash
git commit -m "Describe the change"
```

Creates a new commit from staged content. A commit includes the saved project state plus metadata such as author, email, timestamp, message, optional signature, and parent reference(s).

### `git log`

```bash
git log
```

Displays previous commits and their metadata. Useful variants include `--oneline`, `--graph`, `--all`, and `--decorate`.

### `git help`

```bash
git help
git <subcommand> --help
```

Provides general or command-specific documentation.

### Other commands explicitly exercised by the linked official lab

You must also recognize and use:

- `git --version`
- `git config`
- `git init`
- `git clone`
- `git checkout`
- `git diff`
- `git restore --staged`
- `git branch`
- `git switch`
- `git merge`
- `git push`
- `git pull`

---

## Unit 5 — Module assessment

Official unit: <https://learn.microsoft.com/en-us/training/modules/intro-to-git/4-knowledge-check>

This repository uses **original questions**, not copied Microsoft Learn assessment items. The assessment covers the same measured knowledge plus the concepts that appear in the linked official hands-on exercise:

- version-control use cases and SCM terminology;
- distributed vs centralized version control;
- Git vs GitHub;
- working directory, staging area, repository, commit, branch, remote, and `HEAD`;
- command purposes;
- diff states;
- branch/merge concepts;
- clone/push/pull/pull-request collaboration vocabulary.

The answer key is not displayed before submission.

---

## Unit 6 — Summary

Official unit: <https://learn.microsoft.com/en-us/training/modules/intro-to-git/5-summary>

After completion you should be able to explain and demonstrate:

- the purpose and benefits of version control;
- why Git is distributed;
- Git terminology and object/history concepts;
- the difference between Git and GitHub;
- Git identity configuration and privacy considerations;
- repository creation vs cloning;
- working-directory → staging → commit workflow;
- status, add, commit, log, help, checkout, diff, branch, switch, merge, push, and pull basics;
- history inspection and temporary historical checkout;
- unstaged vs staged diffs;
- safe branch experimentation;
- fast-forward, merge-commit, and squash concepts;
- basic remote collaboration.

### Official/primary references

- Microsoft Learn module: <https://learn.microsoft.com/en-us/training/modules/intro-to-git/>
- Official linked GitHub exercise: <https://github.com/skills/introduction-to-git>
- Git documentation: <https://git-scm.com/doc>
- GitHub Git documentation: <https://docs.github.com/en/get-started/using-git/about-git>
