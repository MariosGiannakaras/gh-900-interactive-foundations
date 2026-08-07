#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path

import runtime_protocol

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / ".gh900" / "data"
TEMPLATES = ROOT / ".gh900" / "templates"

ACTIVITY_OVERRIDES = set()
SCENARIO_OVERRIDES = {"m03-u07", "m07-u06", "m12-u05", "m13-u05"}
CHECKPOINT_OVERRIDES = {"m16-u03"}
PR_ACTIVITY_MODULES = {2, 9, 14}
REFLECTION_MODULES = {4, 5, 6, 11, 14, 16}


@dataclass(frozen=True)
class Unit:
    id: str
    part: int
    module: int
    number: int
    title: str
    mode: str
    branch: str | None
    sandbox: str | None
    content_path: str
    detail_path: str | None
    module_units: int
    ordinal: int


def _catalog() -> dict[str, dict[str, object]]:
    return json.loads((DATA / "course-catalog.json").read_text(encoding="utf-8"))


def load_units() -> list[Unit]:
    manifest = (DATA / "official-curriculum.yml").read_text(encoding="utf-8")
    catalog = _catalog()
    rows = re.findall(
        r"\{\s*id:\s*(m\d{2}-u\d{2}),\s*title:\s*(.*?),\s*implementation:\s*[^}]+\}",
        manifest,
    )
    counts = {
        int(m): int(c)
        for m, c in re.findall(
            r"(?ms)^      - id: m(\d{2})\n.*?^        unit_count: (\d+)",
            manifest,
        )
    }
    units: list[Unit] = []
    for ordinal, (unit_id, title) in enumerate(rows, start=1):
        module = int(unit_id[1:3])
        number = int(unit_id[-2:])
        part = 1 if module <= 8 else 2
        lower = title.strip().lower()
        if unit_id in CHECKPOINT_OVERRIDES:
            mode = "checkpoint"
        elif unit_id in SCENARIO_OVERRIDES:
            mode = "scenario"
        elif unit_id in ACTIVITY_OVERRIDES or "exercise" in lower:
            mode = "activity"
        elif "assessment" in lower or "knowledge check" in lower:
            mode = "assessment"
        elif lower == "summary":
            mode = "summary"
        else:
            mode = "read"
        branch = f"lab/{unit_id}" if mode == "activity" else None
        sandbox = f"sandbox/{unit_id}" if mode == "activity" else None
        item = catalog[f"{module:02d}"]
        units.append(
            Unit(
                unit_id,
                part,
                module,
                number,
                title.strip(),
                mode,
                branch,
                sandbox,
                str(item["readme"]),
                str(item["detail"]) if item.get("detail") else None,
                counts[module],
                ordinal,
            )
        )
    if len(units) != 106:
        raise RuntimeError(f"Expected 106 units, parsed {len(units)}")
    return units


def find(unit_id: str) -> Unit:
    for unit in load_units():
        if unit.id == unit_id:
            return unit
    raise KeyError(unit_id)


def next_unit(unit_id: str) -> Unit | None:
    units = load_units()
    for i, unit in enumerate(units):
        if unit.id == unit_id:
            return units[i + 1] if i + 1 < len(units) else None
    raise KeyError(unit_id)


def extract_local_section(unit: Unit) -> str:
    text = (ROOT / unit.content_path).read_text(encoding="utf-8")
    pattern = rf"(?ms)^## Unit {unit.number}\b[^\n]*\n(.*?)(?=^---\s*$|^## Unit \d+\b|^## Official references\b|\Z)"
    match = re.search(pattern, text)
    if not match:
        raise RuntimeError(f"No learner content found for {unit.id}")
    section = match.group(1).strip()
    section = re.split(
        r"(?mi)^## (?:Interactive(?:\s+course\s+flow|\s+lab(?:\s*/\s*enterprise\s+simulation)?|\s+identity\s+simulation)?|Hands-on/simulation layer)\s*$",
        section,
        maxsplit=1,
    )[0].strip()
    return section


def extract_detail_section(unit: Unit) -> str:
    if not unit.detail_path:
        return ""
    path = ROOT / unit.detail_path
    if not path.exists():
        return ""
    text = path.read_text(encoding="utf-8")
    pattern = rf"(?ms)^## {re.escape(unit.id)}\s*$\n(.*?)(?=^## m\d{{2}}-u\d{{2}}\s*$|\Z)"
    match = re.search(pattern, text)
    return match.group(1).strip() if match else ""


