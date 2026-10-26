---
description: "Bootstrap the SDLC Skill Pack in this repository: create or complete .claude/sdlc.profile.yaml, generate CLAUDE.md, scaffold the deliverable directories, seed the registers, and print the phase plan. Run once per project. Usage: /sdlc-init"
---

# Initialise a development project

## Step 1 — Inspect before asking

Before asking the user anything, determine from the repository what you can:

- Is there an existing `.claude/sdlc.profile.yaml`? → completion mode, not creation.
- What stack is present? Read the build files: package manifests, solution files, build
  scripts, container definitions.
- What build, test and lint commands exist? Read the scripts section of the package
  manifest, or the build tool's task list.
- Is there a database, and does this repository own its migrations?
- Do document directories already exist, and in what language are they named?
- Is there an existing CI configuration, and what does it run?
- What does the git remote say the SCM platform is, and which CI definition files exist?
  (`.github/workflows/`, `.gitlab-ci.yml`, `azure-pipelines.yml`, `Jenkinsfile`, …)
- Is there IaC, a container definition, or neither?
- Are there existing deliverable templates or filled deliverables anywhere — `.xlsx`, `.docx`
  or Markdown under a `templates/`, `様式/`, `雛形/` or `docs/` directory? Their format is the
  project's format, whatever anyone says in the interview.
- Are there existing mockups — HTML prototypes, image exports, a Figma link in a README?
- Which formatters, linters and static-analysis tools are configured (Prettier, ESLint,
  Checkstyle, Spotless, PMD, Ruff, `.editorconfig`), and how each runs on a single file?
- Is there a client coding standard — a `コーディング規約`, "coding standard" or "coding
  conventions" document in PDF, Excel or Word, or a supplied Checkstyle / ESLint config?
- Does the test runner have a listing command, and in what format does it write results?

Report what you found. Do not ask about anything you just determined.

## Step 2 — Ask only for what cannot be inferred

Use one grouped question round, not a sequence of prompts. Typically needed:

- project key, display name, vendor, client
- the five stakeholder roles (`{{profile.stakeholders}}`) — every decision needs an owner
- delivery model and contract type — they set how hard the gates block and how strict
  change control is
- the deliverable language(s) and which directories they bind to
- module id pattern, with one real example
- the surfaces (form factors) the system will have
- the environments, and which one is production-like enough for system test
- **deliverable format per category** — Markdown, Excel, Word — and whether the client
  supplies their own forms. Ask this explicitly: it is the single most expensive thing to
  discover late, because it invalidates every document already generated
- **mockup form** — HTML prototype, design canvas, Figma, image exports, or none
- **infrastructure** — SCM and CI platform, hosting, IaC tool, and **who owns them**. An
  infrastructure owned by a platform team changes what this pack may write versus request
- **coding standards** — does the client impose its own, per stack, and is any of it
  enforced by a tool configuration they supply?
- **review in the delivered file** — do the client's reviewers correct the delivered Excel
  or Word files themselves? If so, those files become the source of truth (DIO-09), and a
  translation correction log is worth starting now (TL-10)

## Step 3 — Write the profile

Write `.claude/sdlc.profile.yaml` from the template. Every field either has a real value or
an explicit `<...>` placeholder — never a plausible guess presented as fact. List the
placeholders you left, so the user knows what is still open.

Quality targets in `quality.targets` ship with defaults. Say plainly that they are
placeholders for the team's own historical numbers, not industry constants, and that a
target nobody agreed to is a target nobody will act on.

## Step 4 — Scaffold

Create the directories named by `paths.*` and `paths.bd_categories[].dir`. 
The default names carry numeric prefixes so a directory listing follows the development
lifecycle instead of the alphabet: under `docs/`, `00.inception` → `01.requirements` →
`02.basic-design` → `03.detail-design` → `04.test-design` → `05.drift` → `06.metrics` →
`07.operations` → `08.reviews` → `09.uat` (P8) → `10.maintenance` (P9) →
`11.change-requests` → `12.bug-trace`. Every deliverable lives under `docs/`; nothing is
scaffolded at the repository root. Keep the prefixes when a profile renames a directory.

Create, with their header rows if absent:

- `{{profile.paths.traceability}}`
- `{{profile.paths.decision_log}}`
- `{{profile.paths.assumption_log}}`
- `{{profile.paths.risk_register}}`
- `{{profile.paths.glossary}}`

## Step 5 — Take the templates in

**The pack ships no deliverable templates**, and this is the step where that becomes the
user's problem rather than a surprise at the first review. Say it plainly: every
organisation has its own forms, the pack will not invent one, and a deliverable generated
into the wrong form is re-work across every file.

Load `sdlc-document-io`, then:

1. **Ask for the templates the client has already supplied.** Most projects have them; they
   are usually Excel, usually attached to an email, and usually not in the repository yet.
   Copy each into `{{profile.templates.root}}`, keeping the original under `_received/` with
   its date.
2. **Register each one** — this is `/sdlc-template-register` and you may simply run it.
   Opening the file, deriving the field map and reporting the gaps against the category
   skill all happen there.
3. **Verify the toolchain** for every format in `{{profile.templates.formats_enabled}}`:
   `openpyxl` for `xlsx`, `python-docx` for `docx`. A format enabled with no working
   library is a run that will fail forty files in — report it now and either install it or
   drop the format from the list.
4. **Set `{{profile.templates.on_missing}}` deliberately.** `ask` is the default and the
   safest. `skeleton` is legitimate for a project that has agreed to the pack's own
   structure — but it is an agreement, not a fallback, and it is recorded as a `DEC-*`.
5. **Add every template path to `{{profile.constraints.readonly_globs}}`** so the guard hook
   blocks a write to the form itself.

