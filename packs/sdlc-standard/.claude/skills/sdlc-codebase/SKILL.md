---
name: sdlc-codebase
description: "P2→P4 — the codebase skeleton. Turns the approved architecture document and the profile's stack into a building, testable, empty repository: solution/workspace layout, layer projects with the dependency direction enforced, cross-cutting plumbing, test harnesses, tooling, and real build commands written back to the profile. No business behaviour. Load for ANY task that creates, restructures or audits the project's source layout before or alongside the first module."
---

# Codebase — the skeleton the modules are built into

> Prerequisite: `sdlc-project` resolved; the P2 **architecture** document approved (§2, §3,
> §5, §9 at minimum). The rest of P2 and P3 need not be finished — the skeleton depends on
> the architecture, not on any module's design.
> Runs once per repository, or once per new subsystem added to an existing one. Its output
> is what `sdlc-implementation` assumes already exists.

The first `/sdlc-implement-feature` should add a module to a repository that already builds,
already tests, and already refuses the wrong dependency. When there is no skeleton, the first
module invents one: its folder names become the convention, its error handling becomes the
error-handling policy, and nobody ever decided either.

The skeleton is a **design deliverable made executable**. It is held to the same rule as every
other: nothing in it without a source.

---

## CB-01 — The layout comes from the architecture, not from a favourite template

Every directory, project, package and dependency in the skeleton traces to one of:

| Source | Decides |
|---|---|
| architecture §2 — logical architecture | layers, modules, which may depend on which |
| architecture §3 — technology stack / `{{profile.system.stack}}` | languages, frameworks, versions, package manager |
| architecture §5 — cross-cutting concerns | auth, logging, error handling, validation, i18n, audit |
| architecture §6 — data strategy | data access, migrations, transactions |
| architecture §9 — build, deploy, release | build tool, artifact shape, configuration model |
| a `DEC-*` entry | anything the sections above left to a decision |
| `{{profile.system.architecture}}`, `{{profile.system.surfaces}}` | architectural style, one UI project per surface where §2 separates them |
| `stack convention` — the framework's own documented layout | structural choices that carry no behaviour: where test projects sit, config file names, folder casing. Cited as such, never used for anything a user could observe |

**Print the derivation table before creating anything:**

| Path | Kind | Purpose | Source |
|---|---|---|---|
| `src/Ordering.Domain/` | project | domain model, no framework references | arch §2.3 |
| `src/Ordering.Api/Middleware/ErrorEnvelope.cs` | file | error response shape | arch §5.3, DEC-{NNN} |

A row with an empty Source column is not created. It is either an open question for the
architect or it is not part of the skeleton.

A `<placeholder>` in `{{profile.system.stack}}` or a stack in the profile that disagrees
with architecture §3 **stops the run**. Name the field and ask. The profile and the
architecture document must agree before either is turned into files.

## CB-02 — Official generators first, pinned, and recorded

Use the stack's own generator (`dotnet new`, `npm create vite`, `spring init`,
`cargo new`, `django-admin startproject`, …) rather than writing its boilerplate by hand —
the generator's output is what the ecosystem's documentation assumes.

- **Pin the version** of the generator and of every framework it installs. `@latest` is a
  different skeleton next month.
- **Record every command run**, with its version, in the skeleton record (see *What this
  skill produces*). Someone rebuilding the layout for a second subsystem needs to reproduce
  it, not reverse-engineer it.
- **Commit the lock file.** A skeleton without one builds a different dependency tree on the
  CI runner than on the laptop that created it.
- **No piped remote scripts** (`curl … | sh`) — `rules/common/coding-style.md`
  *Dependencies*. Install through the package manager in `{{profile.system.stack.package_manager}}`.
- A dependency the architecture did not name needs a stated reason and a licence check; one
  that shapes the architecture needs a `DEC-*` first.

## CB-03 — The skeleton contains no business behaviour

This is RS-06 applied to the first commit. An upward orphan created by the scaffold is still
an upward orphan (TR-02).