def _assessment_file(module: int) -> Path:
    if module == 1:
        return TEMPLATES / "labs" / "module-01" / "assessment.md"
    return TEMPLATES / "labs" / f"module-{module:02d}" / "submission.md"


def assessment_questions(module: int) -> tuple[str, int]:
    text = _assessment_file(module).read_text(encoding="utf-8")
    if module != 1 and "## Knowledge check" in text:
        text = text.split("## Knowledge check", 1)[1]
    sections = re.split(r"(?=^#{2,3} Q\d+\s*$)", text, flags=re.MULTILINE)
    rendered: list[str] = []
    count = 0
    for section in sections:
        header = re.match(r"^#{2,3} Q(\d+)\s*$", section, flags=re.MULTILINE)
        if not header:
            continue
        count += 1
        qnum = header.group(1)
        body = re.sub(r"^#{2,3} Q\d+\s*$", "", section, count=1, flags=re.MULTILINE).strip()
        body = re.sub(r"(?m)^- \[[ xX]\] ([A-C])\.\s*", r"- **\1.** ", body)
        rendered.append(f"### Question {qnum}\n\n{body}")
    if not rendered:
        raise RuntimeError(f"No assessment questions found for Module {module}")
    return "\n\n".join(rendered), count


def scenario_instruction(unit: Unit) -> str:
    prompts = {
        "m03-u07": """A paid/enterprise billing environment is not required. Make the same administration decisions in a structured checkpoint.

Reply using this shape (hyphens may replace spaces inside values):

`/scenario usage=<what-is-consumed> cost=<what-is-charged> dimension=<product|sku|repository|organization|period|date|runner> decision=<what-you-verify-before-acting>`

Example structure only: `usage=runner-minutes cost=billed-amount dimension=repository decision=verify-budget-and-included-allowance`.""",
        "m07-u06": """If your account can create a real Project, inspect the relevant field/workflow/insight UI while making the choices below. If not, the same decisions are validated without requiring organization permissions.

Reply with:

`/scenario trigger=<automation-trigger> field=<status|priority|iteration|assignee|date> insight=<chart|view|burnup|status|progress|iteration> reason=<why-this-combination-helps>`""",
        "m12-u05": """A public course should not require buying GitHub Enterprise or changing a real company's governance. Choose the appropriate administrative scope and least-privilege role instead.

Reply with:

`/scenario scope=<repository|organization|enterprise> role=<specific-role-or-permission> least_privilege=<yes|enforced|limited|minimum> reason=<why-this-is-the-smallest-correct-scope>`""",
        "m13-u05": """A real corporate IdP is optional. Model the identity lifecycle explicitly so authentication, provisioning, and team membership cannot be confused.

Reply with:

`/scenario idp=<provider-or-group> team=<github-team> sync=team-sync auth=saml provisioning=scim`""",
    }
    return prompts[unit.id]


def checkpoint_instruction(unit: Unit) -> str:
    if unit.id != "m16-u03":
        raise KeyError(unit.id)
    return """### Interactive setup checkpoint

The official Microsoft exercise is **Set up GitHub Copilot to work with Visual Studio Code**. This course does not require you to buy Copilot and does not pretend that Actions can see private editor telemetry.

**If Copilot is available:**
1. Open Visual Studio Code or a Codespace.
2. Confirm GitHub sign-in and locate Copilot/Chat or inline suggestions.
3. Review at least one suggestion interaction (accept/reject/cycle is sufficient).
4. Confirm that the Python environment you will use later is available.

Submit, for example:

`/checkpoint access=available editor=vscode signin=confirmed interface=both suggestion=reviewed python=ready copilot=located`

**If Copilot is unavailable:**
1. Open/review the official Microsoft Learn exercise linked above.
2. Follow the setup steps conceptually in VS Code or a Codespace without claiming Copilot was actually used.
3. Complete the course fallback by identifying sign-in, Copilot UI, suggestion review, and Python-environment steps.

Submit, for example:

`/checkpoint access=unavailable editor=vscode signin=understood interface=understood suggestion=understood python=understood official=reviewed fallback=completed`

> [!NOTE]
> This checkpoint validates the required setup decisions honestly; it does not fabricate proof of an entitlement or editor action that GitHub Actions cannot observe."""


