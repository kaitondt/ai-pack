# `vibe.profile.yaml` — Field Specification

The profile is the **only** file a project authors before the pack becomes operational. Skills
read it through `vibe-project` and substitute `{{profile.<dotted.path>}}` tokens.

Canonical location: `<repo-root>/.claude/vibe.profile.yaml`

It is deliberately much shorter than `sdlc.profile.yaml` or `pm.profile.yaml`. A vibe project
that needs more configuration than this is usually a project that needs one of those packs.

---

## Resolution contract

| Token | Resolves to |
|---|---|
| `{{profile.stage}}` | `spike` · `prototype` · `mvp` · `production` |
| `{{profile.commands.test}}` | the command string |
| `{{profile.paths.state}}` | repo-relative path |
| `{{profile.slices.max_files}}` | integer |

**Unresolvable token** → at stage `spike`, proceed with a stated guess; from `prototype`, stop
and ask. Never write a placeholder value into code or a record as if it were real.

---

## Sections

### `project`
| Field | Required | Notes |
|---|---|---|
| `key` | ✅ | 2–5 uppercase chars; used in report file names |
| `name` | ✅ | display name |
| `one_liner` | ✅ | what, for whom — the first line of PRODUCT.md |
| `owner` | ✅ | the human who decides. Default owner of every `DEC-*` and the only one who can promote a stage |
| `start_date` | — | anchors "as of" statements |

### `stage` ✅
`spike` · `prototype` · `mvp` · `production`. Decides which rules are in force
(`skills/vibe-project` — the stage model; VT-08; SB-07). Changed **only** by `/vibe-graduate`,
which records a `DEC-*`. The `check-vibe-profile` hook reports an invalid value at session start.

### `team`
| Field | Notes |
|---|---|
| `shape` | `solo` · `pair` · `small`. From `small`, slices land via pull request |
| `reviewers` | who may accept a diff besides the owner |

### `product`
| Field | Required | Notes |
|---|---|---|
| `users` | ✅ | mirrors PRODUCT.md "Users" |
| `core_flows` | ✅ | 3–7 entries, mirrors PRODUCT.md. From `mvp`, each flow's done-when checks must be automated (VT-08); graduation checks each |
| `public_url` | ✅ | `true` when reachable from the internet. At `spike`/`prototype` this raises security to the `mvp` column (SB-07); the session hook warns |

### `stack`
Free text per field: `language`, `framework`, `ui`, `database`, `orm`, `auth`, `hosting`,
`package_manager`. Recorded as `DEC-001` by `/vibe-scaffold`. Changing any of them later is a
decision (IF-05).

