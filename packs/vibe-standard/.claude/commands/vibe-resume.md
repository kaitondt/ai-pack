---
description: "Start a session from the project's memory — read STATE.md, the active intent and recent decisions, compare with git, report discrepancies first, re-verify if stale, and propose the next step. Usage: /vibe-resume"
---

# Resume

Load `vibe-project`, then `vibe-session` (SN-02).

1. Read `{{profile.paths.state}}`, the active intent, the last 5 `DEC-*`.
2. `git status` · `git branch --show-current` · `git log --oneline -10`.
3. Report discrepancies before anything else: unexplained commits or changes, unexpected
   branch (`attempt/*`, `spike/*`), stale "Last verified".
4. Stale → run the stage checks (`/vibe-verify`) before building on top.
5. Propose the next step from Now / Next. Wait for a yes if anything in 3 was off.

```
Resume — {project}                           stage: {stage}
  Branch    : {branch} @ {sha}   tree: {clean | n changes}
  STATE.md  : updated {when} @ {sha}   {in sync | ⚠ {discrepancies}}
  Now       : {slice} — {where it stopped}
  Broken    : {n}   Open questions: {n}
  Verified  : {fresh | stale → re-ran: result}
  Proposed  : {next command}
```
