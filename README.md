# GH-900 Interactive Foundations

> [!IMPORTANT]
> **Curriculum freshness:** [![Monthly Microsoft Learn drift check](https://github.com/MariosGiannakaras/gh-900-interactive-foundations/actions/workflows/curriculum-drift.yml/badge.svg?branch=main)](https://github.com/MariosGiannakaras/gh-900-interactive-foundations/actions/workflows/curriculum-drift.yml)  
> This source template checks the 16 locked Microsoft Learn module paths **once per month**. A red **Curriculum Drift** badge means Microsoft Learn changed after the verified baseline and the course should be reviewed before relying on its curriculum status.

[![Course Quality](https://github.com/MariosGiannakaras/gh-900-interactive-foundations/actions/workflows/quality.yml/badge.svg?branch=main)](https://github.com/MariosGiannakaras/gh-900-interactive-foundations/actions/workflows/quality.yml)
![Curriculum](https://img.shields.io/badge/curriculum-16%20modules%20%7C%20106%20units-0969da)
![Template](https://img.shields.io/badge/GitHub-template-8250df?logo=github)
[![License: MIT](https://img.shields.io/badge/license-MIT-2da44e)](LICENSE)

An interactive **GH-900: GitHub Foundations** course implemented directly on GitHub.

It covers **2 / 2 Microsoft Learn learning paths, 16 / 16 modules, and 106 / 106 official units** in sequence. Lessons, assessments, hands-on instructions, validation feedback, and progress are presented in GitHub Issues. Exercise files exist only when editing a file is part of the current lesson.

This is an independently written educational project and is not an official Microsoft or GitHub product. Microsoft Learn is used as the public curriculum/source baseline.

[![Copy Exercise](https://img.shields.io/badge/Copy%20Exercise-%E2%86%92-1f883d?style=for-the-badge&logo=github)](https://github.com/new?template_owner=MariosGiannakaras&template_name=gh-900-interactive-foundations&owner=%40me&name=gh-900-interactive-foundations-course&description=Interactive%20GH-900%20GitHub%20Foundations%20course&visibility=public)

> **Start here:** select **Copy Exercise**, create a repository from the template, then open the course Issue that starts automatically.

## How it works

The learner experience is **Issue-first**.

1. Create a repository from this template.
2. **Step 0 - Start GH-900 Course** initializes the learner copy automatically.
3. Open **GH-900 Interactive Foundations — Course** under Issues.
4. Follow the latest lesson in that Issue.
5. Reading and summary units advance with `/next`.
6. Assessments are answered directly in the Issue.
7. Hands-on units create only the temporary files/branches needed for that exercise.
8. Account/entitlement-dependent exercises use a real path when available and an explicit guided fallback when it is not.
9. Enterprise/paid scenarios use structured decisions rather than fake worksheets or destructive tenant changes.
10. The course validates Git/GitHub state automatically where GitHub exposes durable evidence.
11. Successful temporary exercises are cleaned before the next lesson.

There is no normal **Actions → Run workflow** setup step. Manual workflow dispatch exists only for recovery.

## A clean workspace for every lesson

A learner repository is deliberately kept close to empty.

Permanent learner-visible content is essentially:

```text
README.md
LICENSE
.github/workflows/   # course automation
.gh900/              # internal course engine
```

When a hands-on unit starts, the engine creates an isolated temporary workspace:

```text
main
  └─ sandbox/mXX-uYY      # generated baseline
       └─ lab/mXX-uYY     # learner work
```

Only the artifacts required by that unit are generated. Depending on the lesson this might be:

- a small Git practice file;
- a Markdown document;
- a temporary `.devcontainer/devcontainer.json`;
- a Python file and tests;
- a temporary CodeQL configuration;
- `SECURITY.md`, `.gitignore`, Dependabot, or `CODEOWNERS` when creating those files is the exercise itself.

After successful validation, temporary branches, exercise files, labels, milestones, or Issues created solely for the lesson are removed or closed as appropriate.

The intended lifecycle is:

```text
clean workspace → current lesson → validate → cleanup → next lesson
```

State is carried forward only when the next lesson genuinely needs it.

## What appears in the course Issue

Every unit is rendered directly into the course interface with:

- **Part 1 / Part 2** position;
- module and unit number;
- total progress out of **106**;
- the complete independently written lesson for that unit;
- additional source-audited detail where needed;
- the current exercise, assessment, scenario, or account-aware checkpoint;
- the exact action required to continue.

Each rendered lesson carries an internal stable unit marker. Learner responses such as `/reflection` and `/investigation` are associated with the unit that was visible when they were posted, so old evidence cannot satisfy a later unit accidentally.

Learners are never instructed to browse internal course files in order to study. A file is opened only when working with that file is itself the practical task.

## Microsoft Learn structure

### Part 1 of 2 — 8 modules / 57 units

1. Introduction to Git
2. Introduction to GitHub
3. Introduction to GitHub's products
4. Configure code scanning on GitHub
5. Introduction to GitHub Copilot
6. Code with GitHub Codespaces
7. Manage your work with GitHub Projects
8. Communicate effectively on GitHub using Markdown

The course explicitly marks **Part 1 complete** before Part 2 begins.

### Part 2 of 2 — 8 modules / 49 units

9. Contribute to an open-source project on GitHub
10. Manage an InnerSource program by using GitHub
11. Maintain a secure repository by using GitHub best practices
12. Introduction to GitHub administration
13. Authenticate and authorize user identities on GitHub
14. Manage repository changes by using pull requests on GitHub
15. Search and organize repository history by using GitHub
16. Using GitHub Copilot with Python

**Total: 16 modules / 106 units.**

## Interaction model

### Reading and summary units

Read the lesson in the Issue and comment:

```text
/next
```

Official Microsoft Learn units whose title is an **Exercise** are not downgraded to plain reading solely because the real product surface is difficult to automate.

### Assessments

Questions and answer choices are shown directly in the Issue. Submit the letters in order:

```text
/answer B C A B A C
```

The validator reports only the questions that need review. Correct answers are not printed in normal course output.

### Hands-on units

The Issue provides the complete checklist. The engine creates the exact temporary repository state required for the exercise.

Depending on the unit, completion is detected from commits, diffs, branches, tags, Issues, Pull Requests, review state, generated configuration, tests, or other GitHub state. Generic answer worksheets are not used.

If a manual recheck is needed:

```text
/check
```

Some exercises also request an observation directly in the Issue:

```text
/reflection <your observation>
```

The response is scoped to the active unit rather than treated as global course evidence.

### Account-aware / external checkpoints

Some official exercises depend on an account entitlement or editor/product surface that GitHub Actions cannot prove from a repository—for example GitHub Copilot setup in Visual Studio Code.

Those units remain interactive with:

```text
/checkpoint key=value ...
```

The course uses this order of preference:

1. perform/inspect the real GitHub or editor action when the feature is available;
2. follow the exact official Microsoft Learn unit linked in the lesson;
3. if the entitlement is unavailable, complete the structured fallback without pretending the unavailable product was used.

The validator checks the required setup decisions honestly; it does not fabricate private editor telemetry.

### Scenario units

Enterprise, billing, identity-provider, or organization-level capabilities cannot always be safely provisioned in an ordinary personal repository. Those units remain interactive without requiring a paid tenant or fake worksheet.

The Issue supplies a structured response shape, for example:

```text
/scenario scope=organization role=maintain least_privilege=yes reason=limit-access-to-required-scope
```

Validators check required fields and relationships between decisions, not merely response length or a bag of keywords. Learners who have the corresponding real product access can inspect the UI as part of the same checkpoint.

### Help and self-healing

```text
/help
```

always re-renders the **authoritative current state**. It intentionally bypasses stale-command protection.

If GitHub successfully advances the hidden course state but a transient API error prevents the next lesson comment from being posted, the next engine event reconciles the state with the Issue transcript and restores the missing lesson idempotently.

Queued duplicate commands from a previous unit do not advance the course twice.

## Course coverage

| Item | Coverage |
|---|---:|
| Microsoft Learn learning paths | **2 / 2** |
| Microsoft Learn modules | **16 / 16** |
| Official units | **106 / 106** |
| Part 1 | **8 modules / 57 units** |
| Part 2 | **8 modules / 49 units** |
| Progression | **Unit by unit** |
| Lessons | **Issue-native** |
| Assessments | **Issue-native, original blind questions** |
| Official exercises | **Interactive; real, account-aware, or structured fallback** |
| Hands-on state | **Generated on demand** |
| Cleanup | **Automatic after validation** |

The course is not an exam-cram summary. Every official unit is represented in the locked sequence. Paid or Enterprise-only concepts are not silently omitted: the course prefers a real action where available, keeps the official Microsoft Learn unit visible, and otherwise uses an account-aware checkpoint or structured scenario rather than pretending unavailable infrastructure exists.

## Source baseline

The course is audited against:

```text
MicrosoftDocs/learn@66ab07a355b38fb0f5a4cef8240eb2f765c839c8
Baseline date: 2026-08-06
```

The canonical maintained source is intentionally compact:

```text
README.md
LICENSE
.github/
  workflows/
  CONTRIBUTING.md
  CODE_OF_CONDUCT.md
  SECURITY.md
  ARCHITECTURE.md
  MAINTAINING.md
.gh900/
  content/       # Part 1 / Part 2 independently written lesson source
  details/       # additional audited depth
  data/          # curriculum, source lock, concepts, exam objectives, assessment hashes
  templates/     # temporary exercise fixtures
  quality/       # source, coverage, runtime and regression audits
  *.py           # learner runtime and validators
```

There are no parallel `modules/`, `labs/`, `course-content/`, `unit-details/`, or `curriculum/` trees. `.gh900/` is the single canonical course package.

The repository does not reproduce Microsoft Learn prose or Microsoft's knowledge-check question bank verbatim.

## Quality gates

The source template runs **Course Quality**, which verifies:

- exact **2 / 2 paths, 16 / 16 modules, 106 / 106 units**;
- Part 1 = **57** units and Part 2 = **49** units;
- exact runtime order from `m01-u01` through `m16-u07`;
- successful Issue rendering of every unit with stable unit markers;
- Issue-native assessments, scenarios, and account-aware checkpoints;
- no official `Exercise` unit is silently reduced to reading-only mode;
- isolated lab/sandbox branch contracts;
- pinned Microsoft Learn source resolution;
- source-depth checks that prevent title/objective-only placeholders;
- curated **concept-level coverage contracts for all 106 units**;
- a separate **January 2026 GH-900 exam-objective → course-unit coverage contract**;
- a deterministic **106-unit runtime/protocol simulation**, including stale-command and unit-scoped-evidence behavior;
- Python compilation;
- workflow YAML and embedded Bash syntax;
- rejection of malformed assessments, unstructured scenarios, incomplete account-aware checkpoints, and unprepared activities;
- public-repository/community requirements;
- immutable full-SHA references for external Actions.

The depth check is intentionally not presented as semantic equivalence. Concept-level coverage is enforced separately by the curated machine-readable coverage manifest, and GH-900 exam coverage has its own independent mapping.

`Course Quality` is source-maintenance CI only. Learner copies do not run the full upstream source audit.

## Security and reliability model

The automation is designed around explicit trust and recovery boundaries:

- the template source itself never creates learner progress;
- learner automation runs only in non-template copies;
- source-quality CI runs only in the template repository;
- workflow permissions are declared explicitly;
- unrelated Issue comments and unrelated PR branch pairs are filtered before the course runner starts;
- drive-by Issue comments and untrusted fork Pull Requests are rejected;
- course events are serialized per repository;
- PR exercises use temporary sandbox branches instead of merging exercise content into `main`;
- temporary exercise state is removed after validation and stale course-owned branches are cleaned on later transitions;
- learner responses are scoped to the lesson marker that was active when they were posted;
- partial state/render transitions self-heal on the next engine event;
- external commands and validators have explicit timeouts;
- external Actions are pinned to immutable commit SHAs;
- no exercise requires a real secret.

Report security issues using [`.github/SECURITY.md`](.github/SECURITY.md). Do not post credentials, exploit details, or private vulnerability information in a public Issue.

## Contributing

Corrections and improvements are welcome when they preserve curriculum completeness, independent wording, learner safety, and the clean per-unit workspace model.

Read [`.github/CONTRIBUTING.md`](.github/CONTRIBUTING.md) and [`.github/MAINTAINING.md`](.github/MAINTAINING.md) before changing course content or runtime behavior.

## License and attribution

Original material and code in this repository are available under the [MIT License](LICENSE), except where a file explicitly states otherwise.

Microsoft, GitHub, Microsoft Learn, GH-900, and related names or marks belong to their respective owners.

Reference sources:

- [Microsoft Learn — GitHub Foundations Part 1](https://learn.microsoft.com/en-us/training/paths/github-foundations/)
- [Microsoft Learn — GitHub Foundations Part 2](https://learn.microsoft.com/en-us/training/paths/github-foundations-2/)
- [Microsoft Learn — GH-900 Study Guide](https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/gh-900)
- [GitHub Skills](https://skills.github.com/)
- [GitHub Docs](https://docs.github.com/)
- [Git documentation](https://git-scm.com/doc)

For implementation details, see [`.github/ARCHITECTURE.md`](.github/ARCHITECTURE.md).
