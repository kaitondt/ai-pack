---
name: vibe-build-loop
description: "Build one slice through the vibe loop — checkpoint, map, smallest change, run, verify, diff summary, commit, log — while staying inside the intent, the size budget and the doom-loop limit. Use for 'build this', 'implement', 'add', 'make it do X', and for any code change that is not a bug fix."
---

# Build — One Slice Through the Loop

> The heart of the pack. `sdlc-standard`'s implementation phase reads an approved design and
> implements it layer by layer. Here the "design" is the intent and the slice line, and the
> discipline moves from *before* the code to *around* it: a checkpoint before, a map at the
> start, a hard stop when it goes in circles, and evidence at the end.

Load `vibe-project`, the intent file, and `vibe-verification` (a slice is finished by verifying it).

---

## BD-01 — Before the first edit

1. **Slice in hand.** An `INT-*.n` from the intent's slice list. No intent → `vibe-intent-spec`
   first (IN-04). The slice is not in the list → add it to the plan first, or it is scope creep.
2. **Restate.** One line of intent, one line of slice, the done-when checks it must satisfy.
3. **Checkpoint.** `git status` clean (SS-03). Otherwise commit or stash and say which.
4. **Read before writing.** The files the slice touches, the nearest similar feature in this
   codebase, and the installed versions of the libraries involved (VT-03). Match the existing
   patterns; a second way of doing the same thing is debt.
5. **Map.** Print the file map (SS-04). Over budget → split the slice now.

## BD-02 — While building

- **Smallest change that satisfies the checks.** No speculative generality, no config option
  nobody asked for, no abstraction with one caller.
- **Follow the stack.** New package / service / framework feature not already used → stop,
  propose, record a `DEC-*` when approved (IF-05). Then verify it exists (VT-03).
- **Stay in the intent.** A good idea → `/vibe-park` (IF-03). A needed refactor → its own slice
  (SS-07). A bug found in unrelated code → `BUG-*`, not a drive-by fix.
- **Write the check with the code.** From stage `mvp`, each core-flow done-when check becomes a
  test in this slice, with expected values from the intent (VT-04).
- **Record shortcuts as you take them** — `DEBT-*` + code marker (DL-01, DL-03).
- **Run early.** Start the app / run the test after the first meaningful change, not after the
  last. The cheapest error is the one found one edit after it was made.

## BD-03 — When it does not work

Count attempts at the **same symptom**. At `{{profile.loop.max_fix_attempts}}` (SS-05):

1. Stop editing.
2. Write what was tried and what each attempt showed.
3. `git switch -c {{profile.loop.attempt_branch_prefix}}<slice>-<n>` and commit the attempt
   there (evidence, not trash). Switch back to the checkpoint.
4. Hand to `/vibe-fix` (structured debugging) or `/vibe-unstuck` (re-slice / ask).

Signs you are already in the loop even before the count: the error changes but does not go
away; each fix touches a new file; you are adding `try/catch`, `?.`, `as any` or retries to
make symptoms stop; you are about to edit a test (VT-05).

## BD-04 — Finishing the slice

1. **Verify** — `vibe-verification` VE-01: every done-when check of this slice run, output observed;
   the stage's checks green (VT-08).
2. **Self-review the diff** — `vibe-code-review` RV-02 quick pass: nothing outside the map, no
   secret, no bare TODO, no debug leftovers, no weakened check.
3. **Diff summary** for the human (VT-02) — from `prototype` up, wait for acceptance when the
   slice touched auth, data model, payments or anything irreversible.
4. **Commit** — `{{profile.slices.commit_format}}`, e.g. `INT-007.2: enforce note ownership`.
   One slice, one commit (SS-01).
5. **Log** — tick the slice in the intent file with the commit hash; update STATE.md "Now /
   Next / Last verified" (SC-01). The paydown counter (DL-05) advances by itself — it is
   computed from the `INT-*` commits since the last `DEBT-*` one.
6. **Report** in the `vibe-project` format.

## BD-05 — Working with the human at vibe speed

- Ask **one** precise question when blocked, with the options and a recommendation — not an
  open "how would you like me to proceed?".
- When the human says "just do it" on an ambiguous point, pick, state the pick in one line,
  and record it as an assumption in the intent (IF-04) so it is visible later.
- When the human asks for something that breaks a rule of the pack (skip the tests, commit the
  key "just for now"), say which rule and what it protects against — once, briefly — then
  follow the human's decision **if the rule allows a `DEC-*` override** (VT-05) and record it.
  SB-01 and SB-02 have no override.

## Self-check before commit

- [ ] Slice is from the intent's list; restated before starting
- [ ] Started from a clean checkpoint; every touched file on the map; within budget
- [ ] No new dependency without a `DEC-*` and a VT-03 check
- [ ] Done-when checks run and observed; stage checks green
- [ ] Shortcuts recorded as `DEBT-*`; ideas parked as `IDEA-*`
- [ ] Commit message starts with the slice ID; intent and STATE.md updated
