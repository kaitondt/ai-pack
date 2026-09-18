---
description: "Release a vibe-coded app — release note from slice IDs, stage checklist, env/migration check, deploy commands handed to the human with rollback beside them, post-deploy smoke. Usage: /vibe_ship [preview | production]"
---

# Ship

Load `vibe_project`, then `vibe_ship`.

## Step 1 — What is shipping (SH-01)

Last release from `{{profile.paths.releases}}`; `git log` since then grouped by slice ID. Draft
the release note: changes, env var and migration changes (each one), known broken, new debt.

## Step 2 — The checklist (SH-02)

Run every row for the current stage — checks that can be run, **run**; the rest asked. Stage
checks via `/vibe_verify all` for `production`, the core-flow intents for `mvp`.
`/vibe_security_check` when the row requires it.

A failing row stops here. The owner may ship anyway: that is a `DEC-*`, written before the
deploy, not after.

## Step 3 — Hand over the deploy (SH-03)

Print, for the human to run:

```
Deploy   : {exact commands from {{profile.release.deploy}}, in order}
Watch    : {error tracker / logs URL}
Rollback : {exact commands from {{profile.release.rollback}}}
Data     : backup taken {when / how}   (if migrations)
```

Preview deploys not listed in `{{profile.security.dangerous_commands}}` may be run directly.

## Step 4 — After (SH-04)

When the human confirms it is deployed: smoke the core flows against the real URL; check the
error tracker. Core flow broken → recommend rollback first. Record the outcome in the release
note; update STATE.md.

```
Ship — {version/sha} → {env}                    {SHIPPED | BLOCKED | ROLLED BACK}
  Changes   : {n} intents · {n} bugs · {n} debts paid
  Checklist : {pass}/{rows}   waived: {DEC-* or none}
  Smoke     : {core flows ✅/❌}
  Note      : {path}
```
