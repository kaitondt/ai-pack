---
name: pm_document_io
description: "Reading and writing management deliverables in Word, Excel, Markdown and CSV — the per-artifact format binding, the working-file discipline, and the rule that the WBS is delivered as Excel. Load for ANY task that produces or reads a management artifact, alongside the area skill."
---

# Document I/O for management deliverables

> Prerequisite: `pm_project` resolved. Format bindings come from
> `{{profile.documents.registry}}`; enabled formats from
> `{{profile.documents.formats_enabled}}`.

Management deliverables are contractual artifacts. A weekly report is read by someone
deciding whether to escalate; a WBS is read by someone deciding what to pay for. Their
**format is a property of the artifact**, agreed once with the client, not chosen per task
because one was quicker to write.

This skill owns three things: which format each artifact ends up in, how to read and write
each format without destroying it, and the discipline that keeps a scratch file from being
delivered by accident.

---

## 1. Resolve the format before writing anything

Look the artifact up in `{{profile.documents.registry}}` by `artifact`:

| Field | Meaning |
|---|---|
| `path` | where the **final deliverable** goes |
| `format` | the final form. `md` · `xlsx` · `docx` · `csv` |
| `working[]` | scratch forms permitted while drafting. Never delivered, never baselined |
| `template` | the client's own form to write into, when they supplied one |
| `sheets` | `xlsx` only: which sheet carries what |

No registry entry → ask which format the artifact is delivered in, and add the entry. Do not
default to Markdown because it is convenient; that is the decision this registry exists to
stop being made silently, forty documents in.

**`{{profile.documents.binary_final}}` is the hard list.** An artifact named there has not
been produced until the binary file exists at its registry `path`. A complete, beautiful
Markdown version of it is a working file (DIO-W).

---

## DIO-W — The WBS is delivered as Excel

The rule this pack is most often asked about, stated once, plainly.

**Think in whatever form helps. Deliver `.xlsx`.**

| Form | Status |
|---|---|
| `{{profile.paths.wbs}}` (`.xlsx`) | **the deliverable.** The authority. What gets baselined, cited, and paid against |
| `{{profile.documents.working_dir}}/wbs.md` or `.csv` | **scratch.** Legitimate and encouraged while decomposing. Never delivered, never baselined, never cited |

### Why the constraint is absolute rather than a preference

- The client opens it in Excel, filters it, pivots it, and pastes it into their own
  reporting. A Markdown table cannot be filtered, and the first thing they will do is
  retype it — creating a second WBS that immediately diverges from yours.
- Cost, progress, resource loading and earned value all index into the WBS by code. Those
  consumers are spreadsheets. A WBS that is not a spreadsheet is re-keyed into one, by hand,
  every time it changes.
- It is a baselined artifact. Baselining a file whose delivered form is produced by hand
  afterwards means the thing that was approved and the thing that was delivered are two
  different files.

### The sequence

1. **Draft** in `{{profile.documents.working_dir}}/wbs.md` (or `.csv`) — decomposition,
   the 100% rule argument, owners, sizing. This is the right place to think; text is easier
   to restructure than a workbook.
2. **Generate** the workbook at `{{profile.paths.wbs}}` from the draft.
3. **Verify** the workbook: counts, the 100% rule, sizing, owners, acceptance criteria — read
   back from the file that now exists on disk, not from the draft you generated it out of.
4. **Regenerate the derived view** (DIO-05) so the content stays diffable, and **stamp it**.
5. **Dispose of the draft** per `{{profile.documents.working_retention}}`.

Report the workbook path. A run that reports "WBS complete" with only a Markdown file on
disk has not completed (DIO-W).

### Revising an existing WBS — the hazard that matters

The WBS changes constantly during planning, and this is where a working file destroys work:

> Someone edits `wbs.xlsx` directly — adds two packages, fixes an owner. Next planning
> session, the old `wbs.md` draft is picked up, revised, and regenerated over the workbook.
> Their edits are gone, silently, and the file looks fine.

**So: a working file is never the input to a regeneration unless it was exported from the
current workbook.** Two legitimate routes, and no third:

| Route | When |
|---|---|
| Edit `wbs.xlsx` directly | small change: a name, an owner, an estimate, one package |
| **Export** the workbook to a fresh working file, restructure, regenerate | large change: re-decomposing a branch, renumbering, moving work between branches |

Before regenerating from any working file, check its stamp (DIO-06) against the workbook's
current version. If the workbook is newer, **stop and say so** — do not merge by guessing
which change was intended.

### Workbook layout

Sheet `{{profile.documents.registry}}[wbs].sheets.wbs`, one row per WBS element:

