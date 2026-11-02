# RULE FAMILY: MANAGEMENT ID NAMING

Management artifacts cross-reference constantly: a report cites a risk, a risk cites a work
package, a change request cites a deliverable and a decision. Those references are only
usable if the identifiers are deterministic and permanent.

Formats come from `{{profile.wbs.code_format}}`, `{{profile.change_control.id_format}}` and
the register definitions in `{{profile.risk}}` and `{{profile.paths}}`.

## PN-01 — The standard identifier set

| Object | Format | Register |
|---|---|---|
| Work package | `{{profile.wbs.code_format}}` | WBS dictionary |
| Deliverable | `D-{NNN}` | scope statement |
| Milestone | `M{N}` | schedule |
| Risk | `RSK-{NNN}` | risk register |
| Issue | `ISS-{NNN}` | issue log |
| Change request | `{{profile.change_control.id_format}}` | change register |
| Decision | `DEC-{NNN}` | decision log |
| Assumption | `ASM-{NNN}` | assumption log |
| Action item | `ACT-{NNN}` | action log |
| Dependency | `DEP-{NNN}` | scope / schedule |
| Corrective action | `CAPA-{NNN}` | CAPA log |
| Meeting | `MTG-{YYYYMMDD}-{NN}` | meetings |
| Lesson | `LL-{NNN}` | lessons learned |

Numbers are zero-padded to three digits and issued sequentially from the register. The
register is the allocator: never invent an ID by guessing the next number from a document.

## PN-02 — WBS codes are hierarchical, stable and never reused

`PRJ.4.2.1` means level 1 = 4, level 2 = 2, level 3 = 1. The code carries the position, so
the position cannot change without changing the code.

When scope is removed, the code is **retired**, not reassigned. `PRJ.4.2.1` refers to one
thing for the life of the project and for the life of the archive. Reusing a retired code
silently corrupts every historical report that cited it.

New work added by a change request takes the next free number at its level, and its
dictionary entry names the CR that created it.

## PN-03 — IDs are permanent and never translated

An ID is never renumbered to close a gap, never reordered to look tidy, and never
translated. `RSK-{NNN}` stays `RSK-{NNN}` in the Japanese report, the Vietnamese minutes and
the English contract annex.

Gaps in a sequence are normal and are left alone: a withdrawn CR keeps its number, marked
withdrawn, so that the record shows it was raised.

## PN-04 — Every management object cites its ancestors

| Object | Must cite |
|---|---|
| Work package | the deliverable and the requirement(s) it produces |
| Schedule activity | its work package |
| Cost line | its work package or its control account |
| Risk | the work packages or milestones it threatens |
| Issue | the risk it materialised from, when there was one |
| Change request | the requirement / deliverable / baseline it changes |
| Decision | what it affects |
| Action | the meeting, report or issue it came from |
| Lesson | the risk, issue or CR it was learned from |

An object with no ancestors is either unnecessary or evidence of unplanned work. Both are
worth knowing, and `/pm-trace-check` reports them.

## PN-05 — Report filenames are sortable and self-describing

```
{cadence}_{YYYYMMDD}[_{key}].md      weekly_20260412.md, monthly_202604.md
CR-{NNN}_{short-slug}.md             CR-{NNN}_add-export-format.md
MTG-{YYYYMMDD}-{NN}_{topic}.md       MTG-{YYYYMMDD}-{NN}_ccb.md
gate_{milestone}_{YYYYMMDD}.md       gate_M3_20260430.md
```

Date-first names sort chronologically in every tool anyone will use. A report named
`weekly-report-final-v2-updated.md` is a report nobody will find in six months, which is
exactly when the dispute happens.

## PN-06 — One name for one thing, project-wide

A deliverable, a milestone or a work package has one name, used identically in the charter,
the WBS, the schedule, the contract annex and every report.

When the contract calls it "Phase 2 Delivery" and the schedule calls it "Release 2", the
first change request will spend a meeting establishing that they are the same thing — and
the acceptance discussion will spend longer. Register the mapping in the glossary if the
contract name cannot be changed.
