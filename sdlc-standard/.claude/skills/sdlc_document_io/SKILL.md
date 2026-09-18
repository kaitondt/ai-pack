---
name: sdlc_document_io
description: "Deliverable templates and multi-format document I/O — how a project's own templates are registered and honoured, and how to read and write Markdown, Excel, Word and CSV deliverables without destroying the client's form. Load for ANY task that reads or writes a deliverable, alongside the category skill."
---

# Deliverable templates and document I/O

> Prerequisite: `sdlc_project` resolved. Template registry comes from
> `{{profile.templates}}`; enabled formats from `{{profile.templates.formats_enabled}}`.

**The pack ships no templates.** Every organisation has its own deliverable forms, in its
own format, with its own column names and its own approval block — and in the Japanese SI
market most of them are Excel. A template invented here would be rejected at the first
review, and worse, it would be rejected *after* forty documents had been generated into it.

So the template is an **input to the project**, collected at `/sdlc_init` and maintained by
`/sdlc_template_register`. This skill owns what happens once one exists.

---

## 1. Template resolution — before generating anything

For the category you are about to write, look it up in `{{profile.templates.registry}}` by
`key`:

| Registry state | Do this |
|---|---|
| entry with `status: provided` and a readable file | use it; it is the authority (DIO-01) |
| entry with `status: provided` but the file is missing or unreadable | **stop**. Report the path. Do not fall back silently — the user believes a template is in force |
| no entry, `on_missing: ask` | stop and ask for the template. Offer the skill's own section list as the alternative, and say what it would produce |
| no entry, `on_missing: skeleton` | generate from the category skill's section list, and **say so in the report** for every file produced |
| no entry, `on_missing: block` | refuse the category and name `/sdlc_template_register` |

State which branch you took, per category, in the plan you print before generating. A run
that quietly used a skeleton where the client expected their own form has produced work
that will be redone.

---

## 2. The rules

### DIO-01 — The template is authoritative over the skill

Where a registered template and the category skill's section list disagree, **the template
wins**, and the difference is reported. Never silently resolve it.

Three cases, three different actions:

| Disagreement | Action |
|---|---|
| Template has a section the skill does not describe | fill it. Ask what belongs there if it is not obvious; never leave a client's section blank without an explicit "not applicable" |
| Skill requires content the template has nowhere to put | report it as a **template gap**, with what the content is and why the skill requires it. Do not drop the content and do not bolt a new section on unilaterally |
| Template contradicts an invariant rule (no revision table, no Open Items, auto-versioning) | the template still wins on **form**; the invariant is raised as a finding against the template, to the document owner. Record it once, not once per document |

`{{profile.templates.template_wins_over_skill}}` records this; it exists so a project that
genuinely wants the pack's skeleton can say so, not so the rule can be waived per file.

### DIO-02 — Never invent, extend or "improve" a template

Not a helpful extra column. Not a renamed header that reads better. Not a reordered
section. The client's tooling parses these documents, their reviewers read them in a fixed
order, and a template drift discovered at acceptance is re-work across every file written
since.

A genuine improvement goes to the document owner as a proposal, and enters the project as a
new template version — the same way any other baselined artifact changes.

### DIO-03 — Round-trip fidelity

When `{{profile.templates.preserve_unfilled_structure}}` is true, writing a deliverable into
a copy of the client's file must change **nothing outside the filled fields**: not column
widths, not merged ranges, not print areas, not the sheet order, not the styles, not the
defined names, not the header and footer.

The test is mechanical and worth running on the first file of every category: write one
deliverable, then diff the produced file against the template for everything except the
cells you meant to fill. If the diff is larger than your edits, the writer is wrong — fix
the writer before generating the other thirty-nine.

### DIO-04 — The template's own placeholders are the field map

When `registry[].fields` is empty, derive the fields from the template itself. Recognised
placeholder forms, in the order they are looked for:

```
{{field}}   {field}   <field>   ${field}   XXXX   ○○○○   〇〇   ____
```

