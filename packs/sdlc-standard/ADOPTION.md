# Adoption Guide

Getting the SDLC Skill Pack running on a new project. Budget about 30 minutes for steps
1–4; step 5 onward is the project itself.

If you have never run Claude Code before, start at step 0 — it takes another 15 minutes and
assumes nothing.

---

## 0. Prerequisites — from nothing to a working environment

Four things, and the third is the one people miss.

| # | What | Why the pack needs it |
|---|---|---|
| 1 | **Git** | the pack lives in the repository; `sdlc-bug-trace` reads history |
| 2 | **Node.js 18+** and **Claude Code** | runs the pack |
| 3 | **Python 3.9+** | the three guard hooks and the on-edit hook are Python. Without it they fail silently and baseline protection is off |
| 4 | **`openpyxl` / `python-docx`** | only if your deliverables are Excel or Word. See step 0d |

### 0a. macOS

```bash
# Homebrew, if you do not have it
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

brew install git node python@3.12
npm install -g @anthropic-ai/claude-code
claude login          # opens a browser to authenticate
```

### 0b. Windows 10 / 11 (PowerShell as Administrator)

```powershell
winget install --id Git.Git -e
winget install --id OpenJS.NodeJS.LTS -e
winget install --id Python.Python.3.12 -e

# restart PowerShell so PATH picks up node and python, then:
npm install -g @anthropic-ai/claude-code
claude login
```

On Windows, check that `python` resolves to the real interpreter rather than the Microsoft
Store stub — `python --version` must print a version, not open the Store. If it opens the
Store, disable the alias in *Settings → Apps → App execution aliases*.

### 0c. Linux (Debian / Ubuntu)

```bash
sudo apt update && sudo apt install -y git python3 curl
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt install -y nodejs
npm install -g @anthropic-ai/claude-code
claude login
```

### 0d. Document format libraries — only if you need them

Install these when your deliverables are not Markdown. Match them to
`{{profile.templates.formats_enabled}}`:

```bash
pip install openpyxl        # .xlsx deliverables and templates
pip install python-docx     # .docx deliverables and templates
pip install python-pptx     # only to READ .pptx inputs (decision decks, walkthroughs)
```

A format enabled in the profile with no working library is a run that fails forty files in
rather than on the first. `/sdlc-profile-check` check 29 catches it — run it before P2.

### 0e. Verify

```bash
git --version
node --version          # 18 or higher
claude --version
python --version        # or python3 --version; 3.9 or higher
python -c "import openpyxl, docx; print('document libraries ok')"   # only if you installed them
```

All five printing a version means the environment is ready. If `python` works but
`python3` does not (or the reverse), note which one — the hooks in `settings.json` invoke
`python`, and on some Linux distributions that name does not exist. See the FAQ.

---

## 1. Install

```bash
cp -r sdlc-standard/.claude                 <project>/.claude
cp sdlc-standard/profile/sdlc.profile.yaml  <project>/.claude/
```

If the project already has a `.claude/`, merge instead: copy `skills/`, `commands/`,
`agents/`, `rules/sdlc/`, the stack rule directories the project uses (`rules/java/`,
`rules/typescript/`, `rules/react/`, `rules/sql/`), `hooks/`, and merge the `hooks` block of
`settings.json`. Existing `rules/<language>/` files are kept — the pack's `rules/common/` is the
base layer they were already written to extend, and the pack's stack files are named
`<stack>.md` so they sit beside them without overwriting anything. Where an existing file is
the client's coding standard, register it in `system.coding_standards` so it is known to
outrank the pack's stack rules.

## 2. Configure

```
/sdlc-init
```

It inspects the repository first — stack from the build files, build and test commands from
the package scripts, existing document directories — and only asks about what it cannot
determine. Then it writes the profile, scaffolds directories, seeds the registers, and
generates `CLAUDE.md`.

Then:

```
/sdlc-profile-check
```

Fix every Critical before running any phase. A Critical means the pack's assumptions do not
hold — most often an unfilled stakeholder role, or baseline protection switched off.

## 2b. Take the templates in

**The pack ships no deliverable templates**, and this is deliberate: every organisation has
its own forms, usually Excel, usually contractual, and an invented one is rejected at the
first review — after a whole category has been generated into it.

`/sdlc-init` asks for them. If you skipped it, or a new category starts later:

```
/sdlc-template-register             # inventory: which categories have a form, which do not
/sdlc-template-register screen      # register one
/sdlc-template-register --check     # validate without changing the registry
```

Three things it does that are worth knowing about:

