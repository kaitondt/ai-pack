---
name: mig_codebase
description: "P1→P4 — the target codebase skeleton. Turns the approved TSD and the profile's target stack into a building, testable, empty repository beside the read-only legacy: layout, layer projects with the dependency direction enforced, cross-cutting plumbing that reproduces legacy conventions, data access against the existing schema, test harnesses, tooling, and real build commands written back to the profile. No business behaviour. Load for ANY task that creates, restructures or audits the target source layout."
---

# Codebase — the target skeleton the migrated modules are built into

> Prerequisite: `mig_project` resolved; the **TSD** approved (§1, §2, §4, §5, §6, §9 at
> minimum). The skeleton depends on the TSD, not on any module's design, so it can be built
> while P2 is still running.
> Runs once per target repository, or once per new target subsystem. Its output is what
> `mig_implementation` assumes already exists.

The first `/mig_implement_feature` should port a module into a repository that already
builds, already tests, and already refuses the wrong dependency. When there is no skeleton,
the first module invents one — and in a migration it usually invents it by copying the
legacy structure, which is the one thing the TSD was written to decide deliberately.

The skeleton is a **design deliverable made executable**. Nothing in it without a source.

---

## CB-01 — The layout comes from the TSD, not from a favourite template or from the legacy

Every directory, project, package and dependency traces to one of:

| Source | Decides |
|---|---|
| TSD §1 — target architecture / `{{profile.target.architecture}}` | layers, their responsibilities, which may depend on which |
| TSD §2 — technology stack / `{{profile.target.stack}}` | languages, frameworks, versions, package manager |
| TSD §4 — repository and module layout | where each layer and each module lives |
| TSD §5 — cross-cutting concerns | auth, logging, error handling, validation, i18n |
| TSD §6 — data strategy | schema frozen or converted, access pattern, transactions |
| TSD §9 — build, deploy, rollback | build tool, artifact shape, configuration model |
| a written client decision, or a TSD Open Item closed with one | anything the sections above left open (NI-01, third anchor) |
| `{{profile.target.surfaces}}` | one UI project per surface where TSD §4 separates them |
| `stack convention` — the framework's own documented layout | structural choices that carry no behaviour: where test projects sit, config file names. Cited as such, never used for anything an operator could observe |

**The legacy layout is not a source.** A VB.NET solution split by form, or a COBOL library
split by copybook, is evidence of how the old system was organised — not of how the target
should be. Where TSD §4 decides to mirror it, cite TSD §4.

**Print the derivation table before creating anything:**

| Path | Kind | Purpose | Source |
|---|---|---|---|
| `src/app/Receiving.Domain/` | project | domain model, no framework references | TSD §1.2 |
| `src/app/Shared/Messages/catalogue.json` | file | verbatim legacy messages, keyed by `MSG-*` | TSD §5.4 |

A row with an empty Source column is not created.

A `<placeholder>` in `{{profile.target.stack}}`, or a stack in the profile that disagrees
with TSD §2, **stops the run**. Name the field and ask.

## CB-02 — The legacy is read-only, and the target is not inside it

- **Nothing is written under `{{profile.legacy.root}}`** or anything matching
  `{{profile.constraints.readonly_globs}}` (LR-01). A generator run from the wrong directory
  is the easiest way to break this — run generators with an explicit output path.
- **`{{profile.target.root}}` must not sit inside `{{profile.legacy.root}}`.** If it does,
  stop: the hook protects the legacy by path, and a target nested in it cannot be written.
- **No build reference from the target to the legacy** — no project reference, no shared
  assembly, no copied library linked in. A target that needs a legacy binary to build has not
  been migrated. Where the TSD says the two must coexist at runtime, that is
  `mig_infrastructure` IN-07, not a compile-time dependency.
- Legacy code is not copied into the target as a starting point. It is read, per module, by
  `/mig_implement_feature`, with the anchor carried into the port (IM-06).

## CB-03 — Official generators first, pinned, and recorded

Use the stack's own generator rather than hand-writing its boilerplate. **Pin** the generator
and framework versions, **commit the lock file**, **record every command** with its version
in the skeleton record. No piped remote scripts. A dependency the TSD did not name needs a
reason and a licence check.

## CB-04 — The skeleton contains no business behaviour

NI-01 applied to the first commit: nothing in the skeleton reproduces a legacy behaviour,
because nothing in the skeleton has an `LEG-*` anchor.

- **Delete generator samples** — `WeatherForecast`, the demo route, the example entity, the
  `1 + 1 == 2` test — before the skeleton is reported done.
- **Module folders are created empty**, only for modules in the FRD, each with a one-line
  README naming the module ID and its `LEG-*` range. A module the FRD does not list is either
  excluded (`{{profile.legacy.excluded}}`) or missed scope — raise it, do not create it.
