# RULE FAMILY: MANAGEMENT DOCUMENT STANDARDS

Management documents are read by people who did not attend the meeting, sometimes years
later, sometimes in a dispute. They are contractual artifacts, and they are written that
way.

Settings come from `{{profile.document}}` and `{{profile.language}}`.

## MD-01 — The standard skeleton

Every management deliverable, in this order:

```
1. Title block        document name, project, version, status, date, confidentiality
2. Revision history   {{profile.document.revision_table_headers}}
3. Approval block     role, name, signature/record, date  (when require_approval_block)
4. Distribution list  who receives it              (when require_distribution_list)
5. Purpose and scope  what this document decides, and what it does not
6. Body               the document's own sections
7. Open Items         id, item, owner, due date, impact if unresolved — "None." when empty
8. References         documents this one depends on, with versions
9. Footer             {{profile.document.footer}}, once, at the end
```

Status is one of `draft` · `in review` · `approved` · `baselined` · `superseded`. The status
on the title block and the state of the baseline register always agree.

## MD-02 — No automatic version bump

Add a revision-history row **only** when explicitly instructed, or when a gate baselines the
document. `{{profile.document.auto_version_bump}}` stays `false`.

Drafts run `0.1`, `0.2`, `0.3`. Baselining takes the document to
`{{profile.document.baseline_version}}`. After baseline, a CR-driven change takes the next
minor (`1.1`), and a re-baseline takes the next major (`2.0`).

Every row names what changed and why, and cites the `CR-*` or `DEC-*` behind it. "Updated"
is not a change description.

## MD-03 — References carry versions

A management document that cites another document cites its **version**: "Scope Baseline
v1.2", not "the scope baseline". Baselines move; a reference without a version silently
re-points to whatever exists today, which is how two people quote the same document to
opposite conclusions.

## MD-04 — Every commitment is attributable

Any statement of what will be delivered, by when, for how much, or to what quality standard
traces to: the charter, a baselined document, an approved CR, a recorded `DEC-*`, or a
contract clause.

A plausible sentence with no anchor is the specific failure mode of management writing: it
reads exactly like a commitment that was agreed, it survives review because it is
reasonable, and it is discovered at acceptance by the person who never agreed to it.

Where there is no anchor, write the open question or the labelled assumption instead.

## MD-05 — Numbers carry their units, currency and as-of date

`120` is not an estimate. `120 person-hours, bottom-up, as of 2026/04/12` is. Every figure
in a management document carries unit (or currency), method where relevant, and the date it
was true. Percentages carry their denominator: "40% complete" of what, measured how.

## MD-06 — Open Items is a section, not an omission

Every document has an Open Items section, even when it reads "None." Each item: an ID, the
item, one named owner, a due date, and the impact if it is not resolved.

A document that hides its unresolved points inside the prose looks finished and is not. The
section is where a reviewer looks first, and where the next gate starts.

## MD-07 — Language follows the directory and the audience

Deliverable language is set by `{{profile.language.by_path}}`, never by the language of the
request. Client-facing reports use `{{profile.language.client_facing}}`.

`{{profile.language.immutable_tokens}}` are never translated — WBS codes, IDs, metric names,
formulas and amounts stay byte-identical across every language version, so a translated
report can still be reconciled against the register.

When a document exists in two languages, one is authoritative and says so on the title
block. Two authoritative versions is two projects.

## MD-08 — Write for the reader who was not there

No unexplained internal shorthand. No pronouns whose referent was on the call. No "as
discussed". Each document stands alone: someone joining the steering committee in month
seven should be able to read the last monthly report and understand the position without
asking anyone.

The test is simple and worth applying literally: if the document requires you to explain it,
it is not finished.

## MD-09 — Format is a property of the artifact, and the WBS is Excel

Every management artifact has one final form, bound in `{{profile.documents.registry}}` and
agreed with the client once. It is not chosen per task because one format was quicker to
write, and it does not drift to Markdown because Markdown is easier to review.

`{{profile.documents.binary_final}}` lists the artifacts whose final form **must** be a
binary office file. **The WBS is on that list and is delivered as `.xlsx`.** Markdown and CSV
are legitimate working forms while decomposing — text is easier to restructure than a
workbook — but they are never delivered, never cited and never baselined.

A run that reports the WBS complete with only a Markdown file on disk has not produced the
deliverable, however good the content is. `pm-document-io` DIO-W owns the mechanics, the
workbook layout and the revision hazard.

The reason is not formatting taste. Cost, progress, resource loading and earned value all
index into the WBS by code, and every one of those consumers is a spreadsheet. A WBS that is
not one gets re-keyed into one by hand, and from that moment there are two WBSs.

## MD-10 — A working file is not a deliverable, and says so on line one

Drafting in text before producing a workbook is encouraged. Delivering the draft is not, and
the distance between the two is one careless copy.

So every file under `{{profile.documents.working_dir}}` opens with a stamp saying whether it
is a draft or a generated export, and an export names the version it came from:

```
> DRAFT — working file for pm/scope/wbs.xlsx. Not a deliverable. Not baselined.
> GENERATED from pm/scope/wbs.xlsx v1.2 on 2026/09/15. Do not edit — edit the workbook.
```

Three consequences:

- **Exactly one authority per artifact.** A `wbs.md` and a `wbs.xlsx` both present, both
  plausible, differing by three work packages, with nobody able to say which was approved, is
  the failure this rule exists to prevent.
- **The baseline register points at the deliverable**, never at a working file. A baselined
  path under `working_dir` is a Critical finding.
- **Never regenerate a workbook from a working file whose stamp is older than the workbook.**
  Someone edited the workbook directly; regenerating over it destroys their change silently
  (DIO-W).
