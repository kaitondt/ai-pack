---
description: "Set up the PM Skill Pack on a project: inspect the repository, detect an installed technical pack, interview for what cannot be inferred, write pm.profile.yaml, scaffold the pm/ tree and the registers, and generate CLAUDE.md. Usage: /pm-init"
---

# Initialise the PM pack

## Step 1 — Inspect before asking

Determine from the repository, without asking:

| Signal | Tells you |
|---|---|
| `.claude/sdlc.profile.yaml` | technical pack `sdlc` — read its phases, gates, quality targets, paths |
| `.claude/migration.profile.yaml` | technical pack `migration` — same |
| existing `pm/`, `docs/`, charter or plan files | artifacts that already exist; never overwrite them |
| git history and contributors | team size and shape, roughly |
| CI config | build and test commands, environments |
| README / CLAUDE.md | project name, purpose, stack |

Report what you found **before** asking anything. An interview that asks what is already on
disk wastes the user's attention and makes the rest of their answers less careful.

## Step 2 — Interview for what cannot be inferred

Only these, asked in one batch:

1. **Governance** — sponsor, client PM, project manager, technical lead, QA lead, delivery
   manager. Every role. An unfilled role means decisions with no owner (DA-01), and
   `/pm-profile-check` fails Critical on it.
2. **Contract and delivery** — contract type, delivery model, engagement model, currency,
   start and planned end dates, release cadence.
3. **Scope outline** — the capabilities in scope, and the notable exclusions with reasons.
4. **Calendar** — working days, holidays per location, hours per day, time zones.
5. **Reporting** — which cadences are actually required, to whom, in which language.
6. **Quality targets** — accept the defaults, or supply the organisation's own history.
7. **Estimating rates** — measured rates if they exist; otherwise mark them unverified (ES-08).
8. **Deliverable formats** — which artifacts the client receives as Excel, which as Word,
   which as Markdown, and whether they supply their own forms for any of them. Ask
   explicitly: format is the thing that is cheap to decide now and expensive to discover
   after forty documents exist.

   The WBS is not part of that question. It is Excel
   (`{{profile.documents.binary_final}}`, MD-09); what is worth asking is whether the client
   has a WBS form of their own to write into.

## Step 3 — Write the profile

Copy `pm.profile.yaml` to `.claude/pm.profile.yaml` and fill every field you can. Leave
`<...>` only where the user genuinely could not answer, and list those in the report so they
stay visible rather than being forgotten.

Set `integration.technical_pack` and `integration.technical_profile_path` from step 1. When a
technical pack exists, **inherit** its quality targets rather than inventing a second set
(QP-02), and record the milestone/gate mapping if the milestones are known.

## Step 4 — Scaffold

Create, from `{{profile.paths}}`:

```
pm/charter  pm/plan  pm/scope  pm/schedule  pm/cost  pm/process  pm/quality
pm/registers  pm/reports/{daily,weekly,monthly,quarterly,quality,_data}
pm/changes  pm/resource  pm/meetings  pm/closing/archive
```

Seed each register with its header row, so the first entry has a shape to follow: risk
register, issue log, decision log, assumption log, action log, change register, CAPA log,
contingency drawdown log.

## Step 5 — Bind the deliverable formats and check the toolchain

Fill `{{profile.documents.registry}}` from the interview: one entry per artifact, with its
final `format`, the `working` forms allowed while drafting, and the client's own `template`
where they supplied one.

Then verify the toolchain for every format in `{{profile.documents.formats_enabled}}`:
`openpyxl` for `xlsx`, `python-docx` for `docx`. **`openpyxl` is not optional on this pack**
— the WBS cannot be delivered without it. A missing library is reported now, not discovered
by `/pm-wbs` at the point of writing the workbook.

```bash
python -c "import openpyxl; print('xlsx ok')"
python -c "import docx;     print('docx ok')"
```

Create `{{profile.documents.working_dir}}` and add it to the project's `.gitignore` unless
`working_retention` is `keep` — scratch files in version control are how a draft ends up
looking like a deliverable.

## Step 6 — Generate CLAUDE.md

From the pack's `CLAUDE.md` template, with profile values resolved. If the project already
has one — likely, when a technical pack is installed — **append** a project-management
section rather than overwriting it.

## Step 7 — Report

```
PM pack initialised
  Profile        : .claude/pm.profile.yaml
  Technical pack : {sdlc | migration | none} ({path})
  Scaffolded     : {n} directories, {n} registers
  Formats        : {n} artifacts bound   binary_final: {list}
  Toolchain      : openpyxl {ok|MISSING — the WBS cannot be delivered} · python-docx {ok|n/a}
  CLAUDE.md      : {created | appended}
  Unfilled       : {fields still <...>} — each blocks the artifact that needs it
  Next           : /pm-profile-check, then /pm-charter
```
