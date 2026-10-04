# RULE FAMILY: TRACEABILITY

A migration is judged on whether the new system provably does what the old one did.
That proof is the traceability chain. It is maintained continuously, not reconstructed
at the end.

## The chain

```
LEG-{AREA}-{NNN}        legacy artifact          P0
      ↓ implements
REQ-{AREA}-{NNN}        requirement              P1
      ↓ realised by
{MODULE}-SC-{NNN}       screen design            P2
{MODULE}-FC-{NNN}       function design          P2
{MODULE}-API-{NNN}      interface design         P2
      ↓ detailed by
{MODULE}-DD-{NNN}       detail design            P3
      ↓ implemented in
<source file>:<symbol>  code                     P4
      ↓ verified by
UT-{MODULE}-{NNN}       unit test                P5
IT-{MODULE}-{NNN}       integration test         P6
UAT-{NNN}               acceptance               P7
```

## TR-01 — Every link is bidirectional and recorded

The register lives at `{{profile.paths.traceability}}` (CSV, one row per link):

```csv
legacy_id,requirement_id,design_id,detail_id,code_ref,test_ids,status,note
LEG-RCV-004,REQ-RCV-012,KK0030PG-FC-001,DD-KK0030PG-003,ReceivingQuery.cs#Handle,"UT-KK0030PG-001;IT-KK0030PG-002",done,
```

- A row is appended the moment a downstream artifact is created — not in a later sweep.
- `status`: `todo | in-progress | done | blocked | excluded | spec-gap`
- `excluded` rows must carry a `note` giving the reason.

## TR-02 — Orphans are defects

Two kinds, both reported by `/mig-trace-check`:

| Kind | Meaning | Severity |
|---|---|---|
| **Upward orphan** | A design/code/test artifact with no legacy or requirement ancestor | Critical — likely invented (see NI-01) |
| **Downward orphan** | A legacy artifact in scope with no descendant | Critical — likely missed scope |

Neither is closed by deleting the row. Upward orphans are either anchored or removed
from the deliverable; downward orphans are either implemented or moved to
`legacy.excluded[]` with a reason.

**Change requests are the one legitimate ancestor that is not `LEG-*`.** Behaviour a client
asked for after sign-off has no legacy source by construction (NI-01's third anchor: an
explicit written client decision). Record the CR id in the ancestor position of the row,
with the report path in `note`:

```csv
CR-014,REQ-RCV-031,KK0030PG-SC-001,DD-KK0030PG-003,ReceivingGrid.tsx#columns,"UT-KK0030PG-014",done,change-requests/CR-014_KK0030PG_remarks-column.md
```

Without that row the artifact is an upward orphan, and correctly so: an unrecorded CR is
indistinguishable from an invention.

## TR-03 — Phase gates are traceability assertions

A phase is complete when its `{{profile.gates.*}}` assertions hold **and** the register
has no orphans for artifacts owned by that phase. `/mig-trace-check` is the gate check;
run it before declaring any phase done.

## TR-04 — IDs are permanent

Once issued, an ID is never reused, renumbered, or re-scoped. A superseded artifact keeps
its ID and gains `status: excluded` with a note pointing at the successor. Renumbering
silently invalidates every downstream reference and every client review already done.

## TR-05 — Cross-document consistency checks

At P2/P3, these pairs must agree. Each mismatch is a Critical finding:

| Check | Left | Right |
|---|---|---|
| X-01 | Screen grid columns | Legacy grid/list definition |
| X-02 | Screen field list | Legacy form control list |
| X-03 | Function input params | API request fields |
| X-04 | Function output fields | API response fields |
| X-05 | Function error codes | API error codes |
| X-06 | Screen MSG-IDs | Function MSG-IDs |
| X-07 | Data-design column list | Legacy DDL / copybook |
| X-08 | Detail design | Actual implemented code |
| X-09 | Mockup — fields, columns, buttons, messages, states, navigation, permissions, dialogs | Screen design |
| X-10 | Mockup — field set, order, tab order, columns, label text, blocked controls | Legacy screen (skipped when `mockup.fidelity` is `redesigned`) |
| X-11 | Environments the pipeline deploys to | `{{profile.target.environments}}` |

`/mig-review-design` runs X-01..X-07; `/mig-generate-detail-design` runs X-08 and emits
the GAP report; `/mig-generate-mockup` runs X-09 and X-10; `/mig-generate-infra` runs X-11.

X-09 to X-11 exist because all three artifacts are routinely maintained outside the document
set. The mockup is what everybody looks at, so a field that exists only there gets built —
and in a migration, a field that exists only there is an invention (NI-01). X-10 is what
holds the mockup to the legacy screen at the fidelity the contract assumes. X-11 catches an
environment the pipeline knows about and the profile does not — including, in the worst case,
a deploy step pointing at legacy production.

None of them is resolved by editing one side to match the other. Decide against the legacy
source; where the legacy is silent, raise a SPEC-GAP with an owner.

## TR-06 — The register is append-friendly, conflict-averse

One row per link, sorted by `legacy_id` then `design_id`. Never rewrite unrelated rows in
the same edit — it makes the diff unreviewable and loses concurrent updates.
