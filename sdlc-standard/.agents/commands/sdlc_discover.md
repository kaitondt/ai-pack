---
description: "P0 — inception and discovery: stakeholder map, scope statement, business requirements, glossary, decision/assumption/risk logs, and the as-is process model. Usage: /sdlc_discover [business area, or nothing for the whole scope]"
---

# P0 — Discovery

## Step 1 — Load

`sdlc_project`, then `sdlc_discovery`.

## Step 2 — Inventory what already exists

Before eliciting anything, read what the organisation has already written: proposals,
statements of work, existing system documentation, spreadsheets, tickets, process
descriptions. Report what you found and what it already answers.

Existing spreadsheets and workarounds are specifications that have already been debugged by
their users (E-06). They are usually the fastest route to the business rules nobody
remembers stating.

## Step 3 — Produce the elicitation plan

Per business area: who to talk to, what to ask, and which artifact the answers feed. Print
it before starting — a discovery phase without a plan converges on whoever is most
available rather than whoever knows.

## Step 4 — Elicit and record

Delegate per area to `sdlc_analyst`. Every session produces a dated record under
`{{profile.paths.inception}}/elicitation/`, with attendees, questions, answers and the
decisions extracted.

Apply the elicitation method from the skill: process before screens, exceptions before the
happy path, numbers instead of adjectives, the problem behind the request, and confirmation
in writing.

## Step 5 — Build the artifacts

In this order — each consumes the previous:

1. stakeholder map
2. glossary — before the requirements, so they are written in one vocabulary
3. as-is process model per business area
4. scope statement, with every exclusion carrying a reason
5. business requirements `BR-*`, each with owner, priority and source
6. decision log, assumption log, risk register

## Step 6 — Report against the gate

```
P0 — Discovery
  Areas covered     : {n}/{n}
  Elicitation       : {n} sessions recorded, {n} confirmed by the stakeholder
  BR-*              : {n}   with owner {n} · with source {n} · Won't {n}
  Glossary          : {n} terms, {n} with banned synonyms recorded
  Open              : ASM-* {n} open · DEC-* {n} · RSK-* {n} ({n} unmitigated)
  Gate {{profile.gates.P0_inception.exit}} : {each assertion, pass/fail}
```

A `BR-*` without an owner or a source is reported as incomplete, by id. Those two fields are
what every later phase anchors to; filling them later means reconstructing them from memory.

Then run `/sdlc_phase_gate P0`.
