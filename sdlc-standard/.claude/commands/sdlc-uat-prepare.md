---
description: "P8 — prepare user acceptance testing: entry criteria check, UAT plan, environment and data readiness, scenario set from the acceptance criteria, and the written disclosure of known limitations. Usage: /sdlc-uat-prepare [scope]"
---

# P8 — Prepare UAT

## Step 1 — Load

`sdlc-project`, then `sdlc-test-uat`.

## Step 2 — Entry criteria

Check E1..E6 from the skill and print the result per criterion. A waived criterion is
recorded with who waived it and what risk was accepted.

**E6 is not negotiable**: known limitations and deferred defects are disclosed to the client
in writing, before UAT starts. A deferred defect the client discovers themselves costs more
trust than the defect costs effort.

## Step 3 — Environment and data readiness

| Check | Evidence |
|---|---|
| UAT deployed from the ST-verified build | build id matches the ST results |
| Client accounts exist, with the right roles | a client tester has logged in |
| Test data prepared and reachable | the client confirms, not the vendor |
| External interfaces pointed at their UAT counterparts | a real message exchanged |
| Reset procedure exists | how the client restarts a scenario after a mistake |

Data preparation is the most common start-day delay. Confirm it a week out, not the
morning of.

## Step 4 — Build the UAT plan

Per the skill's §-list, written in the client's language and vocabulary. Scenarios come
from the SRS acceptance criteria (T-07), rewritten as the client's own work — not copied
from the ST scenarios.

## Step 5 — Agree the working model

Before day one, in writing: the reporting channel and template, the severity definitions,
`{{profile.testing.uat.defect_sla_hours}}`, the deployment cadence (UA-03), and who decides
severity — the client.

## Step 6 — Report

```
P8 — UAT preparation
  Entry criteria    : {each, pass/waived/fail}
  Environment       : deployed build {id} · accounts {ok} · data {ok} · interfaces {ok}
  Plan              : {path}   signed: {yes|no}
  Scenarios         : {n}   covering {n}/{n} acceptance criteria
  Disclosed         : {n} known limitations, {n} deferred defects — sent {date}
  Working model     : channel {x} · SLA {y} · deploy cadence {z}
```

Do not start UAT with an unmet entry criterion and an unrecorded waiver. The phase will
still run; the argument about whose fault it was arrives later.
