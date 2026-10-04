---
description: "Park an idea that is outside the current intent as IDEA-* in the backlog instead of building it — or review the backlog and promote/reject parked ideas. Usage: /vibe-park <idea> | /vibe-park review"
---

# Park an idea

Load `vibe-project`, then `vibe-session` (SN-04).

## Park (default)

1. Next `IDEA-*` id from `{{profile.paths.backlog}}` (ID-03).
2. Append: `IDEA-{NNN} · {date} · {idea in one line} · from {active slice or "chat"} · status: parked`.
3. If it contradicts a PRODUCT.md non-goal, note that on the entry.
4. Report one line and **return to the current slice**. Do not build it (IF-03).

## Review

List parked ideas, oldest first, each tagged with the core flow it would serve (or none) and
whether it hits a non-goal. For each, the human chooses:

- **promote** → `/vibe-intent` from it; status `promoted (INT-*)`
- **reject** → status `rejected (<reason>)` — the row stays (ID-02)
- **keep parked**

```
Backlog — {n} parked
  {IDEA-id · age · idea · serves: {flow|none} · non-goal: {y/n}}
```
