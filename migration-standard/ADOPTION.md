# Adoption Guide

Getting the Migration Skill Pack running on a new project. Budget about 30 minutes for
steps 1–4; step 5 onward is the project itself.

If you have never run Claude Code before, start at step 0 — another 15 minutes, and it
assumes nothing.

---

## 0. Prerequisites — from nothing to a working environment

Four things, and the third is the one people miss.

| # | What | Why the pack needs it |
|---|---|---|
| 1 | **Git** | the pack lives in the repository; `mig_bug_trace` reads history |
| 2 | **Node.js 18+** and **Claude Code** | runs the pack |
| 3 | **Python 3.9+** | the three guard hooks are Python. Without it they fail silently — and in this pack that means **the legacy tree is writable** |
| 4 | **`openpyxl` / `python-docx`** | only if your deliverables or legacy inputs are Excel or Word. See 0d |

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

Check `python` resolves to the real interpreter, not the Microsoft Store stub — `python
--version` must print a version, not open the Store. If it opens the Store, disable the alias
in *Settings → Apps → App execution aliases*.

Windows matters more on migration work than elsewhere: legacy source is frequently checked
out with CRLF endings and non-UTF-8 encodings (Shift-JIS, EBCDIC-derived). Do not let git
normalise line endings inside the legacy tree — a `.gitattributes` marking the legacy paths
`-text` keeps `git blame` usable, which LR-01 depends on.

### 0c. Linux (Debian / Ubuntu)

```bash
sudo apt update && sudo apt install -y git python3 curl
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt install -y nodejs
npm install -g @anthropic-ai/claude-code
claude login
```

### 0d. Document format libraries — only if you need them

Match these to `{{profile.templates.formats_enabled}}`:

```bash
pip install openpyxl        # .xlsx deliverables, templates, and legacy exports
pip install python-docx     # .docx deliverables, templates, legacy specifications
pip install python-pptx     # only to READ .pptx inputs (client decision decks)
```

A format enabled with no working library fails forty files into a run rather than on the
first. `/mig_profile_check` check 23 catches it — run it before P2.

### 0e. Verify

```bash
git --version
node --version          # 18 or higher
claude --version
python --version        # or python3 --version; 3.9 or higher
python -c "import openpyxl, docx; print('ok')"   # only if you installed them
```

If `python` works but `python3` does not, or the reverse, note which — the hooks in
`settings.json` invoke `python`, and on some distributions that name does not exist. See the
FAQ.

---

## 1. Install

```bash
cp -r migration-standard/.claude              <project>/.claude
cp migration-standard/profile/migration.profile.yaml  <project>/.claude/
```

If the project already has a `.claude/`, merge instead: copy `skills/`, `commands/`,
`agents/`, `rules/migration/`, `hooks/`, and merge the `hooks` block of `settings.json`.
Existing `rules/<language>/` files are kept — the pack's `rules/common/` is the base layer
they were already written to extend.

## 2. Configure

```
/mig_init
```

It inspects the repository first — legacy kind by file extension, target stack from build
files, build commands from package scripts — and only asks about what it cannot determine.
Then it writes the profile, scaffolds directories, seeds the traceability register, and
generates `CLAUDE.md`.

Then:

```
/mig_profile_check
```

Fix every Critical before running any phase. A Critical means the pack's safety
assumptions do not hold — most often a read-only path that is not actually protected.

## 2b. Take the templates in, and keep the legacy documents separate

**The pack ships no deliverable templates**, deliberately: every organisation has its own
forms, on migration work they are usually Excel and usually contractual, and an invented one
is rejected at the first review — after a whole category has been written into it.

`/mig_init` asks for them. If you skipped it, or a new category starts later:

```
/mig_template_register             # inventory: which categories have a form, which do not
/mig_template_register screen      # register one
/mig_template_register --check     # validate without changing the registry
```

What it does that is worth knowing:

- **Opens the file** and derives the field map from its placeholders. An unrecognised
  placeholder is asked about, not guessed.
- **Reports the gap against the category skill**, once, now — not once per document, later.
- **Checks the form has somewhere to record the `LEG-*` anchor.** Many client forms do not,
  because they were designed for new development. That does not suspend NI-01: the anchors go
  in a section the form does have, and the missing column is reported as a gap.
