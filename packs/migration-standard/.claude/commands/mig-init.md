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

## Step 3 — Write the profile

Write `.claude/migration.profile.yaml` from the template. Every field either has a real
value or an explicit `<...>` placeholder — never a plausible guess presented as fact.
List the placeholders you left, so the user knows what is still open.

## Step 4 — Scaffold

Create the directories named by `paths.*` and `paths.bd_categories[].dir`. Create
`{{profile.paths.traceability}}` with its header row if absent.

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

## Step 6 — Apply the model policy

Set the `model:` frontmatter of every `.claude/agents/mig-*.md` to
`{{profile.execution.agent_model}}`, honouring any entry in
`{{profile.execution.agent_model_overrides}}`.

Then tell the user what `{{profile.execution.intended_effort}}` records: reasoning effort
is a **session-level** setting in Claude Code, not agent frontmatter, so the profile can
only state the intended level — the team sets it in their session. Say so plainly rather
than implying the profile enforces it.

## Step 7 — Generate CLAUDE.md

From `.claude/CLAUDE.md` in the pack, resolving profile tokens. If a `CLAUDE.md` already
exists, do not overwrite it — show the block to merge in.

## Step 8 — Validate and report

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
  Mockup      : {kind}, fidelity {fidelity}   surfaces: {list}
  Infra       : {scm} / {ci} / {hosting} / {iac}   owner: {owner}
  Coexistence : {strategy}, system of record {x}
  Agent model : {{profile.execution.agent_model}} applied to {n} agents
  Effort      : {{profile.execution.intended_effort}} — set this in your session
  Next phase  : P0 — run /mig-analyze-legacy
```
