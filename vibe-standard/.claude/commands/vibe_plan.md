---
description: "Break an intent into small vertical slices within the size budget, map every done-when check to a slice, put the riskiest first, and give an honest time range. Delegates to vibe_planner. Usage: /vibe_plan INT-NNN"
---

# Plan an intent

Load `vibe_project`, then `vibe_slicing`.

## Step 1 — Pre-check

The intent exists and is `active`. Missing → `/vibe_intent`. Open questions that change the
slicing → ask them first (IF-04).

## Step 2 — Slice

Delegate to `vibe_planner`. It reads the intent, PRODUCT.md, and the parts of the codebase the
intent touches, and returns slices per PL-01..PL-03: vertical, each with its checks, predicted
files and lines, risk, and any decision needed.

## Step 3 — Check the plan

- every done-when check covered (PL-03)
- every slice within `{{profile.slices.max_files}}` / `{{profile.slices.max_changed_lines}}`
- riskiest slice early
- paydown counter: if due (DL-05), the plan's first slice is a debt paydown

## Step 4 — Write it into the intent

Fill the intent's "Slices" section. Update STATE.md "Next".

## Step 5 — Report

```
Plan — INT-{NNN}
  Slices   : {n}   {id · title · checks · ~files · ~lines · risk}
  Coverage : checks {covered}/{total}
  Decisions needed : {list or none}
  Estimate : {range} — basis: {history | none yet}   (only if asked)
  Next     : /vibe_build INT-{NNN}.1
```
