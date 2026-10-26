---
description: "Bootstrap the Migration Skill Pack in this repository: create or complete .claude/migration.profile.yaml, generate CLAUDE.md, scaffold the deliverable directories, seed the traceability register, and print the phase plan. Run once per project. Usage: /mig-init"
---

# Initialise a migration project

## Step 1 — Inspect before asking

Before asking the user anything, determine from the repository what you can:

- Is there an existing `.claude/migration.profile.yaml`? → completion mode, not creation.
- What legacy source is present? Detect by file extensions and directory names
  (`.vb`/`.Designer.vb` → vbnet, `.cbl`/`.cpy` → cobol, `.pas`/`.dfm` → delphi,
  `.srw`/`.sru` → powerbuilder, `.jsp`+`.java` → java-ee, `.php` → php).
- What target stack is present? Read the build files: package manifests, solution files,
  build scripts.
- What build commands exist? Read the scripts section of the package manifest, or the
  build tool's task list.
- Do document directories already exist, and in what language are they named?
- What does the git remote say the SCM platform is, and which CI definition files exist?
  (`.github/workflows/`, `.gitlab-ci.yml`, `azure-pipelines.yml`, `Jenkinsfile`, …)
- Is there IaC, a container definition, or neither?
- Are there deliverable templates or filled deliverables anywhere — `.xlsx`, `.docx` or
  Markdown under a `templates/`, `様式/`, `雛形/` or `docs/` directory? Their format is the
  project's format, whatever anyone says in the interview.
- Are there **legacy documents** — old design specs, operator manuals, handover packs? They
  are inputs, not templates, and they go somewhere different (DIO-08).
- Are there legacy screen captures, or an existing prototype?
- Which formatters, linters and static-analysis tools are configured for the **target**
  (Prettier, ESLint, Checkstyle, Spotless, PMD, Ruff, `.editorconfig`), and how each runs on
  a single file?
- Is there a client coding standard for the target — a `コーディング規約`, "coding standard"
  or "coding conventions" document in PDF, Excel or Word, or a supplied Checkstyle / ESLint
  config?
- Does the test runner have a listing command, and in what format does it write results?

Report what you found. Do not ask about anything you just determined.

## Step 2 — Ask only for what cannot be inferred

Use one grouped question round, not a sequence of prompts. Typically needed:

- project key, display name, vendor, client
- the deliverable language(s) and which directories they bind to
- module id pattern, with one real example
- the surfaces (form factors) the target has
- whether the database schema is frozen and whether stored procedures are read-only
- **deliverable format per category** — Markdown, Excel, Word — and whether the client
  supplies their own forms. Ask explicitly: it is the most expensive thing to discover late,
  because it invalidates every document already generated
- **mockup form and fidelity** — HTML / canvas / Figma / images / none, and whether the UI is
  reproduced `as-is`, `restyled`, or deliberately `redesigned`. The last one needs a funded
  client decision and changes what counts as a defect
- **infrastructure** — SCM and CI platform, hosting, IaC, and **who owns them**
- **coexistence** — big-bang, phased, strangler or parallel; and which system owns the data
  while both are live. This shapes the architecture, so it is asked at init, not at cutover
- **coding standards** — does the client impose its own for the target code, per stack, and
  is any of it enforced by a tool configuration they supply?
- **review in the delivered file** — do the client's reviewers correct the delivered Excel
  or Word files themselves? If so, those files become the source of truth (DIO-10), and a
  translation correction log is worth starting now (TL-09)

## Step 3 — Write the profile

Write `.claude/migration.profile.yaml` from the template. Every field either has a real
value or an explicit `<...>` placeholder — never a plausible guess presented as fact.
List the placeholders you left, so the user knows what is still open.

## Step 4 — Scaffold

Create the directories named by `paths.*` and `paths.bd_categories[].dir`. Create
`{{profile.paths.traceability}}` with its header row if absent.

The default names carry numeric prefixes so a directory listing follows the migration
lifecycle instead of the alphabet: under `docs/`, `00.legacy-documents` →
`01.legacy-captures` → `02.requirements` → `03.design` → `04.detail-design` →
`05.test-design` → `06.gap` → `07.reviews` → `08.uat-bug` (P7) → `09.change-requests` →
`10.bug-trace`. Every deliverable lives under `docs/`; nothing is scaffolded at the
repository root. Keep the prefixes when a profile renames a directory.

## Step 5 — Take the templates in, and separate the legacy documents

**The pack ships no deliverable templates.** Say it plainly: every organisation has its own
forms, on migration work they are usually Excel and usually contractual, and a deliverable
generated into the wrong form is re-work across every file in the category.

Load `mig-document-io`, then:

1. **Ask for the forms the client has supplied.** Copy each into
   `{{profile.templates.root}}`, keeping the original under `_received/` with its date.
2. **Register each one** — run `/mig-template-register`. Opening the file, deriving the field
   map, and reporting the gaps against the category skill all happen there. It also checks
   each form has somewhere to record the `LEG-*` anchor; a form without one does not suspend
   NI-01.
