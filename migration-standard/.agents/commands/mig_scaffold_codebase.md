---
description: "P1→P4 — create the target codebase skeleton from the approved TSD, beside the read-only legacy: layout, layer projects with the dependency direction enforced, cross-cutting plumbing that reproduces legacy conventions, data access against the existing schema, test harnesses, tooling, and real build commands written back to the profile. No business behaviour. Usage: /mig_scaffold_codebase [plan | apply | review]"
---

# Scaffold the target codebase

## Step 1 — Load

`mig_project`, then `mig_codebase`. Add `mig_data_design` for the type mapping, and
`mig_infrastructure` when containers, a compose file or a parallel-run seam are in scope.

## Step 2 — Pre-check

Required:

- the TSD approved — §1, §2, §4, §5, §6 and §9 at least;
- `{{profile.target.stack}}` and `{{profile.target.root}}` with no `<placeholder>`;
- the stack in the profile matching TSD §2;
- `{{profile.target.root}}` not inside `{{profile.legacy.root}}` (CB-02).

Missing → name the command that produces it (`/mig_generate_requirements tsd`) or the
profile field to fill, and stop.

## Step 3 — Pick the mode

| Mode | When | Writes |
|---|---|---|
| `plan` | always first; the default with no argument | nothing — prints the derivation table and the file tree |
| `apply` | after the plan is confirmed | the skeleton, the skeleton record, the profile (after confirmation) |
| `review` | `{{profile.target.root}}` already holds source | findings and proposals only (CB-12) |

Nothing that exists is overwritten. Nothing is written under `{{profile.legacy.root}}`.

## Step 4 — Plan

Print, before any file is created:

1. **The derivation table** (CB-01) — every path, its purpose, its TSD section or client
   decision. The legacy layout is not a valid source.
2. **The tree** it produces, with the legacy root shown as untouched.
3. **The generator commands**, pinned, each with an explicit output path.
4. **The cross-cutting list** (CB-05) — built, and the SPEC-GAPs where the TSD is silent.
5. **The data-access shape** — frozen schema (access only) or converted (empty baseline).
6. **The build commands** to be written to `target.build` (CB-08).

Ask the user to confirm the plan. A SPEC-GAP blocks `apply` for the concern it affects, not
for the whole skeleton.

## Step 5 — Apply

In this order — each step builds before the next begins:

1. generators run into `{{profile.target.root}}`, versions pinned, lock file committed;
2. generator samples deleted (CB-04);
3. layer projects and references, then the architecture tests, including
   no-reference-to-legacy (CB-06);
4. cross-cutting plumbing, each piece anchored — messages, error display, auth, logging,
   validation hook, numbers, dates, collation, configuration (CB-05);
5. data access per the schema's status, and the type mapping registered once (CB-07);
6. generator wiring and the read-only glob for its output (CB-10);
7. test projects, harness tests, seams, and the parallel-run comparison seam if called for
   (CB-09);
8. tooling with the encoding policy, `.env.example`, developer README (CB-11);
9. empty module folders for the FRD modules (CB-04).

## Step 6 — Verify

Run every `target.build` command in order and report the real output — the
`/mig_verify_build` procedure against the new skeleton. Confirm with `git status` that
nothing under `{{profile.legacy.root}}` changed. Then show the profile diff for
`target.build` and write it only on confirmation.

A failing build stops here. The skeleton is not handed to P4 until it builds.

## Step 7 — Record

Write the skeleton record (derivation table, commands with versions, SPEC-GAPs raised) as
the TSD §4 appendix, or as `codebase-skeleton.md` beside the TSD when the TSD is signed off.

## Step 8 — Report

The `mig_codebase` report block, then the next commands:

- `/mig_generate_infra pipeline` — the build commands are now real (CB-13);
- `/mig_implement_feature {first module}` — once its design is approved.

A skeleton that does not build is reported failing, with the output, never as "set up".
