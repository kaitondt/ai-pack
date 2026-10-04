# RULE FAMILY: BASELINE AND CHANGE CONTROL

In a migration project the frozen thing is the legacy source. In a development project
the frozen thing is **what was agreed**. A baseline is the moment a document stops being
a draft and starts being a commitment — and from then on it changes only through a
recorded decision.

Without this rule the project still delivers documents. It just cannot say which version
the client approved, which is the same as not having approval.

## BL-01 — A baseline is an event, not an adjective

A document is baselined when all four are true:

1. its review is complete and every Critical finding is closed,
2. it contains no TBD (RS-03) and no unconfirmed assumption its content depends on,
3. the approver named in `{{profile.stakeholders}}` has approved it, with a date,
4. its version has been set to `{{profile.document.baseline_version}}` and the approval
   recorded in the revision history.

`/sdlc_phase_gate` performs the check and appends the entry to
`{{profile.constraints.baselined}}`. A document called "final" that is not in that list is
not baselined.

## BL-02 — A baselined document changes only through a change request

When `{{profile.constraints.baseline_change_requires_cr}}` is true, editing a baselined
document requires an approved CR id, and the edit records that id in the revision history.

This includes the edits that feel too small to be worth a CR — a corrected label, a
widened field, a clarified sentence. Especially those: they are the ones that reach
production without anyone testing them, because nobody registered that anything changed.

**Typo and formatting corrections that change no meaning** are the one exception. They are
made without a CR and noted in the revision history as editorial. If you have to think
about whether it changes meaning, it changes meaning.

## BL-03 — Design follows the document, code follows the design

The order is not bureaucracy; it is what keeps the artifacts able to disagree with each
other usefully.

```
change agreed → requirement updated → design updated → code updated → tests updated
```

Code that implements a change the design does not describe creates drift that the next
`/sdlc_generate_detail_design` run reports as a defect — correctly, because at that point
nobody can tell whether the code or the document is right.

When urgency forces code first (a production incident), the documentation debt is recorded
with a deadline: `{{profile.maintenance.hotfix.retro_documentation_days}}` days. See BL-06.

## BL-04 — Production is changed only through the release process

When `{{profile.constraints.production_change_via_release_only}}` is true:

- no manual edits to production configuration, data or files outside a recorded change,
- no "quick fix applied directly on the server",
- every production change traces to a release tag or a hotfix record,
- data fixes are scripts, reviewed and stored under `{{profile.paths.maintenance}}`,
  never ad-hoc statements typed into a console.

A data fix run by hand and not stored is unrepeatable and invisible. The next incident
investigation will not know it happened, and will reach the wrong conclusion.

## BL-05 — The decision log is append-only

`{{profile.paths.decision_log}}` records `DEC-*` entries: the question, the options
considered, the decision, the owner, the date, and the artifacts affected.

- Entries are appended, never edited into a new meaning.
- A reversed decision gets a **new** entry that supersedes the old one by ID, and the old
  entry gains a "superseded by" note. The original stays readable.

A decision log that is quietly rewritten to match the current design cannot answer the one
question it exists for: *why is it like this?*

## BL-06 — Emergency changes skip the queue, never the record

A hotfix is allowed when `{{profile.maintenance.hotfix.allowed}}` is true and approved by
`{{profile.maintenance.hotfix.approval}}`. What it may skip: the release train, the full
regression cycle, the normal CR lead time. What it may **not** skip:

- an incident record with class and severity,
- the root cause (RCA where `{{profile.maintenance.rca_required_for}}` applies),
- a regression test that would have caught it,
- bringing the design documents back in line within
  `{{profile.maintenance.hotfix.retro_documentation_days}}` days.

An undocumented hotfix is a defect the project has deliberately hidden from itself.

## BL-07 — Generated files are not edited

Files matching `{{profile.constraints.generated_files_glob}}` are never hand-edited.
Change the generator input and regenerate.

**Verify the generator exists before relying on it.** Hand-written files are frequently
mistaken for generated ones. Check the build scripts first; if no generator exists, the
file is hand-written and the profile's glob is wrong.

## BL-08 — Versioning discipline

| State | Version | Who sets it |
|---|---|---|
| Draft, under construction | `0.x.y` | author |
| Baselined | `{{profile.document.baseline_version}}` | approver, at the gate |
| Changed after baseline | minor bump, one row per CR | approver |

`{{profile.document.auto_version_bump}}` is `false`. Editing a document does not bump its
version — the version tracks approval cycles, not keystrokes (DS-02).
