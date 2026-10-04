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

## Adopt in a project

Run `/<prefix>-init` (e.g. `/vibe-init`). It writes `.gemini/<profile>.yaml`, copies the rules
into `.gemini/rules/`, and generates the project `GEMINI.md`, which imports those rules. The
hooks and the extension context stay inactive in any repository without `.gemini/<profile>.yaml`.

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
