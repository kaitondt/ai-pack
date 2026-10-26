---
name: sdlc-defect-management
description: "Defect lifecycle and triage — the record format, severity and priority model, injection-phase attribution, the failure-classification decision tree for automated runs, root-cause grouping, deferral rules, the triage report, and the client-facing bug list (deduplicated results, one bug per root cause, written in the deliverable language with evidence). Load for ALL test failure analysis, defect handling and bug-list tasks."
---

# Defect Management

> Prerequisite: `sdlc-project` resolved. Results under
> `{{profile.testing.paths.results_root}}`.

A failing suite is not a list of defects, and a defect list is not a status report. This
skill covers both: how one defect is recorded, and how a run's failures are classified into
something actionable.

---

## 1. The defect record

Every `BUG-*` carries:

| Field | Rule |
|---|---|
| Summary | what is wrong, in one line, from the user's point of view |
| Found in | test case id, level, environment, build |
| Steps | reproducible by someone who was not there |
| Expected | with its anchor: the requirement or design item (TR-AN01) |
| Actual | observed, with evidence attached |
| Severity | from `{{profile.quality.severity}}` — impact, not urgency |
| Priority | when it will be fixed — urgency, negotiable |
| **Injection phase** | the phase whose deliverable was wrong (TR-07) |
| Root cause | filled at fix time, not at raise time |
| Fix | what changed, and the regression case added |

**Severity and priority are different fields and they are set by different people.**
Severity is a fact about impact, assessed by the tester or the client. Priority is a
scheduling decision, made by the product owner. Merging them lets scheduling pressure
rewrite impact — which is how an S1 becomes "low priority, therefore not critical".

## 2. Injection phase — the field everyone gets wrong

Attribute the defect to the phase that **injected** it, not the phase that found it:

| The defect is | Injected in |
|---|---|
| The requirement was wrong, ambiguous or missing | P1 |
| The requirement was right; the design contradicted it | P2 |
| The design was right; the detail design was wrong or under-specified | P3 |
| The design was right; the code did something else | P4 |
| The code was right; the test asserted the wrong thing | the test's own phase |
| An environment or data setup problem | not a product defect — see §4 `INFRA` |

This is a judgement, and it must be made honestly enough to be uncomfortable. Recording
everything as P4 makes phase containment (QM-04) report a flat 100% upstream and tells the
project nothing about where its process leaks.

The most valuable single number a project produces is **the count of UAT defects injected
in P1**. It is the direct measure of how well requirements were elicited.

---

## 3. Deferral and closure rules

| Closure | Requires |
|---|---|
| Fixed | the fix, the regression case that would have caught it, a re-test by someone other than the fixer |
| Deferred | a named approver, a target release, and the risk accepted in writing |
| Not reproducible | an investigation record: what was tried, in what environment, with what data |
| Not a defect | the specification quoted, showing the behaviour is as designed (UA-04) |
| Duplicate | the id it duplicates, verified as the same root cause — not merely the same symptom |

**Never close a defect to make a gate.** Reclassifying severity, merging distinct defects,
or closing as "not reproducible" without investigation are the four ways a report is
improved and a release is made worse (QM-08).

---

## 4. Classifying an automated run's failures

Most failures in an automated suite are **not** product defects, and reporting them as such
destroys the credibility of the ones that are.

| Class | Meaning | Goes to |
|---|---|---|
| `PRODUCT-DEFECT` | the application behaves differently from the specification | development, as `BUG-*` |
| `SCRIPT-ERROR` | the test is wrong: bad locator, bad data, bad wait, bad assumption | test author |
| `NEEDS-REVIEW` | the failure is ambiguous from the log alone | a human, with evidence |
| `INFRA` | environment: service down, database unreachable, timeout under load | environment owner |

There is a fifth outcome that is not a class: **the test is right and the specification is
wrong.** When the code matches the design and the case matches the design but they disagree
with each other, that is a design defect — raise it with injection phase P2 or P3, not as a
code fix.

### Decision tree — apply in this order

Order matters. Applied out of order, infrastructure failures get logged as product defects
and the report becomes noise.

1. **Infrastructure signature?** Connection refused, DNS, auth service unavailable, the
   whole suite failing at the same step, wall-clock timeout with no page interaction →
   `INFRA`. Stop; do not analyse further, and do not report the rest of the run until it is
   re-run.
2. **Did the test ever reach its assertion?** Failure during setup, navigation or login →
   `SCRIPT-ERROR` or `INFRA`, never a product defect. The product was not exercised.
3. **Does the failure reproduce?** A failure that passes on re-run with no change is flaky
   → `SCRIPT-ERROR`, quarantined with a reason. Never re-run until green and report pass.
4. **Does the actual behaviour match the specification?** If yes, the case is wrong →
   `SCRIPT-ERROR` or a manual case defect. If no → `PRODUCT-DEFECT`.
5. **Ambiguous** — locator not found, element not visible, timeout at an interaction →
   `NEEDS-REVIEW`, escalate with evidence.

### Step 5 in practice

"Element not found" is the most common ambiguous failure and it has two very different
causes: the element genuinely is not rendered (product defect), or it is rendered under a
locator the script does not match (script error). The log cannot tell them apart. **Read
the screenshot** before classifying. Where no screenshot exists, that is a gap in the
automation setup worth fixing before the next round.

---