- **It opens the file**, derives the field map from the placeholders it finds, and prints
  it. An unrecognised placeholder is asked about, not guessed.
- **It reports the gap against the category skill** in three classes: sections the template
  has and the skill does not describe, content the skill requires that the template has
  nowhere to put, and conflicts with an invariant rule. Once, now — not once per document,
  later.
- **It runs a fidelity check** on the first template of each binary format: write one value
  into each field, then diff everything else. If a round-trip through your form destroys
  merged ranges or the print area, you want to know before forty files exist.

Set `templates.on_missing` deliberately. `ask` is the default and the safest. `skeleton` —
generate from the pack's own structure — is legitimate for a team that has agreed to it, but
it is an agreement recorded as a `DEC-*`, not a fallback.

## 3. Decide the four things that are expensive to change later

### 3a. The identity scheme

- **Module id pattern.** If the organisation already has a screen or program numbering
  convention, use it. Every conversation with their team becomes directly usable.
- **Surface suffixes.** One per form factor, distinguishable at a glance.
- **Business areas** for the `{AREA}` segment. These become the batching unit for every
  generation run, so pick areas of roughly comparable size.

Write the answers into the profile before cataloguing anything. Renumbering after P0
invalidates every downstream reference (ID-05).

### 3b. Who owns which decision

Fill every role in `stakeholders`. A decision with no owner cannot be recorded, and an
unrecorded decision is an assumption that will be discovered at UAT (RS-02). This is the
field teams leave as a placeholder and then spend the project working around.

### 3c. The delivery model and contract type

They set how hard a gate blocks and how strict change control is. A fixed-price project
where CRs are handled informally is a fixed-price project that will absorb them.

### 3d. The quality targets

`quality.targets` ships with plausible defaults. **They are placeholders for your own
historical numbers, not industry constants.** Set them from your organisation's data, agree
them with the team, then hold them. A target nobody agreed to is a target nobody will act
on — and it will be quietly moved the first time a gate would fail.

## 3e. Confirm the model and effort

<!-- model-policy:claude -->
`/sdlc-init` resolves `execution.model_profile` (default `balanced`: Opus at `high` effort for
the analysis, design and review roles, Sonnet at `medium` for the production roles — see README
"Model policy") into the `model:` and `effort:` frontmatter of every agent file. Agree the
profile with the team before the first generation run.

`execution.intended_effort` is different: it is the effort for your own session, where the
commands run. Claude Code takes that level from `/effort`, not from the profile, so set it there.

`/sdlc-profile-check` compares the profile against the agent frontmatter and warns when they
disagree. Drift here is easy to miss, because an agent running on the wrong model or effort still
produces plausible-looking deliverables.
<!-- /model-policy:claude -->

## 4. Verify the pack is live

- Open a new session — the profile check must report clean.
- Baseline a throwaway document (add it to `constraints.baselined`), then ask Claude to edit
  it — the hook must block with `[BL-02]`. **If it does not block, the hooks are not
  running**, and every baseline guarantee in this pack is off. See the FAQ.
- Run `/sdlc-trace-check` — it should report an empty register, not an error.
- Run `/sdlc-template-register --check` — every registered template resolves, and every
  enabled format has its library.
- If `{{profile.mockup.kind}}` is not `none`, confirm the surfaces in `mockup.surfaces` all
  name real `system.surfaces[]` entries.
- If infrastructure matters on this project, run `/sdlc-generate-infra` with no argument —
  the inventory tells you whether the platform fields resolve and whether the pipeline's
  environments match the profile (X-12).

## 5. Run the phases

Do not run them all at once. Each gate exists because the next phase amplifies the previous
phase's errors:

```
/sdlc-discover                → review scope with the client      → gate P0
/sdlc-generate-requirements   → SRS review and sign-off           → gate P1  (SRS baselined)
/sdlc-generate-basic-design   → /sdlc-review-design               → gate P2
/sdlc-generate-mockup         → X-11 against the screen design    → gate P2
/sdlc-generate-detail-design  → resolve drift items               → gate P3
/sdlc-scaffold-codebase       → once, after the architecture is approved
/sdlc-generate-infra          → pipeline, environments, monitors
/sdlc-implement-feature       → per module
/sdlc-generate-test ut|it     → per module / flow
/sdlc-generate-test st        → whole system, on staging          → gate P7
/sdlc-uat-prepare → _triage → _report                             → gate P8
/sdlc-release-check           → go/no-go → cutover
/sdlc-maintain-*              → per incident
/sdlc-cr-*                    → per change request, whenever one arrives
```

