# Module 1 assessment — Introduction to Git

Complete this only when the interactive course tells you to. For each question, check **exactly one** answer by changing `[ ]` to `[x]`. Do not change the question or answer text.

## Q1

Which statement best describes the main purpose of a version control system?

- [ ] A. It automatically deploys every file change to production.
- [ ] B. It records project changes over time so versions can be inspected, restored, and developed safely in parallel.
- [ ] C. It replaces project-management tools such as Issues and Projects.

## Q2

Why is Git described as a distributed version control system?

- [ ] A. Every Git command must contact GitHub before it can run.
- [ ] B. Only the default branch is stored locally; all history stays on the server.
- [ ] C. A normal clone contains repository history locally, allowing many version-control operations without a network connection.

## Q3

Which statement correctly distinguishes Git from GitHub?

- [ ] A. GitHub is the version-control algorithm and Git is its website interface.
- [ ] B. Git is a distributed version-control system; GitHub hosts Git repositories and adds collaboration and platform features.
- [ ] C. Git and GitHub are two names for the same executable.

## Q4

What does `git add` primarily do?

- [ ] A. Places selected file content into the staging area for a future commit.
- [ ] B. Creates a remote named `origin`.
- [ ] C. Permanently saves staged work as a commit.

## Q5

In a typical working repository, what does `HEAD` normally identify?

- [ ] A. The oldest commit that still exists in the repository.
- [ ] B. The remote repository used for push and pull.
- [ ] C. The currently checked-out position, normally the current branch.

## Q6

After cloning a repository, what is `origin` normally used for?

- [ ] A. It is the name Git gives to the staging area.
- [ ] B. It is the default remote name pointing back to the repository that was cloned.
- [ ] C. It is the default name for the first commit.

## Q7

You edited a tracked file but have not staged the change. Which command normally shows the difference between your working copy and the staging area?

- [ ] A. `git log --oneline`
- [ ] B. `git diff`
- [ ] C. `git branch --list`

## Q8

You staged a file and want to review exactly what is prepared for the next commit compared with the last commit. Which command is appropriate?

- [ ] A. `git status --remote`
- [ ] B. `git diff HEAD --working-tree`
- [ ] C. `git diff --staged`

## Q9

What is a fast-forward merge?

- [ ] A. The target branch pointer advances to commits already reachable through the source branch because the target has not diverged.
- [ ] B. Every source commit is collapsed into one new commit by definition.
- [ ] C. Git always creates a two-parent merge commit even when histories have not diverged.

## Q10

Why might someone deliberately use `git merge --no-ff <branch>` in a learning exercise?

- [ ] A. To delete every commit made on the feature branch.
- [ ] B. To force a merge commit so the branch convergence remains visible in history.
- [ ] C. To prevent the target branch from receiving the feature changes.

## Q11

You accidentally staged a file but want to keep its working-directory edits. Which command is designed for that situation?

- [ ] A. `git branch --delete <file>`
- [ ] B. `git checkout --hard <file>`
- [ ] C. `git restore --staged <file>`

## Q12

Which collaboration statement is correct?

- [ ] A. `git push` publishes local refs/commits to a remote repository; a pull request is a proposal to review and integrate changes.
- [ ] B. `git pull` publishes your local branch to a remote, while `git push` downloads somebody else's changes.
- [ ] C. A pull request is required before Git can create any local commit.
