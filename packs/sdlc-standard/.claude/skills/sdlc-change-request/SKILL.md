---
name: sdlc-change-request
description: "Changes to a baselined artifact, in six phases with two approval gates — analyse, options, design update, implementation, test, report. Contains the standing constraints, the CR-versus-defect distinction, the classification table, the impact matrix, the estimate rules, the document cascade and the report template. Load for ALL change-request tasks."
---

# CR — Change Request Workflow

> Prerequisite: `sdlc-project` resolved.
> Six phases, two gates. The gates are the point: a CR run without them is a rewrite
> nobody approved.

```
Phase 1  ANALYSE    as-is from three sources, impact matrix, classification
Phase 2  OPTIONS    two or more options, each estimated       -> GATE 1  option chosen
Phase 3  DESIGN     documents updated in cascade order        -> GATE 2  diff approved
Phase 4  IMPLEMENT  code follows the updated documents
Phase 5  TEST       test cases updated, verification actually run
Phase 6  REPORT     written to {{profile.paths.change_requests}}
```

A CR is also the mechanism that unlocks a baselined document (BL-02). `/sdlc-cr-design`
writes the CR id to `.claude/.active_cr`; `/sdlc-cr-report` clears it.

---

## A change request is not a defect

| | Defect (`BUG-*`) | Change request (this skill) |
|---|---|---|
| What happened | the system contradicts the baselined specification | the specification itself changes |
| Authority | the baselined SRS and design | the CR text; the baseline establishes only the as-is |
| Documents | changed only where they were wrong | always changed — they are the deliverable |
| Gates | one, on the cause | two: the option, then the document diff |
| Cost | absorbed by the project | estimated and approved before work starts |
| Output | defect record | `{{profile.paths.change_requests}}` |

The failure is asymmetric. Treating a CR as a defect gives away scope that was never agreed
and hides a contractual event inside a bug fix; treating a defect as a CR asks the client
to pay for the project's own error. Decide which it is **before** starting; when the
wording is ambiguous ("this should be…" is either), ask.

Under `contract_type: fixed-price`, this distinction is a commercial one and the estimate
in Phase 2 is not optional.

---

## Standing constraints

**C1 — the gates are not self-clearable.** Phases 1–2 are read-only: no `Write`, no `Edit`
to product code or deliverables. Cross a gate only on an explicit approval naming the choice
("option B", "approved"). If the user says "just do all of it", still **print** both gate
blocks in sequence — the record of what was decided is what the client reads back.

**C2 — the CR is the authority, and only within its own text.** RS-01 accepts four kinds of
anchor; a CR is a recorded client decision. That authority is narrow:

| Behaviour | Anchor |
|---|---|
| stated in the CR | the CR, quoted verbatim in the report |
| not mentioned by the CR | unchanged, still anchored to the baselined specification |
| implied but not stated | an open question. Not an assumption |

The trap is the adjacent question. "Add a remarks column to the grid" does not say whether
it sorts, whether it is exported, whether it is required, or whether the other surfaces get
it. That is four questions, not four reasonable defaults.

**C3 — a dependency this project does not own stops the change.** When the CR needs a
schema, an interface or a service owned by another team or an external party
(`{{profile.scope.external_systems}}`, `{{profile.constraints.db_schema_owner}}`), stop.
Report the three live paths — compensate inside this system from data already available,
request the change from the owner with its lead time, or narrow the CR — and let the client
choose. Never route around another team's contract silently.

**C4 — documents first, code second** (BL-03, CM-04). The deliverable set is what the
client signs; code that leads the documents produces a diff nobody can review and a cascade
with holes. The only exception is a purely cosmetic class touching no documented item, and
even then the skip is recorded in the report.

**C5 — the CR id comes from `{{profile.change_request.id_source}}`.** Never invent one,
never derive it from a module id, never number it from the count of files in the report
directory. Phases 1–5 run without it; Phase 6 does not — ask.

**C6 — minimum scope.** Implement the approved option and nothing else. A pre-existing
defect found on the way is recorded in the report and raised as a `BUG-*`; fixing it inside
the CR diff makes both changes unreviewable and unrevertable.

