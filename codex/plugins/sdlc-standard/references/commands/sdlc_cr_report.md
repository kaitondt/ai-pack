---
description: "CR phase 6 — write the change-request report into change-requests/, record actual effort against the estimate, and clear the active-CR marker. An existing report for the same CR is appended to, never overwritten. Usage: /sdlc_cr_report [path to an existing report]"
---

# CR — Report

## Step 1 — Load

`sdlc_project`, then `sdlc_change_request`.

## Step 2 — Get the CR id

From `{{profile.change_request.id_source}}` (C5). Never invent one, never derive it from a
module id, never number it from the count of files in the directory. No id → ask; this
phase cannot run without it.

## Step 3 — Locate or create the file

`{{profile.paths.change_requests}}/{CR-ID}_{MODULE}_{short-slug}.md`, in the language bound
to that path.

An existing file for the same CR id is **appended to** as a new round, never overwritten.
Rounds are how the client sees that the second thoughts were second thoughts and not the
original request.

## Step 4 — Write the six sections

Per the template in `sdlc_change_request` Phase 6:

1. the request — **verbatim** original, interpretation, open questions and their answers
2. impact — as-is from three sources with anchors, the full matrix, risks, any
   pre-existing defect found and not fixed
3. options — all of them with their estimates, the one chosen, who approved it and when
4. what was done — documents, code, test cases, and what was found but left out of scope
5. verification — real build and test output, manual walk-through, regression checked and
   not checked
6. conclusion — status, what is waiting on the client, and **actual effort against the
   estimate**

Class variants: `CR-DATA` or `CR-NFR` blocked on an externally-owned dependency carries the
analysis and the three paths instead of a §4 diff. `CR-CLARIFY` may be documents only.
`CR-OUT-OF-SCOPE` states plainly that nothing was implemented, with the conflict and the
smaller change that would fit.

## Step 5 — Close the CR

- update `{{profile.paths.traceability}}` — every CR-sourced artifact has a row citing the
  CR id (C11)
- record the decision in `{{profile.paths.decision_log}}` where the CR settled something
  that will be asked about again
- **clear `.codex/.active_cr`** — baseline protection goes back on (BL-02)

## Step 6 — Report

```
CR {id} — closed
  File           : {path}   round {n}
  Class / size   : {class} / {S|M|L}
  Option         : {chosen}   approved by {name} on {date}
  Estimate       : {estimated}   actual {actual}   variance {±}
  Documents      : {n} updated   Code: {n} files   Test cases: {n}
  Traceability   : {n} rows citing {CR id}
  Active CR      : cleared
  Outstanding    : {what is waiting on the client or on a deploy}
```

Print the report path for the user.

**Estimate variance is recorded, not smoothed.** It is the only feedback the next
estimate has.
