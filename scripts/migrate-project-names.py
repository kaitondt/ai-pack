#!/usr/bin/env python3
"""Migrate a project adopted with pack version 1.x (snake_case names) to 2.x (kebab-case).

Version 2.0.0 renamed every command, skill, agent and hook from snake_case to kebab-case
(/vibe_build -> /vibe-build, vibe_project -> vibe-project). Files the pack copied or generated
into the project still carry the old names; this script rewrites them.

    python scripts/migrate-project-names.py <project-dir>            # preview only
    python scripts/migrate-project-names.py <project-dir> --apply    # write the changes
    python scripts/migrate-project-names.py <project-dir> --docs     # also other *.md files

Scope (always): CLAUDE.md and everything under .claude/ except the profile files — profile keys
such as vibe_root or pm_root are NOT names and stay as they are. With --docs it also rewrites
mentions in the project's other Markdown files (intents, ledgers, reports).
Agent/skill/command/hook overrides under .claude/ are renamed to the new file names too.
"""
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PACKS = ["sdlc-standard", "migration-standard", "pm-standard", "vibe-standard"]
TEXT = {".md", ".json", ".py", ".txt"}
SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__", "dist", "build"}


def pack_names():
    """Old snake_case name -> new kebab-case name, from the current pack sources."""
    names = {}
    for pack in PACKS:
        claude = ROOT / pack / ".claude"
        found = [p.stem for p in (claude / "commands").glob("*.md")]
        found += [p.stem for p in (claude / "agents").glob("*.md")]
        found += [p.name for p in (claude / "skills").iterdir() if p.is_dir()]
        found += [p.stem for p in (claude / "hooks").glob("*.py")]
        for new in found:
            if "-" in new:
                names[new.replace("-", "_")] = new
    names["_run_hook"] = "run-hook"
    return names


def build_rewriter(names):
    rx = re.compile(r"(?<![A-Za-z0-9_])(" + "|".join(
        map(re.escape, sorted(names, key=len, reverse=True))) + r")(?![A-Za-z0-9_])")
    wild = re.compile(r"(?<![A-Za-z0-9_])((?:sdlc|mig|pm|vibe)(?:_[a-z]+)*)_\*")

    def rewrite(text):
        text = rx.sub(lambda m: names[m.group(1)], text)
        return wild.sub(lambda m: m.group(1).replace("_", "-") + "-*", text)
    return rewrite


def candidate_files(project, docs):
    claude = project / ".claude"
    files = [project / "CLAUDE.md"] if (project / "CLAUDE.md").exists() else []
    if claude.is_dir():
        files += [p for p in claude.rglob("*") if p.is_file() and p.suffix in TEXT]
    if docs:
        for p in project.rglob("*.md"):
            rel = p.relative_to(project).parts
            if rel[0] == ".claude" or p.name == "CLAUDE.md" or SKIP_DIRS.intersection(rel):
                continue
            files.append(p)
    return files


def renames(project, names):
    """Overrides copied into .claude/{agents,commands,hooks,skills} with an old name."""
    out = []
    claude = project / ".claude"
    for sub, is_dir in (("agents", False), ("commands", False), ("hooks", False), ("skills", True)):
        base = claude / sub
        if not base.is_dir():
            continue
        for p in base.iterdir():
            stem = p.name if is_dir else p.stem
            if p.is_dir() == is_dir and stem in names:
                target = base / (names[stem] + ("" if is_dir else p.suffix))
                out.append((p, target))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("project", type=Path)
    ap.add_argument("--apply", action="store_true", help="write the changes (default: preview)")
    ap.add_argument("--docs", action="store_true", help="also rewrite other *.md in the project")
    args = ap.parse_args()

    project = args.project.resolve()
    if not (project / ".claude").is_dir():
        sys.exit("{} has no .claude/ directory - is it an adopted project?".format(project))

    names = pack_names()
    rewrite = build_rewriter(names)
    mode = "APPLY" if args.apply else "PREVIEW (nothing is written; add --apply)"
    print("Project: {}\nMode:    {}\n".format(project, mode))

    changed = 0
    for path in candidate_files(project, args.docs):
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        new = rewrite(text)
        if new == text:
            continue
        changed += 1
        before = re.findall(r"(?:sdlc|mig|pm|vibe)_[a-z_]+\*?|_run_hook", text)
        olds = sorted({w for w in before if rewrite(w) != w})
        print("  edit   {}  ({} name(s): {})".format(path.relative_to(project), len(olds),
                                                     ", ".join(olds[:6]) + (" ..." if len(olds) > 6 else "")))
        if args.apply:
            path.write_bytes(new.encode("utf-8"))

    moves = renames(project, names)
    for src, dst in moves:
        clash = " (SKIPPED: target exists)" if dst.exists() else ""
        print("  rename {} -> {}{}".format(src.relative_to(project), dst.name, clash))
        if args.apply and not clash:
            src.rename(dst)

    print("\n{} file(s) to edit, {} override(s) to rename.".format(changed, len(moves)))
    if not args.apply and (changed or moves):
        print("Review the list, commit or back up the project, then re-run with --apply.")


if __name__ == "__main__":
    main()
