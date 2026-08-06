## Step 3 — Inspect history and compare changes

Now practice the history and diff material from the linked official Git exercise.

### Inspect an earlier state

1. Run `git log --oneline` and copy the ID of the first lab commit you created.
2. Run `git checkout <commit-id>` and inspect `labs/module-01/version-control-notes.md` as it existed at that point.
3. Return to the lab branch with `git checkout lab/module-01-git` (or `git switch lab/module-01-git`).
4. Open VS Code's Source Control graph and inspect the same history visually.

### Practice diffs and unstaging

Edit `labs/module-01/diff-practice.txt` so that you:

- change `Current score` to `Current high score`;
- change the numeric value;
- add one new line of your choice;
- remove the line containing `Temporary status line`.

Before committing:

1. Run `git diff labs/module-01/diff-practice.txt` and identify the added/removed lines.
2. Stage the file.
3. Run `git diff labs/module-01/diff-practice.txt` again and observe why it is now empty.
4. Run `git diff --staged labs/module-01/diff-practice.txt`.
5. Deliberately unstage it with `git restore --staged labs/module-01/diff-practice.txt` without losing the working edit.
6. Inspect status, then stage it again.
7. Also inspect the graphical diff in VS Code.
8. Commit the change.
9. Run `git diff HEAD~1` to compare the current commit with its parent.
10. Push the lab branch.

If Git opens long output in a pager, press `q` to exit it.
