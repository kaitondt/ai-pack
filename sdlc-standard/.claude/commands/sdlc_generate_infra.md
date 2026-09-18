---
description: "Design, generate or review the repository, CI/CD pipeline, environments, containers, IaC, secrets and observability — on the platform declared in the profile. Usage: /sdlc_generate_infra [pipeline | iac | environments | observability | review]"
---

# Infrastructure — design, generate, review

## Step 1 — Load

`sdlc_project`, then `sdlc_infrastructure`. Add `sdlc_release` for anything touching
deployment, cutover or rollback.

## Step 2 — Resolve the platform, and stop if you cannot

Read `{{profile.infrastructure}}`. Print what you resolved:

```
SCM        : {scm.platform} ({scm.host}), default branch {scm.default_branch}
CI         : {ci.platform} -> {ci.definition_path}
Hosting    : {hosting.provider} / {hosting.runtime}
Containers : {containers.runtime or "none"}
IaC        : {iac.tool} at {iac.root}
Secrets    : {secrets.store}
Ownership  : {owner}   write: {yes | proposals only}
```

A `<placeholder>` in a field the mode needs **stops the run** — name the field and ask.
There is no default platform (IN-01).

## Step 3 — Check ownership

When `{{profile.infrastructure.owner}}` is not `this project`, or `repo_may_write_infra` is
false, this run produces **proposals and reviews only**. Say so before starting, so nobody
is waiting for committed files.

## Step 4 — Run the mode

| Mode | Produces |
|---|---|
| `pipeline` | the CI/CD definition at `ci.definition_path`, from `ci.stages` and `{{profile.system.build}}` |
| `iac` | infrastructure as code under `iac.root`, or the runbook procedure when `iac.tool: none` |
| `environments` | the environment matrix for architecture §4, reconciled against the pipeline (X-12) |
| `observability` | the NFR monitor table (IN-06) for architecture §8 |
| `review` | findings against what already exists — the mid-project default |
| nothing | inventory: what exists, what is declared, what is missing |

Delegate to `sdlc_infra_engineer`.

**Pipeline stages run the same commands `/sdlc_verify_build` runs.** Where they differ, the
pipeline tests something no developer can reproduce — make them the same, or state why.

**Build once, promote the same artifact.** A pipeline that rebuilds per environment ships
something no test ran against (`sdlc_release` G3).

## Step 5 — Checks

- **X-12** — every environment the pipeline deploys to is in
  `{{profile.system.environments}}`, and exactly one is `production_like`. Without it, P7 has
  nowhere to run; raise that now, not at P7.
- **Secrets** — nothing in the repository, the pipeline file, an IaC default, a document or
  an example. Check the history, not just the working tree. A committed secret is rotated.
- **IN-06** — every measurable `NFR-PERF-*`, `NFR-AVAIL-*` and `NFR-OPS-*` has a monitor row
  with a signal, a destination and an alert threshold.
- **Gate honesty** — `ci.enforces_gates` lists what the pipeline asserts mechanically. Name
  those assertions; a green pipeline is evidence for them and for nothing else (IN-03).
- **Rollback** — written down, and rehearsable. `sdlc_release` G6 will ask for the rehearsal.

## Step 6 — Update the design document

Architecture §9 (build, deploy, environments, release, rollback) is a P2 deliverable. If the
infrastructure changed, §9 changes with it — and if the architecture document is baselined,
that goes through a CR (BL-02). Infrastructure changing first does not exempt the document;
it is the usual way §9 goes stale.

## Step 7 — Report

```
Infrastructure — {mode}
  Platform       : {scm} / {ci} / {hosting} / {iac}
  Ownership      : {owner}   {written | proposed}
  Files          : {paths}
  Stages         : {list}    gate assertions: {list}
  Environments   : {declared} declared, {deployed} deployed   X-12: {pass|fail}
  Secrets        : {n} findings   history checked: {yes|no}
  NFR monitors   : {covered}/{measurable}
  Rollback       : {documented | rehearsed | absent}
  Architecture §9: {updated | CR required | unchanged}
  Findings       : Critical {n} · Warning {n}
```

Real output for anything you ran. A failing pipeline is reported failing, with its output.
