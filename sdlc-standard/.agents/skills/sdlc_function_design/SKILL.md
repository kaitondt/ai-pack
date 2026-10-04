---
name: sdlc_function_design
description: "P2 category — function/processing design. Rule families FD-S (structure), FD-P (parameters), FD-D (diagram), FD-R (rules and calculations), FD-E (errors), FD-T (transactions). Server-side scope discipline, flow-to-table completeness, paging and sorting, idempotency. Load for ALL function-design tasks."
---

# P2 — Function Design

> Load with `sdlc_basic_design`. Prerequisite: `sdlc_project` resolved; SRS baselined.

Function design specifies **server-side processing**: what a request does, in what order,
with what rules, producing what and failing how. It is the document the integration test
verifies, and the document the detail design elaborates.

---

## Section skeleton (FD-S01) — fixed order, nothing omitted

```
# {FunctionName}（{MODULE}-FC-{NNN}）
  <Revision history>  <Review record>  <Contents>

## 1  Function information     purpose, trigger, caller, requirement covered
## 2  Input parameters
## 3  Processing flow          diagram + step table
## 4  Business rules and calculations
## 5  Data access              entities read and written, in order
## 6  Output
## 7  Error cases
## 8  Transaction and concurrency
## 9  Non-functional notes     volume, expected duration, budget from NFR design

## Open Items
```

- **FD-S02 — server-side scope only.** No UI colours, component names, CSS, focus order or
  screen layout. The screen document owns those and links here by id (DS-05).
- **FD-S03 — one function, one document.** A document describing "the order screen's
  functions" cannot be cross-checked against an API contract or covered by a test case.

---

## Parameter rules (FD-P)

**FD-P01 — every parameter typed and constrained**: name, type, length/precision,
required, default, and the validation applied. Blank means "not applicable", not "unknown".

**FD-P02 — parameter names match the interface document byte-for-byte** (X-03). A rename
between the two is a Critical finding, and it is the single most common cross-document
defect.

**FD-P03 — paging and sorting are explicit** for every function returning a list: the
parameter names, the default page size, the maximum, the default sort, and which columns
are sortable. A list function with no paging specification is a defect
(`rules/common/performance.md`).

**FD-P04 — the caller's identity is a parameter of the design**, even when the transport
carries it implicitly. Every function states which permission it requires and what happens
without it (X-05 error `MSG-*`).

---

## Diagram rules (FD-D)

**FD-D01 — top-down flowchart**, per `{{profile.document.diagram_constraints}}`.

**FD-D02 — every branch is labelled** with its condition, in the same words as the rule
table row it implements.

**FD-D03 — every error path terminates in a node naming its `MSG-*`.** A flow that ends in
"error" without an identifier cannot be tested.

**FD-D04 — flow ↔ table completeness, both ways.** Every diagram branch has a row in §4 or
§7; every row in §4 or §7 appears in the diagram. This bidirectional check is what stops
the diagram and the tables from describing two different functions.

**FD-D05 — the step table accompanies the diagram**: step no, action, condition, next
step, error. The diagram is the shape; the table is the specification.

---

## Rules and calculations (FD-R)

**FD-R01 — one rule per row**, with the `REQ-*` it implements. A rule with no requirement
is unrequested behaviour (RS-06).

**FD-R02 — calculations state precision explicitly**: the formula, the intermediate
precision, the rounding mode, the point at which rounding is applied, and the scale of the
result. "Total = qty × price" is not a specification — it is the half that everyone agrees
on.

**FD-R03 — evaluation order is specified when it is observable.** If the function stops at
the first validation failure, say so; if it collects all failures, say so. The two produce
different screens and different test cases.

**FD-R04 — date and time rules name the zone.** Which clock decides "today", what happens
at a day boundary, and how a business calendar (working days, month-end, cut-off time)
applies.

**FD-R05 — every state transition is enumerated**: from-state, event, guard, to-state,
side effects. A status field with no transition table is a status field that will accept
an impossible transition.

---

## Data access (FD-R / §5)

State the entities read and written, in the order they are touched, with the purpose of
each. Logical names in prose; physical names only in the data-design document (DS-06).

Name the index or access path the design depends on for any operation the NFR table
promises to be fast (X-09). "Selects the orders" is not enough when the promise is 2
seconds over 5 million rows.

---

## Error cases (FD-E)

| # | Condition | `MSG-*` | HTTP/result mapping | Data state after | Logged as |
|---|---|---|---|---|---|

- **FD-E01** — every error the function can produce has a row, including the ones from
  dependencies (timeout, unavailable, conflicting update).
- **FD-E02** — the error set matches the interface document exactly (X-05).
- **FD-E03** — "data state after" is mandatory. Whether a partial write survives an error
  is the difference between a recoverable failure and a support incident.
- **FD-E04** — internal detail never reaches the user message; it reaches the log
  (`rules/common/security.md`).

---

## Transaction and concurrency (FD-T)

**FD-T01 — transaction boundary is explicit**: where it begins, what it covers, what is
outside it, and what is compensated if a later step fails.

**FD-T02 — concurrent update policy is named**: last-write-wins, optimistic version check,
or a lock — with the `MSG-*` the loser sees. Leaving this to the ORM default is a decision
made by no one.

**FD-T03 — idempotency for anything retryable.** State the key that makes a repeat safe.
Users double-click, clients retry, and batches rerun.

**FD-T04 — long operations state their behaviour**: synchronous with a timeout, or
asynchronous with a status the user can query. A function that takes 40 seconds in a
2-second budget is a design defect, not a performance-tuning task for P4.

---

## Self-check

- [ ] server-side scope only; no UI detail
- [ ] every parameter typed, constrained, and matching the interface document
- [ ] paging, sorting and permission specified for every list function
- [ ] diagram ↔ rule/error tables complete in both directions
- [ ] every calculation states precision, rounding mode and rounding point
- [ ] every state transition enumerated with its guard
- [ ] every error has `MSG-*`, result mapping and data state after
- [ ] transaction boundary, concurrency policy and idempotency key stated
- [ ] every rule traces to a `REQ-*`
- [ ] Open Items present
