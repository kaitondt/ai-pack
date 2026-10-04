---
name: mig-function-design
description: "P2 category — function/processing design documents. Rule families FD-S (structure), FD-P (parameters), FD-E (errors), FD-D (data access), FD-L (legacy fidelity). Flow-diagram rules, IO parameter tables, error tables with MSG-IDs, paging/sorting contract. Load for ALL function-design tasks."
---

# P2 — Function Design

> Load with `mig-basic-design`. Prerequisite: `mig-project` resolved.

The function design is the **server-side** counterpart of the screen design: what happens
after a trigger, in what order, with what data, and what can go wrong.

---

## Section skeleton (FD-S01)

```
# {FunctionName}（{MODULE}-FC-{NNN}）
  <Revision history>
  <Contents>

## 1  Function overview        purpose, trigger, caller screen/job, related ids
## 2  Processing flow          diagram + numbered steps
## 3  Input parameters
## 4  Output
## 5  Data access              objects touched, operation, transaction boundary
## 6  Business rules           one row per rule, each with a legacy anchor
## 7  Error handling           error table with MSG-IDs
## 8  Related documents        SC / API / DD ids

## Open Items
```

**FD-S02 — scope.** Server-side only. No UI colours, no component names, no CSS, no
client-side field toggling. Those live in the screen design.

**FD-S03 — the flow diagram is normative.** Every branch in section 2 has a corresponding
row in section 6 or 7. A branch present in the diagram but absent from the tables is a
Critical finding.

---

## Flow diagram rules

- top-down flowchart, `{{profile.document.diagram_tool}}` fenced block
- one node per meaningful step; no node that merely says "process"
- every decision node has both edges labelled
- every error path ends in a terminal node naming its `MSG-*` id
- honour `{{profile.document.diagram_constraints}}`

---

## Parameter rules (FD-P)

**FD-P01 — one row per parameter**, with: name, logical name, type, length, required,
default, source, note. The source column says where the value comes from: a screen field
id, a session value, a constant, or a caller.

**FD-P02 — names match the contract.** Input parameter names match the API request field
names exactly (X-03); output field names match the API response fields (X-04). When they
differ, one of the two documents is wrong: determine which against the legacy source.

**FD-P03 — hidden and fixed parameters are documented here**, not in the screen design.
A parameter the user never sees still crosses the wire and still needs a value.

**FD-P04 — paging and sorting are explicit.** When a function returns a list it declares
page number, page size, sort key, sort direction and total-count behaviour. The names are
chosen once and used by every function in the project.

**FD-P05 — no implicit ordering.** If the legacy output order matters and the legacy query
had no explicit sort, that is a finding: record the observed order, anchor it, and specify
an explicit sort that reproduces it.

---

## Data-access rules (FD-D)

- **FD-D01** — every data object touched is listed with its operation and the parameters
  passed.
- **FD-D02** — when `{{profile.constraints.stored_procedures_readonly}}` is true, the
  procedure signature is copied from the legacy definition, never proposed. A required
  change stops the work (LR-02).
- **FD-D03** — transaction boundary stated explicitly: what is inside, what is outside,
  and what happens on partial failure.
- **FD-D04** — the parameter list in this document matches the actual procedure signature
  parameter-for-parameter, in order.

---

## Error rules (FD-E)

**FD-E01 — the error table** has: code, condition, `MSG-*`, message text, severity,
recovery.

**FD-E02 — every error is reachable from the flow diagram**, and every error branch in the
diagram appears in the table.

**FD-E03 — the `MSG-*` set matches the screen design message list** (X-06) and the API
design error list (X-05).

**FD-E04 — no invented error cases.** An error the legacy did not raise is not added
because it seems prudent (NI-02). Raise it in Open Items instead.

---

## Legacy-fidelity rules (FD-L)

- **FD-L01** — the processing sequence follows the legacy sequence. Reordering steps
  changes observable behaviour when the steps have side effects.
- **FD-L02** — calculations reproduce the legacy expression exactly, including rounding
  direction, truncation point and intermediate precision. State the arithmetic explicitly:
  "round half-up at 2 decimals after multiplication, before summation".
- **FD-L03** — validation order matters when the first failure short-circuits. Preserve it.
- **FD-L04** — every rule row carries a legacy anchor, or sits in Open Items.

---

## Self-check

- [ ] flow diagram present, branches labelled, errors terminal with `MSG-*`
- [ ] every diagram branch has a row in the rule or error table
- [ ] parameter names match the API contract in both directions
- [ ] paging and sorting declared; no implicit ordering
- [ ] data-access parameters match the real procedure signature
- [ ] calculations state rounding and precision
- [ ] every business rule anchored
- [ ] Open Items present
