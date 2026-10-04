---
name: mig_infrastructure
description: "Repository, CI/CD, environments, IaC and secrets for the target system, plus the parts only a migration has — coexistence with the still-running legacy system, data migration and its reconciliation, the parallel run, cutover and rollback to legacy. Resolved from the profile, so the same rules produce GitHub Actions, GitLab CI, Azure Pipelines or Jenkins. Load for ANY task about the pipeline, environments, deployment, data migration or cutover."
---

# Infrastructure — pipeline, environments, coexistence, cutover

> Prerequisite: `mig_project` resolved. Everything platform-specific comes from
> `{{profile.infrastructure}}`. Read it before writing a line of pipeline YAML.

A greenfield project's infrastructure question is "where does this run?". A migration's is
harder: **the old system is still running, still holds the data, and still has the users**,
and for some period both are live. Most of this skill is about that period.

---

## IN-01 — The platform is read, never assumed

There is no default. `scm.platform`, `ci.platform`, `hosting.provider`, `iac.tool` and
`containers.runtime` are declared in the profile; a task that needs one and finds a
`<placeholder>` **stops and asks**.

Resolve the vocabulary once and use the platform's own words in every document — the
client's team searches for the words their tools use:

| Concept | github | gitlab | azure-repos / azure-pipelines | bitbucket | jenkins |
|---|---|---|---|---|---|
| Review unit | pull request | merge request | pull request | pull request | — |
| Pipeline file | `.github/workflows/*.yml` | `.gitlab-ci.yml` | `azure-pipelines.yml` | `bitbucket-pipelines.yml` | `Jenkinsfile` |
| Unit of work | job / step | job / script | job / step / task | step | stage / step |
| Runner | runner | runner | agent | runner | agent / node |
| Secret store | repository / environment secrets | CI/CD variables (masked) | variable group / library | repository variables | credentials |
| Env approval | environment protection rule | protected environment | environment check | deployment permission | input step |
| Artifact | artifact | artifact | pipeline artifact | artifact | archived artifact |

`none` — no CI, no IaC, no containers — is an answer, not a gap to fill. Record it as a
decision with its reason and do not generate the thing anyway.

## IN-02 — The legacy system's infrastructure is read-only

LR-01 is not only about source files. The legacy servers, jobs, schedules, shares and
database instances are the running production system, and they are outside this project's
write scope entirely. `{{profile.infrastructure.legacy_infrastructure}}` exists so documents
can *name* them, not so anything can change them.

Two consequences that come up constantly:

- **A legacy scheduled job is not disabled by this project.** Turning one off at cutover is a
  client operation, in the cutover plan, with a named owner.
- **A frozen database object is not "fixed" in infrastructure either** (LR-02). If the
  target's performance depends on a new index on a frozen schema, that is a client decision,
  stated as one — not an IaC change nobody mentioned.

## IN-03 — Infrastructure is code

When `iac.manual_changes_allowed` is false, every target-environment change goes through
`{{profile.infrastructure.iac.root}}`, is reviewed, and ships in a release. A change made in
a web console exists only in the memory of whoever made it and is the single most common
cause of "it works in the parallel environment".

Where `iac.tool` is `none`, the obligation moves rather than disappearing: the environment
build becomes a documented procedure, reproducible by someone who has never seen it. A
project with neither IaC nor that document cannot rebuild what it is about to cut over to.

## IN-04 — The pipeline asserts only what it can run

`{{profile.infrastructure.ci.enforces_gates}}` names them — build, typecheck, lint, unit
tests are machine-checkable and belong there.

What a pipeline cannot assert, and must not be described as asserting: that a behaviour is
anchored to legacy source, that a message is verbatim, that a blocked feature was escalated,
that a GAP item was resolved rather than closed. Those are the migration's actual risks and
none of them is green-or-red. Say which assertions ran; "CI passed" is not a gate result.

