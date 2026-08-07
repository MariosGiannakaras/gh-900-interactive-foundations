# Module 8 — Communicate effectively on GitHub using Markdown

Official Microsoft Learn module: <https://learn.microsoft.com/en-us/training/modules/communicate-using-markdown/>

This module maps **1:1 to all 5 official units**.

## Learning objectives

After this module you should be able to:

- explain what Markdown is and why GitHub uses it;
- use headings, paragraphs, emphasis, blockquotes, lists, links, images, code, horizontal rules, and tables;
- use GitHub Flavored Markdown (GFM) features such as task lists and fenced code blocks;
- use mentions, issue/PR references, emoji, alerts, and other GitHub-specific communication conveniences where supported;
- know where Markdown appears across GitHub;
- create readable repository documentation and comments.

---

## Unit 1 — Introduction

Official unit: <https://learn.microsoft.com/en-us/training/modules/communicate-using-markdown/1-introduction>

Markdown is a lightweight plain-text markup language. It is easy to read in source form and can be rendered as formatted HTML-like content.

GitHub uses Markdown extensively in:

- README files;
- Issues;
- Pull Requests;
- Discussions;
- comments;
- repository documentation;
- Gists;
- Wikis;
- profile README content and many other text surfaces.

---

## Unit 2 — What is Markdown?

Official unit: <https://learn.microsoft.com/en-us/training/modules/communicate-using-markdown/2-what-is-markdown>

### Headings

```markdown
# Heading 1
## Heading 2
### Heading 3
```

Use heading levels structurally. Do not choose heading levels only for visual size.

### Paragraphs and line breaks

Separate paragraphs with a blank line. Markdown renderers may treat ordinary line wrapping differently from explicit paragraph breaks.

### Emphasis

```markdown
*italic*
_italic_
**bold**
__bold__
***bold italic***
~~strikethrough~~
```

### Blockquotes

```markdown
> Quoted text
>> Nested quote
```

### Lists

Unordered:

```markdown
- one
- two
  - nested
```

Ordered:

```markdown
1. first
2. second
3. third
```

### Task lists

GitHub Flavored Markdown supports interactive-style task list syntax:

```markdown
- [ ] not complete
- [x] complete
```

Task lists are especially useful in Issues and Pull Requests for visible checklists.

### Links

```markdown
[GitHub](https://github.com/)
```

Autolinks may also be recognized when a full URL is pasted.

### Images

```markdown
![Alternative text](path-or-url-to-image)
```

Always provide meaningful alt text when the image communicates information.

### Inline code

```markdown
Use `git status` to inspect repository state.
```

### Fenced code blocks

````markdown
```python
print("hello")
```
````

A language identifier enables syntax highlighting where supported.

### Tables

```markdown
| Feature | Purpose |
| --- | --- |
| Issue | Track work |
| Discussion | Open conversation |
```

Alignment markers can be added to separator cells when needed.

### Horizontal rule

```markdown
---
```

### Escaping Markdown

Use a backslash when you need a Markdown punctuation character to render literally rather than being interpreted as markup.

### HTML

GitHub Markdown supports a safe subset of HTML in many contexts. Markdown should remain the default because it is easier to read and maintain, but HTML can be useful for specific formatting needs supported by GitHub's renderer.

---

## GitHub Flavored Markdown and GitHub-specific communication

GitHub extends CommonMark-style Markdown with platform-aware behavior.

### Mentions

```text
@username
@org/team-name
```

Mentions can notify relevant users/teams subject to permissions and notification settings.

### Issue and pull-request references

Within the same repository:

```text
#123
```

Cross-repository:

```text
owner/repository#123
```

GitHub automatically creates links and often shows rich context around references.

### Commit references

Full or sufficiently unique commit SHAs can be recognized and linked by GitHub.

### Closing keywords

Pull request descriptions/commit messages can use supported keywords such as `Fixes #123` to link work and automatically close an Issue when the qualifying change is merged to the appropriate default branch.

Recognize keywords such as close/closes/closed, fix/fixes/fixed, resolve/resolves/resolved according to GitHub's supported syntax.

### Emoji

GitHub supports emoji and `:shortcode:` forms in many Markdown contexts.

### Alerts/callouts

GitHub Markdown supports alert-style blockquote syntax in supported surfaces, for example:

```markdown
> [!NOTE]
> Useful information.
```

Other supported alert categories may include TIP, IMPORTANT, WARNING, and CAUTION.

### Collapsed details

Where HTML is allowed, `<details>` and `<summary>` can hide long optional content while keeping the main page concise.

### Diagrams and math

GitHub supports additional rich Markdown capabilities in supported contexts, including Mermaid diagrams and mathematical expressions. These are useful extensions but should be used when they improve communication rather than for decoration.

### Footnotes

GFM supports footnote-style references in supported Markdown rendering contexts.

---

## Unit 3 — Exercise: Communicate using Markdown

Official unit: <https://learn.microsoft.com/en-us/training/modules/communicate-using-markdown/3-communicating-using-markdown>

The integrated exercise requires a real Markdown artifact rather than multiple-choice-only practice.

On `lab/module-08-markdown`, create/update:

```text
labs/module-08/markdown-showcase.md
```

The file must demonstrate:

1. hierarchical headings;
2. bold and italic text;
3. ordered and unordered lists;
4. a task list with at least one checked and one unchecked item;
5. an external link;
6. an image with useful alt text;
7. inline code;
8. a fenced code block with language highlighting;
9. a table;
10. a blockquote;
11. a repository Issue/PR reference;
12. a mention syntax example;
13. a GitHub alert/callout;
14. a small Mermaid diagram or another supported rich-Markdown feature;
15. readable organization and concise prose.

The engine validates the required syntax patterns and then asks the learner to use the same Markdown in an Issue comment so they see both source and rendered forms.

---

## Unit 4 — Module assessment

Official unit: <https://learn.microsoft.com/en-us/training/modules/communicate-using-markdown/4-knowledge-check>

The integrated assessment covers:

- core Markdown syntax;
- GitHub Flavored Markdown;
- task lists;
- links/images;
- code formatting;
- tables;
- mentions/references;
- closing keywords;
- appropriate use of Markdown across GitHub surfaces.

---

## Unit 5 — Summary

Official unit: <https://learn.microsoft.com/en-us/training/modules/communicate-using-markdown/5-summary>

After completing the module you should be able to write clear GitHub-native documentation and collaboration messages without relying on a rich-text editor.

## Official references

- Microsoft Learn module: <https://learn.microsoft.com/en-us/training/modules/communicate-using-markdown/>
- GitHub Docs — Basic writing and formatting syntax: <https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax>
- GitHub Flavored Markdown specification: <https://github.github.com/gfm/>
