# Module 1 — Introduction to Git: hands-on checkpoint

Work on the exact branch `lab/module-01-git`. Complete these tasks in order. The course workflow checks durable repository state after every push and tells you what is still missing.

## 1. CLI staging and commit

1. Open `labs/module-01/version-control-notes.md`.
2. Replace every `TODO:` with your own notes explaining the requested Git concept.
3. Use the Git CLI to inspect status, stage the file, inspect staged state, and commit it with a meaningful message.
4. Record the commit SHA below.

EVIDENCE_CLI_COMMIT: REPLACE_ME

## 2. VS Code Source Control commit

1. Use VS Code's **Source Control** view rather than the terminal for this checkpoint.
2. Make a small meaningful addition to `labs/module-01/version-control-notes.md` (for example, a note about the Source Control UI).
3. Stage and commit the change from the Source Control UI.
4. Inspect the commit/history/diff in VS Code and record the commit SHA.

EVIDENCE_VSCODE_COMMIT: REPLACE_ME

## 3. Diff, staging, and restore/unstage practice

1. Open `labs/module-01/diff-practice.txt`.
2. Remove the line containing `Temporary status line`.
3. Before committing, inspect the unstaged diff with Git.
4. Stage the file, inspect the staged diff, then unstage it with `git restore --staged` (or the equivalent Git operation taught in the module).
5. Stage it again and commit the final intended change.

EVIDENCE_DIFF_COMMIT: REPLACE_ME

## 4. Branch and merge practice

1. From `lab/module-01-git`, create a temporary child branch such as `lab/module-01-merge-practice`.
2. Make a small change and commit it on that child branch.
3. Return to `lab/module-01-git` and merge the child branch using a **merge commit** (`--no-ff` is acceptable) so the merge is visible in history.
4. Inspect the resulting graph/log.

EVIDENCE_MERGE_COMMIT: REPLACE_ME

## 5. VS Code branch exercise

1. Open `labs/module-01/vscode-branch.txt` and complete its `TODO:`.
2. Use a branch/Source Control workflow in VS Code for the edit where practical.
3. Ensure the completed change is present on `lab/module-01-git`.

EVIDENCE_VSCODE_BRANCH_NOTE: REPLACE_ME

## 6. Remote collaboration checkpoint

Push `lab/module-01-git` to GitHub. This demonstrates the local/remote relationship (`origin`, fetch/push, remote-tracking branch) and gives the course engine durable state to validate.

EVIDENCE_REMOTE_NOTE: REPLACE_ME

Set this only after all six checkpoints are genuinely complete:

ACTIVITY_STATUS: INCOMPLETE

> Do not answer `assessment.md` yet. The official assessment unit will unlock later and validate it separately.