## 5. Evidence and source lookup

**For `NEEDS-REVIEW`:** open the captured screenshot or trace. Decide from what is on the
screen, not from the exception type.

**For `SCRIPT-ERROR`:** find the concrete fix before reporting. Read the page object, the
locator, the data file. A triage report that says "script error" without naming the line
and the fix hands the whole investigation back to the author — which is the work triage was
supposed to do.

**For `PRODUCT-DEFECT`:** anchor it. The expected behaviour must trace to the requirement
or design document. An unanchored product defect will be disputed and will consume more
time in argument than investigation.

---

## 6. Systematic vs isolated

Before writing the report, group the failures. Defects arrive in families:

- the same locator pattern failing across many screens → one script fix, not twenty
- the same rounding difference across every monetary field → one product defect, one root
  cause
- the same permission failure for one role → one authorisation defect

Reporting twenty instances of one root cause as twenty defects makes the suite look worse
than it is and the backlog unactionable. Report the root cause with its instance list — and
note that this grouping is legitimate, unlike the merging forbidden in §3, because it is
one cause rather than a count reduction.

---

## 7. Report

```
Triage — run {id}, {date}, build {id}
  Total {n}   passed {n}   failed {n}   blocked {n}

  PRODUCT-DEFECT  {n}   → {grouped by root cause}
      {TC ID} · {module} · expected {x} · actual {y} · anchor {doc §} · injection {phase}
  SCRIPT-ERROR    {n}   → {file}:{line} — {fix}
  NEEDS-REVIEW    {n}   → {TC ID} — {what the screenshot shows} — {question}
  INFRA           {n}   → {symptom} — re-run required

  Root causes     : {n} distinct behind {n} failures
  Injection phase : P1 {n} · P2 {n} · P3 {n} · P4 {n}
  Containment     : {found in injecting phase}/{total} = {%}   target {{profile.quality.targets.phase_containment}}
  Blocked         : {tests not run because of INFRA}
```

State the run and the build being analysed. A triage report that does not identify them
cannot be compared with the next one, and comparison across rounds is how you tell whether
the system is converging (QM-07).

---

## 8. The client-facing bug list

The triage report in §7 is for the team. When a round's defects go to the client — at IT
and ST exit, during UAT, or whenever the contract asks for a bug list — produce a separate
deliverable from the **triaged** run. Never generate it from raw results: a bug list that
contains script errors and infrastructure failures is retracted line by line, and the
retractions are what the client remembers.

**Input.** The results in `{{profile.testing.automation.results_format}}` under
`{{profile.testing.paths.results_root}}`, plus the §7 classification. Only `PRODUCT-DEFECT`
rows enter the list; `NEEDS-REVIEW` rows enter only after a human has classified them.

**Deduplicate before counting.** Result formats record every attempt: retries, re-runs and
the history of earlier rounds. Collapse to one result per TC ID — the **last attempt of the
run being reported** — and say that you did. Counting attempts inflates the failure rate;
keeping the first attempt reports failures that were already fixed.

**One bug per root cause.** Group the failures by root cause (§6); each group gets one
`BUG-*` id with every affected TC ID listed under it. This is not the merging §3 forbids —
distinct root causes stay distinct bugs even when the symptom looks the same. When unsure
whether two failures share a cause, keep them apart.

**Written for the reader, in the reader's language.** The list is a deliverable: its language
is the one `{{profile.language.by_path}}` binds to its directory, and its terms come from the
glossary and `{{profile.language.dictionary}}`. For every bug:

| Field | Content |
|---|---|
| Bug ID | `BUG-*`, stable across rounds — a bug found again in round 2 keeps its id |
| Summary | what the user experiences, in one sentence, no framework vocabulary |
| Screen / function | the module id and the screen or function name from the design |
| Steps | the case's steps, rewritten as a user would perform them |
| Expected | in plain words, **with the anchor** (requirement or design item) — never "expected `toBeVisible`" |
| Actual | what happened, in plain words; the assertion error translated, not pasted |
| Affected cases | every TC ID in the group |
| Severity | from `{{profile.quality.severity}}` |
| Evidence | the screenshot or trace for each affected case, copied beside the list and named per `{{profile.testing.evidence.naming}}` |

A raw assertion message (`expected "保存しました" received "登録しました"`, `locator resolved
to 0 elements`) is evidence, not a description. Translate it into what the user sees, and put
the raw message in the evidence column if the reader needs it.

**Statistics, honestly.** Executed, passed, failed and blocked per module, after the
deduplication, with the run id and build. Skipped tests are listed as not run, never folded
into passed.

**Format** comes from the registry entry `bug_list` in `{{profile.templates.registry}}` —
Markdown, Excel or an HTML page — written through `sdlc-document-io`. With no template
registered, follow `{{profile.templates.on_missing}}` like any other category. Evidence files
are copied, never linked to a location the client cannot open.

```
Bug list — round {n}, run {id}, build {id}
  Results read   : {n} attempts → {n} TC IDs after deduplication (last attempt kept)
  Bugs           : {n} root causes covering {n} failed cases
  Excluded       : SCRIPT-ERROR {n} · INFRA {n} · NEEDS-REVIEW unresolved {n}
  Language       : {lang}   format: {md|xlsx|html}   evidence copied: {n}
  Carried over   : {n} bug ids from earlier rounds
```
