---
name: mig_change_request
description: "Client-initiated change requests in six phases with two approval gates — analyse, options, design update, implementation, test, report. Contains the standing constraints, the CR-versus-bug distinction, the classification table, the impact matrix, the document cascade order and the report template. Load for ALL change-request tasks."
---

# CR — Change Request Workflow

> Prerequisite: `mig_project` resolved.
> Six phases, two gates. The gates are the point: a CR run without them is a rewrite
> nobody approved.

```
Phase 1  ANALYSE    as-is from three sources, impact matrix, classification
Phase 2  OPTIONS    two or more options with a recommendation  -> GATE 1  option chosen
Phase 3  DESIGN     documents updated in cascade order         -> GATE 2  diff approved
Phase 4  IMPLEMENT  code follows the updated documents
Phase 5  TEST       test cases updated, verification actually run
Phase 6  REPORT     written to {{profile.paths.change_requests}}
```

---

## A change request is not a bug

| | UAT bug (`mig_uat_bug`) | Change request (this skill) |
|---|---|---|
| What happened | the code contradicts an approved spec | the spec itself changed |
| Authority | legacy source + approved design | the CR text; legacy only establishes the as-is |
| Documents | changed only where they were wrong | always changed — they are the deliverable |
| Gates | one, on the cause | two: the option, then the document diff |
| Output | `{{profile.paths.uat_reports}}` | `{{profile.paths.change_requests}}` |

