# Adoption Guide

Getting the PM Skill Pack running on a project. Budget about 30 minutes for steps 1–4; step 5
onward is the project itself.

---

## 1. Install

**New project, no existing pack:**

```bash
cp -r pm-standard/.claude              <project>/.claude
cp pm-standard/profile/pm.profile.yaml <project>/.claude/pm.profile.yaml
```

**Alongside `sdlc-standard` or `migration-standard`** — the common case. Merge rather than
overwrite:

```bash
cp -r pm-standard/.claude/skills/*   <project>/.claude/skills/
cp -r pm-standard/.claude/commands/* <project>/.claude/commands/
cp -r pm-standard/.claude/agents/*   <project>/.claude/agents/
cp -r pm-standard/.claude/rules/pm   <project>/.claude/rules/
cp -r pm-standard/.claude/hooks/*    <project>/.claude/hooks/
cp pm-standard/profile/pm.profile.yaml <project>/.claude/pm.profile.yaml
```

Then merge the `hooks` block of `settings.json` by hand: keep the technical pack's hooks and
add the three `pm_*` ones. They do not conflict — the guard hooks read different profiles and
protect different paths — but both must be listed or one silently stops running.

Names do not collide: every skill, command and agent in this pack is prefixed `pm_`, and its
rule IDs (`PB-`, `ES-`, `RI-`, `DA-`, `PN-`, `MD-`) are distinct from the technical packs'.

## 2. Configure

```
/pm_init
```

It inspects the repository first — the technical profile if one exists, existing document
directories, CI configuration, git history — and asks only about what it cannot determine.
Then it writes the profile, scaffolds `pm/`, seeds the registers, and generates or appends to
`CLAUDE.md`.

Then:

```
/pm_profile_check
```

Fix every Critical before running a planning command. A Critical means an artifact produced now
would carry a defect into everything built on it — most often an unfilled governance role, or
baseline protection switched off.

## 3. Decide the six things that are expensive to change later

### 3a. Who decides what

Fill every role in `governance`, and every entry in `governance.approvals`. A decision with no
owner cannot be recorded, and an unrecorded decision is an assumption that will be discovered
at acceptance (DA-01).

This is the field teams leave as a placeholder and then spend the project working around. It
is also the one that makes every later "who signs this?" question answerable in seconds.

### 3b. The calendar arithmetic

`calendar.hours_per_day`, `productive_hours_per_day`, `planned_absence_allowance`, and
`resource.max_planned_allocation_percent`.

These four numbers multiply into every duration in the plan. Planning at 8 productive hours and
100% allocation produces a schedule that is roughly 30% optimistic before a single dependency
is considered — and the error is invisible, because each individual activity looks reasonable.

### 3c. The WBS identity scheme

`wbs.code_format`, the level-1 branches, and the 8/80 thresholds. WBS codes are permanent and
never reused (PN-02): every report, risk, cost line and change request will cite them.

Decide the level-1 branches before decomposing anything. And keep the three branches teams
habitually omit — **project management**, **quality assurance and process**, **training and
handover** — because work that is not in the WBS is work nobody planned but everybody does.

### 3d. The reserve policy

`cost.contingency_percent` and `management_reserve_percent`, and who owns each (ES-06).
Contingency is the PM's, inside the cost baseline, drawn against identified risks with a log.
Management reserve is the sponsor's, outside it.

A fixed-price project with zero reserves has nothing behind the risks it has already
identified, and will absorb them out of margin silently.

### 3e. The quality targets

`quality.targets` ships with plausible defaults. **They are placeholders for your own
historical numbers, not industry constants.** Set them from your organisation's data, agree
them with the team and the client, then hold them.

When a technical pack is installed, these must match its `quality.targets` exactly. Two sets
means the gate verdict depends on which document someone quotes.

### 3f. The reporting cadences that are actually required

`reporting.cadences`. Delete the ones nobody will read; an unread report consumes the attention
the important message will need (SE-03).

For each one you keep, name the decision it supports. If there is no decision, there is no
report.

## 3b. Bind the deliverable formats, and install `openpyxl`

Management deliverables are contractual, so their format is a property of the artifact rather
than a per-task choice. `/pm_init` asks which artifacts the client receives as Excel, which as
Word, which as Markdown, and whether they supply their own forms — and writes the answers to
`{{profile.documents.registry}}`.

**One binding is not a question: the WBS is delivered as Excel** (MD-09). Markdown and CSV are
working forms — draft in them freely, `{{profile.documents.working_dir}}` exists for that —
but the deliverable is the `.xlsx`, and `wbs` sits in `{{profile.documents.binary_final}}`,
which makes the workbook existing the completion criterion for `/pm_wbs`.

