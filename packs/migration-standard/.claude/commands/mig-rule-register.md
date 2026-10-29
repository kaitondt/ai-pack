---
description: "Add, inspect or validate the project's own rules — conventions the team or client imposes on the target code and deliverables on top of the pack's rules (naming, layering, security, document or process rules, a house style). Writes .claude/rules/project/<topic>.md and registers it in the profile. Run at init, and whenever the project decides a new rule. Usage: /mig-rule-register [topic | file path | --list | --check]"
model: sonnet
effort: medium
---

# Register a project rule

The pack's rules are the baseline for every migration. This command is how a project adds its
own, without editing the pack's files — which the next plugin update or re-init may replace.

A project rule is a file under `.claude/rules/project/`. The pack never writes there, so it
survives updates. Claude Code loads it by itself (with the files its `paths:` governs, or
always when it has none); the registration in the profile is what gives it a place in the
order of authority and lets the reviewer cite it.

Project rules govern the **target** code and the deliverables. A scope that matches
`{{profile.legacy.root}}` is refused: the legacy tree is read-only and no rule applies to it.

## Step 1 — Load

`mig-project`. Read `.claude/migration.profile.yaml` for `project_rules` and
`target.coding_standards`.

## Step 2 — Decide the mode from the argument

| Argument | Mode |
|---|---|
| nothing, or `--list` | **inventory** — pack rules in force, client standards, project rules; then offer to add one |
| `--check` | **validate only** — no file or profile changes |
| a topic (`naming`, `error-handling`, `commit-messages`, ...) | **add one** — interview for that topic |
| a file path | **digest a document** — the team's wiki page, ADR or style guide becomes the rule file |

A client's *coding standard* (the document the client supplies per stack) is not a project
rule: it goes through `/mig-init` Step 6 into `target.coding_standards` and outranks this
command's output. If the document the user names is that, say so and route them there.

## Step 3 — Inventory

| Layer | Source | Files | Overridable by a project rule |
|---|---|---|---|
| Invariants | legacy parity, `.claude/rules/migration/*`, the non-negotiables in `rules/common/security.md` | {n} | **no** — a project rule may tighten them, never relax them |
| Client coding standard | `target.coding_standards[]` | {n} | n/a — it outranks project rules |
| Project rules | `project_rules[]` | {n} | — |
| Pack stack and common rules | `rules/java|typescript|react|sql`, `rules/common/*` | {n} | **yes**, with the override recorded |

Then list each project rule: id, file, scope, kind, status, enforced by.

## Step 4 — Interview (add mode)

Ask once, as one grouped round. Do not ask for what the user's document already says.

1. **The rule** — in one imperative sentence. A rule that cannot be checked by looking at a
   diff or a document ("write clean code") is not a rule; say so and ask for the observable
   form.
2. **Why** — the reason, or the source: a client decision (author and date), a client
   document and section, an incident or defect, a regulation. A rule with no reason is the
   first to be ignored and the last to be removed.
3. **Scope** — which target files it governs, as globs (`paths:`), or "everything" for a
   process or document rule.
4. **Kind** — `coding` · `naming` · `architecture` · `security` · `document` · `process` ·
   `testing` · `other`.
5. **Severity** — `must` · `should` · `avoid` · `forbidden`, in the words the reviewer will
   use. Never soften a client's wording.
6. **Check** — how it is verified: a tool (`enforced_by`), the reviewer, or a hook. If a
   tool can enforce it, propose the `target.build.on_edit` entry now (Step 7).
7. **Approver and date** — who agreed to it. Needed whenever it overrides a pack rule.

## Step 5 — Conflict check, before anything is written

Read the rules already in force for the same scope and report each conflict:

| The new rule... | Outcome |
|---|---|
| would change **observable legacy behaviour** (a rounding, a message, a sort order, a default) | **Refuse.** Parity wins (NI-*). It is a client decision, raised once, and a change request if agreed. |
| contradicts or relaxes an **invariant** (`rules/migration/*`, security non-negotiables) | **Refuse.** Say which rule, and that relaxing an invariant is a change to the pack: `/mig-refine-skill`, or a profile setting where the invariant is profile-driven. |
| differs from a **pack stack or common rule** | Allowed. Record it in the rule's `Overrides` line by rule id, with the reason, the approver and the date. |
| contradicts the **client coding standard** | Refuse unless the new rule is stricter. The client's reviewer holds the code to the original. |
| duplicates an existing project rule | Show it. Extend that rule instead of adding a second. |
| is already enforced by a configured linter or formatter | Do not restate it. Point `enforced_by` at the tool; a rule the tool reports twice just produces two findings. |
| asks for an improvement over legacy behaviour | It is not a rule. Improvements are a separate, funded decision (NI-02): `/mig-cr-analyze`. |

