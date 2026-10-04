---
description: "Honest project status computed from the files and git — intents, core flows, checks, broken, debt, backlog, distance to the next stage. Read-only. Usage: /vibe_status"
---

# Status

Load `vibe_project`, then `vibe_session` (SN-05).

Compute every number **now** from `{{profile.paths.intents}}`, the four logs, STATE.md and git.
Nothing from memory of the session; a number that cannot be computed is `?`.

- Intents by status; active intent's slice progress
- Core flows: with a `done` intent / with automated checks
- Last verified: sha, age, result; commits since
- Broken: open `BUG-*` by severity
- Debt: open, security, due at next stage, paydown counter
- Backlog: parked count
- Next stage: GR-01 criteria failing (quick evaluation from files — say which were not run)
- Open questions and their age

Output in the SN-05 format. End with the one next action that most reduces risk.
