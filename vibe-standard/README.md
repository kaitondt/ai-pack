# Vibe Skill Pack (VSP) — Standard Edition

A **project-agnostic Claude Code skill pack for vibe coding** — building software by steering
an AI with intent, accepting most of the code it writes, and judging the result by running it.

The fourth sibling of [`sdlc-standard`](../sdlc-standard/README.md),
[`pm-standard`](../pm-standard/README.md) and
[`migration-standard`](../migration-standard/README.md). Same architecture — one profile file,
invariant rules, skills, entry-point commands, delegated agents, guard hooks — built from the
parts of `sdlc-standard` and `pm-standard` that survive at vibe speed, plus rules for the ways
AI-written code specifically goes wrong.

> `sdlc-standard` manages the **product** through specifications and phases.
> `pm-standard` manages the **project** through baselines and commitments.
> This pack manages the **loop** — intent → slice → run → verify → commit — so that speed
> produces software instead of a pile of plausible code nobody understands.

---

## The core idea

```
┌──────────────────────────────────────────────────────────────────┐
│  vibe.profile.yaml     ← the ONLY file you edit per project      │
│  (stage, stack, real commands, slice budget, security, release)  │
└───────────────────────────┬──────────────────────────────────────┘
                            │ resolved by  skill: vibe_project
                            ▼
┌──────────────────────────────────────────────────────────────────┐
│  rules/vibe/ — 7 invariant rule families, scaled by stage        │
│  skills/     — 13 skills, loaded on demand                       │
│  commands/   — 20 entry points the human types                   │
│  agents/     — 6 delegated workers with narrow tool sets         │
│  hooks/      — 4 guards: secrets, irreversible commands,         │
│                slice size, session handoff                       │
└──────────────────────────────────────────────────────────────────┘
                            │ writes the project's memory into
                            ▼
┌──────────────────────────────────────────────────────────────────┐
│  vibe/  PRODUCT.md · STATE.md · intents/ · decisions · debt ·    │
│         bugs · backlog · reviews/ · releases/                    │
└──────────────────────────────────────────────────────────────────┘
```

---

## What is different from the sibling packs

A migration project has an oracle: the old system. A development project has an approved
specification. A managed project has its baselines. **A vibe-coded project has none of them** —
only what the human meant, and the software that is running. The AI will fill the gap between
the two with something plausible. Every rule in this pack keeps that gap small, cheaply.

| Sibling invariant | Vibe counterpart | Taken from |
|---|---|---|
| Nothing is specified without a source (RS-01) | **Intent first** — every slice starts from an `INT-*` with observable done-when checks; a one-page PRODUCT.md instead of an SRS | `sdlc` RS-01, `pm` charter/scope |
| Undecided requirements stop the design (RS-04) | **Ambiguity stops the part that depends on it** — ask one question; never build both branches | `sdlc` RS-04 |
| Nothing enters scope without a requirement / CR (RS-06, PB-07) | **Park, don't build** — every extra becomes an `IDEA-*`, including the AI's own suggestions | `sdlc` RS-06, `pm` PB-07 |
| WBS work packages, 8/80 sizing | **Small vertical slices with a hard budget**, one commit each | `pm` WBS |
| Estimate with method, basis, range; never back-fit (ES-01/02) | Range + basis from slice history; cut options instead of a smaller number | `pm` ES-01, ES-02 |
| Expected values from the specification, never the code | **Expected values from the intent**; checks never bent to go green | `sdlc` common/testing |
| Decisions recorded when made; append-only log (DA-03) | `DEC-*` log, same format — carries over on graduation | `pm` DA-03 |
| Risk register with owner and response | **Debt ledger** — every shortcut a `DEBT-*` with a due stage | `pm` risk |
| Phase gates / V-model | **Stage model** — spike → prototype → mvp → production, rules tighten per stage, promotion by evidence | `sdlc` gates |
| Report honestly; evidence-based status (RI-02) | **Seen running, or not done**; status computed from files and git | all packs |
| Refine loop (`/…_refine_skill`) | same loop, triggered by the second repeat of a finding | all packs |
| — | **Doom-loop limit** — 3 failed attempts, then preserve, revert, change approach | vibe-specific |
| — | **No phantom packages or APIs** — verify against the installed version | vibe-specific |
| — | **Irreversible commands are run by the human** — enforced by hook | vibe-specific |
| — | **Session continuity** — STATE.md handoff, because every session starts blank | vibe-specific |

What was deliberately **not** taken: document skeletons, revision histories, deliverable
templates, ID patterns per module, test levels as separate phases, baselines and CR approvals,
EVM, reporting cadences. They are right for their packs and wrong at this speed — and when a
project starts needing them, `/vibe_graduate` hands it over (see below).

---

## The load-bearing rules