| Column | Notes |
|---|---|
| `Code` | `{{profile.wbs.code_format}}`. Text-formatted, or Excel turns `1.2.3` into a date and `1.10` into `1.1` |
| `Level` | 1..`{{profile.wbs.max_levels}}` |
| `Name` | the deliverable, a noun (WB-01). Indent by level for readability |
| `Type` | `deliverable` · `control account` · `work package` |
| `Parent code` | makes the hierarchy checkable by formula, not by eye |
| `Owner` | exactly one named person (WB-04) |
| `Effort (h)` | leaves only; parents are sums |
| `Duration (d)` · `Cost` | leaves only |
| `Control account` | flag at `{{profile.wbs.control_account_level}}` |
| `Deliverable` / `Requirement` | the scope item and requirement it satisfies — the RTM join |
| `Status` | |

Sheet `{{profile.documents.registry}}[wbs].sheets.dictionary`, one row per leaf, columns from
`{{profile.wbs.dictionary_fields}}`. It lives in the **same workbook** when
`dictionary_in_same_workbook` is true — one file, one version, and no way for the WBS and its
dictionary to drift apart, which they otherwise always do.

Mechanics that make it usable rather than merely present:

- **Freeze the header row**, and put `AutoFilter` on it. The client will filter by owner and
  by branch within ten seconds of opening it.
- **Outline grouping** by level (`ws.row_dimensions[r].outline_level`) so branches collapse.
- **Never merge cells in the data region.** Merged cells break sorting, filtering and every
  formula that reads the column. Indentation goes in the cell's alignment, not in a merge.
- **Write the 100% rule as a formula**, not only as a check you ran:
  `=SUMIF($E:$E, $A2, $G:$G)` against the parent's own effort, with a flag column that reads
  `OK` or `MISMATCH`. The client can then see the rule holding in their own tool — and it
  keeps holding after they edit a number, which your one-time check does not.
- **Totals row** per level-1 branch, including the management, QA and handover branches
  (WB-02). Those three reading zero is the report's most useful line.
- Text format on `Code`; number formats with real units on effort, duration and cost (MD-05).

---

## 2. The general rules

### DIO-01 — Format follows the artifact, never the task

`{{profile.documents.registry}}[artifact].format`. Not the language of the request, not what
is faster, not "Markdown for now and Excel later" — later does not arrive, and when it does
there are two files.

Where a project genuinely wants a text working copy of a binary deliverable, that is
`derived_view` (DIO-05), which is generated and stamped, not maintained.

### DIO-02 — One authority per artifact

Exactly one file is the deliverable. Everything else is a draft, a scratch file or a derived
view, and each says so on its face (DIO-06).

The failure this prevents is specific and common: a `wbs.md` and a `wbs.xlsx` both present,
both plausible, differing by three work packages, with nobody able to say which was approved.

### DIO-03 — Write into the client's form when they supplied one

When `registry[].template` names a file, the deliverable is a **copy of that file with the
fields filled** — never a new document with similar headings. Their column names, their
order, their approval block, their sheet names.

Where their form has nowhere to put content the skill requires, report it once as a
**template gap** to the document owner. Do not drop the content and do not add a column of
your own invention; a client's WBS form with a changed column header breaks the macro they
use to import it.

### DIO-04 — Round-trip fidelity

Writing into a template changes nothing outside the filled fields: not column widths, not
merged ranges in the header block, not print areas, not sheet order, not styles.

Verify on the **first** file produced against a new template, not the fortieth: write one
value into each field, then diff everything else.

### DIO-05 — A binary deliverable carries a derived text view

When `{{profile.documents.derived_view}}` is true, regenerate a plain-text view of every
binary artifact after writing it, under `{{profile.documents.working_dir}}`.

It exists so the content is diffable in review and in version control — a `.xlsx` in a diff
is one opaque line, which means a WBS change is invisible to everyone who was not in the
room. The derived view is **generated, stamped and never edited** (DIO-06).

### DIO-06 — Every non-deliverable file states what it is, on line one

Scratch and derived files are one careless copy away from being sent to a client. So each
opens with a stamp:

```
> DRAFT — working file for pm/scope/wbs.xlsx. Not a deliverable. Not baselined.
```

```
> GENERATED from pm/scope/wbs.xlsx v1.2 on 2026/09/15. Do not edit — edit the workbook.
```

The version in an export stamp is what DIO-W checks before regenerating. A working file with
no stamp is treated as stale: stop and ask which it is.

### DIO-07 — Numbers keep their units and their as-of date across formats

MD-05 does not relax in a spreadsheet. A cost column is headed with its currency, an effort
column with its unit, and the sheet carries the as-of date and the estimating method. A bare
`120` in a cell is read as whatever the reader assumes.

Use real Excel number formats rather than typing units into the cell — `1,200 h` as text
cannot be summed, and somebody will try.

### DIO-08 — Registers are CSV or Excel, and appended, never rewritten

Risk, issue, decision, action, change and CAPA registers are tabular and long-lived. One row
per item, IDs permanent (PN-03), new rows appended.

Never rewrite unrelated rows in an edit that adds one: it makes the diff unreviewable and
loses concurrent updates by other people working the same register.