def _activity_steps(unit: Unit) -> str:
    m = unit.module
    if m == 1:
        return """1. Verify Git and use Git help from the terminal.
2. Configure a **repository-local** Git name/email (a GitHub `noreply` address is appropriate if desired).
3. Complete the CLI edit/stage/commit practice in `exercise/version-control-notes.md`.
4. Use VS Code Source Control for the `exercise/vscode-branch.txt` change and commit.
5. Use `git status`, `git log`, and the graph/history views to inspect the commits you created.
6. Use `exercise/diff-practice.txt` to compare working-tree, staged, and committed differences; stage and unstage as instructed.
7. Create a temporary practice branch, make a change, return to the learner branch, and merge with a visible non-fast-forward merge commit.
8. Push the completed learner branch to GitHub. The validator requires real changed fixtures, multiple commits, and visible merge history."""
    if m == 2:
        return f"""1. Work in `exercise/github-flow.md` and make a focused change.
2. Create an Issue whose title includes **`[GH-900 {unit.id}]`** and use it to track the exercise.
3. Commit and push your learner-branch change.
4. Open a Pull Request from **`{unit.branch}`** into **`{unit.sandbox}`**.
5. Link the Pull Request to the exercise Issue.
6. Inspect the PR **Conversation** and **Files changed** views.
7. Merge the PR when your change and metadata are complete.
8. Observe the linked Issue/PR state and resulting branch history."""
    if m == 4:
        return """1. Inspect the repository **Security** area and identify where code-scanning alerts/configuration would appear.
2. Complete `.github/workflows/module-04-codeql.yml` as an **advanced-style** CodeQL configuration: keep push, pull-request, and scheduled trigger concepts and document the language/build strategy you would use.
3. Complete `exercise/code-scanning-simulation.yml`, including SARIF 2.1.0 and upload constraints from the lesson.
4. Inspect `exercise/sample.sarif.json` and connect an external SARIF-producing scanner to the `upload-sarif` model conceptually.
5. If repository policy allows the temporary workflow to run, inspect the corresponding Actions run. If it does not, explain the expected run/configuration instead.
6. In this course Issue, post **`/reflection ...`** comparing **default setup, advanced setup, and external SARIF**, and mention what you observed/expected in Security or Actions.
7. Commit and push the temporary configuration."""
    if m == 5:
        return """1. Open the temporary workspace in Codespaces or VS Code.
2. Confirm Copilot access if available; if it is unavailable, use the clearly marked prompt-review fallback rather than claiming Copilot was used.
3. Read the required behavior before coding.
4. Use inline suggestions, chat, or agent assistance where available.
5. Implement `exercise/copilot-practice.py` so input is validated and the result is deterministic/readable.
6. Keep/add executable tests in `exercise/test_copilot_practice.py` and run them.
7. Review generated/suggested code manually rather than accepting it blindly.
8. Post **`/reflection ...`** describing the Copilot interaction mode (or fallback) and at least one suggestion you rejected or changed.
9. Commit and push the final implementation."""
    if m == 6:
        return """1. Create/open a Codespace for the learner branch if available to your account.
2. Verify repository and branch state from the Codespaces terminal.
3. Inspect and customize `.devcontainer/devcontainer.json` with a meaningful repository-level development-container setting.
4. Rebuild the Codespace, or describe the rebuild action if the environment already matches the desired configuration.
5. Run a sample terminal command/test and commit the customization.
6. Compare the capability with **github.dev**: identify what requires Codespaces compute/terminal access.
7. Distinguish **stopping** a Codespace from **deleting** it.
8. Post **`/reflection ...`** confirming the observed Codespaces/github.dev/stop-vs-delete behavior.
9. Push the branch; repository configuration is validated automatically."""
    if m == 8:
        return """Complete `exercise/markdown-showcase.md` so it demonstrates all of the following in one coherent artifact:

1. at least two heading levels;
2. **bold** and *italic* emphasis;
3. ordered and unordered lists;
4. a task list with checked and unchecked items;
5. an external link;
6. an image with meaningful alt text;
7. inline code;
8. a fenced, language-tagged code block;
9. a table;
10. a blockquote;
11. an Issue/PR-style reference;
12. mention syntax;
13. a GitHub alert/callout;
14. a Mermaid diagram or another supported rich-Markdown feature;
15. readable organization and concise prose.

Commit and push the Markdown artifact. The Issue remains the instruction surface; the file exists only because authoring Markdown is the exercise."""
    if m == 9:
        return f"""1. Open the temporary Issue titled for **`{unit.id}`**, confirm it is not assigned to somebody else, and comment your intent to work on it.
2. Make the requested focused documentation improvement in `exercise/open-source-pr.md`.
3. Commit and push the learner branch.
4. Open a Pull Request from **`{unit.branch}`** into **`{unit.sandbox}`** and link the temporary Issue.
5. Inspect the automated status check and the automated training review comment posted by the course.
6. Respond to that review comment in the PR, update the branch with another commit, and inspect the updated check/diff.
7. Merge the PR when the contribution is ready.

This reproduces Issue communication, branch/PR/status-check/review/update/merge mechanics inside the safe learner repository."""
    if m == 10:
        return """Build the temporary repository as a realistic InnerSource project by completing **all** generated artifacts:

1. `exercise/README-sample.md` — purpose, consumers, setup/use, support, contribution entry point;
2. `exercise/CONTRIBUTING.md` — development setup, branch/PR workflow, tests, review and help;
3. `exercise/CODEOWNERS` — meaningful ownership examples;
4. `exercise/ISSUE_TEMPLATE/feature.yml` — structured feature-request intake;
5. `exercise/PULL_REQUEST_TEMPLATE.md` — change, validation, review/ownership prompts;
6. `exercise/discoverability-plan.md` — naming, description, topics, README/catalog/support ownership;
7. `exercise/access-visibility-matrix.md` — visibility/permission roles and least privilege;
8. `exercise/success-metrics.md` — cross-team contribution, response time, reuse/adoption and qualitative onboarding signals.

Commit and push the completed InnerSource toolkit. Every artifact is temporary and is removed with the unit branch after validation."""
    if m == 11:
        return """Secure the temporary repository supply-chain exercise:

1. create root `SECURITY.md` with a responsible vulnerability-disclosure process;
2. create `.gitignore` that protects a local-secret path such as `exercise/local-secret.env` (do **not** commit a real secret);
3. create `.github/dependabot.yml` for the supplied npm/package manifest;
4. create `.github/CODEOWNERS` with ownership for `/exercise/sensitive/`;
5. inspect the supplied `package.json` as dependency-graph/Dependabot input;
6. in **`/reflection ...`**, design repository rules requiring PRs, checks and meaningful review, and explain secret remediation using **revocation/rotation plus appropriate history handling**, not merely deleting the latest file;
7. where available, inspect Dependabot/code-scanning/secret-scanning surfaces under Security;
8. commit and push the configuration. Only fake training data is used."""
    if m == 14:
        return f"""1. Make the Pull Request exercise contain **multiple learner commits** while fixing the intentional defect in `exercise/review_fixture.py`; keep `exercise/test_review_fixture.py` passing.
2. Open the PR from **`{unit.branch}`** into **`{unit.sandbox}`** as a **draft**.
3. Inspect Conversation, Commits, Checks and Files changed.
4. Convert the PR to **Ready for review**.
5. Add an **inline review comment** on the changed code/intentional defect.
6. Push an additional update resolving the review point and inspect the resulting diff/check state.
7. Post **`/reflection ...`** comparing merge commit, squash, and rebase implications for history.
8. Merge the temporary training PR using an allowed merge method. The course records draft/ready transitions and cleans the branches afterward."""
    if m == 15:
        return f"""This unit is a history investigation. The course has prepared a regression Issue and a fixture branch, while **you** create the temporary PR so the repository can keep GitHub Actions on secure defaults.

1. Open the temporary Module 15 regression Issue.
2. Create a Pull Request titled **`[GH-900 {unit.id}] History fixture PR`** from **`fixture/{unit.id}`** into **`{unit.sandbox}`** and link the regression Issue.
3. Inspect the PR's **Commits** and **Files changed**, then merge it. Note the regression commit SHA shown in the PR before moving on.
4. Use GitHub search to locate the now-merged PR, the regression commit, and the related Issue from repository context.
5. Open **Blame** for `exercise/history-fixture.txt` on **`{unit.sandbox}`** and compare the commit/history shown there with the PR history (merge method can affect the visible target-branch commit).
6. Apply the prepared `gh900-history` label and the prepared Module 15 milestone to the regression Issue, and assign the Issue to yourself.
7. Add an Issue comment containing an `@mention`, the historical PR reference, and the regression commit SHA from the PR.
8. Back in the course Issue, submit **`/investigation issue=#N pr=#N commit=<regression-commit-sha> explanation=<what-the-linked-history-tells-you>`**.
9. Comment `/check` when the investigation and Issue metadata are complete."""
    if m == 16:
        return """Update the supplied FastAPI exercise while preserving the independently written implementation target:

1. add a Pydantic request model with `text: str`;
2. add POST `/analyze-text`;
3. accept JSON matching the request model;
4. return a deterministic checksum/hash and input length;
5. add any imports needed by the implementation;
6. reject/handle invalid empty input appropriately;
7. update/add automated tests and run `exercise/test_app.py`;
8. run the API and verify the endpoint through `/docs` or an HTTP request where your environment permits it;
9. use Copilot iteratively when available, or the clearly marked prompt-review fallback when not;
10. post **`/reflection ...`** describing prompt iterations and at least one Copilot suggestion you rejected or modified;
11. commit and push the final tested implementation."""
    return "Complete the GitHub/repository task described in this unit and push the resulting temporary learner state."


