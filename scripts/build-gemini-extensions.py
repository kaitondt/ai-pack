#!/usr/bin/env python3
"""Build Gemini CLI extensions from the four canonical Claude packs.

Source of truth stays in packs/<pack>/.claude/ and packs/<pack>/profile/. This script regenerates
gemini/<pack>/ as a self-contained Gemini CLI extension (gemini-extension.json at its root).
Each gemini/<pack>/ is its own git submodule (repo_name()); commit and push there after a
rebuild, then commit the new submodule pointers in ai-pack.

    python scripts/build-gemini-extensions.py

Then, in a shell:
    gemini extensions install ./gemini/sdlc-standard        # or: gemini extensions link ...
"""
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "gemini"

VERSION = "1.2.0"
REPOSITORY = "https://github.com/kaitondt/ai-pack"
GITHUB = "https://github.com/kaitondt"


def repo_name(pack):
    """gemini/<pack>/ is the git submodule <GITHUB>/ai-pack-gemini-<short name>."""
    return "ai-pack-gemini-" + pack["name"].replace("-standard", "")

PACKS = [
    {
        "name": "sdlc-standard",
        "prefix": "sdlc",
        "profile": "sdlc.profile.yaml",
        "description": "Project-agnostic SDLC pack, P0 Inception to P9 Maintenance: requirements, "
                       "basic/detail design, implementation, test levels, UAT, change requests, "
                       "traceability.",
    },
    {
        "name": "migration-standard",
        "prefix": "mig",
        "profile": "migration.profile.yaml",
        "description": "Rewrite or replatform a legacy system while preserving behaviour: legacy "
                       "analysis, gap-driven design, no-invention rules, read-only legacy guards.",
    },
    {
        "name": "pm-standard",
        "prefix": "pm",
        "profile": "pm.profile.yaml",
        "description": "PMBOK-aligned project management: charter, scope/WBS, estimation, cost and "
                       "schedule baselines, EVM, reporting, quality, risk, change control, closing.",
    },
    {
        "name": "vibe-standard",
        "prefix": "vibe",
        "profile": "vibe.profile.yaml",
        "description": "Vibe coding with guard rails: intent -> slice -> run -> verify -> commit, "
                       "stage model, debt ledger, and handoff to sdlc/pm when the project outgrows it.",
    },
]

DOCS = ["README.md", "ADOPTION.md", "COMMAND-FLOW.md"]

# Claude Code tool -> Gemini CLI tools. activate_skill is added to every restricted subagent
# because the pack's agents start by loading skills.
TOOL_MAP = {
    "Read": ["read_file", "read_many_files"],
    "Write": ["write_file"],
    "Edit": ["replace"],
    "MultiEdit": ["replace"],
    "Grep": ["grep_search"],
    "Glob": ["glob", "list_directory"],
    "Bash": ["run_shell_command"],
    "PowerShell": ["run_shell_command"],
    "WebFetch": ["web_fetch"],
    "WebSearch": ["google_web_search"],
}

EVENT_MAP = {"SessionStart": "SessionStart", "PreToolUse": "BeforeTool", "PostToolUse": "AfterTool"}

# BeforeTool cannot add model context in Gemini CLI, only allow/deny. Hooks whose job is to
# inject rules (exit 0 + text) run as AfterTool instead, so the model reads the rules right
# after the write and can correct the file.
CONTEXT_HOOKS = {"check-doc-rules.py", "check-pm-doc-rules.py"}

