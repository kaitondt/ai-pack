# RULE FAMILY: ID NAMING

> Six kinds of record, one format each. Deliberately fewer than the sibling packs: a vibe
> project needs enough IDs to link intent → slice → commit → check, and to keep the four
> logs apart. More than that would not be kept up.

## ID-01 — The identifiers

| Record | Format | Lives in |
|---|---|---|
| Intent | `INT-{NNN}` | `{{profile.paths.intents}}/INT-{NNN}-<slug>.md` |
| Slice | `INT-{NNN}.{n}` | inside its intent file |
| Decision | `DEC-{NNN}` | `{{profile.paths.decisions}}` |
| Debt | `DEBT-{NNN}` | `{{profile.paths.debt}}` |
| Bug | `BUG-{NNN}` | `{{profile.paths.bugs}}` |
| Parked idea | `IDEA-{NNN}` | `{{profile.paths.backlog}}` |

`{NNN}` is zero-padded to three digits and counts per record type across the whole project.

## ID-02 — IDs are permanent

Never renumber, never reuse, never recycle a deleted or rejected ID. A rejected idea keeps its
`IDEA-*` with status `rejected`; a cancelled intent keeps its `INT-*` with status `dropped`.
Gaps in the sequence are normal and carry information.

## ID-03 — The next ID is computed, not remembered

Take the highest existing ID of that type in its file or directory and add one. Never
guess it from the conversation — two sessions guessing produce two different entries that both claim the same `DEC-{NNN}`.

## ID-04 — Compatible with the sibling packs

`DEC-{NNN}` uses the same format as `sdlc-standard` and `pm-standard`, so the decision log
carries over unchanged on graduation. `INT-*`, `DEBT-*`, `BUG-*` and `IDEA-*` map onto the
sibling records as described in `skills/vibe-graduation` — they are never renamed in place;
the sibling record cites the vibe ID as its origin.