A project with no templates yet is fine. A project that has them and did not register them
is not — it will generate Markdown for three weeks and then be asked for the Excel.

For every category whose delivered file the client's reviewers will edit, set
`registry[].authority` now (DIO-09) — before the first regeneration, not after it has
overwritten a review. If client reviewers will correct translations, set
`{{profile.language.correction_log}}` and create the file with its header row (TL-10).

## Step 6 — Coding standards, stack rules and on-edit checks

1. **Keep the stack rules the project uses.** The pack ships `rules/java/`,
   `rules/typescript/`, `rules/react/` and `rules/sql/`; each loads only with the files it
   governs. Keep the directories matching `{{profile.system.stack}}` in `.claude/rules/` and
   remove the others, saying which. A stack the pack has no rules for is reported, not
   improvised.
2. **Digest each client coding standard.** For every standard the client supplies, read the
   whole source document (through `sdlc-document-io` for PDF, Excel or Word) and write
   `.claude/rules/<stack>/client-standard.md`:
   - front matter `paths:` identical to that stack's pack rule file, so it loads with the
     same code;
   - every rule as an imperative line with the source section number and the severity the
     source uses (must / should / avoid / forbidden) — never a paraphrase that loosens it;
   - a table of the source's sections that do **not** apply to this project, with the reason
     (a server-side templating section in a JSON-API project, for instance), so nobody
     re-reads them looking for rules;
   - a list of every point where it contradicts the pack's stack rule file — the client's
     standard wins, and the list says so.

   Record each in `{{profile.system.coding_standards}}` (stack, source, digest,
   `enforced_by`) and add the source document to `{{profile.constraints.readonly_globs}}`.
   Show the digest for confirmation: it is the project's reading of the client's standard,
   and the client's reviewer will hold the code to the original.
3. **Configure the on-edit checks.** From the formatters and linters found in Step 1, propose
   `{{profile.system.build.on_edit}}` entries — one per tool, scoped by glob to the sources it
   owns, running on the single edited file, formatter before linter. Time each on one file;
   an entry slower than ~10s is a whole-project command and is replaced or dropped. Linters
   the client standard mandates are `blocking: true`. Write them only after the user
   confirms; with no tools configured yet, leave `on_edit: []` and say that
   `/sdlc-scaffold-codebase` will fill it.

## Step 7 — Apply the model policy

<!-- model-policy:claude -->
Resolve a model and an effort level for every `.claude/agents/sdlc-*.md` from
`{{profile.execution.model_profile}}`:

| `model_profile` | heavy tier | standard tier |
|---|---|---|
| `quality` | opus · `xhigh` | opus · `high` |
| `balanced` | opus · `high` | sonnet · `medium` |
| `budget` | sonnet · `high` | sonnet · `medium` |

- **heavy** — `sdlc-analyst`, `sdlc-bd-orchestrator`, `sdlc-bd-designer`, `sdlc-dd-designer`, `sdlc-reviewer`, `sdlc-defect-triager`, `sdlc-cr-engineer`, `sdlc-maintenance-engineer`
- **standard** — `sdlc-implementer`, `sdlc-tester`, `sdlc-test-automator`, `sdlc-infra-engineer`, `sdlc-mockup-designer`, `sdlc-uat-coordinator`

An entry in `{{profile.execution.agent_model_overrides}}` or
`{{profile.execution.agent_effort_overrides}}` wins over the table for that agent. A profile
that still sets the deprecated `execution.agent_model` and no `model_profile` reads `opus` as
`quality` and `sonnet` as `budget`; offer to replace the field.

Set each agent's `model:` and `effort:` frontmatter to the resolved values. The pack ships the
`balanced` values, so a `balanced` profile with no overrides changes no file — say so instead of
rewriting them.

Then tell the user that `{{profile.execution.intended_effort}}` is for their own session,
where the commands run: Claude Code takes the session level from `/effort`, not from the
profile, so they set it there. Agents are not affected by it.
<!-- /model-policy:claude -->

## Step 8 — Generate CLAUDE.md

From `.claude/CLAUDE.md` in the pack, resolving profile tokens. If a `CLAUDE.md` already
exists, do not overwrite it — show the block to merge in.

## Step 9 — Validate and report

Run the `/sdlc-profile-check` checks, then print:

```
SDLC Skill Pack initialised
  Profile      : .claude/sdlc.profile.yaml  ({n} placeholders remaining)
  Stack        : {summary}
  Surfaces     : {list}
  Environments : {list}   production-like for ST: {id}
  Delivery     : {model}, {contract type}
  Categories   : {n} scaffolded
  Templates    : {n}/{n categories} registered   formats: {list}   on_missing: {mode}
                 toolchain: {format: ok|missing library}
  Stack rules  : kept {list}   removed {list}   no pack rules for: {list}
  Coding std   : {n} client standards digested   enforced by: {tools}
  On-edit      : {n} entries ({n} blocking)   slowest {s}s on one file
  Mockup       : {kind}   surfaces: {list}
  Infrastructure: {scm} / {ci} / {hosting} / {iac}   owner: {owner}
  Registers    : traceability, decisions, assumptions, risks, glossary
  Agent model  : {{profile.execution.model_profile}} — {n} opus · {n} sonnet · {n} overridden
  Effort       : agents {n} xhigh · {n} high · {n} medium; session {{profile.execution.intended_effort}} — set with /effort
  Next phase   : P0 — run /sdlc-discover
```

Name the unregistered template categories explicitly, and say what
`{{profile.templates.on_missing}}` will do when one of them is generated. That sentence is
the difference between a team that supplies the form now and a team that supplies it after
forty documents exist.