**C7 — language follows the directory** (`{{profile.language.by_path}}`, DS-09).
Counterpart-language directories receive the equivalent business change, never a raw copy.
`{{profile.language.immutable_tokens}}` are never translated, in any direction.

**C8 — surface parity is a question, not an assumption.** When `{{profile.system.surfaces}}`
has more than one entry, every CR against one surface raises the counterpart explicitly.
Silence in the CR is not an answer.

**C9 — existing data is part of the change.** Rows written under the old rule do not
disappear when the rule changes. State what happens to them — shown empty, backfilled,
migrated, knowingly left inconsistent — and have it decided at GATE 1, not discovered in
UAT.

**C10 — report only what actually ran.** Build and test output in the report is real
output. Not run is written as not run; failing is written as failing, with the output.

**C11 — the CR is the ancestor in the register.** Behaviour introduced by a CR has no
`BR-*` ancestor by construction. Record the CR id in the ancestor position of
`{{profile.paths.traceability}}`, with the report path in `note`, at the moment the
artifact changes. Without that row `/sdlc-trace-check` reports the artifact as an upward
orphan — correctly, because an unrecorded CR is indistinguishable from unrequested work
(TR-02).

**C12 — an estimate is part of the option, not a follow-up.** When
`{{profile.change_request.require_estimate}}` is true, no option reaches GATE 1 without
effort, schedule impact and test impact. An option approved without a cost is approved
against a number the client invented.

---

## Classification

Assigned at the end of Phase 1. The class sets the cascade depth, so it is a scoping
decision, not a label.

| Class | Meaning | Documents | Code |
|---|---|---|---|
| `CR-SCOPE` | a capability added to or removed from the agreed scope | scope statement → SRS → full design set | varies |
| `CR-UI` | presentation only: label, order, width, spacing | screen (+ mockup) | UI |
| `CR-FIELD` | a documented item added, removed or re-typed | data → screen → function → interface → detail | UI + service |
| `CR-LOGIC` | business rule, validation, condition, flow | function → screen (if messages move) → interface → detail | service (+ UI) |
| `CR-MESSAGE` | message text, `MSG-*` id, or when it fires | screen → function → interface | message catalogue |
| `CR-REPORT` | printed report or exported file | report / file design | service |
| `CR-DATA` | needs a column, table or result the current model does not supply | data design → everything downstream | service + migration |
| `CR-NFR` | a quality target changes: performance, availability, security, retention | SRS §NFR → architecture → NFR design | varies, often architectural |
| `CR-NEW` | a new module, function or endpoint | full set + index documents | UI + service |
| `CR-REMOVE` | an existing module, function or item withdrawn | affected set + index documents | UI + service |
| `CR-CLARIFY` | not a change — the specification is being read back | possibly documents only | usually none |
| `CR-OUT-OF-SCOPE` | contradicts contracted scope or an approved decision | none | none |

`CR-CLARIFY` legitimately concludes "the current behaviour is already correct" — with
evidence from all three sources, which makes it the class most often concluded too early.
`CR-OUT-OF-SCOPE` stops and states the conflict with anchors, plus the smaller change that
would fit.

`CR-NFR` is the class most often under-scoped: a change from "2 seconds" to "500
milliseconds" is not a tuning task, it is an architecture change with a cascade.

A CR bundling several requests is **split into numbered items**, each classified on its
own. Bundles hide the one item that is `CR-DATA` behind three that are `CR-UI`.

---

## Phase 1 — Analyse

1. **Capture the request verbatim.** The original wording is quoted in the report and is
   the only authority (C2). Do not paraphrase it and then work from the paraphrase.
2. **Identify the module and surfaces.** Resolve the module id against
   `{{profile.ids.module_pattern}}`; note every surface with a counterpart (C8).
3. **Establish the as-is from three sources**, each with an anchor:

   | Source | Read |
   |---|---|
   | requirements | `{{profile.paths.requirements}}` — the baselined `REQ-*` / `NFR-*` |
   | design documents | screen, function, interface, data, detail for the module |
   | code | `{{profile.system.root}}` — UI → client → endpoint → handler → data access |

   Three sources that disagree **before** the CR is applied is a pre-existing defect.
   Record it, do not fix it (C6), and raise it at GATE 1 — it changes which option is safe.
