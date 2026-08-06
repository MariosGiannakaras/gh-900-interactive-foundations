# Module 16 — Using GitHub Copilot with Python

Official Microsoft Learn module: <https://learn.microsoft.com/en-us/training/modules/introduction-copilot-python/>

This module maps **1:1 to all 7 official units**.

## Learning objectives

After this module you should be able to:

- enable/sign in to GitHub Copilot in Visual Studio Code or a Codespace;
- recognize comments, Markdown, editor context, and chat as prompt/context sources;
- accept, reject, and cycle between code suggestions;
- craft specific prompts for Python work;
- improve prompts iteratively and provide relevant open-file/context information;
- use Copilot to extend an existing Python/FastAPI application;
- review missing imports, data models, endpoints, tests, and runtime behavior rather than accepting suggestions blindly.

---

## Unit 1 — Introduction

Official unit: <https://learn.microsoft.com/en-us/training/modules/introduction-copilot-python/1-introduction>

This module narrows the general Copilot concepts from Module 5 into a concrete Python workflow. The goal is not simply to generate code: it is to use an AI suggestion loop while still understanding, running, testing, and correcting the resulting Python application.

The Microsoft Learn module expects basic Python, basic Git commands, and an account with Copilot access. Copilot Free is sufficient for the intended learning flow where available.

---

## Unit 2 — What is GitHub Copilot?

Official unit: <https://learn.microsoft.com/en-us/training/modules/introduction-copilot-python/2-what-is-github-copilot>

Copilot is an AI coding assistant that can generate suggestions from natural-language prompts and surrounding code context.

### Prompt forms

A prompt can be supplied as:

- a source-code comment;
- text in a Markdown file;
- Copilot Chat input;
- partially written code that establishes intent/context.

For example, a Python comment can describe a FastAPI route and allow Copilot to propose an implementation.

### Suggestions

Inline suggestions appear as proposed code ahead of the cursor. The developer can:

- accept;
- ignore/reject;
- continue typing to change context;
- cycle among alternatives where supported.

The official unit uses `Tab` to accept an inline suggestion and `Ctrl+Enter` (or the platform equivalent) to inspect multiple suggestions in supported editor versions.

Exact keybindings can vary with editor/version/settings; the durable concept is **evaluate alternatives rather than accepting the first output automatically**.

---

## Unit 3 — Exercise: Set up GitHub Copilot to work with Visual Studio Code

Official unit: <https://learn.microsoft.com/en-us/training/modules/introduction-copilot-python/3-exercise-setup>

### Required account/environment concepts

To use Copilot you need:

1. a GitHub account;
2. eligible Copilot access (Free or an assigned/paid plan as applicable);
3. a supported IDE/editor integration;
4. authentication from the editor to GitHub.

The official exercise uses a preconfigured GitHub Codespace so the Python environment and Copilot integration are available together.

### IDE integrations

Copilot is supported in major IDE/editor ecosystems. The module specifically focuses on Visual Studio Code and uses the Copilot/Copilot Chat experience there.

### Course setup

This setup unit does **not** create permanent exercise files. Use it to verify or understand the environment you will use later:

1. confirm whether GitHub Copilot is available to your account;
2. know how to sign in to GitHub from Visual Studio Code or a Codespace;
3. identify where Copilot inline suggestions and Copilot Chat appear;
4. understand how to accept, reject, and cycle through suggestions;
5. confirm that Python development can be run in your chosen environment.

The temporary FastAPI application, tests, and dependency file are generated only when Unit 5 begins. This keeps the repository clean until those files are genuinely needed.

---

## Unit 4 — Use GitHub Copilot with Python

Official unit: <https://learn.microsoft.com/en-us/training/modules/introduction-copilot-python/4-use-copilot-with-python>

### Prompt engineering

Prompt quality materially affects suggestion quality.

Weak prompt:

```text
Create an API endpoint.
```

A better prompt describes important constraints, for example:

