---
description: "Release readiness: evaluate the go/no-go criteria, assemble the release package list, check deployment ordering and the rehearsed rollback, and produce the go/no-go record. Usage: /sdlc_release_check [version]"
---

# Release readiness check

## Step 1 — Load

`sdlc_project`, then `sdlc_release`.

## Step 2 — Evaluate G1..G10

One line per criterion: `pass` / `waived by {name}, risk accepted: {what}` / `fail`, each
**with its evidence**. Evidence is a document, a build id, a rehearsal record or a sent
email — not a recollection.

The two that are most often claimed without evidence:

- **G3** — the release build is the build that was tested. Compare build ids against the ST
  and UAT results. A rebuild "with just the version number changed" is a different build.
- **G6** — the rollback plan has been **rehearsed**. An unrehearsed rollback plan is a
  hypothesis, and it is usually wrong about the database.

## Step 3 — Assemble the package list

Artefacts, migrations, configuration, reference data, external interface changes,
documentation, test evidence. Anything not on this list does not ship — and anything
shipping that is not on it is the thing nobody tested.

## Step 4 — Check deployment ordering

| Question | Must have an answer |
|---|---|
| Schema before code, or code before schema? | stated, with the coupling if they must land together |
| Can the previous version run against the new schema? | yes → rollback is possible; no → say so explicitly |
| External interface versions coordinated? | with the counterpart's confirmed release date |
| Batch jobs mid-run at cutover? | what happens to them |
| Caches and sessions? | what is invalidated, what users experience |

## Step 5 — Check the cutover and rollback plans

- every step has an owner, a duration and a **verification**
- there is a named abort point with a named decider (CU-01)
- the backup step verifies restorability, not just completion (CU-03)
- the rollback table covers every element of the package, with its data consequence

## Step 6 — Report

```
Release readiness — {version}
  G1..G10       : {each, pass/waived/fail with evidence}
  Waivers       : {each, who and what risk}
  Package       : artefacts {n} · migrations {n} · config {n} · reference data {n} · docs {n}
  Ordering      : {schema/code decision} · rollback possible: {yes|no}
  Cutover       : {n} steps, {duration}, abort point at {T+n}, decider {name}
  Rollback      : rehearsed {date}   worst-case data consequence: {what}
  Open defects  : S1 {n} · S2 {n}   deferred {n} (all with approvers: {yes|no})
  Verdict       : GO | GO WITH WAIVERS | NO-GO
```

A NO-GO is stated plainly, with the criteria that failed. The point of writing the criteria
down in advance is so this decision is not made at 02:00 by whoever is most tired.
