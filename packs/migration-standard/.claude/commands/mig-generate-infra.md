---
description: "Design, generate or review the target system's repository, CI/CD, environments, containers, IaC and secrets, plus the migration-specific parts — coexistence, data migration and reconciliation, the parallel run, cutover and rollback. Usage: /mig-generate-infra [pipeline | iac | environments | coexistence | data-migration | parallel-run | cutover | review]"
---

# Infrastructure — design, generate, review

## Step 1 — Load

`mig-project`, then `mig-infrastructure`. Add `rules/migration/legacy-readonly.md` for
anything that touches the legacy side.

## Step 2 — Resolve the platform, and stop if you cannot

Print what you resolved:

```
SCM        : {scm.platform} ({scm.host}), default branch {scm.default_branch}
CI         : {ci.platform} -> {ci.definition_path}
Hosting    : {hosting.provider} / {hosting.runtime}
Containers : {containers.runtime or "none"}
IaC        : {iac.tool} at {iac.root}
Secrets    : {secrets.store}
Coexistence: {coexistence.strategy}, system of record {coexistence.system_of_record}
Ownership  : {owner}   write: {yes | proposals only}
Legacy infra: {legacy_infrastructure}   (read-only, LR-01)
```

A `<placeholder>` in a field the mode needs **stops the run** — name it and ask. There is no
default platform (IN-01).

## Step 3 — Check ownership and the legacy boundary

When `owner` is not `this project`, or `repo_may_write_infra` is false, this run produces
**proposals and reviews only**. Say so before starting.

Then confirm the boundary that is specific to this pack: **nothing in this run writes to, or
deploys to, the legacy system.** A pipeline step targeting `legacy-prod` is a Critical
finding. Disabling a legacy job is a client operation in the cutover plan, with a named owner.

## Step 4 — Run the mode

| Mode | Produces |
|---|---|
| `pipeline` | the CI/CD definition, from `ci.stages` and `{{profile.target.build}}` |
| `iac` | infrastructure as code under `iac.root`, or the runbook procedure when `iac.tool: none` |
| `environments` | the environment matrix, reconciled against the pipeline (X-11) |
| `coexistence` | strategy, system of record, routing, conflict rule — for the architecture document |
| `data-migration` | scripts, the reconciliation checks, the rehearsal plan |
| `parallel-run` | the comparison scope, the harness, the tolerance list |
| `cutover` | cutover plan, point of no return, rollback plan and its rehearsal record |
| `review` | findings against what already exists — the mid-project default |
| nothing | inventory: what exists, what is declared, what is missing |

Delegate to `mig-infra-engineer`.

## Step 5 — Checks

- **X-11** — every environment the pipeline deploys to is in
  `{{profile.target.environments}}`; the parallel environment is production-like; **no target
  is `legacy-prod`**.
- **Secrets** — nothing in the repository, pipeline, IaC default, document or example. Check
  the history. Hardcoded credentials found in legacy source are a finding reported to the
  client, never carried across.
- **Coexistence** — `system_of_record` stated for any strategy but `big-bang`; a conflict rule
  wherever `dual_write` is true; `user_routing` says how an operator knows which system they
  are in (IN-07).
- **Data migration** — reconciliation checks defined *before* the script; rehearsals run on a
  production-sized copy and timed against `cutover_window`; `point_of_no_return` written down
  (IN-08).
- **Parallel run** — comparison scope stated; every tolerance exception named with its reason
  and its decision. A difference is a defect against the oracle, not a tolerance to widen
  (IN-09).
- **Rollback** — target stated, data strategy for target-created records stated, rehearsed,
  owner and deadline named (IN-10).
- **Gate honesty** — name the assertions the pipeline actually runs. It cannot assert that a
  behaviour is anchored or a message verbatim (IN-04).

## Step 6 — Update the design document

The deployment and environment sections of the architecture category are P2 deliverables, and
so is the coexistence design. If the infrastructure changed, they change with it — through a
CR where the document is already approved. Infrastructure changing first does not exempt the
document; it is the usual way it goes stale.

## Step 7 — Report

Use the report block in `mig-infrastructure`. Real output for anything you ran — a failing
pipeline is reported failing, with its output.