| # | Rule | Where |
|---|---|---|
| 1 | **Every slice starts from a written intent** with observable done-when checks | `rules/vibe/intent-first.md` IF-01, IF-02 |
| 2 | **Nothing outside the intent gets built** — park it as `IDEA-*` | IF-03 |
| 3 | **Ambiguity stops the dependent part** — ask, don't guess, don't build both | IF-04 |
| 4 | **Decisions are recorded when made**; the log is append-only | IF-05, SC-03 |
| 5 | **Vertical slices, one commit each, within a size budget** — enforced by hook | `rules/vibe/small-slices.md` SS-01, SS-02 |
| 6 | **Start from a clean checkpoint; map the files first** | SS-03, SS-04 |
| 7 | **Three failed attempts → stop, preserve, revert, change approach** | SS-05, SS-06 |
| 8 | **Seen running, or not done** — reported exactly as it happened | `rules/vibe/verify-before-trust.md` VT-01, VT-06 |
| 9 | **No phantom packages or APIs** | VT-03 |
| 10 | **Expected values from the intent; checks never bent to go green** | VT-04, VT-05 |
| 11 | **No secrets in files, prompts, logs or bundles** — enforced by hook | `rules/vibe/security-baseline.md` SB-01 |
| 12 | **Irreversible commands are run by the human** — enforced by hook | SB-02 |
| 13 | **The server decides**: validation and per-resource authorisation server-side | SB-03 |
| 14 | **A public URL means mvp security**, whatever the stage says | SB-07 |
| 15 | **Every shortcut is a `DEBT-*` with a due stage**; security debt due by mvp | `rules/vibe/debt-ledger.md` DL-01, SB-08 |
| 16 | **STATE.md is the handoff**; the conversation is not memory | `rules/vibe/session-continuity.md` SC-01, SC-04 |
| 17 | **The stage changes only through `/vibe_graduate`**, on evidence | `skills/vibe_graduate` GR-02 |

## What is variable (lives in the profile)

Stage · stack · the real dev/test/build commands · slice budget and doom-loop limit ·
verification additions per stage and how the UI is checked · secret store, env files,
extra dangerous commands, protected paths · debt paydown cadence · deploy, rollback,
monitoring and backups · extra graduation criteria · where the project goes after production.

---

## The stage model, which is the spine of the pack

```
  spike ──────► prototype ──────► mvp ──────► production ──────► (graduate: sdlc / pm / stay)
  answer a      show it to        real users   people depend on
  question      someone           use it       it
```

| | spike | prototype | mvp | production |
|---|---|---|---|---|
| Intent | one line + assumptions | full `INT-*` | full `INT-*` | full `INT-*` |
| Verification | done-when run | + diff summary, build/lint/typecheck | + core flows automated, CI, independent review | + E2E smoke before release |
| Security | secrets, destructive ops, synthetic data | + server authz if public | full baseline, audit in CI | + check every release |
| Debt ledger | — | required | + paydown cadence | nothing overdue |
| Branch | `spike/*`, never merged | `main` | `main` (+ PR for teams) | `main` + PR + CI green |

Two rules hold the model honest:

1. **Reality overrides the label upward.** A prototype with a public URL gets mvp security; a
   prototype with real users is an mvp. The internet does not read the profile.
2. **Spike code is evidence, not foundation.** What a spike learned goes into intents and
   decisions; its code reaches `main` only through normal slices.

## The vibe loop

```
  INTENT ─► SLICE ─► CHECKPOINT ─► BUILD ─► RUN ─► VERIFY ─► REVIEW ─► COMMIT ─► LOG
    ▲                    ▲                             │ ✗ ×3
    │                    └──── revert, re-slice ◄──────┘ (/vibe_unstuck → /vibe_fix)
    └──────────────────────────── next slice ◄──────────────────────────────────────┘
```

**How the commands chain, and the stage-by-stage flows: [COMMAND-FLOW.md](COMMAND-FLOW.md).**

---

## Commands

| Area | Commands |
|---|---|
| Setup | `/vibe_init` · `/vibe_profile_check` · `/vibe_scaffold` |
| What to build | `/vibe_product` · `/vibe_intent` · `/vibe_plan` · `/vibe_park` |
| Build | `/vibe_build` · `/vibe_verify` · `/vibe_review` |
| When it breaks | `/vibe_fix` · `/vibe_unstuck` |
| Keep it healthy | `/vibe_debt` · `/vibe_security_check` · `/vibe_refine_skill` |
| Ship and grow | `/vibe_ship` · `/vibe_graduate` |
| Sessions | `/vibe_resume` · `/vibe_handoff` · `/vibe_status` |

## Agents

| Agent | Tools | Does |
|---|---|---|
| `vibe_planner` | read-only + Bash | slices an intent; never writes code |
| `vibe_builder` | read/write | builds one slice; stops at its edges |
| `vibe_verifier` | read-only + Bash | proves it works; never edits source |
| `vibe_reviewer` | read-only + Bash | reviews what another context wrote |
| `vibe_debugger` | read/write | evidence before fix |
| `vibe_security_auditor` | read-only + Bash | the six holes, the endpoint table, SB-07 |

