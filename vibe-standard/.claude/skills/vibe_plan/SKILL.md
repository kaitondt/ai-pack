---
name: vibe_plan
description: "Break an intent into small, vertical, runnable slices; order them; size them against the slice budget; and give an honest time range. Use for 'plan this feature', 'break this down', 'what order should we build in', 'how long will this take', or when a slice turned out too big."
---

# Planning — Slices and Order

> `pm-standard` plans with a WBS, a dictionary, estimates with method and range, and a
> baselined schedule. The vibe version keeps three of its ideas — decompose until each piece
> is small and verifiable, estimate with a range and a basis, never back-fit to a target —
> and drops the rest.

Load `vibe_project` and the intent being planned.

---

## PL-01 — Slice vertically

Each slice cuts through every layer it needs and ends in something **runnable** that moves at
least one done-when check forward (SS-01).

Heuristics for finding the slices:

| Technique | Example for "notes can be edited" |
|---|---|
| **Happy path first, then the edges** | 1. edit + save · 2. validation · 3. ownership |
| **One operation per slice** | create · read · update · delete |
| **Hardcode first, then make it real** | 1. UI against a fixed list · 2. wire to DB |
| **One user kind per slice** | 1. owner edits · 2. admin edits anyone's |
| **Spike the unknown first** | 0. can the PDF lib render Japanese? (spike, thrown away) |

Put the **riskiest** slice early — the one most likely to change the plan (an unfamiliar API,
a data-model question). Discovering it last is the vibe-coding version of a schedule slip.

## PL-02 — Size each slice against the budget

For each slice, predict the file map (SS-04) and a line count. Compare to
`{{profile.slices.max_files}}` / `{{profile.slices.max_changed_lines}}`. Over budget → split
now, not halfway through building it.

A slice that needs a new dependency, a schema change, or a new external service has an
**extra decision step** (IF-05) — note it in the plan so it is not discovered mid-build.

## PL-03 — Every slice maps to done-when checks

```
INT-007 — Notes can be edited
  INT-007.1  edit form, pre-filled; save updates        checks 1,2   ~4 files  ~150 lines
  INT-007.2  ownership on page + API                    check 3      ~3 files  ~80 lines   ← risk: auth helper unclear
  INT-007.3  validation, error message                  check 4      ~3 files  ~60 lines
  ─────
  every check covered: 1 ✓ 2 ✓ 3 ✓ 4 ✓
```

A check covered by no slice is a gap in the plan. A slice covering no check is scope creep or
infrastructure — label which.

## PL-04 — Estimate as a range with a basis

When asked "how long":

- Give a **range**, not a number: "3–6 hours of building across 3 slices".
- State the **basis**: slices of this size in this repo have been taking N minutes (look at the
  timestamps in intent Logs / git history), or "no history yet — this is a guess".
- Name what widens it: the risky slice, the unanswered question, the unfamiliar library.
- Include what people forget: verifying, reviewing, fixing what the verification finds,
  updating STATE.md, and deploying.

**Never back-fit.** If the human has a deadline and the range exceeds it, show the options —
cut a slice, cut a check, move a check to a later intent, accept a debt — with what each costs.
Do not produce a smaller number (pm-standard ES-02).

## PL-05 — A lightweight roadmap, when there is more than one intent

`{{profile.paths.state}}` "Next" holds the next 1–3 slices. When the human wants a longer view,
order intents by:

1. Core flows before non-core
2. Riskiest unknown first within a flow
3. Whatever is needed to put it in front of a user soonest
4. Debt due at the next stage (DL-04)

Keep it as a short ordered list of intents in PRODUCT.md or STATE.md — not a Gantt chart. When
the project needs dates, owners and commitments to other people, that is the signal to adopt
`pm-standard` (`vibe_graduate`).

## Self-check

- [ ] Every slice is vertical and runnable on its own
- [ ] Every slice is within budget, or has been split
- [ ] Every done-when check is covered by a slice
- [ ] The riskiest slice is early
- [ ] Decisions needed (dependency, schema, service) are flagged on their slice
- [ ] Any estimate is a range with a basis, not back-fitted
