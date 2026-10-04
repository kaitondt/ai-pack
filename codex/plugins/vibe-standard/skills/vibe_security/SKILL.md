---
name: vibe_security
description: "Apply the vibe security baseline — secrets handling, server-side validation and per-resource authorisation, dependency vetting, data handling, prompt-injection and LLM-feature risks — scaled to the project's stage. Use for anything touching auth, user input, secrets, payments, file upload, personal data or new dependencies, for 'is this secure', and before every stage promotion from prototype upward."
---

# Security — The Baseline That Does Not Bend

> The invariants are in `references/rules/vibe/security-baseline.md`. This skill is how to apply them to
> the code the AI actually writes, and what `/vibe_security_check` inspects.

Load `vibe_project`.

---

## SE-01 — The six holes vibe-coded apps ship with

Check these first; they account for most real incidents in AI-built apps:

| # | Hole | What it looks like | Check |
|---|---|---|---|
| 1 | **Exposed secret** | key in source, in a `NEXT_PUBLIC_*` var, in git history, in a client bundle | grep source + history for key formats; inspect built client bundle for env values |
| 2 | **Missing authorisation** | `GET /api/notes/:id` returns any note to any logged-in user; update by id with no owner check | for each route/action touching a record: where is ownership checked? |
| 3 | **Database open to the client** | BaaS (Supabase/Firebase) with row-level security off, or rules `allow read, write: if true` | inspect RLS policies / security rules; try access with the anon key |
| 4 | **Trusting the client** | price, role, user id or `isAdmin` taken from the request body | any authz or money decision using client-supplied values |
| 5 | **Injection** | string-built SQL, `exec` with user input, `dangerouslySetInnerHTML` with user content, path from input | grep for the patterns; trace each input |
| 6 | **Hand-rolled auth** | own password hashing, own session tokens, JWT with `none`/weak secret, no rate limit on login | prefer the managed provider (SF-01); otherwise verify each |

## SE-02 — Secrets

- `.env*` in `.gitignore` before the first secret exists; `.env.example` has names only.
- Server-only secrets never in a variable with a public prefix; never imported into client
  components.
- Found a committed secret: **rotate first**, then remove, then (shared repo) clean history.
  Removing without rotating fixes nothing — the key is already in the clone of everyone who
  pulled.
- The `guard_vibe_paths` hook blocks writes containing known key formats. If it blocks a
  legitimate test fixture, use an obviously fake value (`sk_test_FAKE…`), not a real one.

## SE-03 — Every endpoint, every server action

For each one, answer in the code, not in prose:

1. **Who can call it?** Authentication check at the top, or explicitly public (and why).
2. **Which records can they touch?** The query filters by the caller's id/tenant, or checks
   ownership after fetch, **before** returning or mutating.
3. **What does it accept?** A schema (zod / pydantic / …) validating type, length, range —
   rejecting unknown fields that could be mass-assigned (`role`, `ownerId`, `price`).
4. **What does it return?** Only fields the caller may see — no password hashes, tokens,
   other users' emails, internal errors / stack traces.
5. **How often?** Rate-limited if it is login, signup, password reset, send-email, or costs
   money (LLM calls, SMS).

## SE-04 — Dependencies

Apply VT-03 to every new package. Then:

- prefer fewer; a 10-line function beats a new package for a 10-line job
- `{{profile.commands.audit}}` at `mvp`+ in CI; high/critical in a reachable path blocks release
- licences in `{{profile.security.allowed_licenses}}`; anything else is a `DEC-*`

## SE-05 — Data

- Below `mvp`: synthetic data only (`{{profile.security.allow_real_data}}` false).
- Personal fields collected only when a core flow needs them (SB-05); note which in PRODUCT.md
  Constraints.
- Passwords never stored or logged in plain text; tokens hashed when stored.
- Backups exist and a restore has been **tried** before real user data is trusted to the app.

## SE-06 — When the product uses an LLM

- User input and retrieved documents can contain instructions — the model will read them.
  Never give the model tools or data beyond what **this user** may access.
- Model output is untrusted: validate it before using it in SQL, HTML, shell, URLs or as a
  tool call argument.
- Put a cost ceiling on it: rate limit per user, max tokens, and an alert on spend.
- The system prompt will leak; do not put secrets or authorisation logic in it.

## SE-07 — `/vibe_security_check`

Runs SE-01 (all six), SE-02, SE-03 per endpoint, SE-04 audit, SE-05, SE-06 if applicable, and
the SB-07 matrix rows for the **target** stage. Output: findings with severity and file:line,
matrix pass/fail per row, and the list of `DEBT-*` with `category: security` and their due
stage. Critical/High open → the check fails.

## Self-check

- [ ] The six holes checked, each with evidence
- [ ] Every endpoint answers SE-03's five questions in code
- [ ] No secret in source, history, client bundle or logs
- [ ] Security shortcuts are `DEBT-*` due no later than `mvp`
