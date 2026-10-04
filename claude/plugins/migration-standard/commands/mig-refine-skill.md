---
description: "Feed review findings back into the skills and rules that produced them, so a defect is fixed once at its source instead of N times in N artifacts. Usage: /mig-refine-skill [review report path, or a finding description]"
---

# Refine a skill from review findings

> **Installed as a Claude Code plugin?** The pack's files are not in this repository's
> `.claude/` — they live in the plugin directory `${CLAUDE_PLUGIN_ROOT}` (if that token is
> not substituted, use the path from the `[migration] plugin root: …` line printed at session
> start). Map every "pack" path in this command as follows:
>
> | Pack path in this command | Plugin location |
> |---|---|
> | profile template `profile/migration.profile.yaml` | `<plugin root>/templates/profile/migration.profile.yaml` |
> | `.claude/CLAUDE.md` template | `<plugin root>/templates/CLAUDE.md` |
> | `.claude/rules/` | `<plugin root>/templates/rules/` — **copy into this project's `.claude/rules/`** (plugins cannot load rules; they only apply from the project). Never overwrite an existing file without asking. |
> | `.claude/hooks/*.py` | `<plugin root>/hooks/` — already registered by the plugin; do **not** copy `settings.json` hooks, they would run twice |
> | `.claude/agents/mig-*.md` | read-only in the plugin (overwritten on update). To change an agent's `model:` or tools, copy it into this project's `.claude/agents/` and edit the copy — a project agent overrides the plugin agent of the same name |
> | `.claude/skills/` | read-only in the plugin. Propose skill/rule changes as a patch to the pack's source repository, or override locally by copying the skill into this project's `.claude/skills/` |
>
> The profile `.claude/migration.profile.yaml` and everything the pack generates stay in this project, as
> in a manual install.


The third step of the refinement loop. A review tells you an artifact is wrong; this
command asks the more useful question — **why did the pack let it be wrong?**

## Step 1 — Load

`mig-project`, then the skill that owns the artifact category under review.

## Step 2 — Collect the findings

From the review report given as an argument, or from the findings in the conversation.
Group identical findings across artifacts. The grouping is the diagnosis: a finding that
appears once is an artifact defect; a finding that appears three times is a skill defect
wearing a disguise.

## Step 3 — Classify each finding group

| Signal | Fix belongs in | Why |
|---|---|---|
| One artifact wrong, its siblings correct | the artifact | a slip, not a systemic gap |
| Same finding in 2+ artifacts | the **skill** | the rule is missing or too vague to follow |
| Reviewer and generator read the same rule differently | the **skill** | the rule is ambiguous — ambiguity is a defect even when the rule is right |
| Rule is stated clearly, and was still violated | a **hook** | restating it will not help; enforce it mechanically |
| Finding contradicts an actually-correct rule | the **review checklist** | the checklist is wrong, not the generator |
| Finding is about the legacy, not the format | neither | it is a SPEC-GAP; escalate, do not encode a guess as a rule |

State the classification per group before changing anything. A change without a stated
classification is a guess.

## Step 4 — The rule that keeps this loop honest

**Never weaken a rule to make a finding disappear.**

This is the same disease as closing a GAP item by editing the document to match the code
(`mig-detail-design`). The finding stops appearing, the defect stays, and now the pack
actively certifies it. If a rule produces findings you disagree with, either the rule is
wrong — say so, with the evidence — or the findings are correct and inconvenient.

Legitimate skill edits: make an implicit rule explicit; disambiguate wording two readers
took two ways; add a missing case; add a worked example; add a self-check line; move an
unenforceable rule to a hook.

Illegitimate: deleting a rule because artifacts keep failing it; adding an exception that
covers exactly the artifacts that failed; softening "must" to "should".

## Step 5 — Apply

Edit the owning skill, rule file, or hook. Keep the edit minimal and in the file's
existing voice — a skill that accretes patch-shaped paragraphs stops being readable, and
an unread rule is not a rule.

Prefer, in order: strengthen the **self-check list** (cheapest, read last before finishing)
→ sharpen the rule statement → add an example → add a hook.

## Step 6 — Record the change and its blast radius

Append to `{{profile.paths.reviews}}/skill-changes.md`:

| Date | Skill / rule | Finding that motivated it | Change | Artifacts generated under the old rule |
|---|---|---|---|---|

The last column is what makes the loop safe. Artifacts produced before this change were
generated under a rule that has now changed; they are candidates for re-review, and
nobody will remember that in three weeks.

## Step 7 — Report

```
Skill refinement
  Findings in       : {n}   grouped into {n}
  Classified
    artifact defect : {n}  -> fix the artifacts, not the skill
    skill defect    : {n}  -> {files edited}
    hook candidate  : {n}  -> {hook, or "proposed"}
    checklist defect: {n}
    spec-gap        : {n}  -> escalated, not encoded
  Edits             : {file}:{what changed}
  Blast radius      : {n} artifacts generated under the old rule
  Re-run needed     : {which execute command, on which scope}
```

End by naming the exact command to re-run. The loop is only closed when the generator has
run again under the changed rule and the review comes back clean.