4. **Derive the to-be** as a verifiable statement. A to-be that cannot be turned into a
   test case is not yet analysed. No usable to-be in the CR → stop and ask; this is the
   most expensive omission in a CR.
5. **List the open questions.** Walk this checklist explicitly, every time:

   - [ ] the other surfaces (C8)
   - [ ] sort, filter, required, length and default for anything added
   - [ ] printed reports and exported files
   - [ ] rows already written under the old rule (C9)
   - [ ] batch and scheduled jobs reading the same data
   - [ ] external interfaces carrying the changed field
   - [ ] a new `MSG-*` id or an existing one reused (ID-04)
   - [ ] permissions and visibility conditions
   - [ ] any `NFR-*` the change puts at risk
6. **Build the impact matrix.** Walk the whole cascade
   (`{{profile.change_request.cascade}}`) and mark every row, including the unaffected ones
   — an unlisted row is indistinguishable from an overlooked one.

   | # | Kind | Path | Baselined | Required | Planned change |
   |---|---|---|---|---|---|
   | 1 | requirements | `{{profile.paths.requirements}}/SRS.md` | yes | new `REQ-ORD-031` |
   | 2 | screen design | `…-SC-001…` | yes | new row in the item table |
   | 3 | printed report | `…` | no | not involved |
   | 4 | counterpart surface | `…` | yes | **ask** — pending client answer |

7. **Classify, size and scope the risk.** Class; size (S ≤ 3 files · M 4–10 · L > 10, or
   touching data, an external interface or an `NFR-*`); regression surface (what else reads
   the changed endpoint, table or shared type); blockers.

Continue straight into Phase 2 — Phase 1 does not stop on its own.

---

## Phase 2 — Options

At least `{{profile.change_request.min_options}}` options, each complete on seven axes. One
option only where genuinely only one exists — and then say why.

```
Option {A}: {name}
  Approach     : {2-3 sentences}
  Scope        : {n documents, n service files, n UI files}
  Size         : S | M | L
  Estimate     : {effort}, {schedule impact}, {test impact}      ← C12
  Strengths    : …
  Risks        : …
  Existing data: {what happens to rows written under the old rule}
```

Compare on the axes that actually decide it: which layer absorbs the change, whether an
externally-owned contract is touched, whether a published API breaks (API-V02), whether
existing components are reused, the maintenance cost afterwards, and **what it does to the
schedule** — under a fixed-price contract the schedule impact is usually what the client is
actually deciding about.

End with a recommendation. A neutral list hands the decision back without the analysis that
would let the client make it.

Special cases: an externally-owned dependency → C3, and no option assumes it will change
without asking. A conflict with an already-approved CR or decision → stop and name both
sides with anchors. Unanswered open questions → still produce options, marking which option
depends on which answer.

### GATE 1

Print: as-is → to-be, the impact matrix, the open questions, the options with estimates,
the recommendation. Then stop:

> Which option should be implemented, and what are the answers to the open questions above?

---

## Phase 3 — Design update

Only after GATE 1. Load the category skill that owns each document before editing it
(`{{profile.paths.bd_categories}}` names them) — a CR does not suspend the category rules.

| # | Rule |
|---|---|
| D1 | Follow `{{profile.change_request.cascade}}` in order. Later documents consume earlier ones; out-of-order edits produce a set that contradicts itself |
| D2 | Every impact-matrix row marked required is edited, or explicitly deferred with a reason |
| D3 | Re-run the cross-document checks on what changed: X-01/X-02, X-03/X-04, X-05, X-06, X-07, and X-09 if an `NFR-*` moved |
| D4 | A rename propagates everywhere the old name appears — documents, mockups, index documents, test cases. A half-renamed item is worse than the old name |
| D5 | Section skeletons stay fixed (DS-01, DS-04). A CR changes content, never document structure |
| D6 | Adding or removing a module, function, endpoint or table updates the index/catalogue documents (ID-09) |
| D7 | Counterpart-language directories get the equivalent business change (C7) |
| D8 | Baselined documents get a revision row naming the CR id, and the version bumps per BL-08. Non-baselined drafts do not bump (DS-02) |
| D9 | Update `{{profile.paths.traceability}}` as each document changes, citing the CR id (C11) |

