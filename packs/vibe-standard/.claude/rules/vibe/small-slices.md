# RULE FAMILY: SMALL SLICES

> Vibe coding is fast because each step is cheap. It fails when a step stops being cheap —
> when a single prompt rewrites fifteen files, the build breaks in three places, and every
> "fix" introduces the next break. The size of the step is the variable that keeps the whole
> method working. This rule family holds it down.
>
> Derived from `pm-standard`'s work-package discipline (WBS, 8/80) and `sdlc-standard`'s
> context map and "design changes before code" — reduced to what fits in one sitting.

## SS-01 — One slice, one step of one intent, one commit

A slice is the smallest change that moves an intent forward **and can be run**. Prefer
vertical slices — thin, end to end, visible — over horizontal ones:

| Horizontal (avoid) | Vertical (prefer) |
|---|---|
| 1. all the database tables · 2. all the API · 3. all the UI | 1. create a note (form → API → DB → list shows it) · 2. edit a note · 3. delete a note |

A horizontal slice cannot be verified by running the product until the last one lands, so it
defers every surprise to the end — exactly what vibe coding cannot afford.

Each slice ends in exactly one commit, prefixed with its ID: `INT-{NNN}.2: edit a note`.

## SS-02 — Slices have a size budget

From `{{profile.slices}}`:

| Budget | Default | On exceeding it |
|---|---|---|
| Files touched | `max_files` (8) | stop and split the slice |
| Changed lines | `max_changed_lines` (400) | stop and split the slice |
| Time | `max_minutes` (60) | stop, commit what runs, re-plan the rest |

The `check-slice-size` hook warns when the working tree passes the budget. Generated files,
lockfiles and snapshots do not count (`{{profile.slices.exclude_from_budget}}`).

A slice that cannot be made smaller is a sign the design is tangled — record that as a
`DEBT-*` rather than accepting a big slice as normal.

## SS-03 — Checkpoint before building

A slice starts on a **clean working tree**. If the tree is dirty, commit the work (if it runs)
or stash it (if it does not) — and say which — before the first edit.

The checkpoint is what makes every later rule cheap: reverting (SS-06), bisecting a
regression, and showing the human exactly what this slice changed.

## SS-04 — Map the change before making it

Before the first edit, list the files the slice will touch, and why:

```
Slice INT-{NNN}.2 — edit a note
  src/app/notes/[id]/edit/page.tsx   new    edit form
  src/app/api/notes/[id]/route.ts    modify add PATCH
  src/lib/notes.ts                   modify updateNote()
  tests/notes.spec.ts                modify edit case
```

A file touched that is not on the map is either a map error (update it, say so) or scope creep
(IF-03). Either way it is visible.

## SS-05 — The doom-loop limit

After **`{{profile.loop.max_fix_attempts}}` (default 3) failed attempts at the same symptom**,
stop. Do not try a fourth variation.

1. Say what was tried and what each attempt showed.
2. Preserve the attempt: commit it to a branch `attempt/<slice-id>-<n>` — never discard it.
3. Return to the checkpoint.
4. Switch mode: `/vibe-fix` (reproduce → isolate → hypothesis → evidence) or `/vibe-unstuck`
   (re-slice smaller, or ask the human).

The loop in which each fix breaks something else is the characteristic failure of vibe coding.
Every iteration of it makes the code worse and the next fix less likely. The limit exists
because nobody notices they are in it from the inside.

## SS-06 — Revert beats patch-over-patch

When a slice has gone wrong and the cause is not understood, going back to the checkpoint and
re-doing it smaller is **cheaper** than layering fixes — every time. A fix is kept only when
you can state in one sentence why it works.

Code nobody understands is not fixed; it is currently passing.

## SS-07 — No drive-by refactors

A feature slice changes behaviour. A refactor slice changes structure and **not** behaviour.
Never both in one slice: a diff that does both cannot be reviewed, and a regression in it
cannot be attributed.

Refactors are their own slices (`INT-*` with intent "restructure … with no behaviour change"),
or a `DEBT-*` paydown, with the checks green **before and after**.

## Self-check before committing a slice

- [ ] The slice is one of the intent's listed slices, and only that
- [ ] Within the size budget, or split
- [ ] Started from a clean checkpoint
- [ ] Every touched file is on the map
- [ ] No refactor mixed into a behaviour change
- [ ] No fix kept whose reason cannot be stated in one sentence