### `commands`
The **real** commands. `/vibe-verify` runs them in order: `typecheck` → `lint` → `test` →
`build` → (`production`) `test_e2e` / `smoke`. `""` means "not configured", which is a finding
from `mvp` (`/vibe-profile-check` #5).

| Field | Notes |
|---|---|
| `install`, `dev`, `dev_url` | `dev_url` is where verification drives the UI / calls the API |
| `build`, `typecheck`, `lint`, `format`, `test` | |
| `test_e2e` | required at `production` |
| `audit` | dependency audit; required in CI from `mvp` (SB-04) |
| `smoke` | a command proving the deployed app answers; used by `/vibe-ship` |

### `paths`
All repo-relative; defaults under `vibe/`. Commit the folder — it is the project's memory.

| Field | Holds |
|---|---|
| `vibe_root` | the folder |
| `product` | PRODUCT.md (IF-06) |
| `state` | STATE.md, the handoff (SC-01); printed by the session hook |
| `intents` | `INT-NNN-<slug>.md` files |
| `decisions` · `debt` · `bugs` · `backlog` | the four append-only logs (SC-03) |
| `reviews` · `releases` | review reports, release notes |
| `skill_changes` | the refine-loop record (`/vibe-refine-skill`) |

### `slices`
| Field | Default | Notes |
|---|---|---|
| `max_files` | 8 | SS-02; hook warns past it, again at 2× |
| `max_changed_lines` | 400 | added + deleted, excluding `exclude_from_budget` |
| `max_minutes` | 60 | not enforced; a prompt to stop and commit |
| `require_clean_tree` | true | SS-03 |
| `commit_format` | — | **removed** — ignored if present; the format is `commit.format` |
| `exclude_from_budget` | `vibe/**`, lockfiles, migrations, snapshots, generated | glob list |

`/vibe-profile-check` flags budgets above 15 files / 800 lines: a budget that large is not one.

### `loop`
| Field | Default | Notes |
|---|---|---|
| `max_fix_attempts` | 3 | SS-05, the doom-loop limit. Valid 2–5 |
| `attempt_branch_prefix` | `attempt/` | where failed attempts are preserved |

### `commit`

The commit message format and the commit guard (`rules/vibe/git-commit.md`). Chosen at `/vibe-init` (the
"Choose the commit message format" step), used by `/vibe-commit` and `/vibe-build`, enforced on every `git`
command the AI runs by `hooks/guard-vibe-git.py` (PreToolUse on `Bash|PowerShell`). An absent
section means the defaults below, which `/vibe-profile-check` reports as unchosen.

| Field | Default | Notes |
|---|---|---|
| `preset` | `id-action-summary` | `id-action-summary` · `bracketed` · `conventional` · `existing` · `custom` — a record of the choice; `format` is what is enforced |
| `format` | `{ID} {ACTION} {SUMMARY}` | tokens `{ID}`, `{ACTION}`, `{SUMMARY}`; the rest is literal. Must contain `{SUMMARY}`, and `{ID}` unless `no_id` is set (GT-01) |
| `actions[]` | `ADD UPDATE DELETE FIX REVIEW CONFIRM REFACTOR REVERT` | the `{ACTION}` vocabulary, case-sensitive. The `conventional` preset uses `feat fix docs test refactor perf build ci chore revert` |
| `id_pattern` | `""` | regex for one id. Empty → any upper-case id containing a digit (`INT-003.2`, `BUG-004`, `DEBT-002`) |
| `id_separator` | `,` | joins several ids in `{ID}` |
| `no_id` | `""` | token accepted in place of an id for housekeeping commits (`NOID`). Empty → every commit needs a real id (GT-09) |
| `summary_max` | 72 | characters in `{SUMMARY}` |
| `summary_language` | `en` | language of the summary and body |
| `body` | `optional` | `optional` · `required` · `none` |
| `enforce` | `true` | `false` stops the format check only; GT-02..GT-08 stay on |
| `stage_explicit_paths` | `true` | blocks `git add -A` / `.` / `-u` and `git commit -a` (GT-02) |
| `regenerated_globs[]` | `**/*.generated.*`, `vendor/**` | read-only paths whose changes may still be committed, because a generator rewrites them (GT-03) |
| `protected_branches[]` | `[]` | globs of branches that never take a direct commit (GT-06) |
| `allow_push` | `false` | `true` lets the AI run `git push` — never with force (GT-08) |
| `allow_amend` | `false` | `true` allows `--amend` of a commit not yet pushed (GT-07) |

`commit.format` replaces `slices.commit_format`, which the pack no longer reads. `/vibe-init` moves
an old value across (`{SLICE_ID}` becomes `{ID}`) and deletes the key.


### `verification`
| Field | Notes |
|---|---|
| `add.<stage>` | extra checks for a stage. May add to VT-08; may not remove |
| `ui_check` | `playwright` · `browser-tool` · `human` — how "seen running" happens for UI |

### `security`
| Field | Notes |
|---|---|
| `secret_store` | where secrets live beyond local `.env` |
| `env_files` | files the secret guard allows real values in (gitignored). `.env.example` is never exempt |
| `allowed_licenses` | SB-04; anything else is a `DEC-*` |
| `allow_real_data` | `false` below `mvp` (SB-05) |
| `dangerous_commands` | extra Python regexes blocked by `guard-vibe-bash` — put the production deploy here. YAML double-quoted: escape backslashes (`"fly\\s+deploy"`) |
| `protected_paths` | globs `guard-vibe-paths` never lets the AI write |

### `debt`
| Field | Default | Notes |
|---|---|---|
| `paydown_every_n_slices` | 5 | DL-05; the counter is computed from git |
| `block_graduation_on_due` | true | DL-04; `/vibe-profile-check` flags `false` as High |

### `release`
Free text: `environments`, `deploy`, `rollback`, `monitoring`, `backups`. `/vibe-ship` quotes
`deploy` and `rollback` verbatim to the human. From `mvp`, `rollback` must describe something
that works for the current release (SH-02 #5).

### `graduation`
| Field | Notes |
|---|---|
| `extra_criteria.<stage>` | project-specific promotion criteria added to GR-01 |
| `handoff_to` | `sdlc` · `pm` · `both` · `stay` — decided at `production` (GR-03) |

### `integration`
`sibling_packs: auto` detects `.claude/sdlc.profile.yaml` and `.claude/pm.profile.yaml`.

### `project_rules`

Optional. Your own rules on top of the pack's, added with `/vibe-rule-register`. Each entry
points at a file under `.claude/rules/project/` — a directory the pack never writes to.
Claude Code loads the file by itself; the entry lets the reviewer cite it and lets
`/vibe-profile-check` see it (check 19). A project rule may tighten `rules/vibe/*`, never
relax it.

| Field | Required | Notes |
|---|---|---|
| `id` | ✅ | Topic id, `PRJ-{TOPIC}`. Rule ids in the file are `PRJ-{TOPIC}-{NN}`. |
| `file` | ✅ | Repo-relative, under `.claude/rules/project/`. |
| `scope[]` | ✅ | Globs, equal to the file's `paths:` front matter; `["*"]` when the file has none. |
| `overrides[]` | — | Pack rule ids this file overrides; each is recorded as a `DEC-*` in `paths.decisions`. Never an invariant. |
| `enforced_by` | — | The tool or hook that checks it. Empty means review-only. |
| `status` | ✅ | `active` or `retired`. A retired rule is kept, never deleted or renumbered. |

### `execution`

<!-- model-policy:claude -->
| Field | Notes |
|---|---|
| `model_profile` | `quality` · `balanced` (default) · `budget`. `/vibe-init` resolves it, through the two tables below, to the `model:` and `effort:` frontmatter of every `vibe-*` agent. |
| `agent_model_overrides` | `{agent: model}` — wins over `model_profile` for that one agent. Raise a role the project depends on, or lower one that is genuinely mechanical here. |
| `agent_effort_overrides` | `{agent: effort}` — `low` · `medium` · `high` · `xhigh` · `max`; wins over `model_profile` for that one agent. |
| `agent_model` | **Deprecated.** One model for every agent, from older profiles. Read as `quality` when it is `opus` and `budget` when it is `sonnet`; `/vibe-profile-check` asks for it to be replaced by `model_profile`. |
| `intended_effort` | The effort for your own session, where the commands run. Agents do not use it — they take theirs from `model_profile`. Claude Code reads the session level from `/effort`, not from the profile, so set it there. |

| `model_profile` | heavy tier | standard tier |
|---|---|---|
| `quality` | opus · `xhigh` | opus · `high` |
| `balanced` | opus · `high` | sonnet · `medium` |
| `budget` | sonnet · `high` | sonnet · `medium` |

| Tier | Agents | Why |
|---|---|---|
| heavy | `vibe-planner`, `vibe-reviewer`, `vibe-security-auditor`, `vibe-debugger` | Analysis, design, review and triage. Their failures are silent and plausible, and surface only at review, UAT or acceptance. |
| standard | `vibe-builder`, `vibe-verifier` | Production work from an approved document. Build, tests and a heavy-tier review catch what they get wrong. |

The pack ships the `balanced` values in each agent's frontmatter, so a `balanced` project with
no overrides needs no agent edits.
<!-- /model-policy:claude -->

### `language`
| Field | Notes |
|---|---|
| `docs` | language of `vibe/*.md`. IDs are never translated |
| `conversation` | the language the human works in; replies follow it |