- **No entities, endpoints, screens, validations or messages.** They arrive per module,
  through `/mig_implement_feature`, anchored.
- **No "improved" base types** that anticipate a cleaner model than the legacy had (NI-02).

## CB-05 — Cross-cutting plumbing is built as the TSD decides, reproducing what the operator sees

The skeleton is where cross-cutting concerns become code once. In a migration, most of them
have a **legacy convention the operator already depends on**, and the TSD states whether
it is reproduced or deliberately changed (TSD §8 for security deviations). Each piece carries
its anchor as a comment:

| Concern | Built in the skeleton | Anchor |
|---|---|---|
| Messages | catalogue loader keyed by `MSG-*`, **empty**, stored so the verbatim legacy text survives byte-for-byte (NI-03): encoding stated, full-width / half-width preserved, no normalisation on load | TSD §5 |
| Error display | the error envelope and how it reaches the screen — matching the legacy's observable pattern (dialog, inline, status bar) as the TSD records it | TSD §5, `LEG-*` or client decision |
| Authentication / session | middleware, policy registration, session timeout as the legacy had it unless TSD §8 records a deviation | TSD §5, §8 |
| Logging | logger setup, structured fields, redaction list, a correlation id usable for parallel-run comparison | TSD §5, `mig_infrastructure` IN-09 |
| Validation | the pipeline hook validators plug into — first-failure-stops when that is the legacy behaviour (IM-02) | TSD §5 |
| Numbers | the decimal type and rounding helpers the TSD mandates — never binary floating point for legacy fixed-point values (IM-01) | TSD §6, `mig_data_design` |
| Dates, time zone, calendar | the clock abstraction, the legacy's time-zone and date-boundary convention, the fiscal calendar if the legacy has one | TSD §5/§6 |
| Collation and sorting | the comparer the legacy's sort order depends on — a DB collation or culture the target must match (IM-03) | TSD §6 |
| Configuration | typed, injected configuration; `.env.example` with **keys only** | TSD §9 |

**Where the TSD is silent on a concern the stack forces a choice on, it is a SPEC-GAP** —
stop and ask. The scaffold must not quietly pick "the modern default"; that is exactly the
improvement NI-02 forbids, applied once and inherited by every module.

## CB-06 — The dependency direction is enforced by structure, not by convention

Separate compilation units per layer with references pointing inward; where the stack cannot
express it, an architecture test or lint rule that fails the build on a forbidden import.
One test per forbidden direction in TSD §1. Add one more: **no reference from the target to
anything under `{{profile.legacy.root}}`** (CB-02).

## CB-07 — Data access is wired against the schema that exists

Follow TSD §6 and `{{profile.constraints}}`:

| Schema | The skeleton contains |
|---|---|
| frozen / pre-existing (LR-03) | connection and data-access plumbing only — **no migration tool, no DDL, no ORM model generation that would write back**. Where access is through stored procedures, the procedure-call helper; procedures marked frozen are called, never altered (LR-02) |
| converted to a new schema | the migration tool with an **empty** baseline migration. The schema arrives with each module's data design, and the data-migration tooling belongs to `mig_infrastructure` IN-08 |

Type mapping between the database and the target language follows `mig_data_design` — the
skeleton registers it once (decimal precision, fixed-length character padding, date types),
so no module maps it differently.

When local containers are enabled, the local compose file starts a database **seeded from
the masked copy the TSD names**, never from live legacy production.

## CB-08 — The build commands become real here, and go back to the profile

After the skeleton, every command runs clean against it:

```
{{profile.target.build.order}}    each step
{{profile.target.build.typecheck}}
{{profile.target.build.test_unit}}      harness + architecture tests
```

Run each one and report the real output. **Write the commands back to
`.claude/migration.profile.yaml`** — show the diff and get confirmation first. They become
what `/mig_verify_build` and the pipeline run. A command the stack has no use for is set to
`"n/a — <reason>"`, not left as a placeholder.

## CB-09 — Tests have somewhere to go from day one

- A unit-test project per layer that holds logic, and an integration-test project, placed
  where TSD §4 puts them or by `stack convention`.
- Framework, assertions and coverage configured.
- Fakes for the CB-05 seams — clock, id provider — in a shared test-support location.
- **A comparison seam for the parallel run**, only where `mig_infrastructure` IN-09 or the
  TSD calls for one: deterministic output ordering and a stable serialisation of results so
  legacy and target output can be diffed. The comparison harness itself belongs to
  `mig_infrastructure`.
- One harness test per test project, named as such. It is not a `UT-*` case and gets no
  traceability row.

## CB-10 — Generated code is wired, and protected

If the TSD says types or clients are generated: wire the generator into
`{{profile.target.build.order}}` (CM-01 — verify the command exists first), and make sure its
output matches `{{profile.constraints.readonly_globs}}` (LR-04).