Each generation phase is run as a loop, not a single pass: execute → review in a fresh
session → `/sdlc-refine-skill` → re-execute. Calibrate the loop on a 2–3 module pilot
before generating a whole category. See [COMMAND-FLOW.md](COMMAND-FLOW.md).

---

## Adopting mid-project

The common case: the project started without the pack and is at P3 or P4.

1. **Do not back-fill P0 and P1 as documents.** Back-fill the **registers**: the decision
   log, the assumption log, and the traceability rows for what already exists. Those are
   what the gates need.
2. **Baseline what is already agreed.** Add the documents the client has approved to
   `constraints.baselined`, with their real approval dates. From that point, change control
   works.
3. **Start the traceability register from the current phase forward.** A complete register
   from here is worth more than an invented one from the start.
4. **Run `/sdlc-trace-check` and expect a bad first report.** The downward orphans are real
   scope you cannot yet prove is covered; the upward orphans are real work nobody
   requested. Both are findings worth having early.
5. **Run the P-gate you are entering, not the ones you skipped.** Retroactive gates produce
   paperwork; the next gate produces decisions.

---

## Extending the pack for one project

Add project-specific material as **new** files, prefixed with the project key, alongside the
pack rather than inside it:

```
.claude/skills/<key>_design_system/SKILL.md      UI design system for this product
.claude/skills/<key>_domain_glossary/SKILL.md    domain terms and their meanings
.claude/rules/<stack>/client-standard.md         the client's coding standard, digested (outranks <stack>.md)
```

Keep the `sdlc-*` files unmodified so the pack can be updated. When you find yourself
editing an `sdlc-*` file, ask whether the change is project-specific — if so it belongs in a
`<key>_*` file; if not, it belongs upstream in the pack.

Register new skills in the profile where they own a design category
(`paths.bd_categories[].skill`).

## Common adoption mistakes

| Mistake | Consequence |
|---|---|
| Filling the profile with plausible guesses instead of `<placeholders>` | invented values reach deliverables and look authoritative |
| Leaving stakeholder roles unset | decisions have no owner; every assumption stays open |
| Copying the default quality targets without agreeing them | the first gate that would fail moves the target instead |
| Writing requirements before scope is agreed | they get rewritten when it is |
| Skipping the NFR section because "we'll tune it later" | P7 has nothing to measure, and the architecture cannot deliver what nobody specified |
| Treating UAT as a phase the vendor runs | the client accepts a system they never exercised |
| Running ST as "IT again, on staging" | the month-end process, the failover and the volume case are tested never |
| Attributing every defect to the coding phase | phase containment reports 100% upstream and tells you nothing |
| Turning off a review family to reduce findings | the findings still exist, now invisible |
| Editing `sdlc-*` skills for one project's quirk | the pack stops being updatable |
| Treating the traceability register as end-of-project paperwork | it becomes unreconstructable and the gates become unverifiable |
| Generating a category before registering the client's template | the whole category is rejected on formatting, after it is finished |
| Enabling `xlsx` without installing `openpyxl` | the run fails forty files in, not on the first |
| Letting the mockup lead the screen design | behaviour enters the system through a prototype nobody traced (MU-01) |
| Writing into infrastructure another team owns | two sources of truth, and the other team reconciles neither |
| Leaving `python` unavailable so the hooks fail silently | baseline protection is off and nothing says so |

---

## Troubleshooting

### The hooks do not fire — I can edit a baselined document

The most important failure in this list, because nothing announces it. Check in order:

1. **Is `python` on PATH?** `settings.json` invokes `python`, not `python3`. On many Linux
   distributions and some macOS setups only `python3` exists. Either install the alias or
   change the three commands in `.claude/settings.json` to `python3`.
2. **Is `CLAUDE_PROJECT_DIR` resolving?** The hook paths are
   `$CLAUDE_PROJECT_DIR/.claude/hooks/...`. Run the hook by hand to see the real error:
   `echo '{"tool_input":{"file_path":"x"}}' | python .claude/hooks/guard-protected-paths.py`
3. **Did you merge `settings.json` rather than copying it?** A project that already had a
   `settings.json` keeps its own; the pack's `hooks` block has to be merged in by hand.
4. **Is the document actually in `constraints.baselined`?** The guard reads that list. A
   document called "final" that is not in the list is not protected.

Verify with the step-4 test: add a throwaway document to `constraints.baselined`, ask for an
edit, and require the `[BL-02]` message. Do this once per machine, not once per project.

### `[BL-02] BLOCKED` on a document I am supposed to be changing