- **Delete generator samples.** `WeatherForecast`, `Counter.tsx`, the demo `/hello` route,
  the example entity, the sample test that asserts `1 + 1 == 2` — all removed before the
  skeleton is reported done. They are copied into the first real module more often than
  anyone admits.
- **Module folders are created empty**, only for modules that exist in the SRS / basic-design
  module list, each holding a one-line README naming the module ID and its `REQ-*` range. A
  folder for a module nobody specified is scope nobody agreed to.
- **No entities, tables, endpoints, screens, validations or messages.** Those arrive through
  `/sdlc-implement-feature` against a DD — never through the scaffold, however obvious they
  look.
- **No "base" business types** (`BaseOrder`, `AbstractDocument`) invented to anticipate what
  the modules might share. Shared shapes are extracted from real modules, not predicted.

## CB-04 — Cross-cutting plumbing is built as §5 decides, and only as §5 decides

The skeleton is where cross-cutting concerns become code once, so that no module
re-decides them. Each piece carries its anchor as a comment (IM-07):

| Concern | Built in the skeleton | Anchor needed |
|---|---|---|
| Authentication / authorisation | the middleware or filter, the policy registration, a deny-by-default posture | §5 auth, `NFR-SEC-*` |
| Error handling | the error envelope, the exception→response mapping, correlation id | §5 error handling |
| Logging | the logger setup, structured fields, the redaction list | §5 logging, `NFR-OPS-*` |
| Validation | the pipeline hook validators plug into — not any validator | §5 validation |
| Messages | the catalogue location and loader keyed by `MSG-*` (IM-04) — empty catalogue | §5 i18n |
| Configuration | typed, injected configuration; `.env.example` with **keys only** (IN-05) | §9, `rules/common/patterns.md` |
| Time and randomness | a clock and an id/random provider behind an interface — the DD §8 seams | §5, `rules/common/testing.md` |
| Health / readiness | the endpoint, only if §9 or an `NFR-AVAIL-*`/`NFR-OPS-*` calls for it | §9 or NFR |
| Audit | the hook, only if §5 or an `NFR-COMPL-*` requires it | §5 or NFR |

**Where §5 is silent on a concern the stack forces a choice on** — how errors are shaped,
what gets logged, whether auth is deny-by-default — **stop and ask** (IM-08). The scaffold
must not quietly become the decision; raise a `DEC-*` for the architect to own.

## CB-05 — The dependency direction is enforced by structure, not by convention

A layer rule that only lives in a document is broken by the third module. Make the build
refuse it:

1. **Separate compilation units per layer** where the stack allows — projects, modules,
   packages, workspaces — with references that only point inward
   (`rules/common/patterns.md` *Boundaries*).
2. Where the stack cannot express it structurally, **add an architecture test or lint rule**
   (NetArchTest / ArchUnit, `import-linter`, `eslint-plugin-boundaries`,
   `dependency-cruiser`, …) that fails the build on a forbidden import.
3. One such test per forbidden direction named in §2. It is the one test in the skeleton
   that asserts something — and what it asserts is the architecture.

## CB-06 — The build commands become real here, and go back to the profile

Before the skeleton exists, `{{profile.system.build}}` is `<placeholder>`s. After it, every
command runs clean against the empty skeleton:

```
{{profile.system.build.order}}          each step
{{profile.system.build.typecheck}}
{{profile.system.build.lint}}
{{profile.system.build.test_unit}}      harness + architecture tests
{{profile.system.build.test_integration}}
```

- **Run each one and report its real output.** A skeleton that has not been built has not
  been scaffolded.
- **Write the commands back to `.claude/sdlc.profile.yaml`** — show the diff and get the
  user's confirmation first; the profile is theirs. These become the commands
  `/sdlc-verify-build` runs and the pipeline runs (IN-03). Three different sets of commands
  is how "passes locally, fails in CI" starts.
- A command the stack has no use for (no typecheck in a dynamically typed stack) is set to
  an explicit `"n/a — <reason>"`, not left as a placeholder and not deleted.