Stages come from `{{profile.infrastructure.ci.stages}}` and commands from
`{{profile.target.build}}` — the same commands `/mig_verify_build` runs. Where they differ,
the pipeline tests something no developer can reproduce.

## IN-05 — Environments, including the two a greenfield project does not have

Every environment appears in `{{profile.target.environments}}` with its purpose and data
classification (**X-11**). Two are migration-specific:

- **`parallel`** — where legacy and target process the same input and the outputs are
  compared. It must be production-like, or the comparison proves nothing.
- **`legacy-prod`** — listed so documents can name it, marked `readonly: true`, and **never a
  deployment target of this project**. A pipeline with a deploy step pointing at it is a
  Critical finding.

Test data in any non-production environment is masked (`references/rules/common/security.md`). A
migration makes this easy to get wrong, because the most useful test data is a copy of legacy
production.

## IN-06 — Secrets

Never in the repository, a pipeline file, an IaC default, a document, an example, or a log
line. They live in `{{profile.infrastructure.secrets.store}}` and reach the application as
injected environment variables. `.env.example` documents keys with placeholders and is
committed; `.env` is not. A committed secret is **rotated**, not deleted — removing it from
the working tree leaves it in the history and in every clone.

Legacy credentials found hardcoded in legacy source are a **finding, reported to the client**,
not something to carry across. Reproducing behaviour does not mean reproducing a password in
a config file (NI-02 does not extend to security defects).

---

## IN-07 — Coexistence: decide who owns the data

`{{profile.infrastructure.coexistence}}`. For any strategy other than `big-bang`, both
systems are live at once, and the question that matters is not "which is deployed" but
**`system_of_record`: which one owns the data while both are running.**

| `strategy` | What it means | The risk it carries |
|---|---|---|
| `big-bang` | one switch, one date | no way back after the point of no return; the rehearsal is everything |
| `phased` | module by module, or site by site | the seam: records touched by both a migrated and an unmigrated module |
| `strangler` | a router sends named routes to the target, the rest to legacy | routing rules drifting from reality; a route added to legacy that the router does not know about |
| `parallel` | both process the same input, one is authoritative | operator confusion about which screen is real |

**Two writers over one database is the defect class that ends migrations.** When
`dual_write` is true, `conflict_resolution` must state the rule — last-write-wins, legacy
authoritative, target authoritative per table — and that rule is a design decision recorded
in the architecture document, not an implementation detail.

`user_routing` states how a user knows which system they are in. During coexistence,
operators will have both open. A screen that looks the same in both, over data that is only
correct in one, produces the errors nobody can reproduce afterwards.

## IN-08 — Data migration is judged on reconciliation, not on completing

`{{profile.infrastructure.data_migration}}`. A migration script that finishes without raising
an error has demonstrated that it did not crash.

**Reconciliation is the deliverable**, and it is designed before the script:

| Check | Why |
|---|---|
| Row counts per table, source vs target | catches silently skipped rows — the commonest failure |
| Control totals on money and quantity columns | catches truncation, rounding and precision loss |
| Referential integrity in the target | catches rows migrated in the wrong order |
| Spot-check of known records, chosen by the business | catches the mapping that is technically valid and semantically wrong |

`rehearsals_required` rehearsals on a **production-sized** copy, timed. Two things are being
measured: correctness, and whether the run fits `cutover_window`. A rehearsal on a small
extract measures neither.

**`point_of_no_return` is written down before cutover weekend**, not discovered during it. It
is the moment after which rollback costs data — typically the first transaction entered in
the target by a real user. Everyone on the cutover call should be able to say what it is and
whether it has passed.

## IN-09 — The parallel run is the migration's strongest evidence

`{{profile.infrastructure.parallel_run}}`. Same input to both systems, outputs compared field
by field. Nothing else the project can do produces comparable evidence of parity, because it
tests against the oracle itself rather than against somebody's reading of it.

