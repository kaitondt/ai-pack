---
description: "CR phase 3 — update the design deliverables for an approved change-request option, in cascade order, with cross-document checks and traceability rows. Documents only, no code. Stops at GATE 2. Usage: /mig_cr_design [scope notes]"
---

# CR.2 — Update the design for an approved CR

## Step 1 — Verify the approval

There must be an analysis in this conversation, or a report in
`{{profile.paths.change_requests}}` named by `$ARGUMENTS`, **and** a named chosen option.

- No analysis → run `/mig_cr_analyze <the request>` first.
- Analysis but no chosen option → ask which option, and stop. GATE 1 is not self-clearable
  (C1).

## Step 2 — Load

`mig_project`, `mig_change_request`, then the category skill owning each document to be
edited (`{{profile.paths.bd_categories}}`).

## Step 3 — Constraint acknowledgement

Documents only — everything under `{{profile.paths.design_root}}`,
`{{profile.paths.detail_design}}` and the counterpart-language directories. **No code**;
that is `/mig_cr_implement` after GATE 2 (C4). No legacy, no frozen objects (LR-01, C3).
Content the CR does not mention stays as it is (C2).

## Step 4 — Edit in cascade order

`{{profile.change_request.cascade}}`, in order — data → screen → function → interface →
detail → mockup → report/file → index documents → counterpart language → test cases. Later
documents consume earlier ones, so out-of-order edits produce a set that contradicts
itself.

The class from Phase 1 sets the depth. `CR-MESSAGE` stops at message text and its ids;
`CR-FIELD` runs the whole item cascade; `CR-NEW` and `CR-REMOVE` also touch every index
document.

## Step 5 — Consistency

Re-run on what changed: X-03/X-04 function ↔ interface parameters, X-05 error codes, X-06
`MSG-*` sets, X-07 columns. Propagate renames everywhere the old name occurs, test cases
included (D4). Keep section skeletons fixed (DS-01, DS-03) and do not bump versions
(DS-02).

## Step 6 — Traceability

Append or update rows in `{{profile.paths.traceability}}` as each document changes, citing
the CR id as the ancestor for behaviour the legacy does not have (C11). Deferred to the end
of the CR, this is the step that gets skipped, and the artifacts then read as invented.

## Step 7 — GATE 2

```
CR design update — {CR-ID or module}

  Documents changed
    {path} §{section} : {before} -> {after}

  Required rows not yet done
    {path} : {reason}

  Cross-checks re-run : X-03 {pass} · X-04 {pass} · X-05 {pass} · X-06 {pass} · X-07 {pass}
  Index documents     : {updated | not affected}
  Counterpart language: {updated | not affected}
  Traceability rows   : {n} citing {CR-ID}

Approve these document changes so implementation can start?
```

Then stop. Next: `/mig_cr_implement`.
