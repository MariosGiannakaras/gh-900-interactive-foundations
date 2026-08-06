## Step 5 — Branch and merge using VS Code

Repeat the core branch workflow through a graphical Git interface so you understand both representations of the same Git operations.

1. In VS Code, create a new branch named:

```text
lab/module-01-vscode-feature
```

2. Edit `labs/module-01/vscode-branch.txt` and replace the `TODO:` line with a short note describing what the VS Code Source Control graph shows you about branches.
3. Stage and commit the change **using the VS Code Source Control UI**.
4. Use the branch selector in VS Code to switch back to `lab/module-01-git`.
5. Use VS Code's branch/merge command to merge `lab/module-01-vscode-feature` into the lab branch. When no divergence exists, observe that Git may perform a fast-forward merge.
6. Delete the temporary branch through the VS Code UI.
7. Inspect the Source Control graph and compare this history shape with the earlier `--no-ff` merge.
8. Push `lab/module-01-git`.

The validator advances after the VS Code practice file has been completed and committed on the lab branch.
