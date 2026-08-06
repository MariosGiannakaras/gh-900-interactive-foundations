## Step 2 — Configure Git and create repository history

Complete the practical material from **Unit 3** and **Unit 4**.

### CLI setup

1. Open the terminal in your Codespace/local clone.
2. Run `git --version` and `git --help`.
3. Inspect `git config user.name` and `git config user.email`.
4. If needed, configure repository-local identity with `git config --local ...`. Use a GitHub noreply address if you prefer not to expose a personal email in commit history.
5. In a disposable directory outside this repository, run `git init`, inspect `git status`, then remove the disposable directory when finished. This demonstrates initializing a new repository without nesting one inside the course repo.

### First commit — CLI

1. Back on `lab/module-01-git`, run `git status`.
2. Edit `labs/module-01/version-control-notes.md` and replace the TODOs under **Why version control matters** and **Git vs GitHub** in your own words. Leave **Commands I used** for the next commit.
3. Run `git status` again.
4. Stage the file with `git add labs/module-01/version-control-notes.md`.
5. Inspect `git status` and observe that the change is staged.
6. Commit with a meaningful message.

### Second commit — VS Code Source Control

1. Open the **Source Control** view in VS Code.
2. Finish the **Commands I used** section in `labs/module-01/version-control-notes.md`.
3. Observe the file under **Changes**.
4. Stage it using the Source Control UI.
5. Commit it from the UI with a meaningful message.
6. Open the Source Control graph/history view and inspect both commits.
7. Also run `git log`, `git log --oneline`, and `git log --graph --oneline` in the terminal.
8. Push `lab/module-01-git`.

The workflow requires the notes file to contain no `TODO:` markers and at least two commits on the lab branch before advancing.