LAUNCHER = '''#!/usr/bin/env python3
"""Gemini hook launcher: python run-hook.py <event> <profile-file> <hook-script> [--always]

Runs a pack hook only when the project has opted in (.gemini/<profile-file> exists); with
--always (SessionStart) it also reports the extension root so commands can find templates.
Gemini CLI requires hook stdout to be a single JSON object, so the hook's plain-text output
is wrapped: SessionStart/AfterTool -> hookSpecificOutput.additionalContext, BeforeTool ->
systemMessage. Exit 2 (block, reason on stderr) is passed through unchanged.
"""
import json
import os
import subprocess
import sys


def main():
    event, profile, script = sys.argv[1], sys.argv[2], sys.argv[3]
    always = "--always" in sys.argv[4:]
    here = os.path.dirname(os.path.abspath(__file__))
    root = os.path.dirname(here)
    project = (os.environ.get("GEMINI_PROJECT_DIR") or os.environ.get("CLAUDE_PROJECT_DIR")
               or os.getcwd())
    stdin = sys.stdin.buffer.read() if not sys.stdin.isatty() else b""

    if not os.path.exists(os.path.join(project, ".gemini", profile)) and not always:
        return 0

    env = dict(os.environ, GEMINI_PROJECT_DIR=project, CLAUDE_PROJECT_DIR=project,
               EXTENSION_ROOT=root, PYTHONIOENCODING="utf-8")
    proc = subprocess.run([sys.executable, os.path.join(here, script)], input=stdin,
                          env=env, stdout=subprocess.PIPE)
    if proc.returncode != 0:
        return proc.returncode

    text = proc.stdout.decode("utf-8", errors="replace").replace("\r\n", "\n").strip()
    if always:
        text = "[{}] extension root: {}\\n{}".format(profile.split(".")[0], root, text).strip()
    if not text:
        return 0
    try:
        out = json.loads(text)
        if not isinstance(out, dict):
            raise ValueError
        if isinstance(out.get("hookSpecificOutput"), dict):
            out["hookSpecificOutput"]["hookEventName"] = event
    except ValueError:
        if event == "BeforeTool":
            out = {"systemMessage": text}
        else:
            out = {"hookSpecificOutput": {"hookEventName": event, "additionalContext": text}}
    sys.stdout.write(json.dumps(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
'''

CONTEXT = """# {name} (Gemini CLI extension)

This extension applies **only** in a repository that contains `.gemini/{profile}`. In any
other repository ignore everything below and do not load the `{prefix}-*` skills unless the
user asks for them.

When `.gemini/{profile}` exists:

- Start every task by activating the `{prefix}-project` skill. It resolves the profile, loads
  the invariant rules and routes to the phase skill.
- The project's own `GEMINI.md` and `.gemini/rules/` hold the rules; the profile wins over
  anything else.
- Slash commands are `/{prefix}-*` (`/{prefix}-init` adopts the pack in a new repository).
- Subagents `{prefix}-*` are available for delegation, as the commands describe.
- Pack templates live in this extension's directory, printed at session start as
  `[{stem}] extension root: <path>`.
"""

PLUGIN_NOTE = """
> **Installed as a Gemini CLI extension?** The pack's files are not in this repository's
> `.gemini/` — they live in the extension directory printed at session start as
> `[{stem}] extension root: …`. Map every "pack" path in this command as follows:
>
> | Pack path in this command | Extension location |
> |---|---|
> | profile template `profile/{profile}` | `<extension root>/templates/profile/{profile}` |
> | `.gemini/GEMINI.md` template | `<extension root>/templates/GEMINI.md` → write it as `GEMINI.md` at the repository root (it imports `.gemini/rules/` with `@` lines) |
> | `.gemini/rules/` | `<extension root>/templates/rules/` — **copy into this project's `.gemini/rules/`** (Gemini CLI has no rules loader; the project `GEMINI.md` imports them). Never overwrite an existing file without asking. |
> | `.gemini/hooks/*.py` | `<extension root>/hooks/` — already registered by the extension; do **not** add them to `.gemini/settings.json`, they would run twice |
> | `.gemini/agents/{prefix}-*.md` | read-only in the extension (overwritten on update). To change an agent's `model:` or tools, copy it into this project's `.gemini/agents/` and edit the copy |
> | `.gemini/skills/` | read-only in the extension. Override locally by copying the skill into this project's `.gemini/skills/` (workspace skills take precedence) |
>
> The profile `.gemini/{profile}` and everything the pack generates stay in this project.
"""