## CB-11 — Tooling is the repository's

Formatter, linter, `.editorconfig`, `.gitignore`, `.gitattributes` — with the line-ending
**and encoding** policy stated explicitly: legacy files are frequently Shift-JIS, EBCDIC or
CP1252, and the target's are not. The target's encoding is declared once, and anything
reading legacy input converts at the boundary.

A developer `README.md`: prerequisites with versions, setup, the build commands, where the
legacy lives and that it is read-only.

## CB-12 — Existing target code is audited, never regenerated

If `{{profile.target.root}}` already holds source, switch to **review**: compare it to the
CB-01 derivation table, report each difference as a finding (a target→legacy reference or a
forbidden layer dependency is Critical), and propose rather than rewrite. Never overwrite an
existing file.

## CB-13 — The pipeline is handed off, not written here

The CI definition belongs to `mig_infrastructure`. The skeleton makes the build commands real
so `/mig_generate_infra pipeline` can use them. Container and compose files follow
`{{profile.infrastructure.repo_may_write_infra}}` — proposed, not committed, when it is false.

---

## What this skill produces

| Deliverable | Where |
|---|---|
| The target layout, projects and references | `{{profile.target.root}}` |
| Cross-cutting plumbing (CB-05), anchored | inside the layers TSD §1 assigns it to |
| Test projects, harness and architecture tests | per TSD §4 |
| Tooling configuration, developer README, `.env.example` | target repository root |
| Real build commands | `.claude/migration.profile.yaml` → `target.build`, after confirmation |
| **Skeleton record** — the CB-01 derivation table, the commands run with versions, the SPEC-GAPs raised | TSD §4 appendix, or `{{profile.paths.requirements}}/codebase-skeleton.md` when the TSD is signed off — then the reference is updated through a CR |

The skeleton adds no traceability rows: it implements no `REQ-*`. Its anchors are TSD
sections and client decisions, recorded in the skeleton record.

---

## Common failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Target organised exactly like the legacy, by accident | first module copied the legacy layout | CB-01 — the TSD decides |
| Generator wrote into the legacy tree | run from the wrong directory | CB-02 — explicit output path |
| Target builds only with a legacy DLL present | compile-time reference to legacy | CB-02, CB-06 |
| Messages lose full-width characters | catalogue normalised or wrong encoding | CB-05, CB-11 |
| Totals differ by a yen | binary floating point for fixed-point values | CB-05 numbers |
| List order differs from the legacy | different collation | CB-05 collation |
| DDL against a frozen schema | migration tool added by habit | CB-07 |
| Parallel-run diff is all noise | non-deterministic ordering or serialisation | CB-09 |
| `WeatherForecast` in production | generator sample kept | CB-04 |

## Self-check

- [ ] every path in the derivation table has a source; the legacy layout was not used as one
- [ ] nothing written under the legacy root; target root not inside it; no target→legacy reference
- [ ] profile stack and TSD §2 agree; no placeholder guessed through
- [ ] versions pinned, lock file committed, commands recorded
- [ ] no sample code, entity, endpoint, screen, message or table; module folders only for FRD modules
- [ ] every cross-cutting item anchored to the TSD or a client decision; silent ones raised as SPEC-GAP
- [ ] message catalogue preserves bytes; encoding declared; decimal and collation as the TSD states
- [ ] data access matches the schema's status — no DDL against a frozen schema
- [ ] forbidden dependencies fail the build
- [ ] every `target.build` command ran clean, with real output; written back after confirmation
- [ ] no secret anywhere; `.env.example` holds keys only
- [ ] nothing existing overwritten; skeleton record written; pipeline handed off

## Report

```
Target codebase skeleton
  Mode           : {create | review | alongside}
  Source         : TSD §1 §2 §4 §5 §6 §9   client decisions: {list}
  Stack          : {backend} / {frontend} / {database}   pinned: {yes|no}
  Legacy         : {legacy.root} untouched: {yes|no}   target→legacy references: {n}
  Layout         : {n} projects/packages · {n} module folders ({n} modules in the FRD)
  Dependency rule: {structural | architecture test}   forbidden directions: {n}
  Cross-cutting  : {built}/{TSD §5 concerns}   SPEC-GAPs raised: {list}
  Data           : {schema frozen: access only | converted: empty baseline}
  Encoding       : target {enc}   legacy inputs converted at: {boundary}
  Build          : {step}: {PASS|FAIL} …   verdict: {PASS|FAIL}
  Profile        : target.build {written | proposed, awaiting confirmation}
  Findings       : Critical {n} · Warning {n}      (review mode)
  Next           : /mig_generate_infra pipeline · /mig_implement_feature {first module}
```

A skeleton whose build fails is reported failing, with the output. It is not handed to P4.
