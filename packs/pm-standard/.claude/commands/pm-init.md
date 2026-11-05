---
description: "Set up the PM Skill Pack on a project: inspect the repository, detect an installed technical pack, interview for what cannot be inferred, write pm.profile.yaml, scaffold the pm/ tree and the registers, and generate CLAUDE.md. Usage: /pm-init"
---

# Initialise the PM pack

## Step 1 — Inspect before asking

Determine from the repository, without asking:

| Signal | Tells you |
|---|---|
| `.claude/sdlc.profile.yaml` | technical pack `sdlc` — read its phases, gates, quality targets, paths |
| `.claude/migration.profile.yaml` | technical pack `migration` — same |
| existing `pm/`, `docs/`, charter or plan files | artifacts that already exist; never overwrite them |
| git history and contributors | team size and shape, roughly |
| CI config | build and test commands, environments |
| README / CLAUDE.md | project name, purpose, stack |

Report what you found **before** asking anything. An interview that asks what is already on
disk wastes the user's attention and makes the rest of their answers less careful.

## Step 2 — Interview for what cannot be inferred

Only these, asked in one batch:

1. **Governance** — sponsor, client PM, project manager, technical lead, QA lead, delivery
   manager. Every role. An unfilled role means decisions with no owner (DA-01), and
   `/pm-profile-check` fails Critical on it.
2. **Contract and delivery** — contract type, delivery model, engagement model, currency,
   start and planned end dates, release cadence.
3. **Scope outline** — the capabilities in scope, and the notable exclusions with reasons.
4. **Calendar** — working days, holidays per location, hours per day, time zones.
5. **Reporting** — which cadences are actually required, to whom, in which language.
6. **Quality targets** — accept the defaults, or supply the organisation's own history.
7. **Estimating rates** — measured rates if they exist; otherwise mark them unverified (ES-08).
8. **Deliverable formats** — which artifacts the client receives as Excel, which as Word,
   which as Markdown, and whether they supply their own forms for any of them. Ask
   explicitly: format is the thing that is cheap to decide now and expensive to discover
   after forty documents exist.

   The WBS is not part of that question. It is Excel
   (`{{profile.documents.binary_final}}`, MD-09); what is worth asking is whether the client
   has a WBS form of their own to write into.

## Step 3 — Write the profile

Copy `pm.profile.yaml` to `.claude/pm.profile.yaml` and fill every field you can. Leave
`<...>` only where the user genuinely could not answer, and list those in the report so they
stay visible rather than being forgotten.

Set `integration.technical_pack` and `integration.technical_profile_path` from step 1. When a
technical pack exists, **inherit** its quality targets rather than inventing a second set
(QP-02), and record the milestone/gate mapping if the milestones are known.

## Step 4 — Scaffold

Create, from `{{profile.paths}}`:

```
pm/01.charter  pm/02.plan  pm/03.scope  pm/04.schedule  pm/05.cost  pm/06.quality
pm/07.process  pm/08.resource  pm/09.meetings  pm/10.registers  pm/11.changes
pm/12.reports/{daily,weekly,monthly,quarterly,quality,_data}  pm/13.closing/archive
```

The numeric prefixes put the tree in PMBOK order — initiating (charter), planning (plan,
scope, schedule, cost, quality, process, resource, communications, risk), monitoring and
controlling (changes, reports), closing — instead of alphabetical. Keep them when a
profile renames a directory; `pm/_working` stays unnumbered because it is scratch, not a
deliverable area.

Seed each register with its header row, so the first entry has a shape to follow: risk
register, issue log, decision log, assumption log, action log, change register, CAPA log,
contingency drawdown log.

## Step 5 — Bind the deliverable formats and check the toolchain

Fill `{{profile.documents.registry}}` from the interview: one entry per artifact, with its
final `format`, the `working` forms allowed while drafting, and the client's own `template`
where they supplied one.

Then verify the toolchain for every format in `{{profile.documents.formats_enabled}}`:
`openpyxl` for `xlsx`, `python-docx` for `docx`. **`openpyxl` is not optional on this pack**
— the WBS cannot be delivered without it. A missing library is reported now, not discovered
by `/pm-wbs` at the point of writing the workbook.

```bash
python -c "import openpyxl; print('xlsx ok')"
python -c "import docx;     print('docx ok')"
```

Create `{{profile.documents.working_dir}}` and add it to the project's `.gitignore` unless
`working_retention` is `keep` — scratch files in version control are how a draft ends up
looking like a deliverable.

## Step 6 — Choose the commit message format

`/pm-commit` and the `guard-pm-git` hook hold every commit to one format, and this is where the
project chooses it. Ask it as its own question — not folded into the earlier round — because the
answer is visible in every commit from now on and is awkward to change later.

1. **Read the history first.** `git log -50 --format=%s` (skip merges). If most subjects follow
   one convention — a ticket key first, Conventional Commits, a bracketed id — name it and show
   three real subjects. A team that already has a convention keeps it unless it says otherwise.
   Look for a commit-message tool too (`commitlint.config.*`, `.husky/commit-msg`,
   `.pre-commit-config.yaml` with a `commit-msg` stage, `.git/hooks/commit-msg`): it will run
   beside the pack's hook, and the two must agree.