- **`compare`** lists what is compared: screen output, report output, batch output files,
  database state. Batch output files are the highest-value and the most often skipped — they
  are exactly diffable.
- **`tolerance: exact`** is the default and should be defended. Every field allowed to differ
  is named, with the reason and the decision that accepted it. "Timestamps and generated ids"
  is a legitimate exception list; "minor formatting differences" is not an exception list, it
  is an absence of one.
- A difference found in parallel run is a **defect against the legacy oracle** and goes
  through triage like any other — not a tolerance to widen.

Feed the comparison results to `mig_test_it` and the UAT evidence. `sign_off_by` names who
accepts the run.

## IN-10 — Rollback means going back to a system that never stopped

`{{profile.infrastructure.rollback}}`. This is where migration differs most from a normal
release. `target: legacy` means the fallback is the old system — which is still there, still
works, and may have been receiving no updates while the target ran.

The hard part is never the application; it is `data_strategy`: **what happens to records
created in the target after cutover?** Three honest answers, in descending order of comfort:
they are exported and loaded back into legacy by a script that exists and has been tested;
they are re-keyed by hand from a report; they are lost. Pick one, write it down, and tell the
business which it is.

`rehearsed: false` is the normal state and the one to change. A rollback plan that has never
been executed is a hypothesis, and it is usually wrong about the database.
`decision_owner` names who calls it **and by when** — a rollback decision available at any
time is a rollback decision nobody makes.

---

## What this skill produces

| Deliverable | Where | When |
|---|---|---|
| Infrastructure and environment design — the architecture category's deployment sections | `{{profile.paths.design_root}}`/architecture | P2 |
| Coexistence design — strategy, system of record, routing, conflict rule | architecture | P2, before any module that spans the seam |
| Pipeline definition | `{{profile.infrastructure.ci.definition_path}}` | P4 |
| IaC, container definitions | `{{profile.infrastructure.iac.root}}` | P4 |
| Data-migration scripts and the reconciliation report format | `{{profile.infrastructure.data_migration.root}}` | P4, rehearsed before P6 |
| Parallel-run comparison harness and results | `{{profile.testing.paths.results_root}}` | P6 |
| Cutover plan, rollback plan, and their rehearsal records | `{{profile.paths.docs_root}}` | before P7 |

**Ownership gates all of it.** When `{{profile.infrastructure.owner}}` is not `this project`,
or `repo_may_write_infra` is false, this skill produces **proposals and reviews, never
commits**: the change as a described diff, addressed to the owning team, with the requirement
behind it.

---

## The pipeline, generically

Same shape on every platform; only the syntax changes.

```
on change to a feature branch
  1 checkout
  2 restore dependencies        (cached, keyed on the lock file)
  3 build                       {{profile.target.build.order}}
  4 typecheck                   {{profile.target.build.typecheck}}
  5 unit tests                  {{profile.target.build.test_unit}}
  6 publish results as artifacts

on merge to {{profile.infrastructure.scm.default_branch}}
  7 the above, then
  8 e2e / integration           {{profile.target.build.test_e2e}}
  9 package a versioned artifact, tagged with the commit
 10 deploy to test

on release
 11 deploy to parallel, uat, prod, each behind its approval
     ({{profile.infrastructure.cd.approval_required_for}})
```

Three rules that outlive any platform:

1. **The artifact deployed is the artifact that was tested.** Build once, promote the same
   binary. A pipeline that rebuilds per environment has shipped something no parallel run
   ever compared.
2. **Fail on the first failing stage.** A pipeline that continues and reports at the end
   trains the team to read only the last line.
3. **No deploy step targets `legacy-prod`.** Ever (IN-02, IN-05).

---

## Reading infrastructure that already exists

The mid-project case, and the first thing to do on adoption.

1. Read the pipeline definition for `ci.platform` — what it actually runs, not what the
   README says.
