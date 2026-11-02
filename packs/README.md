# Pack sources

These four folders are the **source of truth** for AI Pack. Every installable build — Claude
Code, Codex, Gemini CLI and GitHub Copilot — is generated from them by the scripts in
[`../scripts/`](../scripts/):

```
packs/<pack>/.claude/ + packs/<pack>/profile/
    ├─ build-claude-plugins.py     → claude/      (ai-pack-claude)
    ├─ build-codex-plugins.py      → codex/       (ai-pack-codex)
    ├─ build-gemini-extensions.py  → gemini/...   (ai-pack-gemini-*)
    └─ build-copilot-plugins.py    → copilot/     (ai-pack-copilot)
```

The `.claude/` folder name is historical: Claude Code's layout is the canonical format the other
builds are translated from. It also makes the copy install work — `cp -r packs/<pack>/.claude`
into a project and Claude Code picks it up as is.

| Pack | Purpose |
|---|---|
| [`sdlc-standard`](sdlc-standard/README.md) | Building something new, P0 Inception → P9 Maintenance |
| [`migration-standard`](migration-standard/README.md) | Rewriting or replatforming a legacy system |
| [`pm-standard`](pm-standard/README.md) | Managing the project (PMBOK-aligned) |
| [`vibe-standard`](vibe-standard/README.md) | Vibe coding with guard rails |

**Changing a pack:** edit it here, run the build scripts, then publish the changed submodules
(see [Releasing](../CONTRIBUTING.md#releasing)). Do not edit `claude/`, `codex/`, `gemini/` or
`copilot/` directly — the next build overwrites them.