- **Runs a fidelity check** on the first template of each binary format. If a round-trip
  through your form destroys merged ranges or the print area, you want to know before forty
  files exist.

**Legacy documents go somewhere else.** Old design specifications, operator manuals and
handover packs belong in `{{profile.templates.legacy_documents_dir}}`, not in the template
root. They are read-only inputs, and under DIO-08 they are evidence of **intent, never of
behaviour** — the legacy code is the oracle. A project that anchors deliverables to a
ten-year-old specification has documented what somebody intended in 2011, and the client
finds that out at parallel run.

## 3. Decide the identity scheme — once

The one decision that is expensive to change later. Before P0:

- **Module id pattern.** Prefer the legacy system's own screen/program ids if it has
  stable ones. Keeping them makes every conversation with the client's team about the old
  system directly usable.
- **Surface suffixes.** One per form factor, distinguishable at a glance.
- **Business areas** for the `{AREA}` segment. These become the batching unit for every
  generation run, so pick areas of roughly comparable size.

Write the answers into the profile before cataloguing anything. Renumbering after P0
invalidates every downstream reference (ID-04).

## 3b. Confirm the model and effort

`/mig_init` writes `execution.agent_model` (default `opus`) into every agent file. Effort
is session-level and cannot be set from the profile — `execution.intended_effort` only
records what the project expects, so agree it with the team and set it in your session.

Check the two do not drift apart: `/mig_profile_check` compares the profile against the
agent frontmatter and warns when they disagree. Drift here is easy to miss, because an
agent running on the wrong model still produces plausible-looking deliverables.

## 3c. Decide the three fields that decide what counts as a defect

Unique to a migration, and all three are cheap now and contentious later.

- **`mockup.fidelity`** — `as-is`, `restyled` or `redesigned`. It decides whether a moved
  field is a defect or a deliverable. `as-is` is the default because the client is usually
  buying the same work, cheaper to maintain. `redesigned` needs a funded, written decision.
- **`infrastructure.coexistence.system_of_record`** — which system owns the data while both
  are live. Two writers with no stated conflict rule is the defect class that ends
  migrations.
- **`infrastructure.parallel_run.tolerance`** — `exact`, or a named list of fields allowed
  to differ, each with a reason. "Minor formatting differences" is not an exception list; it
  is the absence of one, and it turns the parallel run into a formality.

## 4. Verify the pack is live

- Ask Claude to edit a file under the legacy root — the hook must block it with `[LR-01]`.
  **If it does not block, the hooks are not running**, and the pack's whole safety model is
  off. See the FAQ.
- Open a new session — the profile check must report clean.
- Run `/mig_trace_check` — it should report an empty register, not an error.
- Run `/mig_template_register --check` — every registered template resolves, every enabled
  format has its library, and no legacy document is registered as a template.
- If `{{profile.mockup.kind}}` is not `none`, confirm every id in `mockup.surfaces` names a
  real `target.surfaces[]` entry, and that every `fidelity_exceptions[]` entry cites a
  decision.
- Run `/mig_generate_infra` with no argument — the inventory says whether the platform
  fields resolve, whether the environments reconcile (X-11), and **whether anything deploys
  to the legacy production environment**, which is a Critical finding.

## 5. Run the phases

Do not run them all at once. Each phase gate exists because the next phase amplifies the
previous phase's errors:

```
/mig_analyze_legacy          → review the inventory with the client → gate
/mig_generate_requirements   → client sign-off on the BRD → gate
/mig_generate_basic_design   → /mig_review_design → gate
/mig_generate_mockup         → X-09 / X-10 against design and legacy → gate
/mig_generate_detail_design  → resolve GAP items → gate
/mig_scaffold_codebase       → once, after the TSD is approved
/mig_generate_infra          → pipeline, environments, coexistence, data migration
/mig_implement_feature       → per module
/mig_generate_test both      → per module
/mig_uat_*                   → per bug
/mig_cr_*                    → per change request, whenever one arrives
```

Each generation phase is run as a loop, not a single pass: execute → review in a fresh
session → `/mig_refine_skill` → re-execute. Calibrate the loop on a 2–3 module pilot
before generating a whole category. See [COMMAND-FLOW.md](COMMAND-FLOW.md).

---

## Extending the pack for one project

Add project-specific material as **new** files, prefixed with the project key, alongside
the pack rather than inside it:

```
.claude/skills/<key>_design_system/SKILL.md      UI design system for this product
.claude/skills/<key>_domain_glossary/SKILL.md    domain terms and their meanings
.claude/rules/<language>/                         stack rules extending rules/common/
```

Keep the `mig_*` files unmodified so the pack can be updated. When you find yourself
editing a `mig_*` file, ask whether the change is project-specific — if so it belongs in a
`<key>_*` file; if not, it belongs upstream in the pack.

Register new skills in the profile where they own a design category
(`paths.bd_categories[].skill`).

## Common adoption mistakes

| Mistake | Consequence |
|---|---|
| Filling the profile with plausible guesses instead of `<placeholders>` | invented values reach deliverables and look authoritative |
| Skipping P0 because "the requirements document already exists" | the existing document is a summary; the anchors it lacks are what P2 needs |
| Running P2 before the P1 gate | design scope is wrong, discovered at client review |
| Turning off a review family to reduce findings | the findings still exist, now invisible |
| Editing `mig_*` skills for one project's quirk | the pack stops being updatable |
| Treating the traceability register as end-of-project paperwork | it becomes unreconstructable and the gates become unverifiable |
| Generating a category before registering the client's form | the whole category is rejected on formatting, after it is finished |
| Anchoring behaviour to a legacy document instead of legacy code | you document what somebody intended years ago; parallel run finds out (DIO-08) |
| Enabling `xlsx` without installing `openpyxl` | the run fails forty files in, not on the first |
| Letting the mockup modernise the UI under `as-is` | operators reject the screens at UAT, after they are built |
| Leaving `coexistence.system_of_record` unset | both systems write, the data diverges, and nobody can say which row is right |
| Judging a data migration on completing without error | reconciliation is the deliverable; finishing is not |
| Never rehearsing the rollback | on cutover night it is a hypothesis, and it is usually wrong about the database |
| Leaving `python` unavailable so the hooks fail silently | the legacy tree is writable and nothing says so |

---

## Troubleshooting

### The hooks do not fire — I can edit a file under the legacy root

The most important failure in this list, because nothing announces it and the pack's entire
safety model rests on it. Check in order:

1. **Is `python` on PATH?** `settings.json` invokes `python`, not `python3`. On many Linux
   distributions and some macOS setups only `python3` exists. Install the alias, or change
   the three commands in `.claude/settings.json` to `python3`.
2. **Is `CLAUDE_PROJECT_DIR` resolving?** Run the hook by hand to see the real error:
   `echo '{"tool_input":{"file_path":"src/legacy/x.vb"}}' | python .claude/hooks/guard_readonly_paths.py`
3. **Did you merge `settings.json` rather than copying it?** A project that already had one
   keeps its own; the pack's `hooks` block has to be merged in by hand.
4. **Does `constraints.readonly_globs` include `legacy.root`?** `/mig_profile_check` check 16
   is exactly this, and it is Critical for this reason.

Verify with the step-4 test: ask for an edit under the legacy root and require the `[LR-01]`
message. Do this once per machine, not once per project.

### `[LR-01] BLOCKED` on a file I need to change

Working as designed. If the change genuinely belongs in the legacy system, it is a client
operation outside this project. If the root cause of a defect is inside a frozen database
object, LR-02 applies: **state the root cause first**, then the workaround as an option —
never present the workaround as the fix.

### `/mig_generate_basic_design` produced Markdown, but the client wants Excel

The template was not registered and `templates.on_missing` was `skeleton` rather than `ask`.
The run should have said so in its plan — that line is the warning.

Register the form (`/mig_template_register`), set `on_missing: ask`, and regenerate.
Regenerating is right: converting forty Markdown files into the client's form by hand costs
more and produces inconsistencies the cross-checks will not catch.

### Excel output lost the formatting, merged cells or print area

Three causes, in order of likelihood:

1. **The file was rebuilt rather than filled.** `pandas.to_excel` discards everything that
   makes the form a form. Load the template with `openpyxl` and write into cells.
2. **A write landed in a non-anchor cell of a merged range** and was silently dropped. Write
   to the top-left cell; find it in `ws.merged_cells.ranges`.
3. **Rows were inserted**, shifting formulas, merges and the print area.

Run the DIO-03 fidelity check on the first file of a category, not the fortieth.

### A deliverable cites an old specification and the behaviour turned out wrong

