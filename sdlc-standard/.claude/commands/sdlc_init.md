---
description: "Bootstrap the SDLC Skill Pack in this repository: create or complete .claude/sdlc.profile.yaml, generate CLAUDE.md, scaffold the deliverable directories, seed the registers, and print the phase plan. Run once per project. Usage: /sdlc_init"
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

## Step 3 — Write the profile

Write `.claude/sdlc.profile.yaml` from the template. Every field either has a real value or
an explicit `<...>` placeholder — never a plausible guess presented as fact. List the
placeholders you left, so the user knows what is still open.

Quality targets in `quality.targets` ship with defaults. Say plainly that they are
placeholders for the team's own historical numbers, not industry constants, and that a
target nobody agreed to is a target nobody will act on.

## Step 4 — Scaffold

Create the directories named by `paths.*` and `paths.bd_categories[].dir`. Create, with
their header rows if absent:

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

Load `sdlc_document_io`, then:

1. **Ask for the templates the client has already supplied.** Most projects have them; they
   are usually Excel, usually attached to an email, and usually not in the repository yet.
   Copy each into `{{profile.templates.root}}`, keeping the original under `_received/` with
   its date.
2. **Register each one** — this is `/sdlc_template_register` and you may simply run it.
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

## Step 6 — Apply the model policy

Set the `model:` frontmatter of every `.claude/agents/sdlc_*.md` to
`{{profile.execution.agent_model}}`, honouring any entry in
`{{profile.execution.agent_model_overrides}}`.

Then tell the user what `{{profile.execution.intended_effort}}` records: reasoning effort is
a **session-level** setting in Claude Code, not agent frontmatter, so the profile can only
state the intended level — the team sets it in their session. Say so plainly rather than
implying the profile enforces it.

## Step 7 — Generate CLAUDE.md

From `.claude/CLAUDE.md` in the pack, resolving profile tokens. If a `CLAUDE.md` already
exists, do not overwrite it — show the block to merge in.

## Step 8 — Validate and report

Run the `/sdlc_profile_check` checks, then print:

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
  Mockup       : {kind}   surfaces: {list}
  Infrastructure: {scm} / {ci} / {hosting} / {iac}   owner: {owner}
  Registers    : traceability, decisions, assumptions, risks, glossary
  Agent model  : {{profile.execution.agent_model}} applied to {n} agents
  Effort       : {{profile.execution.intended_effort}} — set this in your session
  Next phase   : P0 — run /sdlc_discover
```

Name the unregistered template categories explicitly, and say what
`{{profile.templates.on_missing}}` will do when one of them is generated. That sentence is
the difference between a team that supplies the form now and a team that supplies it after
forty documents exist.
