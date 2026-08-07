# Module 9 — Contribute to an open-source project on GitHub

Official Microsoft Learn module: <https://learn.microsoft.com/en-us/training/modules/contribute-open-source/>

This module maps **1:1 to all 7 official units**.

## Learning objectives

After this module you should be able to:

- find open-source projects and contribution opportunities;
- inspect licenses, README, CONTRIBUTING, CODE_OF_CONDUCT, Issues, PRs, and community channels before contributing;
- use search, topics, labels such as `good first issue`/`help wanted`, and the `/contribute` surface;
- communicate intent before doing substantial work;
- fork, clone, branch, commit, push, and open a pull request;
- link a PR to an Issue and work with status checks/reviews;
- use draft PRs appropriately;
- respond constructively to maintainer feedback;
- recognize community participation, GitHub Sponsors, reuse, Actions, Marketplace, and the responsibilities of becoming a maintainer.

---

## Unit 1 — Introduction

Official unit: <https://learn.microsoft.com/en-us/training/modules/contribute-open-source/1-introduction>

Open-source software is software whose license permits people to inspect, use, modify, and redistribute it under the terms of that license. GitHub hosts many open-source communities, but a public repository is not automatically open source merely because the source is visible. Licensing matters.

Contributions are broader than code. Documentation, issue triage, design, testing, translations, community support, review, and sponsorship are all valid forms of contribution.

---

## Unit 2 — Identify where you can help

Official unit: <https://learn.microsoft.com/en-us/training/modules/contribute-open-source/2-identify>

### Start with projects you understand

A good first project is often software you already use. Useful contribution opportunities can include:

- a broken link;
- a typo;
- missing/outdated documentation;
- reproducible bug reports;
- tests;
- small fixes;
- beginner-friendly feature work.

### Search and topics

GitHub search and repository topics can help find projects in an area of interest. Once you find a candidate repository, investigate the project's health and contribution expectations rather than immediately changing code.

### Important repository/community files

#### LICENSE

Defines the legal permissions/conditions for using, modifying, and distributing the work. If a repository has no license, normal copyright restrictions remain; do not assume visible source grants open-source rights.

#### README

Usually explains project purpose, basic setup/use, and how to engage with the project/community.

#### CONTRIBUTING

Defines contribution workflow, development setup, testing, conventions, commit/PR expectations, or other maintainer requirements.

#### CODE_OF_CONDUCT

Establishes behavioral expectations and helps make the community safer and more predictable.

### Observe community activity

Inspect:

- Issues;
- Pull Requests;
- Discussions/forums/chat if linked;
- maintainer responsiveness;
- contributor activity.

This helps determine whether the project is actively maintained and how people collaborate.

### Find tasks

Useful discovery mechanisms include:

- repository Issues;
- labels such as `good first issue`, `help wanted`, `beginner-friendly`, or project-specific labels;
- the repository `/contribute` page where available;
- linked Issues/PRs that reveal work already underway.

Before starting, check assignees, linked PRs, and comments to avoid duplicating someone else's work.

### GitHub Sponsors

GitHub Sponsors is another way to contribute by financially supporting eligible maintainers/projects. Sponsorship is community support, not a replacement for following a project's contribution workflow.

---

## Unit 3 — Contribute to an open-source repository

Official unit: <https://learn.microsoft.com/en-us/training/modules/contribute-open-source/3-contribute>

### Communicate intent first

Before substantial work:

- check whether the task is already assigned;
- check linked/open PRs;
- read recent comments;
- comment to state your intent;
- for a new/large feature, open an Issue and seek maintainer alignment before investing heavily.

Maintainers may be volunteers with limited time. Be patient and respectful; repeated pressure for immediate responses is counterproductive.

### Fork model

If you do not have write access to the upstream repository, a normal contribution flow is:

1. **fork** the upstream repository into an account you control;
2. **clone** your fork;
3. optionally add the upstream repository as another remote;
4. create a feature branch;
5. make and test changes;
6. commit;
7. push the branch to your fork;
8. open a PR from the fork/branch into the upstream base branch.

Example commands:

```bash
git clone <fork-url>
cd <repo>
git switch -c docs/fix-example
# edit/test
git add .
git commit -m "Fix documentation example"
git push -u origin docs/fix-example
```

### Pull request contents

A good PR normally provides:

- a focused title;
- explanation of what changed;
- why the change is needed;
- related Issue link/reference;
- testing/verification notes;
- screenshots or other evidence when appropriate;
- any information required by the project's PR template.

### Linking Issues

Reference the Issue number such as `#123`. Supported closing keywords can automatically close a linked Issue when the PR is merged, when appropriate for the repository/base branch.

### Status checks

Projects can require automated checks before merge. If a check fails:

1. open the check details/logs;
2. understand the failure;
3. update the branch;
4. push new commits;
5. ask maintainers for guidance when needed.

The existing PR automatically updates when new commits are pushed to its source branch.

### Draft pull requests

Use a draft PR when work is intentionally incomplete but you want early visibility, discussion, or guidance.

### Review outcomes

Common outcomes include:

- approval;
- requested changes;
- comments/questions;
- closure without merge.

Requested changes are normal collaboration, not a failure. Address feedback or discuss tradeoffs constructively.

---

## Unit 4 — Exercise: Create your first pull request

Official unit: <https://learn.microsoft.com/en-us/training/modules/contribute-open-source/4-exercise-create-pr>

The integrated exercise recreates the open-source contribution model without requiring learners to modify an unrelated third-party project.

The learner will:

1. create/fork a personal copy of the course if they are not already working in one;
2. find the Issue labeled for Module 9;
3. verify nobody else is assigned in the learner's copy;
4. comment their intent;
5. create `lab/module-09-open-source`;
6. make the requested documentation change;
7. commit/push;
8. open a PR with the provided template;
9. link the Issue;
10. observe automated status checks;
11. respond to an automated review comment;
12. update the branch;
13. merge when the course permits.

This preserves the same contribution mechanics—Issue communication, fork/branch/PR/status-check/review lifecycle—inside a safe training repository.

---

## Unit 5 — Next steps

Official unit: <https://learn.microsoft.com/en-us/training/modules/contribute-open-source/5-next-steps>

### Community participation

Frequent contributors can be discovered through Issue/PR discussions, repository insights/contributor information, profiles, organizations, and linked community channels.

Open-source communities can also exist on:

- Discord/Slack/IRC/Gitter;
- forums;
- mailing lists/newsletters;
- podcasts;
- conferences/meetups;
- office hours.

### Reuse and publishing

A useful solution might be shared as:

- a standalone library/package;
- a maintained fork/mirror;
- a GitHub Action;
- an app/integration;
- a Gist or article when a full maintained project is unnecessary.

GitHub Marketplace improves discoverability for reusable Actions/apps.

### Maintainer responsibility

Publishing reusable software creates maintenance expectations. Consider:

- issue triage;
- review workload;
- documentation;
- releases;
- security updates;
- dependency updates;
- user support;
- bus factor and co-maintainers.

Set expectations clearly rather than implicitly promising support you cannot provide.

---

## Unit 6 — Module assessment

Official unit: <https://learn.microsoft.com/en-us/training/modules/contribute-open-source/6-knowledge-check>

Assessment coverage includes:

- licensing/public vs open source;
- contribution/community files;
- search/topics/labels;
- issue communication;
- fork/clone/branch/PR flow;
- status checks;
- draft PRs and review feedback;
- Sponsors and Marketplace;
- maintainer responsibilities.

---

## Unit 7 — Summary

Official unit: <https://learn.microsoft.com/en-us/training/modules/contribute-open-source/7-summary>

After this module you should be able to evaluate a project before contributing and carry a contribution through the full communication and pull-request lifecycle.

## Official references

- Microsoft Learn module: <https://learn.microsoft.com/en-us/training/modules/contribute-open-source/>
- GitHub Docs — Contributing to open source: <https://docs.github.com/en/get-started/exploring-projects-on-github/contributing-to-open-source>
- GitHub Sponsors: <https://docs.github.com/en/sponsors>
- Choose a License: <https://choosealicense.com/>