Report the map you derived before filling it — an unrecognised placeholder left in a
delivered document is the most visible possible defect, and the cheapest to catch here.

Conversely, a placeholder you could not fill is an **Open Item**, not a blank cell and not a
plausible value (RS-01).

### DIO-05 — Format is a property of the category, not the task

`registry[].output_format` decides what is written; when empty, output matches the
template's own format. A request phrased in chat does not change it. If the client's screen
design is `.xlsx`, then the screen design is `.xlsx` — producing a Markdown one "because it
is easier to review" creates a second source of truth, and the two diverge within a week.

The one legitimate split: `output_format: md` against an `xlsx` template, for a project that
has agreed Markdown is the working form and Excel is generated for delivery. Agree it once,
record it in the registry, and generate the Excel from the Markdown — never maintain both by
hand.

### DIO-06 — Documents the client sends are inputs, and they are read the same way

Requirements arrive as Word. Interface specs arrive as Excel with one sheet per endpoint.
Meeting decisions arrive as PowerPoint. These are elicitation records under RS-01 and they
are **read**, not retyped, not summarised from the filename, and not assumed to match the
last version you saw.

Record the source file path and, where the format has one, the last-modified date in the
document that cites it. "Per the client's interface spec" is not a source; "per
`docs/_incoming/IF_SPEC_v3.xlsx` sheet `API-014`, received 2026/03/12" is.

### DIO-07 — Binary deliverables are still reviewable

An `.xlsx` or `.docx` deliverable cannot be diffed in a pull request. Two consequences, both
required rather than optional:

1. **Regenerate rather than hand-edit** whenever a generator exists — the reviewable artifact
   is then the input plus the generator, not the binary.
2. **Emit a plain-text digest** alongside every binary deliverable, at the same path with a
   `.md` extension under `{{profile.paths.reviews}}/digests/`, carrying the field values that
   were written. The digest is what the reviewer and `/sdlc_review_design` read; the binary
   is what the client receives.

Without the digest, a binary deliverable is outside every review, cross-check and gate the
pack runs — which is exactly how a category passes P2 without anyone having read it.

---

## 3. Per-format mechanics

Check the toolchain before the first write of a run, not per file. `/sdlc_profile_check`
verifies each enabled format; if an import fails, report it and stop rather than falling
back to Markdown.

### Markdown (`md`)

The default and the only format that is diffable as-is. Follow
`rules/sdlc/document-standards.md` in full: DS-01 skeleton, DS-07 cell conventions, DS-08
diagrams as fenced `{{profile.document.diagram_tool}}` blocks.

A Markdown template is used by **copying it and filling the headings**, not by writing a new
file that happens to have similar headings. Heading text, level and order come from the
template.

### Excel (`xlsx`)

Library: `openpyxl` (read/write, preserves most formatting). Read-only tabular extraction:
`pandas.read_excel`. **Never** rebuild the file with `pandas.to_excel` — it discards every
piece of formatting the client's form consists of.

```python
from openpyxl import load_workbook
wb = load_workbook(tpl_path)          # keep_vba=True for .xlsm
ws = wb[sheet or wb.sheetnames[0]]
ws["C4"] = value                      # write into cells, never rewrite the sheet
wb.save(out_path)                     # save a COPY; the template is never the output
```

What breaks, and what to do about it:

| Hazard | Rule |
|---|---|
| **Merged cells** — writing to any but the top-left cell of a merge is silently lost | write to the anchor cell; find it in `ws.merged_cells.ranges` |
| **Grid-paper layouts** (方眼紙) — one logical field spans many narrow cells | treat the merge anchor as the field. Never unmerge to "make it simpler"; the print layout is the deliverable |
| **Row insertion** shifts formulas, merges, conditional formats and print areas | prefer a template with enough pre-formatted rows. Where you must insert, use `ws.insert_rows` and re-verify merges and the print area afterwards |
| **`ws.max_row` over-reports** on templates with formatted-but-empty rows | find the end by scanning the key column for the last non-empty value |
| **Formulas** are read as strings with `data_only=False`, and as stale cached values with `data_only=True` | never write a value into a formula cell. To read a computed value, read the cached one and say in the report that it is cached |
| **Charts, images and pivot tables** are dropped or corrupted by some round-trips | verify on the first file. If they do not survive, the category is filled by hand from the digest, and that is reported, not worked around |
| **Column width and print settings** are part of the form | never touch `column_dimensions`, `print_area`, `page_setup` unless the template is wrong and the owner agreed |
| `.xls` (legacy binary) | not writable. Convert to `.xlsx` once, with the owner's agreement, and register the converted file |

