---
description: "Write or revise PRODUCT.md — the one-page answer to 'what are we building': problem, users, core flows, non-goals, constraints. Usage: /vibe-product [idea or notes]"
---

# PRODUCT.md

Load `vibe-project`, then `vibe-intent-spec` (IN-01).

## Step 1 — Read what exists

`{{profile.paths.product}}`, the profile's `product` section, and — for an existing app — what
the app actually does now (routes, pages, models). Report gaps between them.

## Step 2 — Interview, briefly

Only for sections that are missing or vague, one batch:

- **Problem**: who has it, what does it cost them today, how do they cope now?
- **Users**: which one or two kinds of user, and what are they trying to get done?
- **Core flows**: the 3–7 verbs. Push "dashboard" → "see which invoices are overdue".
- **Not building**: at least three. Offer candidates the AI would otherwise add — accounts,
  teams/sharing, notifications, admin panel, mobile app, i18n, dark mode, payments, export.
- **Constraints**: deadline, budget, platform, personal data, compliance.

## Step 3 — Write

One page, IN-01 template. Mirror core flows into `{{profile.product.core_flows}}`.

**Revising** an existing PRODUCT.md is a decision (IF-06): append a `DEC-*` describing the
change; list the intents affected (a new non-goal may drop an intent; a new core flow needs
one).

## Step 4 — Report

```
PRODUCT.md {created | revised (DEC-*)}
  Core flows : {n} — {list}
  Non-goals  : {n}
  Intents    : existing {n} · affected by this change {list} · core flows with no intent {list}
  Next       : /vibe-intent "{first uncovered core flow}"
```