DIO-08. A legacy document is evidence of **intent**, never of behaviour — it is usually years
out of date, and the gap is invisible unless you check. Anchors come from
`{{profile.legacy.logic_source}}` and `{{profile.legacy.ui_source}}`; the document is quoted
for rationale, which is genuinely valuable and available nowhere else.

`mig_bd_designer` reports the anchor split — source versus document — for exactly this. The
document-anchored rows are the ones to re-check first.

### A category came out short, and nothing failed

The known failure mode of long generation runs: context runs out and the last categories are
dropped silently. The countermeasures are in `mig_basic_design` — batch by module, 10–20 files
per call, dedicated calls for the late categories (report, file, batch), and **count the files
on disk after each batch** rather than trusting the agent's report.

If it already happened, `/mig_generate_basic_design <category>` regenerates one category. The
plan's `written/expected` line tells you which.

### Operators rejected the screens at UAT even though the design was approved

Almost always `mockup.fidelity`. Under `as-is`, a reordered field, a regrouped section or a
corrected typo is a defect, and it usually enters through the mockup rather than the
document — the work is visual and the instinct is to improve it (MU-03).

Run X-10 per screen. If the change was wanted, it belongs in `fidelity_exceptions` with the
decision that authorised it; an exception with no decision is an invention (NI-02).

### The mockup and the screen design disagree

X-09 doing its job. The answer is never "update whichever is easier": decide against the
**legacy source**. Where the legacy is silent, it is a SPEC-GAP with an owner.

A field present in the mockup and in neither the screen design nor the legacy screen is an
invention (NI-01), and if it stays there it gets built.

### `/mig_generate_infra` refuses to write anything

`infrastructure.owner` is not `this project`, or `repo_may_write_infra` is `false`. Usually
correct — it means another team owns the pipeline — and the command produces proposals
instead. Change the field only if the ownership actually changed.

### The pipeline is green but the phase gate fails

Correct. A pipeline asserts what it can run: build, typecheck, lint, unit tests. It cannot
assert that a behaviour is anchored to legacy source, that a message is verbatim, that a
blocked feature was escalated, or that a GAP item was resolved rather than closed — which are
this pack's actual risks (IN-04).

### The data migration finished cleanly but the totals are wrong

It was judged on completing rather than on reconciling (IN-08). Row counts per table, control
totals on every amount column, referential integrity, and business-chosen spot checks —
designed before the script, not after the first bad run.

If a rehearsal has only ever run against a small extract, it has measured neither correctness
at volume nor whether the run fits the cutover window.

### The parallel run reports no differences and nobody believes it

Check `parallel_run.tolerance`. If it has grown a list of vague exceptions — "minor formatting
differences", "timing fields" — the run has been tuned until it passes. Every exception is
named, with a reason and a decision (IN-09). A difference is a defect against the oracle.

Also check `compare`: a run comparing screen output only, on a system whose real work is
batch, is comparing the cheap half. Batch output files are exactly diffable and are the
strongest evidence the project can produce.

### Both systems are live and the data has diverged

`coexistence.system_of_record` was unset, or `dual_write` is true with no
`conflict_resolution` (IN-07). This needs a client decision now, plus a reconciliation of the
rows already diverged — and the rule belongs in the architecture document, not in whichever
service was written last.

### `/mig_trace_check` reports hundreds of orphans on a project we adopted mid-flight

Expected. Back-fill the **register**, not the documents, from the current phase forward. The
first report is a finding list, not a failure: the downward orphans are legacy behaviour you
cannot yet prove is covered, and the upward orphans are target behaviour with no legacy
ancestor — which in a migration is either an unrecorded CR or an invention.

### Agents are running on a model nobody chose

`/mig_profile_check` check 17 compares `execution.agent_model` against each agent's `model:`
frontmatter. Drift happens when the pack is updated and `/mig_init` is not re-run. Re-run its
model-policy step, or fix the frontmatter.

Reasoning effort is **session-level** and cannot be set from the profile;
`execution.intended_effort` only records what the project expects.

### The pack feels too heavy for this migration

Read [`profile/PROFILE-RECIPES.md`](profile/PROFILE-RECIPES.md). Recipes 3 and 6 — lift and
shift, and database replatform — both cut the design categories down to three or four,
because screens and functions genuinely do not change in those shapes. That is a deliberate
reduction with a reason, which is different from quietly skipping categories.
