# AI Pack for Codex

This marketplace publishes four separately installable Codex plugins:

- `sdlc-standard`: development lifecycle, traceability, design and test gates
- `migration-standard`: evidence-led legacy migration
- `pm-standard`: project governance and controls
- `vibe-standard`: fast AI-assisted delivery with safety rails

## Local development install

```powershell
codex plugin marketplace add F:/2.AI/ai-pack/codex
codex plugin add vibe-standard@ai-pack
```

Replace `vibe-standard` with the plugin you need. Start a new Codex thread after installation.

## Adopt a plugin in a project

Copy the selected plugin's `templates/profile/<profile>.yaml` to `.codex/`, copy `templates/rules/` to `.codex/rules/`, and copy `templates/AGENTS.md` to the repository's `AGENTS.md`. Then invoke the `<prefix>_workflow` skill (or describe the task normally).

The generated files in this directory are rebuilt with:

```powershell
python scripts/build_codex_plugins.py
```
