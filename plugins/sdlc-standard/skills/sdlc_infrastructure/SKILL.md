---
name: sdlc_infrastructure
description: "Repository, CI/CD, hosting, IaC, secrets and observability — resolved from the profile rather than assumed, so the same rules produce GitHub Actions, GitLab CI, Azure Pipelines or Jenkins. Owns the infrastructure design section, the pipeline definition, the environment matrix and the NFR monitors. Load for ANY task about the build pipeline, deployment, environments or infrastructure."
---

# Infrastructure — repository, pipeline, hosting

> Prerequisite: `sdlc_project` resolved. Everything platform-specific comes from
> `{{profile.infrastructure}}`. Read it before writing a single line of pipeline YAML.

Infrastructure is where a project's least-documented decisions live. The pack treats it as a
design category with the same obligations as any other: sourced from requirements, recorded
before it is built, reviewed, and traceable to the `NFR-*` it exists to deliver.

---

## IN-01 — The platform is read, never assumed

There is no default platform. `scm.platform`, `ci.platform`, `hosting.provider`, `iac.tool`
and `containers.runtime` are declared in the profile, and a task that needs one and finds a
`<placeholder>` **stops and asks** — it does not write a GitHub Actions workflow into a
GitLab project because that is the common case.

The same design produces different files on different platforms. Resolve the vocabulary
once, at the start of the task, and use the platform's own words in every document — the
client's team searches for the words their tools use:

| Concept | github | gitlab | azure-repos / azure-pipelines | bitbucket | jenkins |
|---|---|---|---|---|---|
| Review unit | pull request | merge request | pull request | pull request | — |
| Pipeline file | `.github/workflows/*.yml` | `.gitlab-ci.yml` | `azure-pipelines.yml` | `bitbucket-pipelines.yml` | `Jenkinsfile` |
| Unit of work | job / step | job / script | job / step / task | step | stage / step |
| Grouping | workflow | stage | stage | pipeline | pipeline |
| Runner | runner | runner | agent | runner | agent / node |
| Secret store | repository / environment secrets | CI/CD variables (masked) | variable group / library | repository variables | credentials |
| Env approval | environment protection rule | protected environment | environment check / approval | deployment permission | input step |
| Artifact | artifact | artifact | pipeline artifact | artifact | archived artifact |
| Package registry | GitHub Packages | GitLab Registry | Azure Artifacts | — | — |

Where the profile says `none` — no CI, no IaC, no containers — that is an answer, not a gap
to fill. Record it as a decision with its reason, and do not generate the thing anyway.

## IN-02 — Infrastructure is code, and a console change is undocumented infrastructure

When `iac.manual_changes_allowed` is false, every environment change goes through
`{{profile.infrastructure.iac.root}}`, is reviewed, and ships in a release. A change made in
a web console exists only in the memory of whoever made it, survives until the next rebuild,
and is the single most common cause of "it works in staging".

Where IaC is `none`, the obligation does not disappear — it moves. The environment build is
then a **documented procedure** in the runbook, with every setting listed and its value
stated, reproducible by someone who has never seen the environment. A project with neither
IaC nor that document cannot rebuild what it is running.

## IN-03 — The pipeline asserts the gates it can assert mechanically

`{{profile.infrastructure.ci.enforces_gates}}` names them. The P4 exit criteria — build,
typecheck, lint, unit tests — are machine-checkable, so the pipeline checks them on every
change and a human never has to.

What a pipeline **cannot** assert, and must therefore not be described as asserting: that a
requirement is testable, that a design matches the SRS, that a defect was attributed to the
right injection phase, that a gate's waivers were accepted by the right person. A green
pipeline is evidence for exactly the assertions it ran (`/sdlc_phase_gate` Step 4). Say which
ones in the gate record, not "CI passed".

The stages come from `{{profile.infrastructure.ci.stages}}` and the commands from
`{{profile.system.build}}` — the same commands `/sdlc_verify_build` runs locally. When they
differ, the pipeline is testing something no developer can reproduce; make them the same
commands or state why they differ.

## IN-04 — The profile's environments are the only environments

Every environment the pipeline deploys to appears in `{{profile.system.environments}}`, with
its purpose and its data classification. An environment the pipeline knows about and the
profile does not is where ST runs against the wrong data, or where a client's production
copy sits unnoticed.

The reverse is the P7 problem: exactly one environment is `production_like: true`, and that
is where system test runs. If the pipeline cannot deploy to it, ST has nowhere to execute and
P7 cannot start — raise that at P2, not at P7.

## IN-05 — Secrets

Never in the repository, never in a pipeline file, never in an IaC variable default, never
in a document, never in an example, never in a log line. They live in
`{{profile.infrastructure.secrets.store}}` and reach the application as injected environment
variables.

`.env.example` documents the **keys** with placeholder values and is committed;
`.env` is not. A secret that has been committed is rotated, not deleted — removing it from
the working tree leaves it in the history and in every clone.

## IN-06 — Every measurable NFR has a monitor

When `observability.nfr_monitors_required` is true, each `NFR-PERF-*`, `NFR-AVAIL-*` and
`NFR-OPS-*` gets a row naming the signal that measures it, where that signal lands, and the
threshold that alerts:

| NFR | Target | Signal | Destination | Alert threshold | Owner |
|---|---|---|---|---|---|

This is the operational half of X-09. The architecture says *how* the NFR is delivered; this
says *how anyone would know it stopped being delivered*. An availability target with no
monitor is a target the project will first learn it missed from the client.

---

## What this skill produces

