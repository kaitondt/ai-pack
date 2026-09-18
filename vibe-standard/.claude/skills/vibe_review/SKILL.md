---
name: vibe_review
description: "Review AI-written code — a slice's diff, a branch, or the whole codebase — for the failure modes of vibe coding: scope creep, security holes, phantom APIs, weakened tests, duplicated logic, unrecorded shortcuts and code nobody can explain. Also owns the refine loop that feeds repeated findings back into the pack. Use for 'review this', 'is this safe', 'audit the codebase', before merging, and before graduation."
---

# Review — Reading What the AI Wrote

> `sdlc-standard` reviews deliverables against checklists and design documents. A vibe
> review reviews code against **the intent** and against the specific ways AI-generated code
> goes wrong: it is fluent, confident, locally plausible, and globally inconsistent.

Load `vibe_project`; for a slice review, its intent file.

---

## RV-01 — Three review depths

| Depth | When | Scope | Time |
|---|---|---|---|
| **Quick** | end of every slice (self-review, BD-04) | the slice diff, RV-02 only | 2 min |
| **Slice** | `/vibe_review` — `mvp`+ every slice; security-relevant slices at any stage | the diff + the files it touches, RV-02 + RV-03 | 10 min |
| **Codebase** | before `/vibe_graduate`, or when the project "feels fragile" | the whole repo, RV-04 | 1 h |

At `mvp`+ the slice review is done by the `vibe_reviewer` agent, **not** the context that
wrote the code — a writer reviewing its own output agrees with itself.

## RV-02 — The quick pass (every slice)

| # | Look for | Rule |
|---|---|---|
| Q1 | a file changed that is not on the slice map | SS-04 / IF-03 |
| Q2 | behaviour beyond the intent — extra endpoint, option, field, button | IF-03 |
| Q3 | a secret, key, token, password or real personal data in the diff | SB-01, SB-05 |
| Q4 | a test skipped / deleted / loosened; `any`, `ignore`, lint-disable added | VT-05 |
| Q5 | `TODO` / `FIXME` / `HACK` without a `DEBT-*` id | DL-03 |
| Q6 | debug leftovers: `console.log`, `print`, `debugger`, commented-out code | VE-05 |
| Q7 | refactor mixed into behaviour change | SS-07 |

## RV-03 — The slice review

In addition to RV-02:

**Intent fit**
- Does each done-when check have code that satisfies it **and** a check that proves it?
- Does the code do anything the "Not now" list excludes?

**Security** (from `vibe_security`)
- Every new endpoint / server action: authentication? authorisation **per resource**?
  server-side validation?
- Any string-built SQL / shell / path; any raw HTML rendering; any secret reaching the client?
- Any new dependency: VT-03 done? `DEC-*` exists?

**Correctness smells typical of AI code**
- Error handling that swallows (`catch {}` / `except: pass`) or returns success on failure
- Optional chaining / null checks sprinkled to silence errors rather than handle a real case
- An API or option that looks right but does not exist in the installed version
- Async mistakes: missing `await`, un-awaited promise in a loop, race on shared state
- Off-by-one / timezone / currency rounding in anything with numbers or dates
- The happy path only: no empty state, no loading state, no error state in UI

**Consistency**
- A second way of doing something the codebase already does one way (fetching, forms,
  validation, errors, styling) → finding: use the existing one, or record a `DEBT-*`
- Duplicated logic that was copied and adjusted → `DEBT-*` if not fixed
- Names that disagree with PRODUCT.md vocabulary

**Explainability** — the vibe-specific check
- Pick the most complex function in the diff. Can the author state in one or two sentences
  what it does and why it is correct? If not, it is not reviewed, it is just read (SS-06).

## RV-04 — The codebase review

For graduation or a health check. Produce counts, not impressions:

| Measure | How |
|---|---|
| Intents vs features | features in the app with no `INT-*`; `INT-*` marked done whose checks fail now |
| Test coverage of core flows | per core flow: automated checks yes/no |
| Unrecorded debt | bare TODO/FIXME count; obvious shortcuts with no `DEBT-*` (DL-06) |
| Security baseline | SB-07 matrix for the target stage, per row pass/fail |
| Duplication | the same concern implemented N ways (auth checks, fetch wrappers, form handling) |
| Dependencies | count, unused ones, outdated majors, audit result |
| Dead code | unreferenced files, exports, routes |
| Hotspots | files changed most often in git log × largest — where the next bug is |

## RV-05 — Findings

Severity: **Critical** (security hole, data loss, wrong result on a core flow) · **High**
(done-when not actually met, weakened check, missing ownership check) · **Medium** (debt not
recorded, inconsistency, missing error/empty state) · **Low** (naming, style).

Every finding: file:line, what, why it matters, suggested fix. Write the report to
`{{profile.paths.reviews}}/<date>-<scope>.md`. Critical and High block the commit / merge /
graduation until fixed or explicitly accepted by the owner as a `DEC-*` (Critical security
findings cannot be accepted — SB-08).

## RV-06 — The refine loop

A finding that appears once is a code defect. A finding that appears in **two or more
slices** is a gap in the pack or the project conventions. `/vibe_refine_skill` handles it:

| Pattern | Fix belongs in |
|---|---|
| Same mistake across slices, the rule is unclear | the skill or rule wording |
| Same mistake, the rule is clear | a hook, or a check in `vibe_verify` |
| A project convention the AI keeps missing | `CLAUDE.md` project section (SC-06) |
| The finding contradicts a correct rule | this review checklist |

**Never weaken a rule to make a finding disappear.** Record each change in
`{{profile.paths.skill_changes}}` with the slices produced under the old rule.

## Self-check

- [ ] Review depth matches the stage and the slice's risk
- [ ] Every RV-02 item checked; findings have file:line and severity
- [ ] At `mvp`+, the reviewer was not the writer
- [ ] Repeated findings routed to the refine loop, not just fixed again
