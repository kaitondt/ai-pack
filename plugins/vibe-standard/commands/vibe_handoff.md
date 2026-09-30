---
description: "End a session cleanly — settle the working tree, log every decision/shortcut/bug/idea from the session, write conventions into CLAUDE.md, and rewrite STATE.md so the next session can continue without asking. Usage: /vibe_handoff"
---

# Handoff

Load `vibe_project`, then `vibe_session` (SN-03).

1. **Tree.** Runs → commit with the slice ID. Does not run → commit to an `attempt/*` branch or
   stash, and say which. Never leave it unexplained.
2. **Logs.** Go through the session: every decision → `DEC-*`; shortcut → `DEBT-*`; problem →
   `BUG-*`; out-of-scope idea → `IDEA-*`. Show the list before appending.
3. **Conventions.** Corrections the human gave that should hold project-wide → the project
   section of `CLAUDE.md` (SC-06). Show them first.
4. **STATE.md.** Rewrite per SN-01. "Now" names the file, function and what is missing.
5. **Print** Now and Next.

```
Handoff — {date}
  Tree      : {committed sha | attempt branch | stash} 
  Logged    : DEC {n} · DEBT {n} · BUG {n} · IDEA {n}
  CLAUDE.md : {n} conventions added
  Now       : {…}
  Next      : {…}
```