- **Fill `{{profile.system.build.on_edit}}` from the same tools**: one entry per formatter
  and linter, scoped by glob to the sources it owns, running on the single edited file
  (`{file}` / `{rel}`), formatter before linter. Time each command on one file — an entry
  slower than ~10s is a whole-project command in disguise and stalls every edit. Linters the
  client standard makes mandatory are `blocking: true`; formatters are `blocking: false`.

## CB-07 — Tests have somewhere to go from day one

- A **unit-test project per layer that holds logic**, and an **integration-test project**,
  placed where §2 puts them, or by `stack convention` where §2 is silent.
- The test framework, the assertion library and the coverage tool configured, with coverage
  reported in the form `{{profile.quality.targets.unit_coverage}}` is measured in.
- **Test-data builders and fakes for the §5 seams** (clock, id provider) in a shared test
  support location.
- **One harness test per test project**, named as a harness check, proving the runner finds
  and executes tests. It is not a `UT-*` case and it gets no traceability row.
- When `{{profile.system.build.test_e2e}}` is set, the `{{profile.testing.automation}}`
  layout is created empty — the scripts come from `/sdlc-generate-testscript`.

## CB-08 — Data access is wired; the schema is not invented

Follow `{{profile.constraints.db_schema_owner}}`:

| Owner | The skeleton contains |
|---|---|
| `this project` | the migration tool configured, with an **empty** baseline migration; the connection, the unit-of-work / transaction boundary per §6 |
| another team, or `frozen` | the connection and the data-access plumbing only — no migration tool, no DDL, and a note naming the owning team (CM-06) |

No tables. The first table arrives with the first module's `{MODULE}-DT-*`.

When `{{profile.infrastructure.containers.compose_for_local}}` is true, the local compose
file starts the database and the other services the §7 integrations need locally — with
credentials from `.env`, never inline.

## CB-09 — Generated code is wired, and protected

If §3 or a `DEC-*` says client types, API stubs or ORM models are generated:

- wire the generator into `{{profile.system.build.order}}` at the step that produces its
  input (CM-01 — the command must exist before anything claims a file is generated);
- make sure its output matches `{{profile.constraints.generated_files_glob}}`, and add the
  output path to `{{profile.constraints.readonly_globs}}` if the glob does not already cover
  it (BL-07).

## CB-10 — Tooling is the repository's, not the author's

Formatter and linter configuration, `.editorconfig`, `.gitignore`, `.gitattributes` with the
line-ending policy, and the settings the stack rules ask for (`rules/java/`,
`rules/typescript/`, `rules/react/`, `rules/sql/` — compiler strictness, Checkstyle or ESLint
rule sets). Configure them **strictly and from the start** — turning a rule on later means a
commit that touches every file and hides every real change behind it.

Where `{{profile.system.coding_standards}}` registers a client standard with an
`enforced_by` tool, that tool's configuration is the client's form of the standard: commit it
as supplied, and never weaken it to make the skeleton pass.

A root `README.md` for developers: prerequisites with versions, the setup steps, the build
commands from CB-06, where things live. It is checked by running it on a clean clone, not
by reading it.

## CB-11 — Existing code is audited, never regenerated

If `{{profile.system.root}}` already holds source — adoption mid-project, or a brownfield
subsystem — the skill switches to **review**:

1. Read what exists: the actual layout, the actual references, the actual build.
2. Compare it to the derivation table from CB-01. Each difference is a finding with a
   severity: a forbidden dependency that already exists is Critical; a missing test project
   is Warning.
3. **Propose, do not rewrite.** Restructuring code that modules already live in is a change
   with its own context map, and — when it moves behaviour — a CR.
4. A new subsystem beside existing code is scaffolded **alongside** it, following the
   conventions that code already has (`rules/common/coding-style.md` *Match the surroundings
   first*), unless the architecture explicitly departs from them.

Never overwrite a file that exists. A generator that wants to overwrite is run into a
scratch directory and its output merged by hand.

## CB-12 — The pipeline is handed off, not written here

