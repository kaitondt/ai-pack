---
name: mig-document-io
description: "Deliverable templates and multi-format document I/O — how a project's own forms are registered and honoured, how to read and write Markdown, Excel, Word and CSV deliverables without destroying the client's form, and how legacy documents are treated as read-only inputs that are never authoritative about behaviour. Load for ANY task that reads or writes a deliverable, alongside the category skill."
---

# Deliverable templates and document I/O

> Prerequisite: `mig-project` resolved. Template registry comes from
> `{{profile.templates}}`; enabled formats from `{{profile.templates.formats_enabled}}`.

**The pack ships no templates.** Every organisation has its own deliverable forms, in its
own format, with its own column names and approval block — and on migration work in the
Japanese SI market, most of them are Excel and most of them are contractual. A template
invented here is rejected at the first review, and rejected *after* forty documents have
been generated into it.

So the form is an input to the project, collected at `/mig-init` and maintained by
`/mig-template-register`. This skill owns what happens once one exists — and, because this
is a migration, what happens to the **legacy system's own documents**, which are a
different thing entirely (DIO-08).

---

## 1. Template resolution — before generating anything

For the category you are about to write, look it up in `{{profile.templates.registry}}` by
`key`:

| Registry state | Do this |
|---|---|
| entry with `status: provided`, file readable | use it; it is the authority (DIO-01) |
| entry with `status: provided`, file missing | **stop**. Report the path. Never fall back silently — the team believes a form is in force |
| no entry, `on_missing: ask` | stop and ask. Offer the skill's own section list as the alternative, and say what it would produce |
| no entry, `on_missing: skeleton` | generate from the category skill's section list, and **say so in the report**, per file |
| no entry, `on_missing: block` | refuse the category and name `/mig-template-register` |

State which branch you took, per category, in the plan you print before generating.

---

## 2. The rules

### DIO-01 — The template is authoritative over the skill

Where a registered template and the category skill's section list disagree, **the template
wins**, and the difference is reported. Never silently resolve it.

| Disagreement | Action |
|---|---|
| Template has a section the skill does not describe | fill it. Ask what belongs there if it is not obvious; never leave a client's section blank without an explicit "not applicable" |
| Skill requires content the template cannot hold | report a **template gap** — what the content is and why the skill requires it. Do not drop it, do not bolt on a section |
| Template conflicts with an invariant (no revision table, no Open Items) | the template wins on **form**; the invariant is raised as a finding against the template, to the document owner, **once** — not once per file |

The one conflict that is not negotiable is anchoring. A form with no column for the legacy
reference does not suspend NI-01: the anchors go in the section the form does have, or in
Open Items, and the missing column is reported as a template gap. **A deliverable with no
anchors is not a migration deliverable**, whatever form it is written on.

### DIO-02 — Never invent, extend or "improve" a template

Not an extra column, not a renamed header that reads better, not a reordered section. The
client's tooling parses these documents and their reviewers read them in a fixed order.

This is NI-02 applied to document form: a migration reproduces, it does not improve. A
genuine improvement goes to the document owner as a proposal and enters as a new template
version.

### DIO-03 — Round-trip fidelity

When `{{profile.templates.preserve_unfilled_structure}}` is true, writing a deliverable into
a copy of the client's file changes **nothing outside the filled fields**: not column
widths, not merged ranges, not print areas, not sheet order, not styles, not defined names,
not headers and footers.

Test it mechanically on the **first file of every category**: write one deliverable, then
diff the produced file against the template for everything except the cells you meant to
fill. If the diff is larger than your edits, the writer is wrong — fix it before generating
the other thirty-nine.

### DIO-04 — The template's own placeholders are the field map

When `registry[].fields` is empty, derive the fields from the template. Recognised forms:

```
{{field}}   {field}   <field>   ${field}   XXXX   ○○○○   〇〇   ____
```

Report the map you derived before filling it. A placeholder you could not fill is an **Open
Item** (SPEC-GAP), not a blank cell and not a plausible value (NI-01).

### DIO-05 — Format is a property of the category, not the task

`registry[].output_format` decides what is written; empty means the template's own format.
A request phrased in chat does not change it. If the client's screen design is `.xlsx`, the
screen design is `.xlsx` — producing Markdown "because it is easier to review" creates a
second source of truth that diverges within a week.

The one legitimate split: `output_format: md` against an `xlsx` template, where the project
has agreed Markdown is the working form and Excel is generated for delivery. Agree it once,
record it in the registry, generate one from the other — never maintain both by hand.

