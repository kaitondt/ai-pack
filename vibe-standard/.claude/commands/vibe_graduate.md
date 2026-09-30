---
description: "Promote the project to the next stage (prototype / mvp / production) after checking every criterion with evidence — or hand it over to sdlc-standard / pm-standard. Usage: /vibe_graduate <prototype | mvp | production | handoff>"
---

# Graduate

Load `vibe_project`, then `vibe_graduation`.

## Promotion (`prototype` · `mvp` · `production`)

### Step 1 — Reality check

Current stage vs. reality (public URL, real users, real data). If reality is already ahead of
the label, lead the report with the gap (GR-02).

### Step 2 — Evaluate every criterion

GR-01 for the target, plus `{{profile.graduation.extra_criteria}}`. Each row **run**, not
asserted: `/vibe_verify all` for core flows, `/vibe_security_check <target>`,
`/vibe_debt list` for due debts, `/vibe_review codebase` for `mvp`.

### Step 3 — Decide

- Any fail → refused. The failing rows are the to-do list, each with the command that fixes it.
  The owner may override non-security rows with a `DEC-*`; never SB-08 or a failing
  core-flow check.
- All pass → append `DEC-*` "Stage → {target}", then set `stage:` in the profile, update
  STATE.md, and list the rules now in force that were not before.

```
Graduate → {target}                               {PROMOTED | REFUSED}
  Criteria : {pass}/{total}
  {✅/❌ · criterion · evidence · fix command}
  Decision : {DEC-*}
  Now in force: {rules newly applicable}
```

## Handoff

GR-03 signals → recommend `sdlc-standard`, `pm-standard`, both, or staying; the owner decides
(`DEC-*`). Then produce the mapping per GR-04 / GR-05 as
`{{profile.paths.vibe_root}}/HANDOFF.md`: every vibe record and where it goes, with
retro-specified requirements marked as assumptions until confirmed. Name the sibling pack's
first commands (`/sdlc_init` → `/sdlc_discover`; `/pm_init` → `/pm_charter`).

Do not install the sibling pack in this command — that is the human's step (ADOPTION.md).
