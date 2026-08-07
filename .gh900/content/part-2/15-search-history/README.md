# Module 15 — Search and organize repository history by using GitHub

Official Microsoft Learn module: <https://learn.microsoft.com/en-us/training/modules/search-organize-repository-history-github/>

This module maps **1:1 to all 5 official units**.

## Learning objectives

After this module you should be able to:

- use global and repository-context search appropriately;
- use qualifiers to find relevant Issues and Pull Requests;
- use labels, milestones, assignees, and Projects metadata to organize/filter work;
- use GitHub blame to identify the commit/author history behind lines of a file;
- cross-link Issues, PRs, commits, users, and related work;
- use saved replies and distinguish them from Issue templates/forms;
- reconstruct project context from repository history rather than relying only on current code.

---

## Unit 1 — Introduction

Official unit: <https://learn.microsoft.com/en-us/training/modules/search-organize-repository-history-github/1-introduction>

A repository contains more context than its current files. Issues, Pull Requests, commits, reviews, comments, labels, milestones, assignments, and links form a record of why the code arrived at its current state.

Searching this history is a core GitHub skill, especially when joining an unfamiliar project or debugging a change you did not originally implement.

---

## Unit 2 — How to search and organize repository history by using GitHub

Official unit: <https://learn.microsoft.com/en-us/training/modules/search-organize-repository-history-github/2-search-organize-repository-history-github>

### Global search

GitHub's global search can search across GitHub and different result types. It is useful when you do not yet know exactly which repository or content type contains the information.

The full search syntax supports qualifiers for repositories, users, Issues/PRs, code, and other searchable resources. Some qualifiers apply only to particular result providers.

Example concepts:

```text
repo:OWNER/REPO sidebar
```

or an Issues/PR-oriented query:

```text
repo:OWNER/REPO is:pr sidebar
```

### Context search

Repository tabs such as **Issues** and **Pull requests** provide a scoped search experience. Context search is often preferable when you already know the repository and content type because GitHub can expose relevant filters such as labels, authors, assignees, projects, and milestones.

### Common search qualifiers

Examples from the official module include concepts such as:

```text
is:open is:issue assignee:@me
is:closed is:pr author:USERNAME
is:pr sidebar in:comments
is:open is:issue label:bug -linked:pr
```

Other useful qualifiers include `label:`, `milestone:`, `author:`, `assignee:`, `mentions:`, `in:title`, `in:body`, and repository/organization scope.

Search syntax evolves; learn how qualifiers compose rather than trying to memorize every possible filter.

### Labels

Labels add searchable metadata to Issues and PRs. They can represent:

- type (`bug`, `feature`);
- priority;
- team/component;
- workflow state;
- review readiness;
- custom project semantics.

Example:

```text
is:open is:issue label:bug
```

### Milestones

Milestones group Issues and Pull Requests around a shared goal such as:

- release;
- sprint;
- product phase;
- migration milestone.

A milestone can have a description and due date, and GitHub automatically tracks progress based on open/closed associated work.

Example:

```text
is:open is:pr milestone:"Release v1.0"
```

Milestones complement Projects: a Project can show a broader planning model while a milestone can group repository work around a specific target.

### Assignees

Assignees communicate responsibility for an Issue or PR. Search can use the `assignee:` qualifier to find work assigned to yourself or another user.

```text
is:open is:issue assignee:@me
```

Do not use an assignee merely to mention someone; use `@mention` for participation/attention when they are not the work owner.

### Git blame

`git blame` associates each line of a file with the commit/author that last changed it.

On GitHub, the **Blame** view provides a navigable interface around this history and can help answer:

- when was this line introduced?
- which commit changed it?
- who worked on this area?
- what related PR/Issue might explain the decision?

Blame is a context-discovery tool, not literally a tool for assigning fault.

### Cross-linking

GitHub automatically links many references and lets collaborators build a navigable context graph.

Useful references include:

- Issue/PR in same repository: `#123`;
- cross-repository: `owner/repo#123`;
- commit: sufficiently unique/full SHA;
- user/team: `@username` / `@org/team`;
- supported URLs/autolinks.

PRs are automatically connected to their commits/branches, and Issues can be manually/automatically linked to PRs through supported references/closing keywords.

Cross-links are valuable because future maintainers can follow decisions through history.

### Saved replies

Saved replies are reusable snippets for responses you send repeatedly in Issues/PRs. They improve consistency and reduce repetitive typing.

They are useful for things such as:

- asking for reproduction steps;
- explaining contribution policy;
- requesting logs;
- guiding a contributor to documentation.

### Saved replies vs Issue templates/forms

Use **Issue templates/forms** to collect required information *before* an Issue is submitted.

Use **saved replies** to respond consistently *after* an Issue/PR already exists.

Templates reduce missing information upfront; saved replies reduce repetitive maintainer responses.

---

## Unit 3 — Exercise: Connect the dots in a GitHub repository

Official unit: <https://learn.microsoft.com/en-us/training/modules/search-organize-repository-history-github/3-connect-dots>

The interactive exercise creates a deliberately connected temporary repository history. The course prepares a regression Issue, `sandbox/m15-u03`, and a `fixture/m15-u03` regression branch. The learner then:

1. opens the temporary regression Issue;
2. creates a Pull Request from `fixture/m15-u03` into `sandbox/m15-u03` and links the Issue;
3. inspects the PR's commits and changed files and merges it;
4. uses global/repository search to find the merged PR, regression commit, and Issue;
5. opens **Blame** for `exercise/history-fixture.txt` on the sandbox branch;
6. applies the prepared label and milestone and assigns the Issue to themselves;
7. adds an `@mention`, PR reference, and regression commit SHA to the Issue;
8. submits the connected result directly in the course Issue with `/investigation issue=#N pr=#N commit=<sha> explanation=<what-the-linked-history-tells-you>`;
9. runs `/check` for the final validation.

The validator checks the real Issue/PR/commit/Blame-adjacent metadata and the unit-scoped investigation response. No `history-investigation.md` worksheet is created.

---

## Unit 4 — Module assessment

Official unit: <https://learn.microsoft.com/en-us/training/modules/search-organize-repository-history-github/4-knowledge-check>

Assessment coverage includes:

- global vs context search;
- search qualifiers;
- labels/milestones/assignees;
- `git blame` / GitHub Blame;
- cross-linked Issue/PR/commit references;
- mentions;
- saved replies;
- saved replies vs Issue templates.

---

## Unit 5 — Summary

Official unit: <https://learn.microsoft.com/en-us/training/modules/search-organize-repository-history-github/5-summary>

After completing this module you should be able to reconstruct why a change exists by moving from search → Issue/PR → commit → blame/cross-links instead of treating current source as context-free.

## Official references

- Microsoft Learn module: <https://learn.microsoft.com/en-us/training/modules/search-organize-repository-history-github/>
- GitHub Docs — Search: <https://docs.github.com/en/search-github>
- GitHub Docs — Viewing a file: <https://docs.github.com/en/repositories/working-with-files/using-files/viewing-a-file>
- GitHub Docs — Autolinked references: <https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/managing-repository-settings/configuring-autolinks-to-reference-external-resources>