The split is the point: from `mvp`, **the context that wrote the code is not the one that
verifies or reviews it**. A writer reviewing its own output agrees with itself.

## Hooks

| Hook | Event | Enforces |
|---|---|---|
| `check_vibe_profile.py` | SessionStart | profile valid; stage vs. reality; `.env` ignored; tree/branch state; open debt & bugs; **prints STATE.md** so the session starts from the handoff |
| `guard_vibe_bash.py` | PreToolUse (Bash, PowerShell) | **blocks** irreversible commands: `rm -rf` of root/home/cwd, `git reset --hard`, `git clean -f`, force-push, `DROP`/`TRUNCATE`/unscoped `DELETE`, ORM resets, `terraform apply/destroy`, publish, `sudo`, `curl | sh`, plus `security.dangerous_commands` |
| `guard_vibe_paths.py` | PreToolUse (Write, Edit) | **blocks** writes containing credentials (AWS, GitHub, Anthropic, OpenAI, Stripe, Slack, Google, private keys, DB URLs with passwords, random-looking hardcoded secrets) outside gitignored env files; blocks `security.protected_paths` |
| `check_slice_size.py` | PostToolUse (Write, Edit) | warns the model when the working tree passes the slice budget, and again at 2× |

---

## Layout

```
vibe-standard/
├── README.md                      ← this file
├── ADOPTION.md                    ← 20-minute onboarding, new or existing repo
├── COMMAND-FLOW.md                ← how the commands chain; flows per stage; refine loop
├── profile/
│   ├── vibe.profile.yaml          ← template to copy
│   ├── PROFILE-SCHEMA.md          ← field-by-field spec
│   └── examples/
│       ├── weekend-prototype.profile.yaml   ← solo, Next.js, prototype
│       └── startup-mvp.profile.yaml         ← 3 people, FastAPI + React, mvp, public
└── .claude/
    ├── CLAUDE.md                  ← project-instruction template
    ├── settings.json
    ├── hooks/                     ← 4 hooks
    ├── rules/vibe/                ← 7 invariant rule files
    ├── skills/                    ← 13 skills
    ├── commands/                  ← 20 slash commands
    └── agents/                    ← 6 agents
```

---

## Growing out of it

Vibe coding is right for a project until the cost of being wrong exceeds the cost of process.
`/vibe_graduate handoff` recognises the crossing and maps every vibe record onto the sibling
packs instead of letting the project drift:

| Signal | Adopt |
|---|---|
| Someone other than the owner approves what gets built; a contract or SLA exists; audit needs traceability | `sdlc-standard` |
| Commitments on cost, dates or scope to a client, sponsor or investor | `pm-standard` (can run alongside this pack, `technical_pack: none`) |
| More than ~5 people, or more than one team | both |

On handoff to `sdlc-standard`, intents become requirements **marked as assumptions until the
product owner confirms them** — the sibling pack's rule that code is not a specification still
holds. `DEC-*` carries over unchanged. Details: `skills/vibe_graduate` GR-04, GR-05.

Staying is also a valid answer. Many products live happily at `production` under this pack.

---

## Model policy

Every `vibe_*` agent ships with `model: opus`, set from `execution.agent_model`.

Vibe coding delegates more judgement to the model than either sibling pack does — there is no
specification to check against, only an intent and the model's reading of it. The failures are
silent and plausible: an ownership check missing from one endpoint, an API from the wrong major
version, a test that asserts what the code does, a slice that quietly grew a feature. The
cheapest place to buy correctness is the model doing the work.

Downgrade a role via `execution.agent_model_overrides` when it is genuinely mechanical
(`vibe_verifier` running a fixed command list is the usual candidate). Do not downgrade
`vibe_reviewer` or `vibe_security_auditor` — they exist to catch what the builder missed.

Reasoning effort is a session-level setting in Claude Code; `execution.intended_effort` records
it for consistency, and does not enforce it.

---

## Quick start

```bash
cp -r vibe-standard/.claude                 <your-project>/.claude     # or merge, see ADOPTION.md
cp vibe-standard/profile/vibe.profile.yaml  <your-project>/.claude/vibe.profile.yaml
# then, inside the project:
/vibe_init
/vibe_intent "the first thing it should do"
/vibe_plan INT-001
/vibe_build INT-001.1
```

Needs Python 3 for the hooks — without it the secret and destructive-command guards are **off
without saying so**. [ADOPTION.md](ADOPTION.md) covers installation, adopting the pack on an
existing vibe-coded repo, and troubleshooting.

---

## Which pack do I want?

| Situation | Pack |
|---|---|
| Building fast with AI — prototype, side project, MVP, internal tool | **`vibe-standard`** |
| Building something with a client, a contract, or an approved specification | `sdlc-standard` |
| Rewriting or replatforming an existing system | `migration-standard` |
| Planning, costing, reporting and governing the project | `pm-standard`, alongside any of them |
| A vibe-coded product that now has contracts or a growing team | `vibe-standard` → `/vibe_graduate handoff` |
