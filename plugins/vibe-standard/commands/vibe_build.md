---
description: "Build one slice through the vibe loop — restate, checkpoint, map, smallest change, run, verify, diff summary, commit with the slice ID, update STATE.md. Stops at the doom-loop limit. Usage: /vibe_build INT-NNN.n | /vibe_build <request in your words>"
---

# Build a slice

Load `vibe_project`, then `vibe_build_loop` and `vibe_verification`.

## Step 1 — Find the slice

- Given `INT-NNN.n` → read the intent; the slice must be in its list.
- Given free text → find the intent it belongs to. None → draft one (`/vibe_intent` Step 2–3,
  show it, wait for yes at `prototype`+), then plan it if it needs more than one slice.
- The paydown counter is due (DL-05) → say so; suggest `/vibe_debt pay` first. The human
  decides.

## Step 2 — Restate and checkpoint (BD-01)

```
Intent : INT-007 — Notes can be edited
Slice  : INT-007.2 — ownership on page + API
Checks : 3 (another user's note → 404, no edit button)
Tree   : clean ✅ @ a1b2c3d
```

Dirty tree → commit or stash first, and say which (SS-03).

## Step 3 — Map (SS-04)

Read the files involved and the nearest similar code. Print the file map. Over budget → split
the slice and update the intent before continuing.

## Step 4 — Build

Delegate to `vibe_builder` with the intent, slice, map and stage. It builds per BD-02, running
early and often, recording debts and parking ideas as it goes.

It **stops and returns** when: a decision is needed (new dependency, schema, service), an open
question blocks (IF-04), the map is exceeded, or the attempt count hits
`{{profile.loop.max_fix_attempts}}` (SS-05) — in which case continue with `/vibe_unstuck`.

## Step 5 — Verify (VE-01, VE-02)

Every done-when check of the slice, observed. The stage's commands, in order. At `mvp`+, hand
the verification to `vibe_verifier` — not the context that wrote the code.

Any ❌ or ⏸ on a done-when check → the slice is not done. Back to step 4 (the attempt count
continues), or report and stop.

## Step 6 — Review and accept

Quick pass (RV-02). At `mvp`+, `/vibe_review` on the diff via `vibe_reviewer`. Print the diff
summary (VT-02). Wait for the human's acceptance when the slice touched auth, the data model,
payments, or anything irreversible.

## Step 7 — Commit and log (BD-04)

Commit `{{profile.slices.commit_format}}`. Tick the slice in the intent with the hash. Rewrite
STATE.md Now / Next / Last verified.

## Step 8 — Report

In the `vibe_project` slice format. Then name the next slice.