Conventions that recur in Japanese-market templates, worth checking for before writing:
a header block in the first 5–10 rows (document id, system name, author, approval stamps);
one deliverable per sheet with a fixed sheet name; a `変更履歴` revision sheet separate from
the content sheet; `○`/`×`/`—` as the marker vocabulary rather than words. Fill the
approval cells with the profile's vendor and client values (DS-01), never with a name you
inferred.

### Word (`docx`)

Library: `python-docx`.

| Hazard | Rule |
|---|---|
| Creating a new `Document()` loses the client's styles | always `Document(tpl_path)` and fill; never build from scratch |
| Writing `paragraph.text = ...` destroys the runs and with them bold, colour and field codes | edit the run, or clear the runs deliberately and re-add with the intended style |
| Tables grow by row | `table.add_row()`; copy the cell style from the row above |
| Content controls / structured document tags | edit the placeholder text inside them, not the tag |
| Headers, footers, and the table of contents | do not rebuild. A TOC is refreshed by Word, not by the writer — say so rather than generating a stale one |
| `.doc` (legacy binary) | not writable. Convert once, with agreement |

### CSV

The register formats (`{{profile.paths.traceability}}`, defect and bug-trace registers) and
any dictionary. Rules: UTF-8 with BOM when the client opens them in Excel on Windows, quote
every field containing a comma or a newline, one row per link, **append rather than rewrite**
(TR-08), and never reorder existing rows in an edit that adds one.

### PowerPoint, PDF, images

`pptx` is an input format (decision records, client walkthroughs) read with `python-pptx`; it
is not a deliverable format the pack generates. PDF and images are read for reference and
written only as mockup exports (`sdlc_mockup`).

---

## 4. Where the template lives, and what is committed

```
{{profile.templates.root}}/
  screen-design.xlsx            the client's blank form, committed, never written to
  function-design.xlsx
  requirements.docx
  _received/                    original files as received, with their dates
```

The template is a **read-only input**: add it to `{{profile.constraints.readonly_globs}}` so
the guard hook blocks an accidental write. Output always goes to the category's own
directory, from a fresh copy of the template per file.

A new template version from the client is a new file with its version in the name, plus a
registry update — not an overwrite. Documents already generated against the old one are
listed when the registry changes; that list is the re-work estimate, and it is smaller the
sooner it is produced.

---

## 5. Self-check before reporting a document written

- [ ] the template branch taken (registry / skeleton / blocked) was stated in the plan
- [ ] the output is a **copy**; the template file is unmodified
- [ ] every placeholder in the template is either filled or listed as an Open Item — none
      left as `{{...}}`, `XXXX` or `○○`
- [ ] nothing outside the filled fields changed (DIO-03), verified on the first file of the
      category
- [ ] merged-cell anchors were used; no write landed in a non-anchor cell
- [ ] the approval / revision block carries the profile's vendor and client values, and no
      invented name or date
- [ ] a `.md` digest exists for every binary deliverable (DIO-07)
- [ ] the format matches `registry[].output_format`, not what was convenient
- [ ] any template gap or invariant conflict was reported **once**, to the document owner,
      not silently absorbed per file

## 6. Report

```
Document I/O
  Category        : {key}
  Template        : {path} ({format})  |  skeleton (no template registered)
  Output format   : {format}
  Files written   : {n}   digests: {n}
  Placeholders    : {filled}/{total}   unfilled -> Open Items: {n}
  Fidelity check  : {pass on first file | diff found: what}
  Template gaps   : {n}  {each, once}
```
