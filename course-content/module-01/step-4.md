## Step 4 — Branch and merge from the CLI

Practice isolated development and make the merge topology visible in history.

1. From `lab/module-01-git`, create and switch to:

```text
lab/module-01-feature
```

You can use `git branch` + `git checkout` or `git switch --create`.

2. Run `git branch --list` and confirm the active branch.
3. Add a `## Merge strategies` section to `labs/module-01/version-control-notes.md`.
4. In your own words, distinguish **fast-forward**, **merge commit**, and **squash merge**.
5. Stage and commit the change on `lab/module-01-feature`.
6. Return to `lab/module-01-git`.
7. Merge the feature branch deliberately with a merge commit:

```bash
git merge --no-ff lab/module-01-feature -m "Practice Module 1 merge strategy"
```

8. Inspect the result with `git log --all --graph --oneline --decorate`.
9. Delete the merged feature branch pointer with `git branch --delete lab/module-01-feature`.
10. Push `lab/module-01-git`.

The course validator checks for durable evidence of a merge commit before continuing.