def _where_to_click(unit: Unit) -> str:
    blocks = {
        2: "**Issue:** Issues → New issue. **PR:** Pull requests → New pull request → set base to the temporary `sandbox/...` branch and compare to `lab/...`.\n\nIf the branches are not visible, refresh after the setup Action finishes.",
        4: "Open **Security → Code scanning** for alerts/setup surfaces and **Actions** for workflow runs. Some code-scanning UI depends on repository/account capabilities; use the supplied SARIF/configuration exercise when unavailable.",
        5: "In VS Code/Codespaces, use the Copilot status/menu and Chat/inline suggestion surfaces where available. If unavailable, use the prompt-review fallback in this Issue instead of claiming a Copilot action occurred.",
        6: "Use **Code → Codespaces** to create/open a Codespace. For github.dev press `.` on a repository page or open the web editor. Account quotas/policies can affect Codespaces availability.",
        8: "Edit the generated `exercise/markdown-showcase.md` on the temporary learner branch. Use **Preview** in the editor to compare source with rendered Markdown.",
        9: "Use **Issues** for intent/assignment and **Pull requests** for the contribution. Keep the temporary Issue and PR linked; do not target `main`.",
        11: "Use **Security** to inspect dependency/secret/code-scanning surfaces where available. The required configuration files are created only for this temporary exercise.",
        14: "In the PR use **Conversation**, **Commits**, **Checks**, and **Files changed**. Start as Draft, then use **Ready for review**, add an inline comment from Files changed, and push the follow-up fix.",
        15: "Use repository **Search**, the merged PR **Commits/Files changed**, file **Blame**, and the temporary Issue metadata controls for label, milestone, and assignee.",
        16: "For the API exercise use the temporary branch in VS Code/Codespaces, run the tests, start Uvicorn, then open `/docs`. Copilot is optional; the fallback remains valid when entitlement is unavailable.",
    }
    text = blocks.get(unit.module)
    if not text:
        return ""
    return f"\n\n<details>\n<summary><strong>Where to click / troubleshooting</strong></summary>\n\n{text}\n\n</details>"


