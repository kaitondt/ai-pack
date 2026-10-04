---
description: "P2→P4 — create the codebase skeleton from the approved architecture: layout, layer projects with the dependency direction enforced, cross-cutting plumbing, test harnesses, tooling, and real build commands written back to the profile. No business behaviour. Usage: /sdlc_scaffold_codebase [plan | apply | review]"
---

# Scaffold the codebase

## Step 1 — Load

`sdlc_project`, then `sdlc_codebase`. Add `sdlc_infrastructure` when
`{{profile.infrastructure.containers.enabled}}` is true or a compose file is in scope.

## Step 2 — Pre-check

Required:

- the architecture document approved — §2, §3, §5, §6 and §9 at least;
- `{{profile.system.stack}}` and `{{profile.system.root}}` with no `<placeholder>`;
- the stack in the profile matching architecture §3.

Missing → name the command that produces it (`/sdlc_generate_basic_design architecture`)
or the profile field to fill, and stop. A skeleton built ahead of its architecture becomes
the architecture.

## Step 3 — Pick the mode

| Mode | When | Writes |
|---|---|---|
| `plan` | always first; the default with no argument | nothing — prints the derivation table and the file tree |
| `apply` | after the plan is confirmed | the skeleton, the skeleton record, the profile (after confirmation) |
| `review` | `{{profile.system.root}}` already holds source | findings and proposals only (CB-11) |

If `{{profile.system.root}}` is not empty and the mode is `apply`, switch to `review` for
the existing part and say so. Nothing that exists is overwritten.

## Step 4 — Plan

Print, before any file is created:

1. **The derivation table** (CB-01) — every path, its kind, its purpose, its source.
2. **The tree** it produces.
3. **The generator commands**, with pinned versions (CB-02).
4. **The cross-cutting list** (CB-04) — built, and the ones §5 is silent on, raised as
   questions with a proposed `DEC-*` owner.
5. **The build commands** that will be written to `system.build` (CB-06).

Ask the user to confirm the plan. Open questions from item 4 block `apply` for the concern
they affect, not for the whole skeleton.

## Step 5 — Apply

In this order — each step builds before the next begins:

1. generators run, versions pinned, lock file committed;
2. generator samples deleted (CB-03);
3. layer projects and references, then the architecture test (CB-05);
4. cross-cutting plumbing, each piece with its anchor comment (CB-04);
5. data access and, if this project owns the schema, the empty baseline migration (CB-08);
6. generator wiring and the read-only glob for its output (CB-09);
7. test projects, harness tests, seams and coverage (CB-07);
8. tooling, `.env.example`, developer README (CB-10);
9. empty module folders for the modules in the SRS / design module list (CB-03).

## Step 6 — Verify

Run every `system.build` command in order and report the real output — the
`/sdlc_verify_build` procedure against the new skeleton. Then show the profile diff for
`system.build` and write it only on confirmation.

A failing build stops here. The skeleton is not handed to P4 until it builds.

## Step 7 — Record

Write the skeleton record (derivation table, commands run with versions, decisions raised)
to architecture §9's appendix, or to `codebase-skeleton.md` in the architecture category
when §9 is baselined — the §9 reference then goes through a CR (BL-02).

Append traceability rows for CB-04 items that realise an `NFR-*`.

## Step 8 — Report

The `sdlc_codebase` report block, then the next commands:

- `/sdlc_generate_infra pipeline` — the build commands are now real (CB-12);
- `/sdlc_implement_feature {first module}` — once its DD is approved.

A skeleton that does not build is reported failing, with the output, never as "set up".