NOTE_TARGETS = ("-init.md", "-profile-check.md", "-refine-skill.md")


PRODUCT = "Gemini CLI"
# Pack sources wrap the Claude-only model/effort policy in these markers. Other builds replace
# the block with a note, after the product rename, so the note can still name Claude Code.
MODEL_POLICY = re.compile(r"<!-- model-policy:claude -->\n.*?<!-- /model-policy:claude -->\n?", re.S)
MODEL_NOTE = (
    "> **Model and effort on {product}:** the agents in this build run on the model and reasoning\n"
    "> effort selected in your session. The `model:` and `effort:` agent fields,\n"
    "> `execution.model_profile`, `agent_model_overrides` and `agent_effort_overrides` take effect\n"
    "> only in the Claude Code build of this pack, so any check comparing agent models with the\n"
    "> profile does not apply here: report it as N/A. Use your strongest model for analysis,\n"
    "> design, review and triage work, and a faster one for production work from an approved\n"
    "> document. How to set both: \"Choosing the model and effort\" in the AI Pack for\n"
    "> {product} README.\n")


def model_note(text):
    return MODEL_POLICY.sub(lambda m: MODEL_NOTE.format(product=PRODUCT), text)


def gemini_text(text):
    """Retarget filesystem and product references from Claude Code to Gemini CLI."""
    return model_note(text.replace("CLAUDE_PROJECT_DIR", "GEMINI_PROJECT_DIR")
                .replace("CLAUDE_PLUGIN_ROOT", "EXTENSION_ROOT")
                .replace(".claude/CLAUDE.md", ".gemini/GEMINI.md")
                .replace("CLAUDE.md", "GEMINI.md")
                .replace(".claude", ".gemini")
                .replace("Claude Code", "Gemini CLI"))


def copy_tree(src, dst):
    for item in src.rglob("*"):
        if "__pycache__" in item.parts:
            continue
        target = dst / item.relative_to(src)
        if item.is_dir():
            target.mkdir(parents=True, exist_ok=True)
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        if item.suffix in {".md", ".py", ".json", ".yaml", ".yml"}:
            target.write_text(gemini_text(item.read_text(encoding="utf-8")), encoding="utf-8")
        else:
            shutil.copy2(item, target)


def split_frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not m:
        return {}, text
    meta = {}
    for line in m.group(1).splitlines():
        key, sep, value = line.partition(":")
        if sep:
            meta[key.strip()] = value.strip()
    return meta, text[m.end():]


def yaml_scalar(value):
    if value.startswith('"'):
        try:
            return json.loads(value)
        except ValueError:
            return value.strip('"')
    return value.strip("'")


def toml_string(value, multiline=False):
    if multiline and "'''" not in value:
        return "'''\n" + value + "'''"
    return json.dumps(value, ensure_ascii=False)


def command_toml(path, pack):
    meta, body = split_frontmatter(path.read_text(encoding="utf-8"))
    if path.name.endswith(NOTE_TARGETS):
        m = re.match(r"(?:\s*\n)*(#[^\n]*\n)?", body)
        note = PLUGIN_NOTE.format(prefix=pack["prefix"], profile=pack["profile"],
                                  stem=pack["profile"].split(".")[0])
        body = body[:m.end()] + note + "\n" + body[m.end():]
    body = gemini_text(body).replace("$ARGUMENTS", "{{args}}").lstrip("\n")
    description = gemini_text(yaml_scalar(meta.get("description", path.stem)))
    return "description = {}\nprompt = {}\n".format(toml_string(description),
                                                   toml_string(body, multiline=True))


def convert_agent(path):
    meta, body = split_frontmatter(path.read_text(encoding="utf-8"))
    lines = ["---", "name: " + meta.get("name", path.stem),
             "description: " + gemini_text(meta.get("description", ""))]
    if "tools" in meta:
        tools = []
        for tool in json.loads(meta["tools"]):
            for mapped in TOOL_MAP.get(tool, []):
                if mapped not in tools:
                    tools.append(mapped)
        tools.append("activate_skill")
        lines.append("tools:")
        lines += ["  - " + t for t in tools]
    # model: is dropped on purpose — Claude model aliases (opus/sonnet) are not Gemini models;
    # the subagent then uses the session model.
    lines.append("---")
    return "\n".join(lines) + "\n" + gemini_text(body)