### DIO-06 — Read every input; never retype it

Legacy specifications arrive as Word. Interface definitions arrive as Excel with a sheet per
endpoint. Client decisions arrive as PowerPoint. These are **read**, not summarised from the
filename and not assumed to match the version you saw last month.

Cite the source file path and its date wherever a document depends on it. "Per the client's
interface spec" is not a citation; "per `docs/legacy-documents/IF_SPEC_v3.xlsx` sheet
`API-014`, received 2026/03/12" is.

### DIO-07 — Binary deliverables are still reviewable

An `.xlsx` or `.docx` deliverable cannot be diffed in a `{{profile.infrastructure.scm.review_unit}}`.
Two obligations follow:

1. **Regenerate rather than hand-edit** wherever a generator exists — the reviewable artifact
   is then the input plus the generator, not the binary.
2. **Emit a plain-text digest** for every binary deliverable, under
   `{{profile.paths.reviews}}/digests/`, carrying the field values that were written, with
   their anchors. The digest is what the reviewer and `/mig-review-design` read; the binary
   is what the client receives.

Without the digest a binary deliverable sits outside every review, cross-check and gate the
pack runs — which is how a category passes P2 with nobody having checked a single anchor.

### DIO-08 — A legacy document is evidence of intent, never evidence of behaviour

The rule that only exists in a migration pack, and the one that costs the most when it is
missed.

Legacy design specifications, operator manuals, handover packs and old test documents live
in `{{profile.templates.legacy_documents_dir}}`. They are read-only inputs (LR-01, LR-05).
They are **not** one of NI-01's three anchors.

| The legacy document says | Its status |
|---|---|
| a rule, a default, a message, a sort order | a **hypothesis**. Confirm it against the legacy source; cite the source, not the document |
| a rule the code contradicts | the **code wins** (NI-05 reported, not arbitrated). Report both with anchors and ask |
| a rule the code does not implement at all | a SPEC-GAP, and an interesting one: it is often a feature that was specified, cut, and never removed from the spec |
| why something works the way it does | genuinely valuable, and unavailable anywhere else. Quote it as rationale, and still anchor the behaviour to the code |

These documents are usually years out of date, and the gap between them and the running
system is invisible unless you check. A deliverable whose anchor is an old specification has
documented what somebody intended in 2011, which the client will discover at parallel run.

**Never write into the legacy documents directory.** Analysis output goes to
`{{profile.paths.docs_root}}` (LR-05).

---

## 3. Per-format mechanics

Check the toolchain once before the first write of a run. `/mig-profile-check` verifies each
enabled format; if an import fails, report it and stop rather than falling back to Markdown.

### Markdown (`md`)

The default and the only diffable format. Follow
`rules/migration/document-standards.md` in full: DS-01 skeleton, DS-06 cell conventions,
DS-07 diagrams as fenced `{{profile.document.diagram_tool}}` blocks.

A Markdown template is used by **copying it and filling the headings**, not by writing a new
file with similar headings. Heading text, level and order come from the template.

### Excel (`xlsx`)

Library: `openpyxl`. Read-only tabular extraction: `pandas.read_excel`. **Never** rebuild
with `pandas.to_excel` — it discards every piece of formatting the form consists of.

```python
from openpyxl import load_workbook
wb = load_workbook(tpl_path)          # keep_vba=True for .xlsm
ws = wb[sheet or wb.sheetnames[0]]
ws["C4"] = value                      # write into cells, never rewrite the sheet
wb.save(out_path)                     # save a COPY; the template is never the output
```

| Hazard | Rule |
|---|---|
| **Merged cells** — writing to any but the top-left cell of a merge is silently lost | write to the anchor cell; find it in `ws.merged_cells.ranges` |
| **Grid-paper layouts** (方眼紙) — one logical field spans many narrow cells | treat the merge anchor as the field. Never unmerge to "make it simpler"; the print layout is the deliverable |
| **Row insertion** shifts formulas, merges, conditional formats and print areas | prefer a template with enough pre-formatted rows; after `ws.insert_rows`, re-verify merges and the print area |
| **`ws.max_row` over-reports** on formatted-but-empty rows | find the end by scanning the key column for the last non-empty value |
| **Formulas** read as strings with `data_only=False`, as stale cached values with `data_only=True` | never write a value into a formula cell; when reading a computed value, say in the report that it is cached |
| **Charts, images, pivot tables** may not survive a round-trip | verify on the first file. If they do not, the category is filled by hand from the digest — reported, not worked around |
| **Column width, print settings** are part of the form | never touch `column_dimensions`, `print_area`, `page_setup` |
| `.xls` (legacy binary) | not writable. Convert once, with the owner's agreement, and register the converted file |

