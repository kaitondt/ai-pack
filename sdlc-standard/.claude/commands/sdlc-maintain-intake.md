---
description: "P9 phase 1 — take in a production incident: capture, triage, classify, investigate to a root cause, and propose. Read-only: no code or document edits. Usage: /sdlc-maintain-intake <the incident report>"
---

# P9 — Incident intake and investigation

**Read-only.** This command ends at a conclusion and a proposal (C1). Fixing needs an
explicit approval and runs through `/sdlc-maintain-fix`.

## Step 1 — Load

`sdlc-project`, then `sdlc-maintenance`.

## Step 2 — Capture and start the clock

What the user did, what happened, what they expected, when, which environment, which user,
which record. Record the arrival time — `{{profile.maintenance.sla}}` is measured from it,
and a clock started late is a clock that will be argued about.

## Step 3 — Triage immediately

Severity from `{{profile.quality.severity}}`, class from
`{{profile.maintenance.classes}}`. Tell the reporter both, and what happens next.

**Is it happening now?** An ongoing production issue is stabilised first — workaround,
restart, toggle — and investigated second. Say clearly which of the two you are doing; the
two have different urgencies and get confused under pressure.

## Step 4 — Check the knowledge base first

`{{profile.maintenance.knowledge_base}}`. A recurring incident already investigated does not
need investigating again; it needs its preventive action finished, and the fact that it
recurred is itself the finding.

## Step 5 — Investigate

Via the locator map in the skill:

1. the source for the behaviour involved
2. the design documents for the module
3. the baselined requirement
4. operational evidence: logs at that timestamp, correlation id, batch run record,
   monitoring signals, what was deployed and when

Every conclusion is anchored (C2). Where all three specification sources are silent, the
class is `REQ-GAP` — ask, do not decide.

## Step 6 — Conclude and stop

```
{INC-ID or "unassigned"} — {short title}
  Arrived        : {timestamp}   acknowledged {timestamp}   SLA {target}
  Severity/class : {S?} / {INC-?}
  Now            : {ongoing | resolved by workaround | historical}
  Symptom        : {restated}
  Root cause     : {direct cause, with anchors}
  Injection phase: {P1..P4}
  Ruled out      : {what else was considered, and why not}
  Route          : {hotfix | scheduled release | data script | other team | client decision}
  Proposal       : {what to change}
  Risk           : {of doing it, and of not}
  KB hit         : {prior incident id, or "none"}
```

Then stop, and ask for approval to proceed to the fix.

For `INC-EXTERNAL`, stop with the evidence assembled for the other system's owner — logs,
timestamps, request and response — rather than a conclusion they have to re-derive.
