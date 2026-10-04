---
description: "Register, inspect or validate the project's own deliverable templates — the forms the client supplies, in Markdown, Excel, Word or CSV. Run at init, whenever a new category starts, and whenever the client issues a new template version. Usage: /sdlc-template-register [category key | template path | --check]"
---

# Register a deliverable template

The pack ships no templates. This command is how the project's own forms get in.

## Step 1 — Load

`sdlc-project`, then `sdlc-document-io`.

## Step 2 — Decide the mode from the argument

| Argument | Mode |
|---|---|
| nothing | **inventory** — list every category and its template status, then offer to fill the gaps |
| `--check` | **validate only** — no registry changes |
| a category key | **register one** — ask for that category's template |
| a file path | **register by file** — infer the category from the path and confirm it |

## Step 3 — Inventory

Build the table from `{{profile.paths.bd_categories}}` plus the non-design categories
(`requirements`, `detail`, `test_ut`, `test_it`, `test_st`, `test_uat`, `review`,
`cr_report`, `incident`, `gate_record`, `release_note`):

| Category | Registered | Path | Format | Output | Exists on disk | Fidelity checked |
|---|---|---|---|---|---|---|

A category with no template is not a defect — it is a decision the project has not made yet.
Show what `{{profile.templates.on_missing}}` would do for each, so the user can see the
consequence before choosing.

## Step 4 — Take the template in

For each template being registered:

1. **Confirm the file is present** under `{{profile.templates.root}}`. If the user names a
   file outside the repository, copy it in first and keep the original under
   `{{profile.templates.root}}/_received/` with its received date — the received copy is the
   evidence of what was supplied, and it is never edited.
2. **Open it and read its structure.** Not the filename, not the user's description of it.
   - `md` — heading text, level and order
   - `xlsx` — sheet names, the header block, the merged ranges that act as fields, where the
     repeating rows begin, the print area
   - `docx` — styles in use, the tables, any content controls
   - `csv` — the header row and the delimiter
3. **Derive the field map** (DIO-04) from the placeholders you find. Print it. An
   unrecognised placeholder is asked about, not guessed.
4. **Compare against the category skill's section list** and report the differences in the
   three DIO-01 classes: template-only sections, skill content with nowhere to go, and
   conflicts with an invariant rule. Report them **now**, once, rather than per generated
   document later.
5. **Ask for the output format** when it should differ from the template's own. Default is
   the same format; a difference is recorded in the registry, never decided per file.
6. **Append the registry entry** to `{{profile.templates.registry}}` with `status: provided`.

## Step 5 — Protect it

Add the template path to `{{profile.constraints.readonly_globs}}` so the guard hook blocks a
write to it. The template is an input; every deliverable is written into a **copy**.

## Step 6 — Fidelity check, on the first template of each binary format

Do not skip this, and do not defer it to the first real generation run:

1. copy the template, write one representative value into each mapped field, save
2. diff the produced file against the template on everything except those fields — styles,
   merges, widths, print area, sheet order, defined names
3. if the diff is larger than the edits, the writer is wrong for this template. Report it and
   stop, rather than generating a category that will be rejected on formatting

## Step 7 — New version of an existing template

A new version is a **new file** with its version in the name, plus a registry update — never
an overwrite. Then list every document already generated against the old version. That list
is the re-work estimate; produce it now, when it is small and visible.

## Step 8 — Report

```
Template registry
  Registered     : {n}/{n categories}
  Added this run : {category} -> {path} ({format} -> {output_format})
  Field map      : {n} fields derived, {n} confirmed by the user
  Template gaps  : {n}   {each: category, what the skill needs, where it does not fit}
  Invariant conflicts : {n}  {each: category, which rule, who it was raised to}
  Fidelity check : {pass | diff found: what}
  Read-only      : {n} paths added to constraints.readonly_globs
  Still missing  : {categories}  -> on_missing = {{profile.templates.on_missing}}
```

End by naming what the missing categories will do on their next generation run. A team that
knows `screen` will stop and ask is in a different position from one that finds out during a
forty-file run.
