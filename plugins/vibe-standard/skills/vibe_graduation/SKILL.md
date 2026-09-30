---
name: vibe_graduation
description: "Stage promotion — check the criteria for moving spike → prototype → mvp → production, record the decision, tighten the rules; and the handoff to sdlc-standard and/or pm-standard when a project outgrows vibe coding, mapping INT/DEC/DEBT/BUG/IDEA onto their records. Use for 'are we ready to launch', 'promote to mvp', 'we have real users now', 'this needs a proper process', and when adopting a sibling pack."
---

# Graduate — Tightening as It Starts to Matter

> Vibe coding is right for a project until the cost of being wrong exceeds the cost of
> process. Graduation is how the pack tracks that crossing honestly: explicit criteria per
> stage, a recorded decision, and — when the project needs a real specification, contracts,
> or a team — a clean handoff to the sibling packs instead of a slow drift into chaos.

Load `vibe_project`.

---

## GR-01 — Promotion criteria

`/vibe_graduate <target>` checks every row for the target, plus
`{{profile.graduation.extra_criteria.<target>}}`. All must pass.

### → prototype (from spike)

- [ ] The spike's question is answered and written down (a `DEC-*` or PRODUCT.md)
- [ ] PRODUCT.md exists with problem, users, core flows, non-goals
- [ ] Scaffold per `vibe_scaffolding` SF-02 on the main branch
- [ ] **Spike code is not merged as-is.** Anything reused enters through normal slices, re-read
      and with intents (spike code is evidence, not foundation)

### → mvp

- [ ] Every core flow has an `INT-*` in status `done`, with its done-when checks passing now
- [ ] Every core-flow done-when check is **automated** and green (VT-08)
- [ ] CI runs typecheck, lint, tests and build on every push (SF-03)
- [ ] `/vibe_security_check` passes the SB-07 `mvp` column; no Critical/High open
- [ ] No open `DEBT-*` due ≤ `mvp` (DL-04), security debts included
- [ ] Real-data readiness: backups configured and a restore tried; personal fields justified
- [ ] Rollback path written and possible (SH-02 #5)
- [ ] Codebase review (RV-04) done; its Critical/High fixed

### → production

- [ ] Everything for `mvp`, still true today
- [ ] E2E smoke of every core flow automated, run against a production-like environment
- [ ] Error tracking + uptime alerting reach a human who will act
- [ ] Rollback rehearsed at least once
- [ ] No open `DEBT-*` due ≤ `production`
- [ ] Dependency audit clean or every finding decided
- [ ] STATE.md "Broken" contains nothing on a core flow
- [ ] A decision on `{{profile.graduation.handoff_to}}` (GR-03)

## GR-02 — Recording a promotion

1. Run the checks; report each row pass/fail with evidence.
2. Any fail → promotion refused; the report is the to-do list. The owner may override a
   non-security row with a `DEC-*`; they cannot override SB-08 or a failing core-flow check.
3. Pass → append `DEC-*`: "Stage → mvp", date, evidence summary, by the owner.
4. Change `stage:` in the profile (this is the only legitimate way it changes).
5. STATE.md "Stage" updated with the new stage and the criteria for the next one.
6. Announce what changed: which rules are now in force that were not.

**Honest demotion:** if a criterion stops holding (CI turned off, core flow broken for a week),
say so in STATE.md. Do not silently keep the stage label.

**Reality overrides the label:** real users on a "prototype" → report that the project is
operating at `mvp` risk without `mvp` controls, and list the gaps. That report is the most
useful thing the pack can produce at that moment.

## GR-03 — Outgrowing the pack

Signals that vibe coding is no longer the right process:

| Signal | Adopt |
|---|---|
| Someone other than the owner must **approve** what gets built; a contract or SLA exists | `sdlc-standard` (requirements, baselines, change requests) |
| Regulatory / audit requirement for traceability or documented design | `sdlc-standard` |
| Commitments on cost, dates or scope to a client or sponsor; status reports expected | `pm-standard` |
| Team beyond ~5 people, or more than one team | both |
| Defects escaping to users faster than slices ship | `sdlc-standard` test levels |

Staying is also valid: many products live happily at `production` under this pack. Record the
choice as a `DEC-*`.

## GR-04 — Handoff to sdlc-standard

The sibling pack's rules still apply in full — in particular, **code is not a specification**
(`sdlc-standard` RS-01). The vibe records seed it; they do not bypass it.

| Vibe record | Becomes, in sdlc-standard | Note |
|---|---|---|
| PRODUCT.md problem / users / non-goals | P0 scope statement, stakeholders, `BR-*`, out-of-scope with reasons | owner confirms each `BR-*` |
| Core flows | `BR-*` + use cases | |
| `INT-*` + done-when checks | `REQ-*` + acceptance criteria, citing `INT-*` as origin | **retro-specified**: each is an `ASM-*` until the product owner confirms it |
| `DEC-*` | `DEC-*` — the log carries over, numbering continues | same format (ID-04) |
| `DEBT-*` open | CR backlog / tech-debt items; security ones as defects | |
| `BUG-*` open | defect register, with injection phase `P4` unless evidenced otherwise | |
| `IDEA-*` | CR backlog — out of scope until approved | |
| Existing code | the P4 baseline; P3 detail design produced **with a drift report**, not by describing the code as correct | |
| Automated checks | P5–P7 cases, re-checked against the confirmed `REQ-*` | |

Run: `/sdlc_init` (it detects the existing repo), then `/sdlc_discover` seeded with PRODUCT.md
and the intents. Keep `vibe/` read-only afterwards as history; do not maintain two sets of
records.

## GR-05 — Handoff to pm-standard

| Vibe record | Becomes, in pm-standard |
|---|---|
| PRODUCT.md | charter input: objectives, scope outline, constraints |
| Intents (done + planned) | scope statement; WBS work packages for the planned ones |
| Slice history (git + intent Logs) | the only honest productivity data the project has — basis for estimates (ES-01), not a target |
| `DEC-*` | decision log (append-only, same format) |
| `DEBT-*`, open `BUG-*` | risk register entries with owners |
| STATE.md "Broken" / open questions | issue log |

`pm-standard` can run with `technical_pack: none` alongside this pack while engineering stays
vibe-coded — the PM pack manages commitments; this one keeps the code honest.

## Self-check

- [ ] Every criterion reported with evidence, not assertion
- [ ] Promotion recorded as a `DEC-*`; profile stage changed only after it
- [ ] Reality checked against the label (public URL, real users)
- [ ] On handoff: retro-specified requirements marked as assumptions until confirmed