CSV for registers exchanged with other tools; UTF-8 with BOM when the client opens them in
Excel on Windows, or the Japanese and Vietnamese text arrives as mojibake.

### DIO-09 — Language and immutable tokens survive the format change

MD-07 applies in every format. `{{profile.language.immutable_tokens}}` — WBS codes,
milestone and risk IDs, metric names, formulas, currency amounts — are byte-identical across
language versions, so a translated report still reconciles against the register.

In a workbook this means the `Code` column is never localised, and the sheet names are
whatever the registry says rather than whatever language the request came in.

### DIO-10 — Verify the toolchain once per run, not per file

`openpyxl` for `xlsx`, `python-docx` for `docx`. Check at the start of a run that produces
binary output; if the import fails, **report it and stop** rather than falling back to
Markdown — falling back silently is how a `binary_final` artifact ends up as a text file
nobody noticed.

---

## 3. Per-format mechanics

### Excel (`xlsx`)

Library: `openpyxl`. Read tabular data with `pandas.read_excel` if convenient, but **never**
write with `pandas.to_excel` against a template — it discards every piece of formatting the
client's form consists of.

```python
from openpyxl import Workbook, load_workbook
from openpyxl.utils import get_column_letter

wb = load_workbook(tpl) if tpl else Workbook()   # template -> load; otherwise build
ws = wb[sheet_name] if sheet_name in wb.sheetnames else wb.create_sheet(sheet_name)
ws["A2"] = "1.2.3"; ws["A2"].number_format = "@"     # text, or Excel eats the code
ws.freeze_panes = "A2"
ws.auto_filter.ref = ws.dimensions
ws.row_dimensions[7].outline_level = 2
wb.save(out_path)                                     # a COPY; never the template
```

| Hazard | Rule |
|---|---|
| `1.2.3` becomes a date, `1.10` becomes `1.1` | format the code column as text (`@`) **before** writing |
| Merged cells silently swallow writes | write to the merge anchor; never merge in a data region |
| `ws.max_row` over-reports on formatted-but-empty rows | scan the key column for the last non-empty value |
| Formulas read as strings (`data_only=False`) or stale cached values (`data_only=True`) | never write a value into a formula cell; say when a read value is cached |
| Leading-zero codes and long IDs lose their zeros | text format |
| Column widths, print area, page setup are part of a client form | leave them alone unless the form is wrong and the owner agreed |
| `.xls` (legacy binary) | not writable — convert once, with agreement |

### Word (`docx`)

Library: `python-docx`. For a narrative deliverable the client supplies as a Word form —
charter, project management plan, monthly report.

| Hazard | Rule |
|---|---|
| `Document()` from scratch loses their styles, header and approval block | always `Document(template)` and fill |
| `paragraph.text = ...` destroys the runs, and with them bold, colour and field codes | edit the run, or clear runs deliberately and re-add with the intended style |
| Tables grow by row | `table.add_row()`, copying the style of the row above |
| Table of contents | refreshed by Word, not by the writer — say so rather than shipping a stale one |

### Markdown (`md`)

The default for narrative artifacts where the client has not specified otherwise, and the
right form for anything reviewed in a pull request. Follow `rules/pm/document-standards.md`
MD-01 in full: title block, revision history, approval block, distribution list, Open Items,
references with versions, footer.

### CSV

Registers and data exchange. UTF-8 with BOM for Excel on Windows; quote every field with a
comma or newline; append, never rewrite (DIO-08).

---

## 4. Self-check before reporting an artifact done

- [ ] the artifact's registry entry was read, and the output is in its `format`
- [ ] **every `{{profile.documents.binary_final}}` artifact exists as its binary file** at the
      registry path — a Markdown version of one is not the deliverable (DIO-W)
- [ ] exactly one authority on disk; every other file is stamped draft or generated (DIO-02,
      DIO-06)
- [ ] where a template was used: the output is a copy, the form is unmodified, and nothing
      outside the filled fields changed (DIO-03, DIO-04)
- [ ] no regeneration ran from a working file whose stamp is older than the workbook
- [ ] WBS workbook: code column text-formatted, header frozen and filtered, no merged cells
      in the data region, 100% rule present as a formula, branch totals including management,
      QA and handover
- [ ] numbers carry units, currency and an as-of date; units are number formats, not text
- [ ] derived view regenerated and stamped with the source version
- [ ] working files disposed of per `{{profile.documents.working_retention}}`
- [ ] registers appended, not rewritten; no unrelated row touched

## 5. Report

```
Document I/O
  Artifact      : {name}
  Final form    : {path} ({format})   template: {path | none}
  Working files : {n} ({kept | deleted})   derived view: {path | none}
  Binary check  : {each binary_final artifact}: {present | *** MISSING ***}
  Toolchain     : openpyxl {ok|missing} · python-docx {ok|missing}
  Fidelity      : {pass on first file | diff found: what}
  Template gaps : {n}  {each, once}
```
