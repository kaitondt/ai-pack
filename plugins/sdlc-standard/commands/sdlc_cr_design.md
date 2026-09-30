---
description: "CR phase 3 — update the design documents for an approved option, in cascade order. No code. Ends at GATE 2, waiting for the document diff to be approved. Usage: /sdlc_cr_design [scope note]"
---

# CR — Update the design documents

Runs only after GATE 1. **No code in this phase** (C4).

## Step 1 — Load

`sdlc_project`, then `sdlc_change_request`, then the category skill that owns each document
being edited (`{{profile.paths.bd_categories}}` names them). A CR does not suspend the
category rules.

## Step 2 — Confirm the approval

State back: the CR id, the chosen option, the answers to the open questions, and who
approved. No explicit choice → stop and re-print GATE 1.

## Step 3 — Open the baseline

Write the CR id to `.claude/.active_cr`. That is what unblocks edits to baselined documents
(BL-02) — and it is what `/sdlc_cr_report` clears when the CR closes.

If the CR id is not yet known, phases 3–5 can run under a placeholder, but say so: the
report cannot be written without the real id (C5).

## Step 4 — Edit in cascade order

`{{profile.change_request.cascade}}`, in order. Later documents consume earlier ones;
out-of-order edits produce a set that contradicts itself.

Apply D1..D9 from the skill. In particular:

- every impact-matrix row marked required is edited, or explicitly deferred with a reason
- a rename propagates **everywhere** — documents, mockups, index documents, test cases
- section skeletons stay fixed; a CR changes content, never structure
- baselined documents get a revision row naming the CR id and a version bump (BL-08)
- counterpart-language directories get the equivalent business change (C7)
- traceability rows cite the CR id as the ancestor (C11)

## Step 5 — Re-run the cross-checks on what changed

X-01/X-02, X-03/X-04, X-05, X-06, X-07, and X-09 if an `NFR-*` moved. A cascade that
updated five documents and broke the sixth is the normal failure here.

## Step 6 — GATE 2

Print the diff table — `document · section · before · after · new version` — plus any
required row not yet done and why. Then stop:

> Approve these document changes so implementation can start?

## Report

```
CR {id} — design update
  Documents edited : {n}/{n required}   deferred: {n} ({reasons})
  Cascade order    : followed {yes|no}
  Cross-checks     : {each, pass/fail}
  Indexes updated  : {yes|n/a}   Counterpart language: {yes|n/a}
  Traceability     : {n} rows citing {CR id}
  Active CR marker : .claude/.active_cr = {id}
```
