---
name: sdlc_release
description: "Release readiness, cutover and rollback. Go/no-go criteria, the release package and its contents, deployment ordering with schema coupling, cutover plan, rollback plan and its rehearsal, post-release verification and handover to maintenance. Load for ALL release, deployment and go-live tasks."
---

# Release — readiness, cutover, rollback

> Prerequisite: `sdlc_project` resolved. Runs between P8 acceptance and P9 maintenance,
> and again for every release afterwards.

A release is the moment every deferred decision becomes visible at once. The work here is
mostly deciding **in advance** what would make you stop, so the decision is not made at
02:00 by whoever is most tired.

---

## 1. Go / no-go criteria — agreed before the release week

| # | Criterion | Evidence |
|---|---|---|
| G1 | P8 acceptance recorded, with approver and date | acceptance record |
| G2 | No open Critical or High defect; every deferral has an approver and a target release | defect register |
| G3 | The release build is the build that was tested — same artefact, same version | build id in the ST/UAT results |
| G4 | Every `NFR-*` measured and met, or its shortfall accepted in writing | ST measurements |
| G5 | Migration and data scripts rehearsed on a production-like copy | rehearsal record with row counts |
| G6 | Rollback plan written **and rehearsed** | rehearsal record |
| G7 | Runbook, monitoring and alerting in place and verified by someone who did not build them | ST operability result (ST-07) |
| G8 | Support model live: who is on call, through what channel, with what SLA | `{{profile.maintenance}}` |
| G9 | Known limitations and deferred defects communicated to the client in writing | the sent document |
| G10 | Cutover plan reviewed, with named owners per step and a stated abort point | cutover plan |

**A no-go criterion that is waived is recorded with who waived it and what risk was
accepted.** That record is what makes the next release's discussion honest.

**G6 is the one skipped.** A rollback plan that has never been executed is a hypothesis,
and it is usually wrong about the database.

---

## 2. The release package

Everything the release consists of, listed once so nothing ships unlisted:

| Item | Notes |
|---|---|
| Application artefacts | version-tagged, built from a tagged commit, reproducible |
| Schema migrations | with their rollback, and their deployment coupling (CM-03) |
| Configuration changes | per environment, with the values that differ |
| Reference data | new or changed code tables (DT §8) |
| External interface changes | with the counterpart's readiness confirmed |
| Documentation | release notes, updated runbook, updated user documentation |
| Test evidence | ST and UAT results for this build |

**Release notes state what changed in business terms**, and what a user has to do
differently. Written from the CR and defect lists, not from the commit log.

---

## 3. Deployment ordering

The ordering problems that cause failed releases, all decidable in advance:

- **Schema before code, or code before schema?** State it. When both must land together,
  say so explicitly — that is a coupling, and it constrains rollback (CM-03).
- **Backward compatibility window.** If the previous version must keep running against the
  new schema (rolling deployment, or a rollback path), the migration must be expand-only,
  and the contracting migration goes in a later release.
- **External interface versions.** A contract change is coordinated with its counterpart's
  release. Neither side deploys first without an agreed compatibility window (API-V02).
- **Batch jobs.** Say what happens to a job that is mid-run at cutover, and whether the
  first post-release run needs anything different.
- **Caches and sessions.** State what is invalidated and what happens to users mid-session.

---

## 4. Cutover plan

A numbered, timed sequence, each step with an owner, an expected duration, and a
verification:

```
T-1d   final data rehearsal          {owner}   verify: row counts match source
T-0    announce maintenance window   {owner}
T+00   stop batch scheduler          {owner}   verify: no jobs running
T+05   backup                        {owner}   verify: backup restorable
T+15   deploy schema migration       {owner}   verify: migration log clean
T+30   deploy application            {owner}   verify: health endpoint green
T+40   smoke test                    {owner}   verify: the smoke suite passes
T+55   ABORT POINT — go/no-go        {owner}   decision recorded
T+60   reopen to users               {owner}
```

**CU-01 — the abort point is a named time and a named decider.** Past it, the release
continues and problems are fixed forward. Before it, rollback is the default. A cutover
without an abort point drifts into fixing forward by exhaustion.

**CU-02 — every step has a verification**, not just an action. A step whose success cannot
be checked is a step you will not know failed until users do.

**CU-03 — the backup is verified restorable, not merely taken.**

---

## 5. Rollback plan

For each element of the release package: how it is reverted, how long that takes, and what
data is lost or left behind.

| Element | Rollback | Duration | Data consequence |
|---|---|---|---|

The hard cases, which need a decided answer rather than an intention:

- **Data written by the new version** in a shape the old version cannot read.
- **A migration that dropped or narrowed a column** — usually not reversible; this is why
  contracting migrations wait for a later release.
- **An external system already sent the new message format.**
- **A partially completed cutover** — rollback from step 4 of 8 is a different procedure
  from rollback after completion.

**RB-01 — rehearse it.** On a production-like copy, at least once, before G6 can be
claimed.

---

## 6. Post-release verification

Within the first hours:

- the smoke suite, against production;
- a real business transaction end to end, done by a business user;
- error rates, response times and queue depths compared with the pre-release baseline —
  which is why the baseline is captured **before** the release;
- the first batch run watched, not assumed;
- external interfaces exchanging a real message in both directions.

Within the first days: watch the incident intake for the shapes that indicate a bad release
— a spike in one screen, a class of data failing validation, a job overrunning its window.

---

## 7. Handover to maintenance

P9 starts with what P8 produced, plus:

- the deferred-defect list, as the initial backlog;
- the known-limitations list, as the initial knowledge-base entries;
- the runbook, verified by a stranger (ST-07);
- the support model and the SLA (`{{profile.maintenance}}`);
- the warranty boundary — `{{profile.maintenance.warranty_period}}`, and what falls inside
  and outside it. Agree this in writing before go-live: after an incident, the boundary
  becomes a negotiation nobody enjoys.

---

## Report

```
Release {version} — {date}
  Go/no-go       : {each criterion, pass/waived/fail}   waived: {who, what risk}
  Package        : artefacts {n} · migrations {n} · config {n} · reference data {n}
  Cutover        : planned {duration}, actual {duration}, abort point {passed|invoked}
  Rollback       : rehearsed {date}   invoked: {no|yes — outcome}
  Post-release   : smoke {pass/fail} · first batch {outcome} · error rate vs baseline
  Handover       : deferred defects {n} · known limitations {n} · runbook verified {yes|no}
```
