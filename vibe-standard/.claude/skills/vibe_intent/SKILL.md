---
name: vibe_intent
description: "Turn a fuzzy idea into something the AI can build without guessing — PRODUCT.md (problem, users, core flows, non-goals, constraints) and INT-* intent files with observable done-when checks. Use when starting a product, adding a feature, when a chat request has no intent yet, or when the AI keeps building the wrong thing."
---

# Intents — Product and Feature Intent

> The spec-lite of the pack. `sdlc-standard` spends P0 and P1 producing BRs, REQs and an SRS;
> `pm-standard` produces a charter and a scope statement. A vibe project gets **one page and a
> handful of intent files** — because nobody writes more at vibe speed, and this much is the
> minimum that stops the AI from filling the gaps with plausible guesses.

Load `vibe_project` first.

---

## IN-01 — PRODUCT.md: one page, five sections

Written once by `/vibe_product`, changed only by decision (IF-06).

```markdown
# <Product name>

> <one_liner from the profile>

## Problem
<Who has the problem, what it costs them today, how they cope now.>

## Users
- **<User kind 1>** — <what they are trying to get done>
- **<User kind 2>** — …

## Core flows
1. <verb phrase — "Sign up and sign in">
2. <"Create, edit and delete a note">
3. …            (3–7. More than 7 is not a product yet, it is a wish list.)

## Not building
- <explicit non-goal> — <why not / not yet>
- …

## Constraints
- Deadline / budget: …
- Platform: …
- Data: <personal data? which? retention?>
- Compliance: <none / GDPR / …>
```

How to get there from a conversation:

1. Ask for the problem before the solution. "What happens today without it?" A product whose
   problem nobody can state is a demo.
2. Name users concretely. "Everyone" produces a UI designed for nobody.
3. Push core flows to verbs. "Dashboard" is a place; "see which invoices are overdue" is a flow.
4. **Get at least three non-goals.** This is the section that saves the most time — every
   non-goal is a class of feature the AI will otherwise helpfully add.
5. Mirror the core flows into `{{profile.product.core_flows}}`.

## IN-02 — The intent file

`{{profile.paths.intents}}/INT-{NNN}-<slug>.md`:

```markdown
# INT-007 — Notes can be edited
Status: active          Stage: prototype         Flow: core flow 2
Asked by: <owner> · 2026-09-18

## Intent
A signed-in user can change the title and body of a note they own.

## Done when
1. From a note's page, "Edit" opens a form pre-filled with the current title and body.
2. Saving shows the updated note and the list shows the new title.
3. Another user's note cannot be edited — the API returns 404 and no form is shown.
4. An empty title is rejected with "Title is required"; nothing is saved.

## Not now
- Edit history / undo
- Rich-text or Markdown preview
- Collaborative editing

## Assumptions / open questions
- Q1 (2026-09-18): Does editing change the note's "updated" sort position? → asked
- (spike only) assumed: …

## Slices
- [x] INT-007.1 — edit form pre-filled, save updates (checks 1, 2)
- [ ] INT-007.2 — ownership enforced on page and API (check 3)
- [ ] INT-007.3 — validation (check 4)

## Log
- 2026-09-18 INT-007.1 a1b2c3d
```

Status values: `draft` → `active` → `done` · or `dropped` (with a reason). Never deleted (ID-02).

## IN-03 — Writing done-when checks

Good checks are the whole value of an intent. For each one:

| Test | Question |
|---|---|
| **Observable** | Could someone who has never seen the code tell whether it passed? |
| **Specific** | Does it name the input, the action, and the expected result? |
| **Includes the unhappy path** | Is there at least one check for wrong input, no permission, or empty state? |
| **Includes ownership** | If data belongs to a user, is there a check that another user cannot touch it? (SB-03) |
| **Small** | 1–5 checks. More means the intent is two intents. |

The unhappy-path and ownership checks are the ones the AI leaves out when not asked, and the
ones users hit first.

## IN-04 — From a chat request to an intent

When the human types a request and no intent covers it:

1. Draft the intent file — intent line, done-when, not now — from the request and PRODUCT.md.
2. **Show it and wait for a yes** (from `prototype` up). The human reads four lines instead of
   four hundred lines of diff.
3. If the request is really a bug, route to `/vibe_fix`; if it is a refactor, it is a debt
   paydown or a refactor intent (SS-07); if it contradicts a non-goal, say so and ask.
4. If it is small enough to be one slice, the intent has one slice. That is fine — the file is
   still the record.

At stage `spike`, a one-line intent in the commit message is enough, but assumptions must be
written down.

## IN-05 — Changing an intent mid-flight

Intents change when the human sees the running thing — that is the point. The rules:

- Changing done-when for **unbuilt** slices: edit the intent, note it in its Log.
- Changing what a **built** slice does: that is a new slice (or a new intent), not a silent
  rework. The old behaviour was committed and may be depended on.
- Dropping an intent: status `dropped`, one line why. The code already built for it is either
  removed in its own slice or recorded as a `DEBT-*`.

## Self-check

- [ ] PRODUCT.md has problem, users, 3–7 core flows, ≥ 3 non-goals, constraints
- [ ] The intent line is from a user's point of view
- [ ] 1–5 done-when checks, all observable, including an unhappy path
- [ ] Ownership check present if the data belongs to a user
- [ ] "Not now" is filled
- [ ] Open questions are listed with the date asked, not answered by guessing