So `openpyxl` is a prerequisite of this pack, not an optional extra:

```bash
pip install openpyxl        # required - the WBS cannot be delivered without it
pip install python-docx     # only if any artifact is bound to docx
python -c "import openpyxl; print('xlsx ok')"
```

`/pm_profile_check` fails **Critical** on a missing library, on `wbs` not being bound to
`.xlsx`, and on `paths.wbs` disagreeing with the registry entry — two paths is two WBSs, and
only one of them gets baselined.

Finally, add `{{profile.documents.working_dir}}` to `.gitignore` unless `working_retention`
is `keep`. Scratch files in version control are how a draft ends up looking like a
deliverable.

## 4. Confirm the model and effort

`/pm_init` writes `execution.agent_model` (default `opus`) into every agent file. Effort is
session-level and cannot be set from the profile — `execution.intended_effort` only records
what the project expects, so agree it with the team and set it in your own session.

`/pm_profile_check` flags drift between the profile and the agent frontmatter. Drift here is
easy to miss, because an agent on the wrong model still produces a plausible-looking plan.

---

## 5. Run the planning sequence, in order

```
/pm_charter
/pm_scope_baseline
/pm_wbs
/pm_estimate
/pm_resource_plan
/pm_schedule_baseline
/pm_cost_baseline
/pm_quality_plan
/pm_process_define
/pm_comm_plan
/pm_risk_assess
/pm_plan
```

Do not reorder it (see README, "The planning order"). Each step consumes the one before; skipping
forward produces numbers with nothing behind them.

Where an input genuinely does not exist yet — a requirement still being elicited, a rate nobody
has measured — record it as an `ASM-*` with an owner and a confirm-by date, and continue. A
baseline carrying a labelled assumption is honest; one carrying an unlabelled guess is not
(PB-08).

## 6. Then run the control loop

```
weekly : /pm_status_collect → /pm_report weekly ; /pm_risk_review
monthly: /pm_status_collect → /pm_evm → /pm_report monthly + /pm_report quality
         /pm_audit ; /pm_sync_technical
gates  : /pm_trace_check → /pm_evm → /pm_gate_review → /pm_lessons
changes: /pm_change_assess → (approval) → /pm_change_apply
```

---

## 7. Adopting mid-project

The common case, and the pack is designed for it. Do not try to reconstruct history.

1. `/pm_init`, then `/pm_profile_check`.
2. `/pm_health_check` — an honest picture of where the project actually is, from the artifacts
   rather than from the last status report.
3. Baseline **from today**: write the charter if none exists, build the WBS for the remaining
   work, and baseline the current schedule and cost as v1.0 with a note that it is a
   mid-project baseline and what it supersedes.
4. Seed the registers from what is already known — the risks everyone talks about but nobody
   wrote down, the decisions made on calls, the changes absorbed without a CR. Record the
   absorbed ones retrospectively with a single summary entry; from this point, record them
   individually (PB-07).
5. Start the control loop. The first weekly report with sourced numbers is the moment the
   project becomes measurable.

Two things not to do: do not back-date a baseline to make the current position look compliant,
and do not reconstruct estimates to match actuals. Both destroy the variance data, which is the
only thing that can explain what happened.

---

## 7b. Common format mistakes

| Mistake | Consequence |
|---|---|
| Delivering the WBS as Markdown because the content was complete | the client re-keys it into Excel, and the project has two WBSs that disagree within a week |
| Keeping `wbs.md` and `wbs.xlsx` both current | nobody can say which was approved; the baseline register points at one and the team works from the other |
| Regenerating the workbook from an old working file | whoever edited the workbook directly loses their change, silently, and the file still looks fine |
| An unstamped file in the working directory | it cannot be used as a regeneration input, because nothing says which version it came from (MD-10) |
| Installing the pack without `openpyxl` | `/pm_wbs` cannot produce its deliverable, and the failure appears at the point of writing rather than at setup |
| Typing units into cells (`1,200 h`) instead of using number formats | the column cannot be summed, and somebody will try |
| Merging cells to make the WBS hierarchy look nice | sorting, filtering and every formula that reads the column break |
| Letting Excel interpret the code column | `1.2.3` becomes a date and `1.10` becomes `1.1`; format the column as text before writing |

## 8. When a rule gets in the way

It is sometimes right to deviate — `pm_process` PR-02 exists for that. The discipline is:

1. Record the tailoring, with the reason and the risk accepted.
2. Name who approved it.
3. Say what replaces the control, if anything.

Schedule pressure is not a tailoring reason. It is a decision to accept risk, recorded with the
sponsor's name on it.

If a rule turns out to be wrong rather than inconvenient, fix the pack: `/pm_refine_skill`.
That is the difference between a standard and a ritual.
