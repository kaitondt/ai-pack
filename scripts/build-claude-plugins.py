#!/usr/bin/env python3
"""Build Claude Code plugins + a marketplace from the four skill packs.

Source of truth stays in packs/<pack>/.claude/ and packs/<pack>/profile/ (so the "copy .claude/" install
keeps working). This script regenerates claude/ as a Claude Code marketplace:
claude/.claude-plugin/marketplace.json plus claude/plugins/<pack>/ in the layout the plugin
loader expects. claude/ is the git submodule https://github.com/kaitondt/ai-pack-claude; commit
and push there after a rebuild, then commit the new submodule pointer in ai-pack.

    python scripts/build-claude-plugins.py

Then, in Claude Code:
    /plugin marketplace add kaitondt/ai-pack-claude
    /plugin install sdlc-standard@ai-pack
"""
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "claude"

MARKETPLACE = "ai-pack"
OWNER = {"name": "ThucND", "url": "https://github.com/kaitondt"}
REPOSITORY = "https://github.com/kaitondt/ai-pack-claude"
VERSION = "2.2.1"

PACKS = [
    {
        "name": "sdlc-standard",
        "prefix": "sdlc",
        "profile": "sdlc.profile.yaml",
        "description": "Project-agnostic SDLC pack for building something new, P0 Inception to "
                       "P9 Maintenance: requirements, basic/detail design, implementation, "
                       "test levels, UAT, change requests, traceability.",
        "keywords": ["sdlc", "requirements", "design", "testing", "traceability"],
    },
    {
        "name": "migration-standard",
        "prefix": "mig",
        "profile": "migration.profile.yaml",
        "description": "Pack for rewriting or replatforming a legacy system where behaviour "
                       "must be preserved: legacy analysis, gap-driven design, no-invention "
                       "rules, read-only legacy guards.",
        "keywords": ["migration", "legacy", "replatform", "traceability"],
    },
    {
        "name": "pm-standard",
        "prefix": "pm",
        "profile": "pm.profile.yaml",
        "description": "PMBOK-aligned project management pack: charter, scope/WBS, estimation, "
                       "cost and schedule baselines, EVM, reporting, quality, risk, change "
                       "control, closing.",
        "keywords": ["project-management", "pmbok", "evm", "risk", "baseline"],
    },
    {
        "name": "vibe-standard",
        "prefix": "vibe",
        "profile": "vibe.profile.yaml",
        "description": "Vibe coding with guard rails: intent -> slice -> run -> verify -> "
                       "commit, stage model spike/prototype/mvp/production, debt ledger, and "
                       "handoff to sdlc/pm when the project outgrows it.",
        "keywords": ["vibe-coding", "prototype", "mvp", "guardrails"],
    },
]

DOCS = ["README.md", "ADOPTION.md", "COMMAND-FLOW.md"]

# Runs a pack hook only when the project has opted in (its profile exists). A plugin enabled
# at user scope fires in every repository; without this gate the guards would block writes
# in projects that never adopted the pack.
LAUNCHER = '''#!/usr/bin/env python3
"""Plugin hook launcher: python run-hook.py <profile-file> <hook-script> [--always]

Without --always the hook is skipped (exit 0) unless .claude/<profile-file> exists in the
project. With --always (SessionStart) it also prints the plugin root so commands can find
the pack's templates.
"""
import os
import subprocess
import sys


def main():
    profile, script = sys.argv[1], sys.argv[2]
    always = "--always" in sys.argv[3:]
    here = os.path.dirname(os.path.abspath(__file__))
    root = os.path.dirname(here)
    project = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
    stdin = sys.stdin.buffer.read() if not sys.stdin.isatty() else b""

    if not os.path.exists(os.path.join(project, ".claude", profile)):
        if not always:
            return 0
    if always:
        print("[{}] plugin root: {}".format(profile.split(".")[0], root))
        sys.stdout.flush()

    env = dict(os.environ, CLAUDE_PROJECT_DIR=project, CLAUDE_PLUGIN_ROOT=root)
    proc = subprocess.run([sys.executable, os.path.join(here, script)],
                          input=stdin, env=env)
    return proc.returncode


if __name__ == "__main__":
    sys.exit(main())
'''

PLUGIN_NOTE = """
> **Installed as a Claude Code plugin?** The pack's files are not in this repository's
> `.claude/` — they live in the plugin directory `${{CLAUDE_PLUGIN_ROOT}}` (if that token is
> not substituted, use the path from the `[{stem}] plugin root: …` line printed at session
> start). Map every "pack" path in this command as follows:
>
> | Pack path in this command | Plugin location |
> |---|---|
> | profile template `profile/{profile}` | `<plugin root>/templates/profile/{profile}` |
> | `.claude/CLAUDE.md` template | `<plugin root>/templates/CLAUDE.md` |
> | `.claude/rules/` | `<plugin root>/templates/rules/` — **copy into this project's `.claude/rules/`** (plugins cannot load rules; they only apply from the project). Never overwrite an existing file without asking. |
> | `.claude/hooks/*.py` | `<plugin root>/hooks/` — already registered by the plugin; do **not** copy `settings.json` hooks, they would run twice |
> | `.claude/agents/{prefix}-*.md` | read-only in the plugin (overwritten on update). To change an agent's `model:` or tools, copy it into this project's `.claude/agents/` and edit the copy — a project agent overrides the plugin agent of the same name |
> | `.claude/skills/` | read-only in the plugin. Propose skill/rule changes as a patch to the pack's source repository, or override locally by copying the skill into this project's `.claude/skills/` |
>
> The profile `.claude/{profile}` and everything the pack generates stay in this project, as
> in a manual install.
"""

