---
name: sdlc-test-artifact-lifecycle
description: "Test artifact lifecycle across execution rounds — version history between test case revisions, carrying results forward by TC ID, condensing multi-flow files into one execution table, checkpoint counting, and evidence file naming. Load for ALL test maintenance tasks between rounds."
---

# Test Lifecycle — between rounds

> Prerequisite: `sdlc-project` resolved.

Test cases are revised while results already exist against the previous revision. Handled
carelessly, a revision silently discards a round of execution evidence — or worse, carries
a stale pass forward onto a case that changed. These are the operations that keep rounds
comparable.

---

## 1. Version history between revisions

When a test case document is revised, produce a **separate** history file. Never edit the
revision table of the test case file by hand from memory.

Compare old and new by TC ID:

| Category | Meaning |
|---|---|
| Added | TC ID present only in the new file |
| Removed | present only in the old file — must be justified, not silently dropped |
| Changed | same TC ID, different steps, expectations or preconditions |
| Unchanged | identical |

Also compare what sits outside the case tables: shared preconditions, flow names,
environment notes. A changed shared precondition affects every case under it, and the
per-case diff will not show it.

Output: the proposed revision row plus the change detail, written to its own file. The
human decides whether to apply it — version bumps are never automatic (DS-02).

**Changed cases invalidate their previous results.** A case whose steps changed was not
executed in its current form. Say so explicitly in the history.

---

## 2. Carrying results forward

When a new revision replaces one that has results, results move by **TC ID only**.

| Situation | Action |
|---|---|
| TC ID exists in both, content unchanged | copy the results forward |
| TC ID exists in both, content changed | **do not copy** — mark for re-execution |
| TC ID only in the new file | leave the result columns empty |
| TC ID only in the old file | leave it behind, and record it as removed |

Ask the user how to handle partial matches before writing, rather than picking a rule.
Getting this wrong fabricates evidence that a case passed when it was never run in that
form — the one failure mode here that is genuinely dangerous, because it is invisible
afterwards.

Never modify the old file. It is the evidence for the round it belongs to.

**A result also belongs to a build.** Record which build each round ran against. A pass
from round 1 against a build that no longer exists is not evidence for the release, and at
the P7/P8 gate someone will ask.

---

## 3. Condensing for execution

A design document organised by flow — a name, shared preconditions, and a table per flow —
is right for review and wrong for execution, where the tester wants one table.

To condense: keep one header row and every data row, in original order, adding the flow
name as a column so the grouping survives. Append the result columns:
`{{profile.testing.rounds.columns}}` × `{{profile.testing.rounds.count}}`, empty.

Drop everything that is not a case row. Keep every case row — condensing is a change of
shape, never of content, and the TC ID set before and after must be identical.

---

## 4. Counting checkpoints

Effort and coverage are estimated from checkpoints, not cases: one case may assert one
thing or fifteen. Count the numbered assertions in the expected-result column.

Count mechanically and state the rule used, so two people counting the same file get the
same number. A count without its rule is not comparable to the next one — and these counts
feed test density (QM-05).

---

## 5. Evidence naming

Evidence files are named for the case they prove, per
`{{profile.testing.evidence.naming}}`, under `{{profile.testing.paths.evidence_root}}`.

Check before a round is closed:
- every file maps to a real TC ID in the current revision
- every case that requires evidence has it
  (`{{profile.testing.evidence.required_for}}`)
- sequence numbers are contiguous within a case
- no file names a TC ID that was removed in this revision

Verify against the **current** revision. Evidence named for TC IDs that no longer exist is
the visible symptom of a revision that skipped step 1.

Rename rather than delete when a name is wrong; deleting evidence destroys the audit trail
of the round it belongs to.

---

## 6. Closing a round

A round is closed when every case has a verdict (`Pass` / `Fail` / `Blocked` / `N/A` with
a reason), every failure has a defect id, and the metrics for the round are recorded
(QM-07). A round closed with cases still marked "in progress" cannot be compared with the
next one, which is the only thing rounds are for.

---

## Reporting

```
Lifecycle — {module}, {operation}
  Old → new       : {file} → {file}
  Added {n} · Removed {n} · Changed {n} · Unchanged {n}
  Results carried : {n}   withheld (content changed) {n}   empty {n}
  Build           : round {n} ran against {build id}
  Checkpoints     : {n}   (rule: {counting rule})
  Evidence        : {n} files, {n} unmatched, {n} cases missing evidence
  Old file modified : no
```