```text
Create a FastAPI POST endpoint that accepts a JSON payload with a text field and returns a deterministic checksum plus input length. Validate empty input.
```

A useful prompt communicates:

- framework/language;
- desired behavior;
- input/output shape;
- validation/error behavior;
- constraints;
- relevant existing functions/types;
- tests or acceptance criteria.

### Iterative prompting

Start with a focused objective and refine it. If a suggestion is poor:

- rewrite the prompt;
- add constraints;
- break the task into smaller steps;
- show an example;
- open/reference relevant files;
- write a small amount of code so Copilot has stronger context;
- compare alternative suggestions.

### Open-file context

Copilot can use relevant open editor files/context. Keep useful interfaces, models, tests, and related code available when asking repository-specific questions. In chat, explicitly reference relevant files/context when supported.

### Review discipline

For Python suggestions verify:

- imports actually exist;
- types/data models match the framework;
- async/sync usage is valid;
- error handling is appropriate;
- security-sensitive operations are safe;
- dependencies are present;
- generated tests assert meaningful behavior;
- code executes in the real environment.

---

## Unit 5 — Exercise: Update a Python web API with GitHub Copilot

Official unit: <https://learn.microsoft.com/en-us/training/modules/introduction-copilot-python/5-exercise-python-web-api>

The Microsoft Learn exercise extends a FastAPI web API with AI-generated suggestions. It introduces API concepts, a Pydantic data model, a new POST endpoint, missing-import diagnosis, and verification through FastAPI's generated `/docs` interface.

Our exercise preserves that workflow without reproducing Microsoft's exact sample code.

### Supplied application

When this unit begins, the course generates a small FastAPI application with one existing `/health` route, an acceptance-test suite, and a dependency file. The new endpoint tests intentionally fail until the learner implements the required change.

### Required change

Using Copilot where available, the learner must:

1. add a Pydantic request model containing a `text: str` field;
2. add a POST endpoint `/analyze-text`;
3. accept JSON matching the request model;
4. return at least a deterministic checksum/hash and input length;
5. identify/add any imports required by the chosen implementation;
6. reject/handle invalid empty input appropriately;
7. review and, where useful, improve the automated tests;
8. run the test suite;
9. run the API and verify the new endpoint via `/docs` or an HTTP request;
10. record the prompt iterations and at least one Copilot suggestion that was rejected or modified.

### Why the reflection is required

The repository can validate final code structure and tests but cannot reliably prove that a specific line came from Copilot. The learner therefore records the prompt/review process while also verifying the executable result in the development environment.

### Fallback when Copilot is unavailable

A learner without Copilot entitlement can use the clearly marked prompt-review alternatives presented directly in the course Issue. They still implement and test the final Python API themselves. The course marks this as a fallback rather than claiming Copilot was used.

---

## Unit 6 — Module assessment

Official unit: <https://learn.microsoft.com/en-us/training/modules/introduction-copilot-python/6-knowledge-check>

Assessment coverage includes:

- setup/access requirements;
- comments/Markdown/chat/code context as prompts;
- accepting/rejecting/cycling suggestions;
- prompt specificity;
- iterative prompting;
- open-file context;
- Pydantic/FastAPI workflow concepts from the exercise;
- reviewing missing imports and runtime failures;
- testing AI-generated code.

---

## Unit 7 — Summary

Official unit: <https://learn.microsoft.com/en-us/training/modules/introduction-copilot-python/7-summary>

After completing the module you should be able to use Copilot as part of a real Python edit-test-debug-review loop instead of treating generated code as an answer that bypasses engineering verification.

## Official references

- Microsoft Learn module: <https://learn.microsoft.com/en-us/training/modules/introduction-copilot-python/>
- GitHub Docs — Copilot: <https://docs.github.com/en/copilot>
- FastAPI: <https://fastapi.tiangolo.com/>
- Pydantic: <https://docs.pydantic.dev/>
