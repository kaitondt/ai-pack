---
description: "Security check scaled to the stage — the six holes vibe-coded apps ship with, every endpoint's authn/authz/validation, secrets in source/history/bundle, dependencies, data, LLM-feature risks, and the SB-07 matrix for the target stage. Read-only; delegates to vibe-security-auditor. Usage: /vibe-security-check [target-stage]"
---

# Security check

Load `vibe-project`, then `vibe-security`.

## Step 1 — Target

The target stage is the argument, else the **next** stage (you check against where you are
going). Reality check first: `product.public_url` true or real users → at least `mvp` (SB-07).

## Step 2 — Audit

Delegate to `vibe-security-auditor` (read-only). It performs SE-07:

- SE-01 — all six holes, with evidence per hole (checked how, found what)
- SE-02 — secrets in tracked files, git history (`git log -p -S` for key prefixes), the built
  client bundle if a build exists
- SE-03 — an endpoint inventory table: route/action · authn · authz per resource · validation
  · response filtering · rate limit
- SE-04 — `{{profile.commands.audit}}` output; licences
- SE-05 — data: real data below `mvp`, personal fields vs. core flows, backups
- SE-06 — if the product calls an LLM
- the SB-07 column for the target stage, row by row

## Step 3 — Record

Report to `{{profile.paths.reviews}}/<date>-security.md`. Each skipped control that will not be
fixed now → `DEBT-*` `category: security`, Due ≤ `mvp` (SB-08).

A committed secret found → the first line of the report says **rotate `<which>` now**.

## Step 4 — Report

```
Security check — target {stage}                 {PASS | FAIL}
  Six holes   : {n}/6 clear   {which not}
  Endpoints   : {n} — missing authz {n} · missing validation {n} · no rate limit {n}
  Secrets     : source {ok|n} · history {ok|n} · client bundle {ok|n|not built}
  Dependencies: audit {ok|n high/critical} · licences {ok|n}
  SB-07 {stage}: {pass}/{rows}
  Findings    : Critical {n} · High {n} · Medium {n}
  Security debt: {n} open, due ≤ mvp: {n}
```
