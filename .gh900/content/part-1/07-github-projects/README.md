# Module 7 — Manage your work with GitHub Projects

Official Microsoft Learn module: <https://learn.microsoft.com/en-us/training/modules/manage-work-github-projects/>

This module maps **1:1 to all 8 official units**.

## Learning objectives

After this module you should be able to:

- distinguish current GitHub Projects from Projects (Classic);
- create and configure an organization-owned Project;
- add issues, pull requests, and draft items;
- use table, board, and roadmap/timeline-style views where supported;
- use filters, sorting, grouping, custom fields, and saved views;
- understand iteration fields and planning cycles;
- understand visibility/access and project metadata;
- use built-in workflows/automation and recognize GraphQL/Actions/webhook integration possibilities;
- use insights/charts to analyze project work.

---

## Unit 1 — Introduction

Official unit: <https://learn.microsoft.com/en-us/training/modules/manage-work-github-projects/1-introduction>

GitHub Projects is a flexible planning and tracking system integrated with Issues and Pull Requests. A Project can represent a backlog, roadmap, sprint/cycle board, team plan, cross-repository program, or other work-management view.

Projects are not Git repositories. They reference work items and add planning metadata/views around them.

---

## Unit 2 — Projects versus Projects Classic

Official unit: <https://learn.microsoft.com/en-us/training/modules/manage-work-github-projects/2-project-vs-project-classic>

The current Projects system is substantially more flexible than Projects (Classic).

### Current Projects

Key capabilities include:

- table and board views;
- roadmap/timeline-style planning views where available;
- custom fields;
- sorting, ranking, filtering, and grouping;
- draft issues/items;
- saved views;
- linked PR/reviewer context;
- iteration fields for sprint/cycle planning;
- charts/insights;
- GraphQL API support;
- GitHub Actions/integration automation;
- webhook/project-item events.

### Projects (Classic)

Projects (Classic) used a board/list/card model with more limited metadata and automation. It is legacy compared with the current Projects experience.

For GH-900, know that current Projects is field/view/data driven rather than only columns-and-cards.

---

## Unit 3 — How to create a project

Official unit: <https://learn.microsoft.com/en-us/training/modules/manage-work-github-projects/3-how-to-create-project>

### Ownership

Projects can be owned at user or organization level depending on the use case and account capabilities. The Microsoft Learn module emphasizes an **organization-owned Project** for shared team planning.

### Project setup

Typical setup tasks include:

- create a new Project;
- choose a starting template or blank Project;
- set a name;
- add a short description;
- add/maintain a Project README for purpose/process/context;
- configure visibility/access as supported;
- add issues and pull requests.

### Adding items

Items can include:

- existing Issues;
- existing Pull Requests;
- draft items that can later become Issues.

A Project may aggregate work across multiple repositories, which is important for organization-level planning.

### Project description vs README

A short description communicates the Project's purpose quickly. A README can document longer guidance such as scope, planning cadence, field definitions, ownership, and working agreements.

---

## Unit 4 — How to organize your project

Official unit: <https://learn.microsoft.com/en-us/training/modules/manage-work-github-projects/4-how-to-organize-your-project>

### Views

A Project can expose different views of the same underlying items. For example:

- table view for dense metadata;
- board view grouped by status/team/other field;
- roadmap view for time-oriented planning.

Changing a view does not create a separate copy of every Issue; it changes how the Project data is presented.

### Custom fields

Common field types include:

- text;
- number;
- date;
- single select;
- iteration.

Fields can represent data such as:

- priority;
- status;
- target date;
- estimate;
- team;
- iteration/sprint;
- risk.

### Sorting, grouping, filtering

Projects can be organized using:

- filter expressions;
- sort rules;
- grouping by fields;
- manual ranking/order;
- saved views for recurring perspectives.

A useful design principle is to avoid duplicating the same meaning across many fields. Use repository-native metadata such as Issue labels when that metadata belongs to the Issue itself, and Project fields when the metadata is primarily planning-specific.

### Iterations

Iteration fields represent repeating planning periods such as sprints or cycles. Iterations can have configurable durations and breaks.

---

## Unit 5 — How to organize and automate your project

Official unit: <https://learn.microsoft.com/en-us/training/modules/manage-work-github-projects/5-how-to-organize-automate-project>

### Built-in workflows

Projects can automatically update items based on supported events and conditions. Common examples include:

- automatically adding items;
- updating a status when an item is closed/merged;
- moving work through a workflow based on Issue/PR state.

Exact built-in workflow options can evolve, so understand the principle: **Project metadata can react automatically to GitHub work-item events**.

### Advanced automation

Projects can be integrated through:

- GitHub Actions;
- GraphQL Projects API;
- GitHub Apps;
- webhooks/events.

Automation is useful for keeping Project state synchronized with real repository activity and avoiding manual status drift.

### Access and management

Project visibility and management permissions should be set to match the intended audience. Organization-owned Projects can support shared planning while repository permissions still control access to private repository content.

---

## Unit 6 — Insight and automation with projects

Official unit: <https://learn.microsoft.com/en-us/training/modules/manage-work-github-projects/6-insight-automation-with-projects>

### Insights

Projects can create charts from Project fields/data. Chart types and available configuration evolve, but the Microsoft Learn curriculum highlights visualizations such as bar/column, line, and stacked-area style charts.

Charts can help answer questions such as:

- how much work is in each status;
- how work changes over time;
- how tasks are distributed by team/iteration/priority;
- whether a backlog is growing or shrinking.

### Aggregation

Project insights can use aggregate functions such as count, sum, average, minimum, and maximum where supported by the field/data type.

### Sharing

Saved views/charts can provide repeatable URLs/perspectives so stakeholders see the same filtered analysis rather than manually recreating it.

### Automation + insight

Automation improves the quality of Project data. Better data in turn makes charts/insights more reliable. A Project that depends on humans manually updating every status field will drift more easily than one tied to repository state where appropriate.

---

## Unit 7 — Module assessment

Official unit: <https://learn.microsoft.com/en-us/training/modules/manage-work-github-projects/7-knowledge-check>

The integrated assessment covers:

- Projects vs Classic;
- Project ownership;
- issues/PRs/draft items;
- views;
- custom fields and iterations;
- filtering/sorting/grouping;
- visibility/access;
- built-in automation;
- GraphQL/Actions/webhooks;
- insights and aggregation.

---

## Unit 8 — Summary

Official unit: <https://learn.microsoft.com/en-us/training/modules/manage-work-github-projects/8-summary>

After completing this module you should be able to design a Project structure for a team scenario and explain how views, fields, automation, and insights work together.

## Interactive lab

GitHub Projects permissions/API behavior differ depending on whether the learner is using a fork, personal account, or organization. The module therefore supports two paths:

### Real Project path

If the learner can create a Project:

1. create a Project for the course;
2. add the module's sample Issues;
3. create fields for Status, Priority, and Iteration;
4. create table and board views;
5. filter/group the views;
6. configure one supported built-in workflow;
7. create one insight/chart;
8. record the Project URL in `labs/module-07/project-report.md`.

### Simulation path

If Project creation is unavailable, the learner completes the same design decisions in a structured Project model file. The engine validates that every official concept has been exercised rather than requiring a paid/organization-specific environment.

## Official references

- Microsoft Learn module: <https://learn.microsoft.com/en-us/training/modules/manage-work-github-projects/>
- GitHub Docs — Projects: <https://docs.github.com/en/issues/planning-and-tracking-with-projects>