2. **Offer the presets**, each with an example built from this project's own ids:

   | Preset | Format | Example |
   |---|---|---|
   | `id-action-summary` (default) | `{ID} {ACTION} {SUMMARY}` | `RSK-014 UPDATE raise the exposure after the vendor slip` |
   | `bracketed` | `[{ID}] {ACTION}: {SUMMARY}` | `[RSK-014] UPDATE: raise the exposure after the vendor slip` |
   | `conventional` | `{ACTION}({ID}): {SUMMARY}`, actions `feat`/`fix`/`docs`/`test`/`refactor`/`perf`/`build`/`ci`/`chore`/`revert` | `fix(ISS-009): correct the owner of the issue` |
   | `existing` | the convention found in step 1 — only when one was found | three real subjects |
   | `custom` | the user's own string, from the tokens `{ID}`, `{ACTION}`, `{SUMMARY}` | — |

   `{ID}` is the id of what the change is about (`CR-*`, `RSK-*`, `ISS-*`, `DEC-*`, `ACT-*`, `MTG-*`, a document id); `{ACTION}` is what the commit does
   to it; `{SUMMARY}` is a short imperative description. Recommend `existing` when step 1 found
   a consistent convention, otherwise the default.
3. **Settle the details in the same round**, with the defaults pre-filled:
   - the action vocabulary — default `ADD`, `UPDATE`, `DELETE`, `FIX`, `REVIEW`, `CONFIRM`,
     `REFACTOR`, `REVERT`; the team may rename, add or remove words (keep them one word each);
   - the summary language (`commit.summary_language`) and maximum length (72);
   - a token for housekeeping commits with no id (`commit.no_id`, e.g. `NOID`), or none —
     then every commit needs a real id;
   - protected branches that never take a direct commit (propose the default branch when the
     team merges through pull requests);
   - whether the AI may push (default no) or amend an unpushed commit (default no).
4. **Validate before writing.** A custom format contains `{SUMMARY}`, and `{ID}` unless
   `no_id` is set; it uses no token other than the three. Build the pattern the hook will apply
   and test it on the example and on the last ten subjects from `git log`: say how many would
   pass. Old history is not rewritten — the format applies from the next commit.
5. **Write `commit:`** in the profile — `preset`, `format`, `actions` and the switches — and
   record the choice as a `DEC-*` in `{{profile.paths.decision_log}}`. When a technical pack is installed, offer its format — one repository, one convention. When an existing commit-message tool disagrees with the chosen
   format, say so: align the tool's configuration or the profile, so one commit cannot pass one
   and fail the other.

## Step 7 — Apply the model policy

<!-- model-policy:claude -->
Resolve a model and an effort level for every `.claude/agents/pm-*.md` from
`{{profile.execution.model_profile}}`:

| `model_profile` | heavy tier | standard tier |
|---|---|---|
| `quality` | opus · `xhigh` | opus · `high` |
| `balanced` | opus · `high` | sonnet · `medium` |
| `budget` | sonnet · `high` | sonnet · `medium` |

- **heavy** — `pm-planner`, `pm-estimator`, `pm-risk-manager`, `pm-change-analyst`
- **standard** — `pm-controller`, `pm-quality-manager`, `pm-closer`

An entry in `{{profile.execution.agent_model_overrides}}` or
`{{profile.execution.agent_effort_overrides}}` wins over the table for that agent. A profile
that still sets the deprecated `execution.agent_model` and no `model_profile` reads `opus` as
`quality` and `sonnet` as `budget`; offer to replace the field.

Set each agent's `model:` and `effort:` frontmatter to the resolved values. The pack ships the
`balanced` values, so a `balanced` profile with no overrides changes no file — say so instead of
rewriting them.

Then tell the user that `{{profile.execution.intended_effort}}` is for their own session,
where the commands run: Claude Code takes the session level from `/effort`, not from the
profile, so they set it there. Agents are not affected by it.
<!-- /model-policy:claude -->

## Step 8 — Generate CLAUDE.md

From the pack's `CLAUDE.md` template, with profile values resolved. If the project already
has one — likely, when a technical pack is installed — **append** a project-management
section rather than overwriting it.

## Step 9 — Report

```
PM pack initialised
  Profile        : .claude/pm.profile.yaml
  Agent model    : {{profile.execution.model_profile}} — {n} opus · {n} sonnet · {n} overridden
  Effort         : agents {n} xhigh · {n} high · {n} medium; session {{profile.execution.intended_effort}} — set with /effort
  Technical pack : {sdlc | migration | none} ({path})
  Scaffolded     : {n} directories, {n} registers
  Formats        : {n} artifacts bound   binary_final: {list}
  Toolchain      : openpyxl {ok|MISSING — the WBS cannot be delivered} · python-docx {ok|n/a}
  Commit         : {format}   e.g. {example}   push: {AI|user}   protected: {branches}
  CLAUDE.md      : {created | appended}
  Unfilled       : {fields still <...>} — each blocks the artifact that needs it
  Next           : /pm-profile-check, then /pm-charter
```