2. Reconcile the environments it deploys to against `{{profile.target.environments}}`
   (**X-11**). Report each difference. Check specifically that nothing deploys to the legacy
   production environment.
3. Find where secrets come from; check the history, not only the working tree.
4. Find the IaC, or establish there is none and the environments are hand-built — a `RSK-*`
   with a rebuild impact, not a note.
5. Check the pipeline's build commands against `{{profile.target.build}}`.
6. Establish whether a parallel environment exists and whether it is production-like. If it
   is not, the parallel run cannot produce evidence, and that is a P6 problem discovered at
   P2 — which is the good outcome.
7. Establish what rollback actually is today, and whether anyone has run it.

Output findings with severities. This is a review and it produces review output.

---

## Common failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Pipeline written for the wrong platform | assumed GitHub | IN-01 — read `ci.platform` first |
| Green pipeline, failed gate | pipeline described as asserting what it cannot | IN-04 — name the assertions it ran |
| Data diverged during coexistence | two writers, no stated conflict rule | IN-07 — `system_of_record` and `conflict_resolution` |
| Migration "succeeded", totals wrong | judged on completing, not reconciling | IN-08 — reconciliation designed before the script |
| Cutover overran its window | rehearsed on a small extract | IN-08 — production-sized, timed |
| Rollback impossible on the night | never rehearsed; no data strategy | IN-10 — rehearse, and decide where target-created records go |
| Parallel run proved nothing | tolerance widened until differences disappeared | IN-09 — a difference is a defect, not a tolerance |
| Operators used the wrong system | no user routing | IN-07 — `user_routing` |
| Legacy job disabled by the project | treated legacy infra as writable | IN-02 — client operation, named owner, cutover plan |
| Architecture document stale | infra changed first | it is a deliverable — update it, through a CR if approved |

## Self-check

- [ ] every platform value came from the profile; nothing assumed
- [ ] ownership checked — commits only where `repo_may_write_infra` allows
- [ ] **no deploy target is the legacy production environment**; legacy infra unmodified
- [ ] pipeline stages map to `{{profile.target.build}}`, the same commands `/mig_verify_build`
      runs
- [ ] `ci.enforces_gates` assertions are the ones actually run, and named as such
- [ ] every environment the pipeline touches is in `{{profile.target.environments}}` (X-11);
      the parallel environment is production-like
- [ ] no secret in the repository, pipeline, IaC default or example; history checked
- [ ] coexistence: `system_of_record` stated, and a conflict rule wherever `dual_write`
- [ ] data migration: reconciliation checks defined, rehearsals run on a production-sized
      copy and timed against the window, `point_of_no_return` written down
- [ ] parallel run: comparison scope stated, every tolerance exception named with its reason
- [ ] rollback: target stated, data strategy stated, rehearsed, owner and deadline named
- [ ] the architecture document reflects all of it

## Report

```
Infrastructure
  SCM / CI       : {scm.platform} / {ci.platform}   definition: {path}
  Hosting / IaC  : {hosting.provider} {hosting.runtime} / {iac.tool}
  Ownership      : {owner}   {written | proposals only}
  Stages         : {list}    gate assertions: {list}
  Environments   : {declared} declared, {deployed} deployed   X-11: {pass|fail}
                   legacy-prod targeted by pipeline: {no | *** CRITICAL ***}
  Secrets        : store {name}   findings: {n}   history checked: {yes|no}
  Coexistence    : {strategy}   system of record: {x}   dual write: {y/n}
  Data migration : reconciliation {defined|missing} · rehearsals {n}/{required}
                   window {fits|overruns by X} · point of no return: {stated|not stated}
  Parallel run   : {enabled}   compare: {list}   tolerance: {exact | n exceptions}
  Rollback       : target {x} · data strategy {stated|absent} · rehearsed {y/n}
  Findings       : Critical {n} · Warning {n}
```

Real output for anything you ran. A failing pipeline is reported failing, with its output.