3. **Put the legacy documents somewhere else** — `{{profile.templates.legacy_documents_dir}}`.
   They are read-only inputs and are **never** authoritative about behaviour (DIO-08): the
   legacy code is. Registering an old specification as a template is how a project ends up
   documenting what somebody intended in 2011.
4. **Verify the toolchain** for every format in `{{profile.templates.formats_enabled}}`:
   `openpyxl` for `xlsx`, `python-docx` for `docx`. A format enabled with no working library
   fails forty files in, not on the first.
5. **Set `{{profile.templates.on_missing}}` deliberately.** `ask` is the default and safest.
6. **Add both directories to `{{profile.constraints.readonly_globs}}`.**

For every category whose delivered file the client's reviewers will edit, set
`registry[].authority` now (DIO-10) — before the first regeneration, not after it has
overwritten a review. If client reviewers will correct translations, set
`{{profile.language.correction_log}}` and create the file with its header row (TL-09).

## Step 6 — Coding standards, stack rules and on-edit checks

These govern the **target** code only. Nothing here applies to, formats or lints the legacy
tree.

1. **Keep the stack rules the target uses.** The pack ships `rules/java/`,
   `rules/typescript/`, `rules/react/` and `rules/sql/`; each loads only with the files it
   governs. Keep the directories matching `{{profile.target.stack}}` in `.claude/rules/` and
   remove the others, saying which. A stack the pack has no rules for is reported, not
   improvised.
2. **Digest each client coding standard.** For every standard the client supplies, read the
   whole source document (through `mig-document-io` for PDF, Excel or Word) and write
   `.claude/rules/<stack>/client-standard.md`:
   - front matter `paths:` identical to that stack's pack rule file, so it loads with the
     same code;
   - every rule as an imperative line with the source section number and the severity the
     source uses (must / should / avoid / forbidden) — never a paraphrase that loosens it;
   - a table of the source's sections that do **not** apply to this project, with the reason;
   - a list of every point where it contradicts the pack's stack rule file — the client's
     standard wins — and every point where following it would change legacy behaviour —
     parity wins, and the point is raised with the client once.

   Record each in `{{profile.target.coding_standards}}` (stack, source, digest,
   `enforced_by`) and add the source document to `{{profile.constraints.readonly_globs}}`.
   Show the digest for confirmation.
3. **Configure the on-edit checks.** From the target's formatters and linters found in
   Step 1, propose `{{profile.target.build.on_edit}}` entries — one per tool, scoped by glob
   to the target sources it owns and **never matching `{{profile.legacy.root}}`**, running on
   the single edited file, formatter before linter. Time each on one file; an entry slower
   than ~10s is a whole-project command and is replaced or dropped. Linters the client
   standard mandates are `blocking: true`. Write them only after the user confirms; with no
   tools configured yet, leave `on_edit: []` and say that `/mig-scaffold-codebase` will fill
   it.

## Step 7 — Apply the model policy

<!-- model-policy:claude -->
Resolve a model and an effort level for every `.claude/agents/mig-*.md` from
`{{profile.execution.model_profile}}`:

| `model_profile` | heavy tier | standard tier |
|---|---|---|
| `quality` | opus · `xhigh` | opus · `high` |
| `balanced` | opus · `high` | sonnet · `medium` |
| `budget` | sonnet · `high` | sonnet · `medium` |

- **heavy** — `mig-legacy-analyst`, `mig-requirements-writer`, `mig-bd-orchestrator`, `mig-bd-designer`, `mig-dd-designer`, `mig-reviewer`, `mig-defect-triager`, `mig-cr-engineer`
- **standard** — `mig-implementer`, `mig-tester`, `mig-test-automator`, `mig-infra-engineer`, `mig-mockup-designer`, `mig-uat-engineer`

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

Run the `/mig-profile-check` checks, then print:

```
Migration Skill Pack initialised
  Profile     : .claude/migration.profile.yaml  ({n} placeholders remaining)
  Legacy      : {kind} at {root}  ({n} files)
  Target      : {stack summary}
  Surfaces    : {list}
  Categories  : {n} scaffolded
  Templates   : {n}/{n categories} registered   formats: {list}   on_missing: {mode}
                toolchain: {format: ok|missing library}
  Legacy docs : {n} files (inputs only, DIO-08)
  Stack rules : kept {list}   removed {list}   no pack rules for: {list}
  Coding std  : {n} client standards digested   enforced by: {tools}
  On-edit     : {n} entries ({n} blocking)   slowest {s}s on one file   legacy excluded: yes
  Mockup      : {kind}, fidelity {fidelity}   surfaces: {list}
  Infra       : {scm} / {ci} / {hosting} / {iac}   owner: {owner}
  Coexistence : {strategy}, system of record {x}
  Agent model : {{profile.execution.model_profile}} — {n} opus · {n} sonnet · {n} overridden
  Effort      : agents {n} xhigh · {n} high · {n} medium; session {{profile.execution.intended_effort}} — set with /effort
  Next phase  : P0 — run /mig-analyze-legacy
```