def activity_instruction(unit: Unit) -> str:
    pr_note = ""
    if unit.module in PR_ACTIVITY_MODULES:
        pr_note = (
            f"\n\n> [!IMPORTANT]\n> This exercise uses a temporary sandbox. Open any training Pull Request from "
            f"`{unit.branch}` into `{unit.sandbox}` — **not** into `main`. The course removes both branches after validation."
        )
    return (
        "### Hands-on checklist\n\n"
        "The course engine has prepared only what this unit needs. "
        f"Use **`{unit.branch}`** as the learner branch.\n\n"
        f"{_activity_steps(unit)}\n\n"
        "The instructions in this Issue are the source of truth; internal course files are not required reading."
        f"{pr_note}"
        f"{_where_to_click(unit)}\n\n"
        "> [!TIP]\n> Repository pushes/PR events validate automatically when possible. Use `/check` for a recovery/manual recheck."
    )


def continuation(unit: Unit) -> str:
    if unit.mode in {"read", "summary"}:
        extra = ""
        if unit.id == "m08-u05":
            extra = "\n\n> [!IMPORTANT]\n> Completing this step finishes **GitHub Foundations Part 1 of 2**."
        return (f"{extra}\n\n### Continue\n\nWhen ready, comment exactly **`/next`**.").strip()
    if unit.mode == "checkpoint":
        return checkpoint_instruction(unit)
    if unit.mode == "activity":
        return activity_instruction(unit)
    if unit.mode == "scenario":
        return f"### Apply it\n\n{scenario_instruction(unit)}\n\nNo worksheet file is created."
    questions, count = assessment_questions(unit.module)
    return (
        "## Check your understanding\n\n"
        f"{questions}\n\n"
        "### Submit\n\n"
        f"Reply with **`/answer `** followed by {count} letters in question order, separated by spaces. "
        "Example: `/answer A C B ...`. The validator reports only the question numbers that need review."
    )


