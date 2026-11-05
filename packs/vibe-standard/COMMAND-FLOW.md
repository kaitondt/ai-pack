# Command Flow

How the 22 commands relate: what each reads and writes, the loop they are built around, the
flow at each stage, and the refine loop.

---

## 1. Command catalogue

### Setup — once

| Command | Reads | Writes | Agent |
|---|---|---|---|
| `/vibe-init` | the repository | profile, `vibe/` memory folder, `CLAUDE.md` | — |
| `/vibe-profile-check` | profile, repo, hooks | nothing (report) | — |
| `/vibe-scaffold` | profile, stack choice | skeleton, tooling, `DEC-001`, real commands | — |

### Decide what to build

| Command | Reads | Writes | Agent |
|---|---|---|---|
| `/vibe-product` | answers, existing app | `PRODUCT.md`, `DEC-*` on revision | — |
| `/vibe-intent` | request, PRODUCT.md | `INT-NNN-*.md` | — |
| `/vibe-plan` | intent, code | slices in the intent, STATE.md Next | `vibe-planner` |
| `/vibe-park` | an idea | `IDEA-*` in backlog | — |

### Build — the loop

| Command | Reads | Writes | Agent |
|---|---|---|---|
| `/vibe-build` | intent, slice, code | code, tests, commit, intent log, STATE.md, `DEBT-*` | `vibe-builder` (+ `vibe-verifier`, `vibe-reviewer` from mvp) |
| `/vibe-verify` | intent, running app | STATE.md Last verified, `BUG-*` for regressions | `vibe-verifier` |
| `/vibe-review` | diff, intent | review report, proposed `DEBT-*` | `vibe-reviewer` |
| `/vibe-commit` | the working tree, `commit:` in the profile | one commit in the agreed format (also `/vibe-build`'s commit step); never a push | — |

### When it breaks

| Command | Reads | Writes | Agent |
|---|---|---|---|
| `/vibe-fix` | symptom, code, git history | `BUG-*`, fix, regression check | `vibe-debugger` |
| `/vibe-unstuck` | the failed attempts | `attempt/*` branch, STATE.md | — |

### Keep it healthy

| Command | Reads | Writes | Agent |
|---|---|---|---|
| `/vibe-debt` | ledger, code | `DEBT-*`, paydown commits | — |
| `/vibe-security-check` | code, history, deps, config | security report, security `DEBT-*` | `vibe-security-auditor` |
| `/vibe-refine-skill` | reviews, bugs, corrections | skill/rule/hook/CLAUDE.md edits, skill-changes log | — |
| `/vibe-rule-register` | a correction given twice, or a style guide | `.claude/rules/project/<topic>.md`, `project_rules`, `DEC-*` for overrides | — |

### Ship and grow

| Command | Reads | Writes | Agent |
|---|---|---|---|
| `/vibe-ship` | git log, checks, profile.release | release note; deploy handed to the human | — |
| `/vibe-graduate` | everything | `DEC-*`, profile `stage`, `HANDOFF.md` | — |

### Sessions

| Command | Reads | Writes |
|---|---|---|
| `/vibe-resume` | STATE.md, git | nothing, or re-verification |
| `/vibe-handoff` | the session | logs, CLAUDE.md conventions, STATE.md |
| `/vibe-status` | all records, git | nothing |

---

## 2. Dependency graph

```mermaid
flowchart TD
  INIT["/vibe-init"] --> SCAF["/vibe-scaffold"]
  INIT --> PROD["/vibe-product"]
  SCAF --> INT
  PROD --> INT["/vibe-intent"]
  INT --> PLAN["/vibe-plan"]
  PLAN --> BUILD["/vibe-build"]
  BUILD --> VER["/vibe-verify"]
  VER --> REV["/vibe-review"]
  REV -->|commit| NEXT{{"next slice"}}
  NEXT --> BUILD
  BUILD -->|"3 failed attempts"| UNS["/vibe-unstuck"]
  UNS --> FIX["/vibe-fix"]
  UNS --> PLAN
  VER -->|regression| FIX
  FIX --> BUILD
  BUILD -.->|"idea outside intent"| PARK["/vibe-park"]
  BUILD -.->|"shortcut"| DEBT["/vibe-debt"]
  NEXT -->|"every N slices"| DEBT
  NEXT --> SHIP["/vibe-ship"]
  SEC["/vibe-security-check"] --> SHIP
  SHIP --> GRAD["/vibe-graduate"]
  SEC --> GRAD
  DEBT --> GRAD
  REV -->|"repeat finding"| REF["/vibe-refine-skill"]
  FIX -->|"why not caught"| REF
```

Every session is wrapped in `/vibe-resume` … `/vibe-handoff`.

---

## 3. A session, end to end

```
/vibe-resume                          ← hook already printed STATE.md; compare with git
  "Now: INT-{NNN}.2 — ownership on page + API; API done, page not"
/vibe-build INT-{NNN}.2                 ← restate, clean tree, map (3 files), build
  … hook: slice budget fine
  … verifier: check 3 ❌ user B sees edit button → fix → ✅
  … reviewer: 0 Critical, 1 Medium (bare TODO → DEBT-{NNN})
  commit "INT-{NNN}.2: enforce note ownership on page and API"
/vibe-build INT-{NNN}.3
  … attempt 1 ❌, 2 ❌, 3 ❌ (zod error message not shown)
/vibe-unstuck                         ← attempts on attempt/INT-{NNN}.3-1, back to checkpoint
/vibe-fix "validation message not shown"
  … cause: server action returns error object but form reads `state.message` (v19 API)
  … regression test red → green; commit "BUG-{NNN}: form reads useActionState error shape"
/vibe-build INT-{NNN}.3                 ← now 1 attempt, done
/vibe-park "markdown preview"         ← the owner's idea mid-slice → IDEA-{NNN}, not built
/vibe-handoff                         ← DEC ×1, DEBT ×1, IDEA ×1 logged; STATE.md rewritten
```

---

## 4. Flows by stage

### spike — "can this even work?"

```
git switch -c spike/<question>
/vibe-intent (one line + assumptions)  →  build freely  →  answer the question
→ DEC-* with the answer  →  delete or abandon the branch
```
Still in force: secrets, destructive-command guard, synthetic data, the answer written down.

### prototype — "show it to someone"

```
/vibe-init → /vibe-scaffold → /vibe-product
loop per feature:  /vibe-intent → /vibe-plan → /vibe-build (→ /vibe-verify) → commit
every session:     /vibe-resume … /vibe-handoff
before showing it: /vibe-verify all
```

### mvp — "real users"

```
/vibe-graduate mvp   ← refused until: core flows automated, CI, security check, due debt paid
loop per feature:  /vibe-intent → /vibe-plan → /vibe-build
                   (verifier and reviewer are separate agents; review every slice)
every 4–5 slices:  /vibe-debt pay
before release:    /vibe-security-check → /vibe-ship
```

### production — "people depend on it"

```
/vibe-graduate production
per release:  /vibe-verify all → /vibe-security-check → /vibe-ship (E2E smoke, rollback rehearsed)
incidents:    /vibe-ship rollback first → /vibe-fix → "why not caught" → /vibe-refine-skill
decide:       /vibe-graduate handoff  (sdlc / pm / both / stay)
```

---

## 5. Adopting on an existing vibe-coded repo

The common case: something already exists, built without any of this.

```
/vibe-init            ← inspect; honest stage; secrets findings first
/vibe-scaffold        ← retrofit lint/typecheck/test; record what they report as DEBT-*, fix nothing yet
/vibe-product         ← from what the app does + what the owner says it should
(one /vibe-intent per existing feature, status done, checks it SHOULD meet)
/vibe-verify all      ← failures become BUG-*
/vibe-debt sweep      ← expect many; that is the point
/vibe-security-check  ← if it has a URL or users, before anything else
```
Then back to the normal loop, with debt paydown weighted toward security and core flows.

---

## 6. The refine loop

```
  execute (/vibe-build) → verify / review → finding
        ▲                                   │ seen before?
        │                                   ├─ no  → fix the code
        │                                   └─ yes → /vibe-refine-skill
        │                                             │ classify: skill · rule · hook · check ·
        │                                             │           CLAUDE.md convention · checklist
        └────────── re-run the affected slices ◄─────┘ record blast radius in skill-changes.md
```

The loop is closed when the generator has run again under the changed rule and the review
comes back clean. **A rule is never weakened to make a finding disappear.**

In vibe coding the signal arrives fast: the same correction given to the AI twice in one week
is already a pattern. Put it in `CLAUDE.md` (SC-06) the second time, not the tenth.