NOTE_TARGETS = ("-init.md", "-profile-check.md", "-refine-skill.md")


def hook_entries(pack, settings):
    """Rewrite $CLAUDE_PROJECT_DIR/.claude/hooks/x.py into the gated plugin launcher."""
    pattern = re.compile(r'\$CLAUDE_PROJECT_DIR/\.claude/hooks/([A-Za-z0-9_-]+\.py)')
    hooks = json.loads(json.dumps(settings.get("hooks", {})))
    for event, groups in hooks.items():
        for group in groups:
            for h in group["hooks"]:
                m = pattern.search(h["command"])
                if not m:
                    sys.exit("unrecognised hook command in {}: {}".format(pack["name"], h["command"]))
                h["command"] = 'python "${{CLAUDE_PLUGIN_ROOT}}/hooks/run-hook.py" {} {}{}'.format(
                    pack["profile"], m.group(1), " --always" if event == "SessionStart" else "")
    return {"hooks": hooks}


def inject_note(path, pack):
    text = path.read_text(encoding="utf-8")
    note = PLUGIN_NOTE.format(prefix=pack["prefix"], profile=pack["profile"],
                              stem=pack["profile"].split(".")[0])
    m = re.match(r"^---\n.*?\n---\n(?:\s*\n)*(#[^\n]*\n)?", text, re.DOTALL)
    cut = m.end() if m else 0
    path.write_text(text[:cut] + note + "\n" + text[cut:], encoding="utf-8")


def clean_dir(path):
    """Empty a generated directory but keep .git: the output is its own git submodule."""
    path.mkdir(parents=True, exist_ok=True)
    for item in path.iterdir():
        if item.name == ".git":
            continue
        if item.is_dir():
            shutil.rmtree(item)
        else:
            item.unlink()


MARKER_LINE = re.compile(r"^<!-- /?model-policy:claude -->\n", re.M)


def strip_policy_markers(root):
    """Pack sources mark the Claude-only model policy for the other builds; Claude keeps the text."""
    for path in root.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        if "model-policy:claude" in text:
            path.write_text(MARKER_LINE.sub("", text), encoding="utf-8")


def build(pack):
    src = ROOT / "packs" / pack["name"]
    claude = src / ".claude"
    dst = OUT / "plugins" / pack["name"]
    dst.mkdir(parents=True)

    for part in ("commands", "agents", "skills"):
        shutil.copytree(claude / part, dst / part)

    shutil.copytree(claude / "hooks", dst / "hooks",
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    (dst / "hooks" / "run-hook.py").write_text(LAUNCHER, encoding="utf-8")
    settings = json.loads((claude / "settings.json").read_text(encoding="utf-8"))
    (dst / "hooks" / "hooks.json").write_text(
        json.dumps(hook_entries(pack, settings), indent=2) + "\n", encoding="utf-8")

    tpl = dst / "templates"
    tpl.mkdir()
    shutil.copy2(claude / "CLAUDE.md", tpl / "CLAUDE.md")
    shutil.copytree(claude / "rules", tpl / "rules")
    shutil.copytree(src / "profile", tpl / "profile")

    for doc in DOCS:
        if (src / doc).exists():
            shutil.copy2(src / doc, dst / doc)

    strip_policy_markers(dst)

    for cmd in (dst / "commands").glob("*.md"):
        if cmd.name.endswith(NOTE_TARGETS):
            inject_note(cmd, pack)

    manifest = {
        "name": pack["name"],
        "version": VERSION,
        "description": pack["description"],
        "author": OWNER,
        "homepage": "{}/tree/main/plugins/{}".format(REPOSITORY, pack["name"]),
        "repository": REPOSITORY,
        "keywords": pack["keywords"],
    }
    (dst / ".claude-plugin").mkdir()
    (dst / ".claude-plugin" / "plugin.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    counts = {p: len(list((dst / p).glob(g))) for p, g in
              (("commands", "*.md"), ("agents", "*.md"), ("skills", "*/SKILL.md"))}
    print("  {:<20} {commands:>3} commands  {agents:>3} agents  {skills:>3} skills".format(
        pack["name"], **counts))


README_SOURCE = ROOT / "scripts" / "readme" / "claude.md"


def main():
    clean_dir(OUT)
    print("Building plugins into {}".format(OUT.relative_to(ROOT)))
    for pack in PACKS:
        build(pack)

    marketplace = {
        "name": MARKETPLACE,
        "owner": OWNER,
        "metadata": {
            "description": "Project-agnostic Claude Code skill packs: sdlc, migration, pm, vibe",
            "version": VERSION,
        },
        "plugins": [
            {
                "name": p["name"],
                "source": "./plugins/{}".format(p["name"]),
                "description": p["description"],
                "version": VERSION,
                "author": OWNER,
                "homepage": "{}/tree/main/plugins/{}".format(REPOSITORY, p["name"]),
                "repository": REPOSITORY,
                "keywords": p["keywords"],
                "category": "workflow",
            }
            for p in PACKS
        ],
    }
    mp = OUT / ".claude-plugin" / "marketplace.json"
    mp.parent.mkdir()
    mp.write_text(json.dumps(marketplace, indent=2) + "\n", encoding="utf-8")
    shutil.copy2(README_SOURCE, OUT / "README.md")
    print("Wrote {}".format(mp.relative_to(ROOT)))


if __name__ == "__main__":
    main()
