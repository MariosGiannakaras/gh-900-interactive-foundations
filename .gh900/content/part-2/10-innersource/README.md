# Module 10 — Manage an InnerSource program by using GitHub

Official Microsoft Learn module: <https://learn.microsoft.com/en-us/training/modules/manage-innersource-program-github/>

This module maps **1:1 to all 5 official units**.

## Learning objectives

After this module you should be able to:

- explain InnerSource and its benefits;
- contrast user-owned and organization-owned projects for organizational collaboration;
- reason about one vs multiple organizations;
- choose appropriate repository visibility and permission levels;
- make repositories discoverable;
- create strong README and CONTRIBUTING guidance;
- use CODEOWNERS and Issue/PR templates;
- establish transparent contribution workflows;
- measure participation/success and distribute an InnerSource toolkit.

---

## Unit 1 — Introduction

Official unit: <https://learn.microsoft.com/en-us/training/modules/manage-innersource-program-github/1-introduction>

**InnerSource** applies open-source collaboration patterns inside a restricted organizational audience. The code is not necessarily public; the organization intentionally makes reusable projects discoverable and contributable across internal team boundaries.

InnerSource is a working model, not merely a repository visibility setting.

---

## Unit 2 — How to manage a successful InnerSource program

Official unit: <https://learn.microsoft.com/en-us/training/modules/manage-innersource-program-github/2-manage-innersource-program>

### Benefits

InnerSource can improve:

- **visibility** — teams can inspect other teams' code, Issues, PRs, and plans;
- **reuse** — common implementations can be shared instead of rebuilt;
- **cross-team contribution** — consumer teams can propose fixes/features upstream;
- **reduced friction** — dependencies between teams can be solved through a known contribution channel;
- **standardization** — contribution conventions become predictable across teams.

GitHub Discussions and Projects can complement repositories/PRs for broader internal collaboration.

### Ownership: personal vs organization

For durable organizational software, organization ownership is generally preferable to a personal account because ownership, permissions, teams, policies, and continuity are not tied to one employee's personal namespace.

A personal/user-owned repository can be useful for individual prototypes, but it is a poor default for shared business-critical InnerSource assets.

### One organization vs many

Microsoft Learn recommends avoiding unnecessary organization sprawl. Multiple organizations can introduce:

- duplicated setup/policies;
- inconsistent configuration;
- more application/integration administration;
- more complex discoverability;
- additional cost in some integration models.

Use multiple organizations when there is a genuine governance, legal, identity, business-boundary, or operational reason—not simply because each team wants its own namespace.

### Repository visibility

Conceptually:

- **Public** — visible outside the enterprise; appropriate for truly public/open-source work;
- **Internal** — visible to enterprise members and useful for broad InnerSource in supported Enterprise environments;
- **Private** — restricted to explicitly granted users/teams and appropriate for narrower confidential work.

Internal visibility is an Enterprise capability.

### Repository permission levels

Know the five standard repository permission roles for organization repositories:

- **Read** — view/participate without managing work;
- **Triage** — manage Issues/PRs without code-write privileges;
- **Write** — push/contribute code;
- **Maintain** — manage repository operations without the full set of destructive/sensitive admin actions;
- **Admin** — full repository administration.

Apply least privilege.

### Discoverability

A repository is more reusable if people can find and understand it.

Use:

- descriptive repository names;
- concise repository descriptions;
- relevant topics;
- clear README content;
- internal catalogs/links as appropriate;
- consistent naming conventions.

### README

A robust README should explain:

- purpose/vision;
- intended consumers;
- screenshots/examples where useful;
- prerequisites;
- setup/deployment/use;
- dependencies and related projects;
- how to get help;
- how to contribute.

GitHub recognizes README files in locations including `.github`, repository root, and `docs`, with precedence when more than one exists.

### CONTRIBUTING

`CONTRIBUTING.md` should define how people participate, such as:

- development setup;
- branch/workflow conventions;
- where to report bugs/propose features;
- testing requirements;
- commit conventions;
- PR expectations;
- review process.

GitHub surfaces contribution guidance during Issue/PR creation.

### CODEOWNERS

`CODEOWNERS` maps repository paths to responsible people/teams. Combined with repository rules/branch protection, code-owner review can be required before changes merge.

### Issue and pull-request templates

Templates reduce repeated clarification and make contributions more consistent.

Common paths include:

```text
.github/ISSUE_TEMPLATE/
.github/PULL_REQUEST_TEMPLATE.md
```

Issue Forms can collect structured input with YAML-based forms.

### Define the workflow

Document how branches and PRs are expected to work. A contributor should not have to reverse-engineer the team's workflow by observing old PRs.

GitHub Flow is a reasonable default for many teams unless release/governance needs justify another model.

### Transparency

InnerSource works better when internal users can observe:

- open Issues;
- roadmap/planning information;
- contribution status;
- PR reviews;
- decision rationale;
- maintainers/owners;
- release/change information.

Transparency reduces duplicate requests and hidden dependencies.

### Measure success

Useful InnerSource signals can include:

- number of cross-team contributors;
- PRs from outside the owning team;
- contribution acceptance time;
- number of reused components/consumer teams;
- issue/PR response time;
- active repositories/maintainers;
- documentation quality/onboarding friction;
- qualitative developer feedback.

Avoid measuring success only by raw commit count.

### InnerSource toolkit

A reusable toolkit can standardize:

- README template;
- CONTRIBUTING template;
- CODE_OF_CONDUCT/security guidance as appropriate;
- Issue/PR templates;
- CODEOWNERS examples;
- repository naming/topics;
- branch/ruleset recommendations;
- workflow examples;
- metrics guidance.

Distribute it through an organization `.github` repository, repository templates, internal docs, reusable workflows, or other organization-wide channels.

---

## Unit 3 — Exercise: InnerSource fundamentals

Official unit: <https://learn.microsoft.com/en-us/training/modules/manage-innersource-program-github/3-exercise-innersource-fundamentals>

The interactive exercise creates a temporary InnerSource workspace only for this unit. On `lab/m10-u03`, complete:

- `exercise/README-sample.md`;
- `exercise/CONTRIBUTING.md`;
- `exercise/CODEOWNERS`;
- `exercise/ISSUE_TEMPLATE/feature.yml`;
- `exercise/PULL_REQUEST_TEMPLATE.md`;
- `exercise/discoverability-plan.md`;
- `exercise/access-visibility-matrix.md`;
- `exercise/success-metrics.md`.

The engine validates that every artifact addresses its required InnerSource concepts, then removes the temporary learner/sandbox branches after completion.

---

## Unit 4 — Module assessment

Official unit: <https://learn.microsoft.com/en-us/training/modules/manage-innersource-program-github/4-knowledge-check>

Assessment topics include:

- InnerSource vs open source;
- repository ownership;
- organization design;
- visibility;
- permission roles;
- discoverability;
- README/CONTRIBUTING/CODEOWNERS;
- templates;
- transparency;
- success metrics;
- toolkit distribution.

---

## Unit 5 — Summary

Official unit: <https://learn.microsoft.com/en-us/training/modules/manage-innersource-program-github/5-summary>

After completing this module you should be able to design a practical InnerSource program that is discoverable, safe, contribution-friendly, and measurable.

## Official references

- Microsoft Learn module: <https://learn.microsoft.com/en-us/training/modules/manage-innersource-program-github/>
- GitHub InnerSource resources: <https://resources.github.com/innersource/>
- Repository permissions: <https://docs.github.com/en/organizations/managing-user-access-to-your-organizations-repositories/repository-roles-for-an-organization>
- Community health files: <https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions>
