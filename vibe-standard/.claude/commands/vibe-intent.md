---
description: "Turn a feature request into an INT-* intent file with observable done-when checks and a 'not now' list, and get the human's yes before any code. Usage: /vibe-intent <what you want, in your words>"
---

# Write an intent

Load `vibe-project`, then `vibe-intent-spec`.

## Step 1 — Classify the request

| It is | Route |
|---|---|
| a new capability or a change to one | continue |
| something broken against an existing intent | `/vibe-fix` |
| restructuring with no behaviour change | a refactor intent (SS-07) or `/vibe-debt pay` |
| contradicts a PRODUCT.md non-goal | say so; ask whether to revise PRODUCT.md (`/vibe-product`) |
| already covered by an active intent | show that intent; ask whether this changes it (IN-05) |

## Step 2 — Draft

Next ID from `{{profile.paths.intents}}` (ID-03). Write `INT-{NNN}-<slug>.md` per IN-02:
intent line, 1–5 done-when checks (IN-03 — include the unhappy path and, for user-owned data,
the ownership check), "Not now", open questions, which core flow it serves.

Do **not** answer open questions by guessing. List them.

## Step 3 — Show and wait

Print the intent line, the checks, "Not now" and the questions. From stage `prototype`, wait
for the human's yes or edits. At `spike`, proceed, with assumptions written into the file.

Status → `active` on yes.

## Step 4 — Report

```
INT-{NNN} — {title}            status: {draft | active}      core flow: {n | none — why}
  Done when : {n} checks ({n} unhappy-path, ownership {yes|n/a})
  Not now   : {n}
  Questions : {n} open
  Next      : /vibe-plan INT-{NNN}
```