def _modernize_section(unit: Unit, section: str) -> str:
    if unit.mode != "activity" or not unit.branch:
        return section
    section = re.sub(r"`lab/module-[^`]+`", f"`{unit.branch}`", section)
    section = re.sub(
        r"create the module branch\s+`[^`]+`",
        f"use the temporary learner branch `{unit.branch}` created by the course engine",
        section,
        flags=re.IGNORECASE,
    )
    section = section.replace("create/edit the module lab file", "edit the temporary exercise artifact created for this unit")
    section = section.replace("module lab file", "temporary exercise artifact")
    path_replacements = {
        "m08-u03": {"labs/module-08/markdown-showcase.md": "exercise/markdown-showcase.md"},
        "m10-u03": {
            "labs/module-10/README-sample.md": "exercise/README-sample.md",
            "labs/module-10/CONTRIBUTING.md": "exercise/CONTRIBUTING.md",
            "labs/module-10/CODEOWNERS": "exercise/CODEOWNERS",
        },
        "m15-u03": {"labs/module-15/history-investigation.md": "the `/investigation ...` response in this course Issue"},
    }
    for old, new in path_replacements.get(unit.id, {}).items():
        section = section.replace(old, new)
    if unit.module in PR_ACTIVITY_MODULES:
        section = section.replace("against `main`", f"against `{unit.sandbox}`")
        section = section.replace("into `main`", f"into `{unit.sandbox}`")
    section = section.replace("Our integrated lab", "The interactive exercise")
    section = section.replace("Our integrated exercise", "The interactive exercise")
    section = section.replace("The integrated course", "The interactive exercise")
    section = section.replace("in the learner's own fork", "in the temporary learner workspace")
    section = section.replace("in the learner’s own fork", "in the temporary learner workspace")
    section = section.replace("in the worksheet", "in the course Issue reflection")
    section = section.replace("the worksheet", "the course Issue reflection")
    section = section.replace("delete the merged source branch when instructed", "let the course clean the temporary branches after validation")
    return section


def render(unit: Unit) -> str:
    section = _modernize_section(unit, extract_local_section(unit))
    detail = extract_detail_section(unit)
    merged = section + (f"\n\n### Additional source-audited detail\n\n{detail}" if detail else "")
    progress = round(unit.ordinal / 106 * 100)
    intro = ""
    if unit.id == "m01-u01":
        intro = "> [!NOTE]\n> **Part 1 of 2 starts here.**\n\n"
    elif unit.id == "m09-u01":
        intro = "> [!IMPORTANT]\n> **Part 1 complete. GitHub Foundations Part 2 of 2 starts here.**\n\n"
    return (
        f"{runtime_protocol.lesson_marker(unit.id)}\n"
        f"{intro}"
        f"# {unit.title}\n\n"
        f"| Course position | Progress |\n"
        f"|---|---:|\n"
        f"| Part **{unit.part} / 2** · Module **{unit.module} / 16** · Unit **{unit.number} / {unit.module_units}** | "
        f"**{unit.ordinal} / 106** ({progress}%) |\n\n"
        f"{merged}\n\n---\n\n{continuation(unit)}\n"
    )


def as_dict(unit: Unit) -> dict[str, object]:
    nxt = next_unit(unit.id)
    return {
        "id": unit.id,
        "part": unit.part,
        "module": unit.module,
        "number": unit.number,
        "ordinal": unit.ordinal,
        "module_units": unit.module_units,
        "title": unit.title,
        "mode": unit.mode,
        "branch": unit.branch,
        "sandbox": unit.sandbox,
        "requires_pr": unit.module in PR_ACTIVITY_MODULES if unit.mode == "activity" else False,
        "requires_reflection": unit.module in REFLECTION_MODULES if unit.mode == "activity" else False,
        "next": nxt.id if nxt else None,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--unit")
    parser.add_argument("--first", action="store_true")
    parser.add_argument("--next", action="store_true")
    parser.add_argument("--render", action="store_true")
    parser.add_argument("--list-json", action="store_true")
    args = parser.parse_args()
    units = load_units()
    if args.list_json:
        print(json.dumps([as_dict(u) for u in units], indent=2))
        return 0
    unit = units[0] if args.first else find(args.unit)
    if args.next:
        nxt = next_unit(unit.id)
        if nxt is None:
            return 3
        unit = nxt
    print(render(unit) if args.render else json.dumps(as_dict(unit)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
