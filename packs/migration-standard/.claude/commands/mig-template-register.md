---
description: "Register, inspect or validate the project's own deliverable templates — the forms the client supplies, in Markdown, Excel, Word or CSV — and the legacy documents that are read-only inputs. Run at init, when a new category starts, and when the client issues a new template version. Usage: /mig-template-register [category key | template path | --check]"
model: sonnet
effort: medium
---

# Register a deliverable template

The pack ships no templates. This command is how the project's own forms get in — and how
the legacy system's documents get kept apart from them.

## Step 1 — Load

`mig-project`, then `mig-document-io`.

## Step 2 — Mode from the argument

| Argument | Mode |
|---|---|
| nothing | **inventory** — every category and its template status, then offer to fill the gaps |
| `--check` | **validate only** — no registry changes |
| a category key | **register one** |
| a file path | **register by file** — infer the category from the path and confirm it |

## Step 3 — Inventory

From `{{profile.paths.bd_categories}}` plus the non-design categories (`requirements`,
`detail`, `test_ut`, `test_it`, `test_uat`, `review`, `cr_report`, `uat_report`,
`legacy_inventory`):

| Category | Registered | Path | Format | Output | Exists | Fidelity checked |
|---|---|---|---|---|---|---|

A category with no template is not a defect — it is a decision not yet made. Show what
`{{profile.templates.on_missing}}` would do for each, so the consequence is visible before
it is chosen.

## Step 4 — Take the template in

For each template being registered:

1. **Confirm the file is present** under `{{profile.templates.root}}`. A file named from
   outside the repository is copied in, with the original kept under `_received/` and its
   received date — the received copy is the evidence of what was supplied, and is never
   edited.
2. **Open it and read its structure.** Not the filename, not the description of it.
   - `md` — heading text, level, order
   - `xlsx` — sheet names, the header block, merged ranges acting as fields, where repeating
     rows begin, the print area
   - `docx` — styles, tables, content controls
   - `csv` — header row and delimiter
3. **Derive the field map** (DIO-04) from the placeholders found. Print it. An unrecognised
   placeholder is asked about, never guessed.
4. **Compare against the category skill** and report the differences in the three DIO-01
   classes: template-only sections, skill content with nowhere to go, and conflicts with an
   invariant. Report them **now**, once — not per generated document, later.

   **Check specifically for an anchor column.** A form with nowhere to record the `LEG-*`
   reference does not suspend NI-01: the anchors go in a section the form does have, or in
   Open Items, and the missing column is a template gap. A deliverable with no anchors is not
   a migration deliverable.
5. **Ask for the output format** where it should differ from the template's own.
6. **Append the registry entry** with `status: provided`.

## Step 5 — Separate the legacy documents

Anything that came from the **old system** — old design specifications, operator manuals,
handover packs, previous test documents — goes to
`{{profile.templates.legacy_documents_dir}}`, not to `{{profile.templates.root}}`.

They are read-only inputs and they are **not** authoritative about behaviour (DIO-08). They
are evidence of intent; the legacy code is the evidence of behaviour, and the gap between
them is usually years wide.

Register nothing from that directory as a template. If the client's blank form happens to be
an old filled-in document, take a copy, blank it, and register the copy — saying so.

## Step 6 — Protect both directories

Add `{{profile.templates.root}}` and `{{profile.templates.legacy_documents_dir}}` to
`{{profile.constraints.readonly_globs}}` so the guard hook blocks a write. Every deliverable
is written into a fresh **copy**.

## Step 7 — Fidelity check, on the first template of each binary format

Do not defer this to the first real generation run:

1. copy the template, write one representative value into each mapped field, save
2. diff the produced file against the template on everything else — styles, merges, widths,
   print area, sheet order, defined names
3. if the diff exceeds your edits, the writer is wrong for this form. Report and stop, rather
   than generating a category that will be rejected on formatting

## Step 8 — A new version of an existing template

A new file with its version in the name, plus a registry update — never an overwrite. Then
list every document already generated against the old version. That list is the re-work
estimate, and it is smallest now.

## Step 9 — Report

```
Template registry
  Registered     : {n}/{n categories}
  Added this run : {category} -> {path} ({format} -> {output_format})
  Field map      : {n} derived, {n} confirmed
  Anchor column  : {present | MISSING in: {categories}}   <- NI-01 still applies
  Template gaps  : {n}   {each: category, what the skill needs, where it does not fit}
  Invariant conflicts : {n}  {each: category, rule, who it was raised to}
  Fidelity check : {pass | diff found: what}
  Legacy documents: {n} files under {legacy_documents_dir} — inputs only (DIO-08)
  Read-only      : {n} paths added to constraints.readonly_globs
  Still missing  : {categories}  -> on_missing = {{profile.templates.on_missing}}
```

End by naming what the missing categories will do on their next generation run.