## Step 6 — Write the rule file

Path: `.claude/rules/project/<topic>.md`. One file per topic; several rules per file. Never
overwrite an existing file — append the new rule with the next number.

```markdown
---
paths:                      # omit for a rule that applies to everything
  - "src/**/*.ts"
---
# PROJECT RULES: {TOPIC}

Project rules for {topic}. They sit above the pack's stack and common rules and below legacy
parity, the pack's invariants and any client coding standard
(`{{profile.target.coding_standards}}`).

## PRJ-{TOPIC}-01 — {short imperative title}

{The rule, as imperative lines. Severity word first: MUST / SHOULD / AVOID / FORBIDDEN.}

- **Why:** {reason, with the anchor — client decision, document §, defect}
- **Overrides:** {pack rule id, or "none"}
- **Check:** {tool | reviewer | hook}
- **Added:** {YYYY/MM/DD}, approved by {name}
```

Rules about the rules:
- IDs are permanent. A rule that no longer applies is marked
  `**Status:** retired — {date}, {approver}` and kept, never deleted or renumbered.
- A document digest (`file path` mode) keeps the source's section numbers and severity words,
  lists the source sections that do **not** apply with the reason, and lists every conflict
  found in Step 5 — the same discipline as a client standard.
- Show the file to the user and wait for confirmation before saving. It is the project's
  reading of its own convention, and every reviewer will hold code to it.

## Step 7 — Register and protect

1. Append the entry to `{{profile.project_rules}}`:
   ```yaml
   - id: PRJ-NAMING            # the topic id; rule ids are PRJ-NAMING-01...
     file: ".claude/rules/project/naming.md"
     kind: coding
     scope: ["src/**/*.ts"]    # same globs as the file's paths:, or ["*"]
     source: "client decision, 2026/03/04, J. Tanaka"   # or a document path, or ""
     overrides: []             # pack rule ids this file overrides, e.g. [TS-07]
     enforced_by: ""           # tool/config, or "" when review only
     status: active            # active | retired
   ```
2. When `source` is a document in the repository, add it to `{{profile.constraints.readonly_globs}}`.
3. When a tool can enforce the rule, propose a `{{profile.target.build.on_edit}}` entry —
   scoped by glob to target sources and **never matching `{{profile.legacy.root}}`**, running
   on the single edited file, timed on one file and under ~10s. Write it only after the user
   confirms. A rule the project says is `must` and that a linter can check belongs there,
   not in a reviewer's attention.
4. Run the checks in Step 8 on the new entry before reporting.

## Step 8 — Validate (`--check`, and after every add)

| # | Check | Severity |
|---|---|---|
| 1 | every `project_rules[].file` exists, and every file under `.claude/rules/project/` is registered | Warning — an unregistered rule is applied but not cited or ranked |
| 2 | each file has valid front matter, and `paths:` equals the entry's `scope` | Warning |
| 3 | every rule id in a file matches `PRJ-{TOPIC}-{NN}` for that file's topic, with no gaps closed and no duplicates | Critical — IDs are permanent |
| 4 | every rule has `Why`, `Overrides` and `Check` | Warning |
| 5 | every `overrides` id exists in a pack rule file, and none names an invariant | Critical for an invariant |
| 6 | every override records its approver and date | Warning |
| 7 | `enforced_by` names a tool that exists in the repository | Warning |
| 8 | no scope matches `{{profile.legacy.root}}`, and no `on_edit` entry added for a rule does | Critical — the legacy tree is read-only |
| 9 | no two active rules in overlapping scope contradict each other | Critical |

## Step 9 — Report

```
Project rules
  Active           : {n}   in {n} files   ({topic list})
  Added this run   : {PRJ-ID} — {title}   scope {globs}   severity {word}
  Overrides        : {n}   {each: PRJ-ID overrides pack-rule-id, approver, date}
  Refused          : {n}   {each: what, which invariant, parity point or client rule}
  Enforced by tool : {n}/{n}   on_edit entries added: {n}
  Review-only      : {n}   {ids} — the reviewer is the only check
  Read-only        : {n} source documents added to constraints.readonly_globs
  Retired          : {n}
```

End by naming the rules that are review-only. Those are the ones a hook or linter could
carry, and the ones that will be forgotten first.