### GATE 2

Print the document diff table, plus any required row not yet done and why. Then stop:

> Approve these document changes so implementation can start?

---

## Phase 4 — Implementation

Only after GATE 2. Load `sdlc-context-mapping` first and emit the map: a CR that edits one
layer of five is the classic source of the next UAT defect.

- The **updated** documents are the specification. Code matching the old document is a
  defect from the moment GATE 2 passes.
- Implement the approved option only. A better idea found mid-implementation goes back
  through GATE 1; it does not get applied quietly.
- Follow the layer order from the context map, through the shared-types node (CM-02) —
  verify how those types are produced before editing them (CM-01, BL-07).
- Behaviour the CR does not mention keeps its existing specification (IM-05).
- A schema change carries its migration, its rollback and its deployment coupling (CM-03).
- Message text lives in the catalogue, not inline, and its `MSG-*` ids match the **updated**
  screen and function documents.

---

## Phase 5 — Test

**The existing test cases now describe the old behaviour.** They are part of the change,
not collateral: update the cases the CR contradicts, add cases for the new behaviour, and
mark withdrawn cases as withdrawn instead of deleting them (`sdlc-test-design`,
`sdlc-test-artifact-lifecycle`).

Then verify in `{{profile.system.build.order}}`: build, type-check, the tests covering the
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

Metadata: CR id, date, module, surface, class, size, chosen option, estimate, status.

## 1. The request
1-1  Original text, verbatim.
1-2  Interpretation: purpose, as-is, to-be, conditions, explicitly out of scope.
1-3  Open questions and the answers received, with dates.

## 2. Impact
2-1  As-is verified from the three sources, with anchors.
2-2  The impact matrix, including the rows that were not affected.
2-3  Risks, dependencies, and any pre-existing defect found (not fixed — C6).

## 3. Options
3-1  The options presented, on the seven axes, with estimates.
3-2  The option chosen, who approved it, when, and why.

## 4. What was done
4-1  Documents updated: document · section · before · after · new version.
4-2  Code changed: path · what · why, with before/after for the load-bearing parts.
4-3  Test cases added, changed, withdrawn.
4-4  Found but out of scope, with the route taken (usually a separate `BUG-*`).

## 5. Verification
Real build, type-check and test output. Manual walk-through results. Regression items
checked — and the ones deliberately not checked.

## 6. Conclusion
Status, what is waiting on the client, what still has to be deployed or confirmed, and
the actual effort against the estimate.
```

Class variants: `CR-DATA` or `CR-NFR` blocked on an externally-owned dependency has no §4
diff — it carries the analysis and the three paths from C3. `CR-CLARIFY` may have documents
only, and §5 carries the evidence that the current behaviour is already correct.
`CR-OUT-OF-SCOPE` carries the conflict and the proposed smaller change, and states plainly
that nothing was implemented.

Finally, clear `.claude/.active_cr` — the baseline protection goes back on (BL-02).

---

## Exit checks

**Gates 1 and 2** — nothing under `{{profile.system.root}}` or
`{{profile.paths.design_root}}` was edited before its gate; both gate blocks were printed;
the approval named a specific option.

**Phase 3** — cascade order followed; every required row done or deferred with a reason;
cross-checks re-run on what changed; index documents and counterpart-language directories
updated; baselined documents versioned with the CR id; traceability rows cite the CR id.

**Phase 4–5** — code matches the updated documents; only the approved option implemented;
externally-owned contracts untouched; test cases updated; verification output is real.

**Phase 6** — CR id from the agreed source; six sections present; verbatim original in
§1-1; a second round appended rather than overwritten; actual effort recorded against the
estimate; `.active_cr` cleared; the report path printed for the user.
