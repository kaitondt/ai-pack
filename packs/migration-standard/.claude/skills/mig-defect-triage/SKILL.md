---
name: mig-defect-triage
description: "Classify failing test results into product defect, test-script error, needs-manual-review, and infrastructure — with a priority-ordered decision tree, escalation by screenshot, source lookup for script errors, the triage report format, and the client-facing bug list (deduplicated results, one bug per root cause, written in the deliverable language with evidence). Load for ALL test failure analysis and bug-list tasks."
---

# Defect Triage

> Prerequisite: `mig-project` resolved. Results under `{{profile.testing.paths.results_root}}`.

A failing suite is not a list of defects. Most failures in an automated migration suite are
**not** product defects, and reporting them as such destroys the credibility of the ones
that are.

---

## The four classes

| Class | Meaning | Goes to |
|---|---|---|
| `PRODUCT-DEFECT` | the application behaves differently from the specified behaviour | development |
| `SCRIPT-ERROR` | the test is wrong: bad locator, bad data, bad wait, bad assumption | test author |
| `NEEDS-REVIEW` | the failure is ambiguous from the log alone | a human, with evidence |
| `INFRA` | environment: service down, database unreachable, timeout under load, browser crash | environment owner |

There is a fifth outcome that is not a class: **the test is right and the specification is
wrong**. When the application matches the legacy and the case matches the design but they
disagree with each other, that is a design defect — raise it through `mig-uat-bug`, not
here.

---

## Decision tree — apply in this order

Order matters. Applied out of order, infrastructure failures get logged as product defects
and the report becomes noise.

1. **Infrastructure signature?** Connection refused, DNS, auth service unavailable, whole
   suite failing at the same step, wall-clock timeout with no page interaction → `INFRA`.
   Stop; do not analyse further, and do not report the rest of the run until it is re-run.
2. **Did the test ever reach its assertion?** Failure during setup, navigation or login →
   `SCRIPT-ERROR` or `INFRA`, never a product defect. The product was not exercised.
3. **Does the failure reproduce?** A failure that passes on re-run without any change is
   flaky → `SCRIPT-ERROR`, quarantined with a reason. Never re-run until green and report
   pass.
4. **Does the actual behaviour match the design and the legacy?** If yes, the case is
   wrong → `SCRIPT-ERROR` (or a manual case defect). If no → `PRODUCT-DEFECT`.
5. **Ambiguous** — locator not found, element not visible, timeout at an interaction:
   could be either. → `NEEDS-REVIEW`, escalate with evidence.

### Step 5 in practice

"Element not found" is the single most common ambiguous failure and it has two very
different causes: the element genuinely is not rendered (product defect), or it is
rendered under a locator the script does not match (script error). The log cannot tell
them apart. **Read the screenshot** before classifying. Where no screenshot exists, that is
a gap in the automation setup worth fixing before the next round.

---

## Evidence and source lookup

**For `NEEDS-REVIEW`:** open the captured screenshot or trace. Decide from what is on the
screen, not from the exception type.

**For `SCRIPT-ERROR`:** find the concrete fix before reporting. Read the page object, the
locator, the data file. A triage report that says "script error" without naming the line
and the fix hands the whole investigation back to the author, which is the work triage was
supposed to do.

**For `PRODUCT-DEFECT`:** anchor it. The expected behaviour must trace to the design
document and, where it is a parity question, to the legacy source. An unanchored product
defect will be disputed and will consume more time in argument than investigation.

---

## Systematic vs isolated

Before writing the report, group the failures. In a migrated system, defects arrive in
families:

- the same locator pattern failing across many screens → one script fix, not twenty
- the same rounding difference across every monetary field → one product defect, one root
  cause
- the same permission failure for one role → one authorisation defect

Reporting twenty instances of one root cause as twenty defects makes the suite look worse
than it is and the backlog unactionable. Report the root cause with its instance list.

---

## Report

```
Triage — run {id}, {date}
  Total {n}   passed {n}   failed {n}

  PRODUCT-DEFECT  {n}   → {grouped by root cause}
      {TC ID} · {module} · expected {x} · actual {y} · design {doc §} · legacy {anchor}
  SCRIPT-ERROR    {n}   → {file}:{line} — {fix}
  NEEDS-REVIEW    {n}   → {TC ID} — {what the screenshot shows} — {question}
  INFRA           {n}   → {symptom} — re-run required

  Root causes     : {n} distinct behind {n} failures
  Blocked         : {tests not run because of INFRA}
```

State the run being analysed. A triage report that does not identify its run cannot be
compared with the next one, and comparison across rounds is how you tell whether the
system is converging.

---

## The client-facing bug list

The triage report above is for the team. When a round's defects go to the client — at IT
exit, during UAT, or whenever the contract asks for a bug list — produce a separate
deliverable from the **triaged** run. Never generate it from raw results: a bug list that
contains script errors and infrastructure failures is retracted line by line, and the
retractions are what the client remembers.

**Input.** The results in `{{profile.testing.automation.results_format}}` under
`{{profile.testing.paths.results_root}}`, plus the classification above. Only
`PRODUCT-DEFECT` rows enter the list; `NEEDS-REVIEW` rows enter only after a human has
classified them.

**Deduplicate before counting.** Result formats record every attempt: retries, re-runs and
the history of earlier rounds. Collapse to one result per TC ID — the **last attempt of the
run being reported** — and say that you did. Counting attempts inflates the failure rate;
keeping the first attempt reports failures that were already fixed.

**One bug per root cause.** Group the failures by root cause (*Systematic vs isolated*); each
group gets one bug id with every affected TC ID listed under it. Distinct root causes stay
distinct bugs even when the symptom looks the same. When unsure whether two failures share a
cause, keep them apart.

**Written for the reader, in the reader's language.** The list is a deliverable: its language
is the one `{{profile.language.by_path}}` binds to its directory, and its terms come from
`{{profile.language.dictionary}}`. For every bug:

| Field | Content |
|---|---|
| Bug ID | stable across rounds — a bug found again in round 2 keeps its id |
| Summary | what the user experiences, in one sentence, no framework vocabulary |
| Screen / function | the module id and the screen or function name from the design |
| Steps | the case's steps, rewritten as a user would perform them |
| Expected | in plain words, **with the anchor** — the design item and, where it decides the behaviour, the legacy anchor |
| Actual | what happened, in plain words; the assertion error translated, not pasted |
| Affected cases | every TC ID in the group |
| Evidence | the screenshot or trace for each affected case, copied beside the list and named per `{{profile.testing.evidence.naming}}` |

A raw assertion message (`expected "保存しました" received "登録しました"`, `locator resolved
to 0 elements`) is evidence, not a description. Translate it into what the user sees, and put
the raw message in the evidence column if the reader needs it. Message texts quoted in the
list are the verbatim catalogue strings (NI-03), not translations.

**Statistics, honestly.** Executed, passed, failed and blocked per module, after the
deduplication, with the run id. Skipped tests are listed as not run, never folded into
passed.

**Format** comes from the registry entry `bug_list` in `{{profile.templates.registry}}` —
Markdown, Excel or an HTML page — written through `mig-document-io`. Evidence files are
copied, never linked to a location the client cannot open.

```
Bug list — round {n}, run {id}
  Results read   : {n} attempts → {n} TC IDs after deduplication (last attempt kept)
  Bugs           : {n} root causes covering {n} failed cases
  Excluded       : SCRIPT-ERROR {n} · INFRA {n} · NEEDS-REVIEW unresolved {n}
  Language       : {lang}   format: {md|xlsx|html}   evidence copied: {n}
  Carried over   : {n} bug ids from earlier rounds
```