Working as designed. A baselined document changes through a change request:
`/sdlc-cr-analyze` → `/sdlc-cr-design`, which writes the CR id to `.claude/.active_cr` and
unblocks the edit until `/sdlc-cr-report` clears it.

For a genuine editorial fix that changes no meaning, write `EDITORIAL` to
`.claude/.active_cr` for the duration and note it in the revision history. If you have to
think about whether it changes meaning, it changes meaning.

### An `.active_cr` file is left behind and everything is editable

`/sdlc-cr-report` removes it; an interrupted CR does not. `/sdlc-profile-check` reports the
active CR at the bottom of its output for exactly this reason. Delete the file when the CR
is closed.

### `/sdlc-generate-basic-design` produced Markdown, but the client wants Excel

The template was not registered, and `templates.on_missing` was `skeleton` rather than
`ask`. The run should have said so in its plan — that line is the warning.

Register the template (`/sdlc-template-register`), set `on_missing: ask`, then regenerate.
Regenerating is the right move: converting forty Markdown files into the client's form by
hand costs more and produces inconsistencies the cross-checks will not catch.

### Excel output lost the formatting / merged cells / print area

Three usual causes, in order of likelihood:

1. **The file was rebuilt rather than filled.** `pandas.to_excel` discards everything that
   makes the form a form. Load the template with `openpyxl` and write into cells.
2. **A write landed in a non-anchor cell of a merged range** and was silently dropped. Write
   to the top-left cell of the merge; find it in `ws.merged_cells.ranges`.
3. **Rows were inserted**, shifting formulas, merges and the print area. Prefer a template
   with enough pre-formatted rows; where you must insert, re-verify afterwards.

Run the DIO-03 fidelity check on the first file of a category, not the fortieth.

### `openpyxl` / `python-docx` not found, mid-run

`/sdlc-profile-check` check 29 catches this before P2. Install the library, or remove the
format from `templates.formats_enabled` — an enabled format with no library is a promise the
pack cannot keep.

### A category came out short — files are missing and nothing failed

The known failure mode of long generation runs: context runs out and the last categories are
silently dropped. The pack's countermeasures are in `sdlc-basic-design` — batch by module,
10–20 files per call, give the late categories their own dedicated calls, and **count the
files on disk after each batch** rather than trusting the agent's report.

If it already happened, `/sdlc-generate-basic-design <category>` regenerates one category.
The plan's `written/expected` line is what tells you which.

### The mockup and the screen design disagree

That is X-11 doing its job, and the answer is never "update whichever is easier". Decide
against the baselined SRS. Where the SRS is silent, it is an open question with an owner —
raise it rather than choosing (MU-01).

If the mockup has a field the design does not, that field is unrequested scope (RS-06) until
somebody produces a requirement for it.

### `/sdlc-generate-infra` refuses to write anything

`infrastructure.owner` is not `this project`, or `repo_may_write_infra` is `false`. That is a
configuration choice, and usually the correct one — it means another team owns the pipeline.
The command produces proposals instead. Change the field only if the ownership actually
changed.

### The pipeline is green but the phase gate fails

Correct, and worth understanding rather than working around. A pipeline asserts what it can
run: build, typecheck, lint, unit tests. It cannot assert that a requirement is testable,
that a design matches the SRS, or that a defect was attributed to the right injection phase.
`/sdlc-phase-gate` evaluates the assertions the pipeline cannot (IN-03).

### `/sdlc-trace-check` reports hundreds of orphans on a project we adopted mid-flight

Expected, and the report is worth keeping. See *Adopting mid-project* above: back-fill the
registers rather than the documents, start the register from the current phase forward, and
treat the first report as a finding list rather than a failure. The downward orphans are
scope you cannot yet prove is covered; the upward orphans are work nobody requested.

### Agents are running on a model nobody chose

<!-- model-policy:claude -->
`/sdlc-profile-check` check 22 compares what `execution.model_profile` and the overrides resolve
to against the `model:` and `effort:` frontmatter of every agent file. Drift happens when the pack
is updated and `/sdlc-init` is not re-run. Re-run its model-policy step, or fix the frontmatter.

The session's own effort is set with `/effort`; `execution.intended_effort` records the level the
team agreed.
<!-- /model-policy:claude -->

### The pack feels too heavy for this project

Read [`profile/PROFILE-RECIPES.md`](profile/PROFILE-RECIPES.md) recipe 7. It is about
switching things off deliberately — fewer categories, three test levels instead of four, no
detail-design documents — and it names the five things that stay on whatever the project
size. An unplanned partial adoption tends to drop exactly the parts that were load-bearing.