The CI definition belongs to `sdlc-infrastructure`. The skeleton's job is to make the build
commands real (CB-06) so that `/sdlc-generate-infra pipeline` can use them. Say so in the
report, with the command to run next. When `{{profile.infrastructure.repo_may_write_infra}}`
is false, the container and compose files follow the same rule: proposed, not committed.

---

## What this skill produces

| Deliverable | Where |
|---|---|
| The source layout, projects and references | `{{profile.system.root}}` |
| Cross-cutting plumbing (CB-04), anchored | inside the layers §2 assigns it to |
| Test projects, harness and architecture tests | as `{{profile.testing}}` lays them out |
| Tooling configuration, developer README, `.env.example` | repository root |
| Real build commands | `.claude/sdlc.profile.yaml` → `system.build`, after confirmation |
| **Skeleton record** — the CB-01 derivation table, the commands run with versions, the decisions raised | architecture §9 appendix, or `{{profile.paths.design_root}}/01.architecture/codebase-skeleton.md` when §9 is baselined — then the §9 reference goes through a CR (BL-02) |
| Traceability | one row per CB-04 item that realises an `NFR-*`, with the code reference. Tooling and harnesses get none — they are not behaviour |

---

## Common failure modes

| Symptom | Cause | Fix |
|---|---|---|
| First module's folder names became the standard | no skeleton; the module invented one | CB-01, before the first module |
| `WeatherForecast` in production | generator sample kept | CB-03 |
| Every module handles errors differently | §5 never became code | CB-04 |
| Domain references the ORM six weeks in | layer rule lived only in a document | CB-05 |
| "Passes locally, fails in CI" | three sets of build commands | CB-06 — one set, in the profile |
| Tests assert the clock | no seam for time | CB-07 |
| A table exists that no DT describes | schema created by the scaffold | CB-08 |
| Generated client hand-edited | output not in the read-only glob | CB-09 |
| Lint enabled late, 900-file diff | tooling added after the code | CB-10 |
| Brownfield code overwritten by a generator | scaffold run on an existing root | CB-11 |
| Skeleton cannot be rebuilt for the next subsystem | commands not recorded | CB-02 |

## Self-check

- [ ] every path in the derivation table has a source; nothing without one was created
- [ ] profile stack and architecture §3 agree; no placeholder was guessed through
- [ ] generator and framework versions pinned, lock file committed, commands recorded
- [ ] no sample code, no entity, no endpoint, no screen, no message, no table
- [ ] module folders exist only for modules in the SRS / design module list
- [ ] every cross-cutting item carries its §5 / `NFR-*` / `DEC-*` anchor; silent §5 raised, not decided
- [ ] forbidden dependencies fail the build (structure or architecture test)
- [ ] every `system.build` command ran clean, with real output; written back to the profile after confirmation
- [ ] test projects, harness tests and seams in place; coverage reported
- [ ] generated output under the read-only glob
- [ ] no secret anywhere; `.env.example` holds keys only
- [ ] nothing existing was overwritten
- [ ] skeleton record written; pipeline handed off to `/sdlc-generate-infra`

## Report

```
Codebase skeleton
  Mode           : {create | review | alongside}
  Source         : architecture {doc id} §2 §3 §5 §6 §9   DEC: {list}
  Stack          : {backend} / {frontend} / {database}   pinned: {yes|no}
  Layout         : {n} projects/packages · {n} module folders ({n} modules in the SRS)
  Dependency rule: {structural | architecture test | none}   forbidden directions: {n}
  Cross-cutting  : {built}/{§5 concerns}   raised as questions: {list}
  Data           : {migrations: empty baseline | owned by {team}}
  Generated code : {generator → output glob | none}
  Build          : {step}: {PASS|FAIL} …   verdict: {PASS|FAIL}
  Profile        : system.build {written | proposed, awaiting confirmation}
  Samples removed: {n}
  Findings       : Critical {n} · Warning {n}      (review mode)
  Next           : /sdlc-generate-infra pipeline · /sdlc-implement-feature {first module}
```

A skeleton whose build fails is reported failing, with the output. It is not handed to P4.
