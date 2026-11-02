---
name: vibe-debug
description: "Structured debugging for vibe-coded apps — break the 'try another fix' loop with reproduce, isolate, hypothesise, prove, fix, and leave a regression check. Owns the BUG-* log and the unstuck protocol. Use for errors, stack traces, 'it's broken', 'it worked yesterday', 'the AI keeps failing to fix this', and after the doom-loop limit trips."
---

# Debug — Out of the Loop

> The characteristic failure of vibe coding is not the bug; it is the loop: paste the error,
> accept the fix, get a new error, paste that. Each turn changes more code with less
> understanding. `sdlc-standard` traces a defect across its whole V-model; the vibe version
> keeps its core — evidence before fix, and a record of why it was missed — and makes it fast.

Load `vibe-project`; the intent the bug belongs to, if any.

---

## DB-01 — Record it

Append to `{{profile.paths.bugs}}`:

```
BUG-{NNN} · 2026-09-18 · open
  Symptom   : saving an edited note returns 500
  Expected  : INT-{NNN} check 2 — list shows new title        (or: PRODUCT.md / DEC-*)
  Found in  : INT-{NNN}.3 verify / user report / prod log
  Severity  : blocks core flow | degrades | cosmetic
```

The "Expected" line anchors the bug to an intent. A "bug" with no expected behaviour anywhere
is a missing intent — route to `vibe-intent-spec`.

## DB-02 — Reproduce before touching code

- Smallest steps / request / test that shows the symptom **every time**.
- Capture the full error: message, stack trace, server log, network response — not the
  summary.
- Can't reproduce → say so; add logging at the suspected boundaries; do **not** "fix" blind.

From stage `mvp`, the reproduction becomes a failing test now (VT-07).

## DB-03 — Isolate

Cut the search space in half each step:

- **Which layer?** Browser console vs network response vs server log vs database state.
- **Which commit?** It worked before → `git log` since the last known good; `git bisect` with
  the reproduction when there are more than a few commits. Slice IDs in commits (SC-05) make
  the suspect obvious.
- **Which input?** The smallest input that still fails.
- **Which assumption?** Print the actual value where the code assumes one.

## DB-04 — Hypothesis, then evidence, then fix

Write the hypothesis in one sentence — *"the PATCH handler reads `params.id` synchronously but
Next 15 made `params` a Promise"* — and the observation that would prove or disprove it. Make
the observation. Only then change code.

Rules:
- **One hypothesis, one change, one run.** Never several speculative edits at once.
- The fix targets the **cause**, not the symptom. A `try/catch`, a `?.`, a retry or a default
  value that makes the error go away is not a fix unless the hypothesis says that is the cause.
- If the fix is right, you can explain why the bug happened. If you cannot, keep going (SS-06).
- Check the version: many AI-introduced bugs are an API from a different major version than
  the one installed (VT-03).

## DB-05 — Close it

1. The regression check exists and was **seen failing before, passing after** (VT-07).
2. The done-when checks of the affected intent all still pass.
3. Commit `BUG-{NNN}: <cause, not symptom>`.
4. Update the bug entry: cause · fix commit · regression check · **why it was not caught**
   (no check for this case / check existed but was weak / new code path / dependency change).
5. The "why not caught" goes to the refine loop when it repeats (RV-06).

## DB-06 — The unstuck protocol

When the doom-loop limit trips (SS-05), or the human says "it keeps going in circles":

1. **Stop editing.** Write down: the symptom, each attempt, what each showed.
2. **Preserve the attempts** on `{{profile.loop.attempt_branch_prefix}}<slice>-<n>`; return to
   the last good checkpoint.
3. **Pick one:**
   - *Debug properly* — DB-02..DB-05 from the clean checkpoint, with the attempt log as input.
   - *Re-slice smaller* — the slice was too big to reason about; split it (PL-02).
   - *Change approach* — the library/pattern is fighting you; propose an alternative as a `DEC-*`.
   - *Ask the human* — with the attempt log, and one specific question.
   - *Spike it* — a throwaway minimal repo that isolates the one unknown.
4. Record which, in STATE.md "Now".

Fresh context helps: when a session is long and full of failed attempts, `/vibe-handoff` and
start a new session from STATE.md — the failed attempts in context bias the next one.

## Self-check

- [ ] `BUG-*` recorded with an Expected anchored to an intent
- [ ] Reproduced reliably before any code change
- [ ] Cause stated in one sentence with the evidence that proved it
- [ ] Regression check seen red then green
- [ ] "Why not caught" recorded