def map_matcher(matcher):
    tools = []
    for part in matcher.split("|"):
        for mapped in TOOL_MAP.get(part.strip(), []):
            if mapped not in tools:
                tools.append(mapped)
    if not tools:
        raise SystemExit("unmapped hook matcher: " + matcher)
    return "^({})$".format("|".join(tools))


def hook_entries(pack, settings):
    """Map Claude settings.json hooks to Gemini events, matchers and the gated launcher."""
    pattern = re.compile(r'\$CLAUDE_PROJECT_DIR/\.claude/hooks/([A-Za-z0-9_-]+\.py)')
    out = {}
    for event, groups in settings.get("hooks", {}).items():
        for group in groups:
            for h in group["hooks"]:
                m = pattern.search(h["command"])
                if not m:
                    raise SystemExit("unrecognised hook command in {}: {}".format(
                        pack["name"], h["command"]))
                script = m.group(1)
                gevent = "AfterTool" if script in CONTEXT_HOOKS else EVENT_MAP[event]
                entry = {
                    "name": "{}:{}".format(pack["prefix"], script[:-3]),
                    "type": "command",
                    "command": 'python "${{extensionPath}}/hooks/run-hook.py" {} {} {}{}'.format(
                        gevent, pack["profile"], script,
                        " --always" if event == "SessionStart" else ""),
                    "timeout": int(h.get("timeout", 10)) * 1000,
                }
                if h.get("statusMessage"):
                    entry["description"] = h["statusMessage"]
                matcher = map_matcher(group["matcher"]) if "matcher" in group else None
                bucket = out.setdefault(gevent, [])
                target = next((g for g in bucket if g.get("matcher") == matcher), None)
                if target is None:
                    target = {"matcher": matcher, "hooks": []} if matcher else {"hooks": []}
                    bucket.append(target)
                target["hooks"].append(entry)
    return {"hooks": out}


def project_context(claude_md, rules_dir):
    """Template for the project GEMINI.md: the pack's CLAUDE.md plus @-imports of the rules."""
    text = gemini_text(claude_md.read_text(encoding="utf-8")).rstrip() + "\n"
    imports = ["@./.gemini/rules/" + p.relative_to(rules_dir).as_posix()
               for p in sorted(rules_dir.rglob("*.md"))]
    return text + ("\n## Rules (imported from `.gemini/rules/`)\n\n" + "\n".join(imports) + "\n")


def clean_dir(path):
    """Empty a generated directory but keep .git: each output is its own git submodule."""
    path.mkdir(parents=True, exist_ok=True)
    for item in path.iterdir():
        if item.name == ".git":
            continue
        if item.is_dir():
            shutil.rmtree(item)
        else:
            item.unlink()


