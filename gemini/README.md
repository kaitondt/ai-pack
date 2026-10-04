# AI Pack for Gemini CLI

Four independently installable Gemini CLI extensions, generated from the Claude packs. Each
`gemini/<pack>/` is a git submodule pointing at its own repository, with the extension
(`gemini-extension.json`) at the repository root:

| Extension | Repository | Commands |
|---|---|---|
| `sdlc-standard` | [ai-pack-gemini-sdlc](https://github.com/kaitondt/ai-pack-gemini-sdlc) | `/sdlc-*` — development lifecycle, traceability, design and test gates |
| `migration-standard` | [ai-pack-gemini-migration](https://github.com/kaitondt/ai-pack-gemini-migration) | `/mig-*` — evidence-led legacy migration |
| `pm-standard` | [ai-pack-gemini-pm](https://github.com/kaitondt/ai-pack-gemini-pm) | `/pm-*` — project governance and controls |
| `vibe-standard` | [ai-pack-gemini-vibe](https://github.com/kaitondt/ai-pack-gemini-vibe) | `/vibe-*` — fast AI-assisted delivery with safety rails |

Each extension ships slash commands (`commands/*.toml`), skills, subagents (`agents/`), hooks
(`hooks/hooks.json`) and adoption templates (`templates/`).

> **Using Antigravity (CLI `agy` or the IDE)?** These are Gemini CLI extensions
> (`gemini-extension.json`); Antigravity has its own plugin format and does not load them. Use
> [ai-pack-antigravity](https://github.com/kaitondt/ai-pack-antigravity) instead.

## Requirements

Install Gemini CLI (Node.js 20+) and run `gemini` once to sign in; the guard hooks also need
Python 3 on `PATH` as `python`.

```sh
npm install -g @google/gemini-cli        # any platform
brew install gemini-cli                  # or Homebrew
gemini --version
```

Since 2026-06-18 Gemini CLI is replaced by the Antigravity CLI for unpaid and Google One users.

## Install

```sh
gemini extensions install https://github.com/kaitondt/ai-pack-gemini-vibe          # from GitHub
gemini extensions install ./gemini/vibe-standard                # from a clone (--recurse-submodules)
gemini extensions link    ./gemini/vibe-standard                # symlink, for pack development
gemini extensions update vibe-standard                          # after a new version is pushed
```

The repositories are private: installing from GitHub needs `git` credentials with access to them.

### From the chat

Inside a `gemini` session the same operations are slash commands:

```text
/extensions install https://github.com/kaitondt/ai-pack-gemini-vibe
/extensions list
/extensions update vibe-standard
```

Restart `gemini` (or run `/extensions restart`) after installing so the commands and skills load.

### Project-only install

Extensions are always installed per machine and enabled everywhere by default. To use a pack in
one project only, switch it off for the user and back on for that workspace:

```sh
gemini extensions disable vibe-standard --scope user
cd <project> && gemini extensions enable vibe-standard --scope workspace
```

(In chat: `/extensions disable ...` / `/extensions enable ...`, then restart `gemini`.) The
hooks are inactive anyway in any repository without `.gemini/<profile>.yaml`.

## Update

```sh
gemini extensions update vibe-standard       # one extension
gemini extensions update --all               # every installed extension
```

In chat: `/extensions update vibe-standard`, then restart `gemini` (or `/extensions restart`).
An extension installed with `gemini extensions link` follows the clone: `git pull
--recurse-submodules` updates it.

### After updating: bring the project in line

Updating the plugin replaces the pack's commands, skills, agents and hooks. It does **not** touch
what `/<prefix>-init` copied into each project:

- `.gemini/rules/` — compare it with the plugin's `templates/rules/` and copy the files that changed.
  Keep your own edits: a local rule change belongs in the pack's source, not only in one project.
- `GEMINI.md` — regenerate the pack's section only when the release notes say its template
  changed.
- `.gemini/<profile>.yaml` — run `/<prefix>-profile-check` in a new session. It reports fields a new release
  added or renamed; fill them in and run it again until it is clean.

## Adopt in a project

Run `/<prefix>-init` (e.g. `/vibe-init`). It writes `.gemini/<profile>.yaml`, copies the rules
into `.gemini/rules/`, and generates the project `GEMINI.md`, which imports those rules. The
hooks and the extension context stay inactive in any repository without `.gemini/<profile>.yaml`.

## Choosing the model and effort

In this build every command and agent runs on the model and reasoning effort of your session —
the per-agent `model:` / `effort:` tiers of the Claude Code build do not carry over. Match the
session to the work, and switch between commands when the kind of work changes:

| Work | Commands (examples) | Model | Effort |
|---|---|---|---|
| Analysis, design, review, triage, estimating, planning | `*-generate-requirements`, `*-generate-basic-design`, `*-generate-detail-design`, `*-review-*`, `*-cr-analyze`, `*-trace-bug`, `*-uat-investigate`, `sdlc-maintain-intake`, `pm-estimate`, `pm-risk-assess`, `pm-change-assess`, `vibe-plan`, `vibe-review`, `vibe-security-check`, `vibe-fix` | your strongest | high — the highest level for fixed-price or regulated work |
| Production from an approved document | `*-implement-feature`, `*-cr-implement`, `*-generate-test`, `*-generate-testscript`, `*-generate-infra`, `*-generate-mockup`, `*-uat-fix`, `pm-report`, `pm-evm`, `vibe-build`, `vibe-verify` | a fast, capable one | medium |
| Mechanical checks | `*-verify-build`, `*-profile-check`, `*-trace-check`, `*-template-register`, `vibe-status` | the fastest | low |

Do not drop the first row to save cost: its mistakes are silent and plausible, and surface only
at review, UAT or acceptance. The `execution` block of the profile (`model_profile`, overrides)
is read only by the Claude Code build; `intended_effort` is still a useful record of the level
the team agreed.

### How to set it in Gemini CLI

- **Model:** `/model` → **Manual** → a Pro model for the first row, a Flash model for the other
  two; **Auto** lets Gemini CLI choose per request. At start-up: `gemini -m <model>`, or
  `GEMINI_MODEL`, or `"model": { "name": "<model>" }` in `~/.gemini/settings.json`.
- **Thinking (effort):** there is no per-session switch; set a thinking budget in
  `settings.json`, globally or for one agent by name:

  ```json
  "modelConfigs": {
    "overrides": [
      {
        "match": { "overrideScope": "sdlc-reviewer" },
        "modelConfig": { "generateContentConfig": { "thinkingConfig": { "thinkingBudget": 8192 } } }
      }
    ]
  }
  ```

- Gemini CLI documents that `/model` and `--model` do not override a sub-agent's own model
  configuration. To give the heavy-tier agents (`*-reviewer`, `*-bd-designer`,
  `*-dd-designer`, `*-defect-triager`, …) more thinking, add one override per agent as above.

## Differences from the Claude plugins

- Hook events map as SessionStart -> SessionStart, PreToolUse -> BeforeTool,
  PostToolUse -> AfterTool. The document-rule hooks (`check-doc-rules`, `check-pm-doc-rules`)
  run as **AfterTool**, because BeforeTool cannot add context in Gemini CLI.
- Subagents drop `model:` (Claude aliases are not Gemini models) and map tool names
  (Read -> read_file, Edit -> replace, Bash -> run_shell_command, ...).
- Rules are imported from the project `GEMINI.md` with `@./.gemini/rules/...` lines.

## Release

```sh
python scripts/build-gemini-extensions.py
git -C gemini/vibe-standard add -A && git -C gemini/vibe-standard commit -m "..." && git -C gemini/vibe-standard push
git add gemini && git commit -m "Bump Gemini extensions"
```

Bump `VERSION` in the build script so `gemini extensions update` picks the change up. Do not edit
files under `gemini/<pack>/` by hand.
