---
description: "Produce the WBS and WBS dictionary from the scope baseline: deliverable-oriented decomposition, work packages within 8/80, one owner and verifiable acceptance criteria each, with control accounts. Usage: /pm_wbs [branch]"
---

# WBS and WBS dictionary

## Step 1 — Load

`pm_project`, then `pm_schedule`, then `pm_document_io`. Agent: `pm_planner`.

**The WBS is delivered as Excel** (MD-09, DIO-W). Draft in text if that helps you think —
`{{profile.documents.working_dir}}/wbs.md` or `.csv` is the right place — but the artifact
this command produces is the workbook at `{{profile.paths.wbs}}`. A run that ends with only a
Markdown file has not produced the deliverable.

Check `openpyxl` imports before starting. If it does not, stop and say so; do not fall back
to Markdown.

## Step 2 — Decompose deliverables, not activities (WB-01)

Start from `{{profile.wbs.level1}}` and the deliverables in the scope statement. Nouns at
every level. A WBS element you cannot point at when it is finished is not a deliverable.

Keep the three branches teams habitually omit, and put real effort behind them (WB-02):
**project management** · **quality assurance and process** · **training and handover**.

When a technical pack is installed, its deliverable categories map into the design,
implementation and testing branches. Map to them; do not invent a parallel set of names
(PN-06).

## Step 3 — Check the 100% rule (WB-02)

Children total exactly the parent — no missing work, no extra work. Then check the root
against the scope statement: every deliverable is produced by at least one work package, and
every work package produces something in scope.

## Step 4 — Size the work packages (WB-03)

Between `{{profile.wbs.work_package_min_hours}}` and
`{{profile.wbs.work_package_max_hours}}` hours, and never longer than one reporting period.
Split anything that cannot be reported finished-or-not at the weekly report.

## Step 5 — Write the dictionary

One entry per leaf, fields from `{{profile.wbs.dictionary_fields}}`. Two fields decide
whether the dictionary is useful:

- **Description including what is explicitly NOT included** — this prevents the most common
  estimate dispute, between two people who agreed on a name and disagreed on its content.
- **Acceptance criteria** (WB-05) — how anyone can tell it is done, applying
  `{{profile.process.definition_of_done}}`.

Set control accounts at `{{profile.wbs.control_account_level}}` — that is where cost and
progress will be measured (`pm_cost`).

## Step 6 — Generate the workbook

Write `{{profile.paths.wbs}}`: sheet `WBS`, one row per element; sheet `WBS Dictionary`, one
row per leaf. Same workbook by default — one file, one version, and no way for the two to
drift apart, which separate files always do.

From `pm_document_io` DIO-W, the details that decide whether the client can use it:

- **`Code` column formatted as text** before writing, or Excel turns `1.2.3` into a date and
  `1.10` into `1.1`
- **header row frozen, `AutoFilter` on** — they will filter by owner and by branch
  immediately
- **outline grouping by level** so branches collapse
- **no merged cells in the data region** — they break sorting, filtering and every formula
- **the 100% rule written as a formula**, not only as a check you ran, so it keeps holding
  after the client edits a number
- **totals per level-1 branch**, management / QA / handover included
- units, currency and the as-of date as real number formats, not typed into cells (MD-05)

**Revising an existing WBS:** either edit the workbook directly, or export it to a fresh
working file, restructure, and regenerate. Never regenerate from a working file whose stamp
is older than the workbook — that silently destroys whoever edited the workbook last
(DIO-W).

## Step 7 — Verify against the file on disk

Read the counts, the 100% rule, sizing, owners and acceptance criteria back **from the
workbook you just wrote**, not from the draft you generated it from. Then regenerate the
stamped derived view and dispose of the draft per
`{{profile.documents.working_retention}}`.

## Step 8 — Report

```
WBS — v{n}
  Levels        : {n}    Work packages: {n}    Control accounts: {n}
  100% rule     : {pass | missing: ... | extra: ...}
  Sizing        : {n} within 8/80 · {n} too large · {n} too small
  Owners        : {n}/{n} have exactly one named owner
  Acceptance    : {n}/{n} have verifiable criteria
  Coverage      : deliverables covered {n}/{n} · requirements covered {n}/{n}
  Branches      : management {h}h · QA {h}h · handover {h}h  ← empty here means unplanned work
  Open items    : {n}
  Deliverable   : {{profile.paths.wbs}}  ({xlsx present | *** MISSING — not delivered ***})
  Working files : {n} ({kept | deleted})   derived view: {path}
```

The deliverable line is not decoration. `wbs` is in `{{profile.documents.binary_final}}`, so
the workbook existing at that path **is** the completion criterion (MD-09).

Then: `/pm_estimate`.
