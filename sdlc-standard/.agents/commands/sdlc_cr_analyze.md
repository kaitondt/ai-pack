---
description: "CR phases 1+2 — analyse a change request and present options. Read-only: no code or document edits. Ends at GATE 1, waiting for the chosen option. Usage: /sdlc_cr_analyze <the change request text>"
---

# CR — Analyse and present options

**Read-only.** Phases 1 and 2 edit nothing (C1). This command ends at GATE 1.

## Step 1 — Load

`sdlc_project`, then `sdlc_change_request`.

## Step 2 — Is it a change request at all?

Compare against the baselined specification before anything else:

| The system | Then it is |
|---|---|
| contradicts the baselined specification | a **defect** — `/sdlc_uat_triage` or `/sdlc_maintain_intake`, not this command |
| matches the specification, and the client wants different | a **change request** — continue |
| the specification does not decide it | an **open question** — get a `DEC-*` first |

Ambiguous wording ("this should be…") is either. Ask rather than assume — under a
fixed-price contract this is a commercial classification, not a clerical one.

## Step 3 — Phase 1: analyse

Per the skill:

1. capture the request **verbatim**
2. identify the module and every surface with a counterpart (C8)
3. establish the as-is from three sources — requirements, design, code — each anchored
4. derive a verifiable to-be; no usable to-be → stop and ask
5. walk the open-question checklist explicitly, every item
6. build the impact matrix over the whole cascade, marking the unaffected rows too
7. classify, size, and name the regression surface

Three sources disagreeing **before** the CR is applied is a pre-existing defect: record it,
do not fix it (C6), and raise it — it changes which option is safe.

## Step 4 — Phase 2: options

At least `{{profile.change_request.min_options}}`, each on seven axes including the
**estimate** — effort, schedule impact, test impact (C12). End with a recommendation, not a
neutral list.

## Step 5 — GATE 1

Print, in order: as-is → to-be · impact matrix · open questions · options with estimates ·
recommendation. Then stop:

> Which option should be implemented, and what are the answers to the open questions above?

Do not continue to Phase 3 on your own, even if the user said "just do it" earlier — print
the gate block so the decision is on the record (C1). What the client reads back later is
this block, not the conversation around it.