| Deliverable | Where | When |
|---|---|---|
| Infrastructure design — §9 of the architecture document (build, deploy, environments, release, rollback) | the `architecture` category | P2, with the rest of the architecture |
| The environment matrix | architecture §4, from `{{profile.system.environments}}` | P2 |
| NFR monitor table (IN-06) | architecture §8, beside the X-09 table | P2 |
| Pipeline definition | `{{profile.infrastructure.ci.definition_path}}` | P4, once the build commands are real |
| IaC | `{{profile.infrastructure.iac.root}}` | P4 |
| Container definitions | repository root / `{{profile.infrastructure.iac.root}}` | P4, when `containers.enabled` |
| Deployment and rollback procedure | `{{profile.paths.runbook}}` | before P7 — ST runs on a deployed build |
| Release/cutover input | `sdlc_release` G3, G5, G6 | P8→release |

**Ownership gates all of it.** When `{{profile.infrastructure.owner}}` is not `this project`,
or `repo_may_write_infra` is false, this skill produces **proposals and reviews, never
commits**: the pipeline change as a described diff, the IaC change as a request to the owning
team, with the requirement behind it. Writing into another team's infrastructure from here is
how two sources of truth start.

---

## The pipeline, generically

Shape it the same way on every platform; only the syntax changes.

```
on change to a feature branch
  1 checkout
  2 restore dependencies        (cached, keyed on the lock file)
  3 build                       {{profile.system.build.order}}
  4 typecheck                   {{profile.system.build.typecheck}}
  5 lint                        {{profile.system.build.lint}}
  6 unit tests + coverage       {{profile.system.build.test_unit}}
  7 publish results and coverage as artifacts

on merge to {{profile.infrastructure.scm.default_branch}}
  8 the above, then
  9 integration tests           {{profile.system.build.test_integration}}
 10 package a versioned artifact, tagged with the commit
 11 deploy to the first environment, automatically

on release
 12 deploy to staging / uat / prod, each behind its approval
     ({{profile.infrastructure.cd.approval_required_for}})
```

Three rules that outlive any platform:

1. **The artifact deployed to production is the artifact that was tested** (`sdlc_release`
   G3). Build once, promote the same binary. A pipeline that rebuilds per environment has
   shipped something no test ever ran against.
2. **Fail the pipeline on the first failing stage.** A pipeline that continues and reports at
   the end trains the team to read only the last line.
3. **The pipeline is reviewed like application code.** It runs with credentials, and it is
   the most privileged code in the repository.

Branch protection follows `scm.branching_model`: `protected_branches` require a passing
pipeline and a review before merge. Without that, the pipeline is advisory.

---

## Reading infrastructure that already exists

The mid-project case, and the first thing to do on adoption.

1. Find the pipeline definition by the path convention for `ci.platform`; read what it
   actually runs, not what the README says it runs.
2. List the environments it deploys to, and reconcile them against
   `{{profile.system.environments}}` — **X-12**. Report each difference; an unlisted
   environment is either missing from the profile or should not exist.
3. Find where secrets come from, and check none is in the repository or its history.
4. Find the IaC, or establish there is none and the environments are hand-built — record
   that as a risk (`RSK-*`) with its rebuild impact, not as a note.
5. Check whether the pipeline's build commands match `{{profile.system.build}}`.
6. Check what the rollback actually is. In most projects the honest answer is "redeploy the
   previous artifact, and nothing for the database" — write that down, because
   `sdlc_release` G6 will ask for a rehearsal of it.

Report as findings with severities, not as prose. This is a review, and it produces the same
kind of output as any other review.

---

## Common failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Pipeline written for the wrong platform | assumed GitHub | IN-01 — read `ci.platform` first |
| Green pipeline, failed gate | pipeline described as asserting what it cannot | IN-03 — name the assertions it ran |
| Works in staging, not in prod | console change never captured | IN-02 — IaC, or a runbook procedure |
| ST cannot start | no production-like environment deployable | IN-04, raised at P2 |
| Secret in the history | committed once, deleted later | rotate; deletion is not remediation |
| NFR missed silently | no monitor | IN-06 |
| Deployed build differs from tested build | rebuild per environment | build once, promote |
| Infra drifts from the design document | infra changed without the architecture §9 update | it is a baselined document — BL-02, via a CR |
| Another team's infra edited from here | ownership not checked | `infrastructure.owner`, `repo_may_write_infra` |

## Self-check

- [ ] every platform value came from the profile; nothing assumed, nothing defaulted
- [ ] ownership checked — commits only where `repo_may_write_infra` allows them
- [ ] pipeline stages map to `{{profile.system.build}}` commands, and to the same ones
      `/sdlc_verify_build` runs
- [ ] `ci.enforces_gates` assertions are the ones actually run, and are named as such
- [ ] every environment the pipeline touches is in `{{profile.system.environments}}` (X-12),
      and exactly one is production-like
- [ ] no secret in the repository, the pipeline file, an IaC default or an example
- [ ] every measurable `NFR-*` has a monitor row with a destination and a threshold (IN-06)
- [ ] the artifact promoted to production is the tested artifact
- [ ] rollback is written down and is rehearsable, not aspirational
- [ ] architecture §9 updated — through a CR if the architecture document is baselined

## Report

```
Infrastructure
  SCM / CI       : {scm.platform} / {ci.platform}   definition: {path}
  Hosting / IaC  : {hosting.provider} {hosting.runtime} / {iac.tool}
  Ownership      : {owner}   write: {yes|proposals only}
  Stages         : {list}   gates asserted: {list}
  Environments   : {n} declared, {n} deployed by the pipeline   X-12: {pass|fail}
  Secrets        : store {name}   findings: {n}
  NFR monitors   : {covered}/{measurable NFRs}
  Rollback       : {documented | rehearsed | absent}
  Findings       : Critical {n} · Warning {n}
```