def build(pack):
    src = ROOT / "packs" / pack["name"]
    claude = src / ".claude"
    dst = OUT / pack["name"]
    clean_dir(dst)

    (dst / "commands").mkdir()
    for cmd in sorted((claude / "commands").glob("*.md")):
        (dst / "commands" / (cmd.stem + ".toml")).write_text(command_toml(cmd, pack),
                                                             encoding="utf-8")

    (dst / "agents").mkdir()
    for agent in sorted((claude / "agents").glob("*.md")):
        (dst / "agents" / agent.name).write_text(convert_agent(agent), encoding="utf-8")

    copy_tree(claude / "skills", dst / "skills")

    copy_tree(claude / "hooks", dst / "hooks")
    (dst / "hooks" / "run-hook.py").write_text(LAUNCHER, encoding="utf-8")
    settings = json.loads((claude / "settings.json").read_text(encoding="utf-8"))
    (dst / "hooks" / "hooks.json").write_text(
        json.dumps(hook_entries(pack, settings), indent=2) + "\n", encoding="utf-8")

    tpl = dst / "templates"
    copy_tree(claude / "rules", tpl / "rules")
    copy_tree(src / "profile", tpl / "profile")
    (tpl / "GEMINI.md").write_text(project_context(claude / "CLAUDE.md", claude / "rules"),
                                   encoding="utf-8")

    for doc in DOCS:
        if (src / doc).exists():
            (dst / doc).write_text(gemini_text((src / doc).read_text(encoding="utf-8")),
                                   encoding="utf-8")

    (dst / "GEMINI.md").write_text(CONTEXT.format(
        name=pack["name"], prefix=pack["prefix"], profile=pack["profile"],
        stem=pack["profile"].split(".")[0]), encoding="utf-8")

    manifest = {
        "name": pack["name"],
        "version": VERSION,
        "description": pack["description"],
        "contextFileName": "GEMINI.md",
    }
    (dst / "gemini-extension.json").write_text(json.dumps(manifest, indent=2) + "\n",
                                               encoding="utf-8")

    counts = {p: len(list((dst / p).glob(g))) for p, g in
              (("commands", "*.toml"), ("agents", "*.md"), ("skills", "*/SKILL.md"))}
    print("  {:<20} {commands:>3} commands  {agents:>3} agents  {skills:>3} skills".format(
        pack["name"], **counts))


README = """# AI Pack for Gemini CLI

Four independently installable Gemini CLI extensions, generated from the Claude packs. Each
`gemini/<pack>/` is a git submodule pointing at its own repository, with the extension
(`gemini-extension.json`) at the repository root:

| Extension | Repository | Commands |
|---|---|---|
{rows}

Each extension ships slash commands (`commands/*.toml`), skills, subagents (`agents/`), hooks
(`hooks/hooks.json`) and adoption templates (`templates/`).

> **Using Antigravity (CLI `agy` or the IDE)?** These are Gemini CLI extensions
> (`gemini-extension.json`); Antigravity has its own plugin format and does not load them. Use
> [ai-pack-antigravity]({github}/ai-pack-antigravity) instead.

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
gemini extensions install {github}/ai-pack-gemini-vibe          # from GitHub
gemini extensions install ./gemini/vibe-standard                # from a clone (--recurse-submodules)
gemini extensions link    ./gemini/vibe-standard                # symlink, for pack development
gemini extensions update vibe-standard                          # after a new version is pushed
```

The repositories are private: installing from GitHub needs `git` credentials with access to them.

### From the chat

Inside a `gemini` session the same operations are slash commands:

```text
/extensions install {github}/ai-pack-gemini-vibe
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
  `GEMINI_MODEL`, or `"model": {{ "name": "<model>" }}` in `~/.gemini/settings.json`.
- **Thinking (effort):** there is no per-session switch; set a thinking budget in
  `settings.json`, globally or for one agent by name:

  ```json
  "modelConfigs": {{
    "overrides": [
      {{
        "match": {{ "overrideScope": "sdlc-reviewer" }},
        "modelConfig": {{ "generateContentConfig": {{ "thinkingConfig": {{ "thinkingBudget": 8192 }} }} }}
      }}
    ]
  }}
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
"""


def main():
    OUT.mkdir(exist_ok=True)
    print("Building Gemini extensions into {}".format(OUT.relative_to(ROOT)))
    for pack in PACKS:
        build(pack)
    prefixes = {"sdlc": "development lifecycle, traceability, design and test gates",
                "mig": "evidence-led legacy migration",
                "pm": "project governance and controls",
                "vibe": "fast AI-assisted delivery with safety rails"}
    rows = "\n".join("| `{}` | [{}]({}/{}) | `/{}-*` — {} |".format(
        p["name"], repo_name(p), GITHUB, repo_name(p), p["prefix"], prefixes[p["prefix"]])
        for p in PACKS)
    (OUT / "README.md").write_text(README.format(rows=rows, github=GITHUB), encoding="utf-8")


if __name__ == "__main__":
    main()
