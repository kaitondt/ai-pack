---
name: vibe_release
description: "Ship a vibe-coded app safely — stage-scaled release checklist, environment and config check, deploy handed to the human, post-deploy smoke, and a rollback path that exists before it is needed. Use for 'deploy', 'ship it', 'release', 'go live', 'roll back', and before putting a URL in front of anyone."
---

# Ship — Putting It in Front of People

> `sdlc-standard` runs release readiness as a go/no-go with rehearsed cutover and rollback.
> The vibe version keeps the three questions that matter at any size — *what are we
> shipping, how do we know it works there, how do we undo it* — and scales the rest by stage.

Load `vibe_project`.

---

## SH-01 — What is being shipped

A release note in `{{profile.paths.releases}}/<date>-<version-or-sha>.md`:

- commits since the last release, grouped by `INT-*` / `BUG-*` / `DEBT-*` (SC-05 makes this a
  `git log` away)
- done-when checks newly satisfied
- known broken (from STATE.md "Broken") — shipped knowingly, or not shipped
- config / env var / migration changes — **each one**, because these are what break deploys
- debts taken since the last release

## SH-02 — The checklist, by stage

| # | Check | prototype | mvp | production |
|---|---|---|---|---|
| 1 | Working tree clean; release commit identified | ✅ | ✅ | ✅ |
| 2 | Stage checks green on that commit (VT-08) | ✅ | ✅ | ✅ |
| 3 | Every env var the code reads exists in the target environment (compare `.env.example` to the host) | ✅ | ✅ | ✅ |
| 4 | No secret in the client bundle (SE-02) | ✅ if public | ✅ | ✅ |
| 5 | Rollback path written in `{{profile.release.rollback}}` and **possible** for this release | — | ✅ | ✅ |
| 6 | Migrations: reversible, or backward-compatible with the previous code; backup taken first | — | ✅ | ✅ |
| 7 | `/vibe_security_check` no Critical/High | — | ✅ first real user | ✅ every release |
| 8 | Error tracking + uptime check live (`{{profile.release.monitoring}}`) | — | ✅ | ✅ |
| 9 | E2E smoke on a preview / production-like environment | — | — | ✅ |
| 10 | Rollback **rehearsed** at least once on this project | — | — | ✅ |
| 11 | No open debt due at the current stage (DL-04) | — | ✅ | ✅ |

`{{profile.verification.add}}` extends it. A failed row is reported, not waived — the owner
may decide to ship anyway, which is a `DEC-*`.

## SH-03 — The deploy is run by the human

Production deploys, database migrations against production, and DNS changes are SB-02
operations. The AI prepares: the exact command(s) from `{{profile.release.deploy}}`, the order,
what to watch, and the rollback command — and the human runs them. The `guard_vibe_bash` hook
blocks the deploy patterns in `{{profile.security.dangerous_commands}}`.

Preview / staging deploys that cannot affect users may be run by the AI if the profile does
not list them as dangerous.

## SH-04 — After the deploy

1. Smoke: `{{profile.commands.smoke}}` or the core flows by hand/browser against the real URL.
2. Watch errors for the first minutes (error tracker, host logs).
3. Anything wrong on a core flow → **roll back first, debug second.** Fixing forward in
   production under pressure is the doom loop with users watching.
4. Record in the release note: deployed at, by, smoke result, incidents.
5. STATE.md: last release, anything now known broken.

## SH-05 — Rollback

- Code: redeploy the previous build, or revert commit(s) + deploy. Know which your host does.
- Data: a migration that dropped or transformed data is not undone by redeploying code — which
  is why SH-02 #6 takes the backup first and prefers expand/contract migrations.
- Record every rollback as a `BUG-*` with the cause, and the "why not caught" (DB-05).

## Self-check

- [ ] Release note lists changes, env/migration changes, known broken, new debt
- [ ] Every checklist row for the stage passed, or its waiver is a `DEC-*`
- [ ] Deploy command handed to the human with the rollback command beside it
- [ ] Post-deploy smoke ran on the real URL, and its result is recorded