The failure is asymmetric. Treating a CR as a bug produces a "fix" that drags behaviour
back to the legacy the client asked to leave, and it passes review because it matches the
anchors. Decide which one it is **before** starting; when the wording is ambiguous ("this
should be…" is either), ask.

---

## Standing constraints

**C1 — the gates are not self-clearable.** Phase 1–2 are read-only: no `Write`, no `Edit`
to product code or deliverables. Cross a gate only on an explicit approval naming the
choice ("option B", "approved"). If the user says "just do all of it", still **print** both
gate blocks in sequence — the record of what was decided is what the client reads back.

**C2 — the CR is the authority, and only within its own text.** NI-01 accepts three kinds
of anchor; a CR is the third — an explicit written client decision. That authority is
narrow:

| Behaviour | Anchor |
|---|---|
| stated in the CR | the CR, quoted verbatim in the report |
| not mentioned by the CR | unchanged, still anchored to legacy (NI-01, NI-02) |
| implied but not stated | an open question. Not an assumption |

The trap is the adjacent question. "Add a remarks column to the grid" does not say whether
it sorts, whether it is exported, whether it is required, or whether the other surfaces get
it. That is four questions, not four reasonable defaults.

**C3 — frozen objects stop the change.** When the CR needs data a read-only object does not
supply (`{{profile.constraints.stored_procedures_readonly}}`, `db_schema_frozen`), stop
(LR-02, LR-03). Report the three live paths — compensate in application code from data
already available, ask the client to change the object, or narrow the CR — and let the
client choose. Never inline a replacement query to route around the freeze.

**C4 — documents first, code second** (CM-04). The deliverable set is what the client signs;
code that leads the documents produces a diff nobody can review and a cascade with holes.
The only exception is a purely cosmetic class touching no documented item, and even then
the skip is recorded in the report.

**C5 — the CR id comes from the client list.** Never invent one, never derive it from a
module id, never number it from the count of files in the report directory. Phases 1–5 run
without it; Phase 6 does not — ask.

**C6 — minimum scope.** Implement the approved option and nothing else. A pre-existing
defect found on the way is recorded in the report and routed to `/mig_uat_investigate`;
fixing it inside the CR diff makes both changes unreviewable and unrevertable.

**C7 — language follows the directory** (`{{profile.language.by_path}}`, DS-08).
Counterpart-language directories receive the equivalent business change, never a raw copy.
`{{profile.language.immutable_tokens}}` are never translated, in any direction.

**C8 — surface parity is a question, not an assumption.** When
`{{profile.target.surfaces}}` has more than one entry, every CR against one surface raises
the counterpart explicitly. Silence in the CR is not an answer.

**C9 — existing data is part of the change.** Rows written under the old rule do not
disappear when the rule changes. State what happens to them — shown empty, backfilled,
migrated, knowingly left inconsistent — and have it decided at GATE 1, not discovered in
UAT.

**C10 — report only what actually ran.** Build and test output in the report is real
output. Not run is written as not run; failing is written as failing, with the output.

**C11 — the CR is the ancestor in the register.** Behaviour introduced by a CR has no
`LEG-*` ancestor by construction. Record the CR id in the ancestor position of
`{{profile.paths.traceability}}`, with the report path in `note`, at the moment the
artifact changes. Without that row `/mig_trace_check` reports the artifact as an upward
orphan — correctly, because an unrecorded CR is indistinguishable from an invention
(TR-02).

---

## Classification

Assigned at the end of Phase 1. The class sets the cascade depth, so it is a scoping
decision, not a label.

| Class | Meaning | Documents | Code |
|---|---|---|---|
| `CR-UI` | presentation only: label, order, width, spacing | screen (+ mockup) | UI |
| `CR-FIELD` | a documented item added, removed or re-typed | screen → function → interface → detail | UI + service |
| `CR-LOGIC` | business rule, validation, condition, flow | function → screen (if messages move) → interface → detail | service (+ UI) |
| `CR-MESSAGE` | message text, `MSG-*` id, or when it fires | screen → function → interface | message catalogue |
| `CR-REPORT` | printed report or exported file | report / file design | service |
| `CR-DATA` | needs a column, table or result a frozen object does not supply | data design | see C3 |
| `CR-NEW` | a new module, function or endpoint | full set + index documents | UI + service |
| `CR-REMOVE` | an existing module, function or item withdrawn | affected set + index documents | UI + service |
| `CR-CLARIFY` | not a change — the spec is being read back | possibly documents only | usually none |
| `CR-OUT-OF-SCOPE` | contradicts contracted scope or an approved design decision | none | none |

`CR-CLARIFY` legitimately concludes "the current behaviour is already correct" — with
evidence from all three sources, which makes it the class most often concluded too early.
`CR-OUT-OF-SCOPE` stops and states the conflict with anchors, plus the smaller change that
would fit.

A CR bundling several requests is **split into numbered items**, each classified on its
own. Bundles hide the one item that is `CR-DATA` behind three that are `CR-UI`.

---

## Phase 1 — Analyse

1. **Capture the request verbatim.** The original wording is quoted in the report and is
   the only authority (C2). Do not paraphrase it into the analysis and then work from the
   paraphrase.
2. **Identify the module and surfaces.** Resolve the module id against
   `{{profile.ids.module_pattern}}`; note every entry in `{{profile.target.surfaces}}` with
   a counterpart (C8).
3. **Establish the as-is from three sources**, each with an anchor:

   | Source | Read |
   |---|---|
   | target code | `{{profile.target.root}}` — UI → client → endpoint → handler → data access |
   | design documents | screen, function, interface, detail for the module |
   | legacy | `{{profile.legacy.ui_source}}`, `{{profile.legacy.logic_source}}`, `{{profile.legacy.db_source}}` |

   Three sources that disagree **before** the CR is applied is a pre-existing defect.
   Record it, do not fix it (C6), and raise it at GATE 1 — it changes which option is safe.
4. **Derive the to-be** as a verifiable statement. A to-be that cannot be turned into a test
   case is not yet analysed. No usable to-be in the CR → stop and ask; this is the most
   expensive omission in a CR.
5. **List the open questions.** Walk this checklist explicitly, every time:

   - [ ] the other surfaces (C8)
   - [ ] sort, filter, required, length and default for anything added
   - [ ] printed reports and exported files
   - [ ] rows already written under the old rule (C9)
   - [ ] batch and scheduled jobs reading the same data
   - [ ] a new `MSG-*` id or an existing one reused (ID-03)
   - [ ] permissions and visibility conditions
6. **Build the impact matrix.** Walk the whole cascade
   (`{{profile.change_request.cascade}}`) and mark every row, including the unaffected ones
   — an unlisted row is indistinguishable from an overlooked one.

   | # | Kind | Path | Required | Planned change |
   |---|---|---|---|---|
   | 1 | screen design | `{{profile.paths.design_root}}/…-SC-001…` | yes | new row in the item table |
   | 2 | printed report | `{{profile.paths.design_root}}/…` | no | not involved |
   | 3 | counterpart surface | `…` | **ask** | pending client answer |

7. **Classify, size and scope the risk.** Class; size (S ≤ 3 files · M 4–10 · L > 10 or
   touching data or frozen objects); regression surface (what else reads the changed
   endpoint, table or shared type); blockers.

Continue straight into Phase 2 — Phase 1 does not stop on its own.

---

## Phase 2 — Options

At least `{{profile.change_request.min_options}}` options, each complete on six axes. One
option only where genuinely only one exists — and then say why.

```
Option {A}: {name}
  Approach     : {2-3 sentences}
  Scope        : {n documents, n service files, n UI files}
  Size         : S | M | L
  Strengths    : …
  Risks        : …
  Existing data: {what happens to rows written under the old rule}
```

Compare on the axes that actually decide it: which layer absorbs the change, whether a
frozen object is touched, whether a published contract breaks, whether existing components
are reused, the maintenance cost afterwards, and **how far the result departs from the
legacy** — that last one weighs more than it looks, because the rest of the system, its
documents and the client's own operators were built around the old behaviour.

End with a recommendation. A neutral list hands the decision back without the analysis that
would let the client make it.

Special cases: a frozen object → C3, and no option proposes changing it. A conflict with an
already-approved CR or design decision → stop and name both sides with anchors. Unanswered
open questions → still produce options, marking which option depends on which answer.

### GATE 1

Print: as-is → to-be, the impact matrix, the open questions, the options, the
recommendation. Then stop:

> Which option should be implemented, and what are the answers to the open questions above?

---

## Phase 3 — Design update

Only after GATE 1. Load the category skill that owns each document before editing it
(`{{profile.paths.bd_categories}}` names them) — a CR does not suspend the category rules.

| # | Rule |
|---|---|
| D1 | Follow `{{profile.change_request.cascade}}` in order. Later documents consume earlier ones; out-of-order edits produce a set that contradicts itself |
| D2 | Every impact-matrix row marked required is edited, or explicitly deferred with a reason |
| D3 | Re-run the cross-document checks on what changed: X-03/X-04 (function ↔ interface), X-05 (error codes), X-06 (`MSG-*` sets), X-07 (columns) |
| D4 | A rename propagates everywhere the old name appears — documents, mockups, index documents, test cases. A half-renamed item is worse than the old name |
| D5 | Section skeletons stay fixed (DS-01, DS-03). A CR changes content, never document structure |
| D6 | Adding or removing a module, function, endpoint or table updates the index/catalogue documents (ID-07) |
| D7 | Counterpart-language directories get the equivalent business change (C7) |
| D8 | No version bump unless asked (DS-02). Record each edit as `document · section · before · after · CR reference` |
| D9 | Update `{{profile.paths.traceability}}` as each document changes, citing the CR id (C11) |

### GATE 2

Print the document diff table, plus any required row not yet done and why. Then stop:

> Approve these document changes so implementation can start?

---

## Phase 4 — Implementation

Only after GATE 2. Load `mig_context_map` first and emit the map: a CR that edits one layer
of five is the classic source of the next UAT bug.

- The **updated** documents are the specification. Code matching the old document is a
  defect from the moment GATE 2 passes.
- Implement the approved option only. A better idea found mid-implementation goes back
  through GATE 1; it does not get applied quietly.
- Follow the layer order from the context map, through the shared-types node (CM-02) —
  verify how those types are produced before editing them (CM-01, LR-04).
- Behaviour the CR does not mention keeps its legacy parity rules (IM-01..IM-06).
- Never touch legacy or frozen objects (LR-01, C3).
- Message text lives in the catalogue, not inline, and its `MSG-*` ids match the **updated**
  screen and function documents.

---

## Phase 5 — Test

**The existing test cases now describe the old behaviour.** They are part of the change,
not collateral: update the cases the CR contradicts, add cases for the new behaviour, and
mark withdrawn cases as withdrawn instead of deleting them (`mig_test_design`,
`{{profile.testing.paths.testcase_root}}`).

Then verify in `{{profile.target.build.order}}`: build, type-check, the tests covering the
change, and a manual walk-through of the changed flow. List the regression surface from
Phase 1 step 7 and state what was checked and what was not.

Real output only (C10). A pre-existing failure unrelated to the CR is reported as
pre-existing, with the evidence that it predates the change.

---

## Phase 6 — Report

File: `{{profile.paths.change_requests}}/{CR-ID}_{MODULE}_{short-slug}.md`, in the language
bound to that path. An existing file for the same CR id is **appended to** as a new round,
never overwritten — rounds are how the client sees that the second thoughts were second
thoughts and not the original request.

```markdown
# {CR-ID} — {MODULE} — {short title}

Metadata: CR id, date, module, surface, class, size, chosen option, status.

## 1. The request
1-1  Original text, verbatim.
1-2  Interpretation: purpose, as-is, to-be, conditions, explicitly out of scope.
1-3  Open questions and the answers received, with dates.

## 2. Impact
2-1  As-is verified from the three sources, with anchors.
2-2  The impact matrix, including the rows that were not affected.
2-3  Risks, dependencies, and any pre-existing defect found (not fixed — C6).

## 3. Options
3-1  The options presented, on the six axes.
3-2  The option chosen, who approved it, when, and why.

## 4. What was done
4-1  Documents updated: document · section · before · after.
4-2  Code changed: path · what · why, with before/after for the load-bearing parts.
4-3  Test cases added, changed, withdrawn.
4-4  Found but out of scope, with the proposed route (usually a separate bug).

## 5. Verification
Real build, type-check and test output. Manual walk-through results. Regression items
checked — and the ones deliberately not checked.

## 6. Conclusion
Status, what is waiting on the client, what still has to be deployed or confirmed.
```

Class variants: `CR-DATA` blocked on a frozen object has no §4 diff — it carries the
analysis and the three paths from C3. `CR-CLARIFY` may have documents only, and §5 carries
the evidence that the current behaviour is already correct. `CR-OUT-OF-SCOPE` carries the
conflict and the proposed smaller change, and states plainly that nothing was implemented.

---

## Exit checks

**Gates 1 and 2** — nothing under `{{profile.target.root}}` or
`{{profile.paths.design_root}}` was edited before its gate; both gate blocks were printed;
the approval named a specific option.

**Phase 3** — cascade order followed; every required row done or deferred with a reason;
X-03..X-07 re-run on what changed; index documents and counterpart-language directories
updated; traceability rows cite the CR id.

**Phase 4–5** — code matches the updated documents; only the approved option implemented;
frozen objects untouched; test cases updated; verification output is real.

**Phase 6** — client-issued CR id; six sections present; verbatim original in §1-1; a
second round appended rather than overwritten; the report path printed for the user.
