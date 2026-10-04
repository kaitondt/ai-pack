---
description: "P1 — generate the SRS: functional requirements, non-functional requirements, use cases, business rules and acceptance criteria, each traced to a BR-*. Usage: /sdlc-generate-requirements [business area, section, or nothing for the whole SRS]"
---

# P1 — Generate requirements

## Step 1 — Load

`sdlc-project`, then `sdlc-requirements`.

## Step 2 — Pre-check

Required: the P0 artifacts — scope statement, `BR-*` list, glossary, decision log — and a
passed P0 gate. Missing → name the command that produces the missing input and stop.

Requirements written before scope is agreed get rewritten when it is. That is not a
sequencing preference; it is the reason P1 has an entry criterion.

## Step 3 — Plan

Print, per business area: `BR-*` to decompose, use cases expected, and the NFR categories
that apply. Derive the plan from the `BR-*` list, never from a remembered count.

## Step 4 — Generate

Delegate per area to `sdlc-analyst`, one call per area, 10–20 requirements per batch.

Order within the SRS: system context → functional requirements → use cases → business
rules → data requirements → NFRs → interfaces → constraints → acceptance criteria.

**Generate the NFR section deliberately, in its own call.** It is the section that gets
thin when a long run runs out of context, and it is the section whose thinness is invisible
until P7 has nothing to measure.

## Step 5 — Cross-check

Run R-01..R-08 from `sdlc-requirements`. Report each with the artifact ids involved.

## Step 6 — Report against the gate

```
P1 — Requirements
  BR-* decomposed   : {n}/{n}     uncovered: {ids}
  REQ-*             : {n}   testable {n} · with verification ref {n} · with source {n}
  NFR-*             : {n}   by category {breakdown}   with target+method {n}
  Use cases         : {n}   realising {n} REQ
  Acceptance criteria : {n}  covering {n}/{n} Must requirements
  TBD remaining     : {n}   ({ids})       ← blocks baseline (RS-03)
  Open ASM-*        : {n}   ({ids, owners, due dates})
  R-01..R-08        : {pass|fail each}
  Gate {{profile.gates.P1_requirements.exit}} : {pass|fail}
```

Then run `/sdlc-phase-gate P1`. Passing it baselines the SRS — from that moment it changes
only through a change request (BL-02).
