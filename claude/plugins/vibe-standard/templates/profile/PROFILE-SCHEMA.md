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
| `commit_format` | `{SLICE_ID}: {summary}` | SC-05 |
| `exclude_from_budget` | `vibe/**`, lockfiles, migrations, snapshots, generated | glob list |

`/vibe-profile-check` flags budgets above 15 files / 800 lines: a budget that large is not one.

### `loop`
| Field | Default | Notes |
|---|---|---|
| `max_fix_attempts` | 3 | SS-05, the doom-loop limit. Valid 2–5 |
| `attempt_branch_prefix` | `attempt/` | where failed attempts are preserved |

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

### `execution`
| Field | Notes |
|---|---|
| `agent_model` | `opus` by default — see README "Model policy" |
| `intended_effort` | recorded, not enforced; set it in your session |
| `agent_model_overrides` | per-agent, e.g. `{ vibe-verifier: sonnet }` |

### `language`
| Field | Notes |
|---|---|
| `docs` | language of `vibe/*.md`. IDs are never translated |
| `conversation` | the language the human works in; replies follow it |
