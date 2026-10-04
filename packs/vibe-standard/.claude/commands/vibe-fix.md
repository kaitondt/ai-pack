---
description: "Fix a bug with evidence instead of guesses — record BUG-*, reproduce, isolate, one hypothesis at a time, fix the cause, leave a regression check, record why it was missed. Delegates to vibe-debugger. Usage: /vibe-fix <symptom, error, or BUG-NNN>"
---

# Fix a bug

Load `vibe-project`, then `vibe-debug`.

## Step 1 — Record (DB-01)

Existing `BUG-*` → read it. Otherwise append one with symptom, **expected (anchored to an
intent)**, where found, severity. No expected behaviour anywhere → it is a missing intent;
say so and offer `/vibe-intent`.

## Step 2 — Checkpoint

Clean tree (SS-03). The fix is its own slice: `BUG-NNN`.

## Step 3 — Investigate

Delegate to `vibe-debugger`: reproduce (DB-02), isolate (DB-03), hypothesis → evidence (DB-04).
It returns the cause **with the evidence** before changing code, and the reproduction as a
failing test from `mvp`.

Show the cause to the human in one or two sentences. For anything touching data, auth or
payments, wait for a yes before the fix.

## Step 4 — Fix

One change for the stated cause. Regression check seen red before, green after (VT-07). The
affected intent's done-when checks all green.

The doom-loop limit applies (SS-05): `{{profile.loop.max_fix_attempts}}` failed fixes → stop,
`/vibe-unstuck`.

## Step 5 — Close (DB-05)

Commit `BUG-NNN: <cause>`. Update the bug: cause, fix commit, regression check, why not caught.
STATE.md "Broken" updated.

```
BUG-{NNN} — {symptom}                         {fixed | not fixed}
  Cause      : {one sentence}   evidence: {what proved it}
  Fix        : {commit} · {files}
  Regression : {test/check} red→green ✅
  Intent     : INT-{NNN} checks {n}/{n} ✅
  Missed by  : {why not caught}
```
