---
name: vibe-session
description: "Session continuity and status — resume from STATE.md and git, detect when they disagree, write the handoff at the end of a session, keep the decision/debt/bug/backlog logs, and report status honestly. Use at the start and end of every working session, for 'where were we', 'what's next', 'status', 'wrap up', and when the context is getting long."
---

# Session — The Handoff Is a File

> The rules are in `rules/vibe/session-continuity.md`. `pm-standard` reports status to a
> steering committee; the vibe version reports to the next session — which is also the
> audience most likely to be misled by an optimistic summary.

Load `vibe-project`.

---

## SN-01 — STATE.md template

```markdown
# STATE — <project>                       updated 2026-09-18 17:40 · commit a1b2c3d

## Stage
prototype → next: mvp (blocking: core flow 3 not automated; DEBT-015 security; no CI)

## Now
INT-007.2 — ownership on page + API. API done and tested; page still shows the edit
button for others' notes. Stopped at: src/app/notes/[id]/page.tsx, needs `canEdit`.

## Next
1. finish INT-007.2
2. INT-007.3 — validation
3. DEBT paydown (counter 4/5) — DEBT-015 rate limit on login

## Broken
- Deleting a note with tags → 500 (BUG-011, open)

## Open questions
- Q1 (asked 2026-09-18): does editing move a note to the top of the list?

## Recently decided
- DEC-014 notes are soft-deleted (restore within 30 days)
- DEC-013 zod for all server input validation

## Last verified
2026-09-18 · a1b2c3d · typecheck ✅ lint ✅ tests 14/14 ✅ · INT-007.1 checks 1–2 ✅
```

Rewritten, not appended. One minute to read.

## SN-02 — Resume (`/vibe-resume`)

1. Read STATE.md, the active intent, the last few `DEC-*`.
2. `git status`, `git log --oneline -10`, current branch.
3. Compare. Report discrepancies **first**:
   - commits after STATE.md's commit that it does not mention
   - uncommitted changes STATE.md does not explain
   - on an `attempt/*` or `spike/*` branch unexpectedly
   - "Last verified" older than the latest commit touching code
4. If "Last verified" is stale, re-run the stage checks before building on top.
5. Propose the next step from "Now/Next"; wait for a yes if anything above was off.

## SN-03 — Handoff (`/vibe-handoff`)

At the end of a session, or when the context is long enough that earlier content is being
lost or failed attempts are crowding it:

1. Working tree: commit if it runs; otherwise stash or commit to an `attempt/*` branch — and
   write which in STATE.md.
2. Log anything decided / shortcut / parked / found this session (SC-04).
3. Conventions the human stated this session → `CLAUDE.md` project section (SC-06).
4. Rewrite STATE.md (SN-01), with "Now" precise enough that a fresh session could continue
   without asking: file, function, what is missing.
5. Print the STATE.md "Now" and "Next" to the human.

## SN-04 — The logs

| File | Record | Appended when |
|---|---|---|
| `{{profile.paths.decisions}}` | `DEC-*` | a choice constrains future work (IF-05) |
| `{{profile.paths.debt}}` | `DEBT-*` | a shortcut is taken or found (DL-01) |
| `{{profile.paths.bugs}}` | `BUG-*` | something does not meet an intent (DB-01) |
| `{{profile.paths.backlog}}` | `IDEA-*` | something is out of the current intent (IF-03) |

Next ID: highest existing + 1, read from the file (ID-03).

Backlog entry: `IDEA-023 · 2026-09-18 · Export notes as Markdown · from INT-007.2 · status: parked`.
Status: `parked` → `promoted (INT-*)` / `rejected (reason)`.

## SN-05 — Status (`/vibe-status`)

```
<project> — status 2026-09-18                              stage: prototype
  Intents    : 9 done · 1 active (INT-007, 1/3 slices) · 3 planned · 1 dropped
  Core flows : 4/5 done · automated 2/5
  Checks     : last verified a1b2c3d, 2 h ago — all green
  Broken     : 1 (BUG-011)
  Debt       : 7 open (2 security) · due at next stage: 4 · paydown counter 4/5
  Backlog    : 6 parked ideas
  Next stage : mvp — 4 criteria failing: <list>
  Open Qs    : 1, oldest 0 days
```

Every number comes from the files and git, computed now — not from memory of the session
(pm-standard RI-02). A number that could not be computed is shown as `?`, not estimated.

## Self-check

- [ ] Resume compared git to STATE.md and reported differences first
- [ ] Handoff rewrote STATE.md with a precise "Now"
- [ ] Every decision, shortcut, bug and idea from the session is in its log
- [ ] Status numbers computed from files, not recalled
