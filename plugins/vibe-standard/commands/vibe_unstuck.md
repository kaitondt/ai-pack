---
description: "Break the doom loop — stop editing, write down what was tried, preserve the attempts on a branch, return to the last good checkpoint, and choose a different approach (debug properly, re-slice, change approach, spike, or ask). Usage: /vibe_unstuck"
---

# Unstuck

Load `vibe_project`, then `vibe_debug` (DB-06).

Run this when the attempt limit trips (SS-05), when the human says "it keeps going in
circles", or when you notice the signs in BD-03 yourself.

## Step 1 — Stop and write it down

No more edits. Produce the attempt log:

```
Symptom : {exact error / behaviour}
Slice   : {INT-NNN.n}   checkpoint: {sha}
Attempt 1 : {what changed} → {what happened}
Attempt 2 : …
Pattern   : {what the attempts have in common — e.g. "all patched the symptom in the handler"}
```

## Step 2 — Preserve, then reset to the checkpoint

```bash
git switch -c {{profile.loop.attempt_branch_prefix}}{slice}-{n}
git add -A && git commit -m "{slice}: failed attempt {n} — {symptom}"
git switch -
```

Now the working tree is back at the checkpoint and nothing was destroyed. (`git reset --hard`
is blocked by the bash guard for exactly this reason.)

## Step 3 — Choose one way forward

| Option | When |
|---|---|
| **Debug properly** → `/vibe_fix` | the cause is unknown; the attempts were guesses |
| **Re-slice smaller** → `/vibe_plan` | the slice touched too much to reason about |
| **Change approach** → propose a `DEC-*` | the library / pattern is fighting back |
| **Spike** → a throwaway `spike/*` branch with only the unknown | a specific API or behaviour needs isolating |
| **Ask the human** | one specific question, with the attempt log |
| **Fresh session** → `/vibe_handoff` then new session | the context is full of failed attempts |

Recommend one, with the reason. The human picks.

## Step 4 — Record

STATE.md "Now": the symptom, the attempt branch, the chosen way forward.

```
Unstuck — {slice}
  Attempts  : {n}, preserved on {branch}
  Tree      : back at checkpoint {sha} ✅
  Pattern   : {one line}
  Next      : {chosen option} — {why}
```
