# Contributing

Contributions that improve correctness, accessibility, reliability, security, or maintainability are welcome.

## Course source vs learner copies

This repository is the maintained **course template**. Learners should create their own repository with the **Copy Exercise** button in the README and complete course work there.

If a repository was created from this template for personal learning, course answers and lab work normally belong in that learner repository rather than in a Pull Request back to the upstream course.

## Useful contributions

Good upstream contributions include:

- factual corrections or clearer independently written explanations;
- fixes to course startup, state progression, validators, or recovery behavior;
- accessibility and documentation improvements;
- security hardening;
- improvements to tests and quality gates;
- updates required by a verified Microsoft Learn or GH-900 curriculum change.

## Curriculum integrity

The maintained course has a strict completeness contract: **2 learning paths, 16 modules, and 106 official units** for the pinned curriculum baseline.

A curriculum change should:

1. identify the relevant Microsoft Learn source unit or GH-900 study-guide objective;
2. preserve independent wording rather than copying Microsoft Learn prose;
3. avoid reproducing Microsoft's knowledge-check question bank;
4. update source-lock/coverage metadata when the upstream baseline changes;
5. keep learner activities safe and achievable in an ordinary GitHub repository, or use an explicit scenario/read-only activity for paid/Enterprise-only capabilities;
6. pass the full `Course Quality` workflow.

## Assessment integrity

Do not submit changes whose purpose is to expose correct assessment answers in learner-visible material. Validators may contain hashes and implementation details because repository owners necessarily control their own copy, but normal course output must not reveal answer keys.

## Pull Requests

Keep Pull Requests focused and explain:

- what problem is being solved;
- which course/module/runtime area is affected;
- whether learner behavior changes;
- what validation was performed.

Changes to workflows or validators should include the smallest practical regression check. Avoid unrelated reformatting in the same Pull Request.

## Security reports

Do not disclose vulnerabilities, tokens, credentials, or exploit details in a public Issue. Follow [SECURITY.md](SECURITY.md) for private-reporting guidance.

## Conduct

Participation in this repository is subject to the [Code of Conduct](CODE_OF_CONDUCT.md).