Legacy inputs are frequently Excel too — table definitions, code-value lists, message
catalogues exported from the old system. Read them with `data_only=True` to get values
rather than formulas, and remember DIO-08: an exported message list is a hypothesis until
it matches the string in the source.

Conventions that recur in Japanese-market forms: a header block in the first 5–10 rows
(document id, system name, author, approval stamps); one deliverable per sheet with a fixed
sheet name; a `変更履歴` revision sheet separate from the content sheet; `○`/`×`/`—` as the
marker vocabulary. Fill approval cells from `{{profile.project.vendor}}` and
`{{profile.project.client}}` (DS-01), never with a name you inferred.

### Word (`docx`)

Library: `python-docx`.

| Hazard | Rule |
|---|---|
| `Document()` from scratch loses the client's styles | always `Document(tpl_path)` and fill |
| `paragraph.text = ...` destroys runs, and with them bold, colour and field codes | edit the run, or clear runs deliberately and re-add with the intended style |
| Tables grow by row | `table.add_row()`; copy the cell style from the row above |
| Content controls / structured document tags | edit the placeholder text inside them, not the tag |
| Headers, footers, table of contents | do not rebuild. A TOC is refreshed by Word — say so rather than generating a stale one |
| `.doc` (legacy binary) | not writable. Convert once, with agreement |

### CSV

`{{profile.paths.traceability}}`, the bug-trace register, dictionaries, and legacy exports.
UTF-8 with BOM when the client opens them in Excel on Windows; quote every field containing
a comma or newline; **append rather than rewrite** (TR-06); never reorder existing rows in an
edit that adds one.

### PowerPoint, PDF, images

`pptx` and `pdf` are input formats (client decisions, legacy handover packs, scanned
specifications) read with `python-pptx` and the PDF reader; they are not deliverable formats
the pack generates. Legacy screen captures under
`{{profile.legacy.screen_capture_dir}}` are images and are read directly — see `mig-mockup`.

---

## 4. Where templates live, and what is committed

```
{{profile.templates.root}}/
  screen-design.xlsx            the client's blank form, committed, never written to
  function-design.xlsx
  _received/                    originals as received, with their dates

{{profile.templates.legacy_documents_dir}}/
  ...                           the OLD system's documents: read-only inputs (DIO-08)
```

Add both directories to `{{profile.constraints.readonly_globs}}` so the guard hook blocks a
write. Output always goes to the category's own directory, from a fresh copy per file.

A new template version from the client is a new file with its version in the name, plus a
registry update — never an overwrite. Then list every document already generated against the
old version: that list is the re-work estimate, and it is smallest the moment it is produced.

---

## 5. Self-check before reporting a document written

- [ ] the template branch taken (registry / skeleton / blocked) was stated in the plan
- [ ] the output is a **copy**; the template file is unmodified
- [ ] every placeholder is filled or listed as an Open Item — none left as `{{...}}`,
      `XXXX` or `○○`
- [ ] nothing outside the filled fields changed (DIO-03), verified on the category's first file
- [ ] merged-cell anchors used; no write landed in a non-anchor cell
- [ ] the revision/approval block carries the profile's vendor and client, no invented name
- [ ] **every behavioural statement still carries its legacy anchor**, whatever the form
      (NI-01) — a form with no anchor column is a template gap, not an exemption
- [ ] no behaviour anchored to a legacy *document* where the legacy *code* was available
      (DIO-08)
- [ ] a `.md` digest exists for every binary deliverable, and it carries the anchors (DIO-07)
- [ ] the format matches `registry[].output_format`, not what was convenient
- [ ] template gaps and invariant conflicts reported **once**, to the document owner

## 6. Report

```
Document I/O
  Category        : {key}
  Template        : {path} ({format})  |  skeleton (none registered)
  Output format   : {format}
  Files written   : {n}   digests: {n}
  Placeholders    : {filled}/{total}   unfilled -> Open Items: {n}
  Anchors         : {resolved}/{total}   from legacy source: {n} · from legacy document: {n}
  Fidelity check  : {pass on first file | diff found: what}
  Template gaps   : {n}  {each, once}
```

The anchor split in that report is the one to read. Anchors resolved from a legacy
*document* rather than from source are the rows most likely to be wrong (DIO-08); list them
so the reviewer can decide whether the source needed checking.
