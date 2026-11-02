#!/usr/bin/env python3
"""Copy AI Pack packs into a project's .claude/ — the install for when the plugin is not used.

Source is packs/<pack>/.claude/ plus the profile template packs/<pack>/profile/<name>.profile.yaml.
Existing project files are never overwritten unless --force is given; settings.json hooks are
merged, not replaced, so packs can be installed one after the other.

    python scripts/install-claude-project.py <project> sdlc-standard
    python scripts/install-claude-project.py <project> sdlc-standard pm-standard
    python scripts/install-claude-project.py <project> all --dry-run
    python scripts/install-claude-project.py <project> vibe-standard --force   # update a copy

Then, in the project, run /<prefix>-init (sdlc, mig, pm, vibe).

Do not install the same pack as a plugin as well: the hooks would run twice.
"""
import argparse
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PACKS = {
    "sdlc-standard": ("sdlc", "sdlc.profile.yaml"),
    "migration-standard": ("mig", "migration.profile.yaml"),
    "pm-standard": ("pm", "pm.profile.yaml"),
    "vibe-standard": ("vibe", "vibe.profile.yaml"),
}
SKIP_DIRS = {"__pycache__"}
SKIP_SUFFIXES = {".pyc"}
# Files that belong to the project once it exists; copied only when absent, even with --force.
PROJECT_OWNED = {"CLAUDE.md", "settings.json"}


class Report:
    def __init__(self, dry_run):
        self.dry_run = dry_run
        self.added, self.updated, self.kept = [], [], []

    def line(self, verb, path):
        print("  {:<8} {}".format(verb + ("*" if self.dry_run else ""), path))


def same(a, b):
    return a.read_bytes() == b.read_bytes()


def copy_file(src, dst, rel, force, report):
    if dst.exists():
        if same(src, dst):
            return
        if not force:
            report.kept.append(rel)
            report.line("keep", rel)
            return
        report.updated.append(rel)
        report.line("update", rel)
    else:
        report.added.append(rel)
        report.line("add", rel)
    if not report.dry_run:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)


def copy_tree(src_root, dst_root, force, report):
    for src in sorted(src_root.rglob("*")):
        if not src.is_file():
            continue
        parts = src.relative_to(src_root).parts
        if SKIP_DIRS.intersection(parts) or src.suffix in SKIP_SUFFIXES:
            continue
        if src.name in PROJECT_OWNED and len(parts) == 1:
            continue
        rel = Path(".claude", *parts).as_posix()
        copy_file(src, dst_root.joinpath(*parts), rel, force, report)


def merge_hooks(existing, incoming):
    """Add incoming hook groups to existing ones, skipping a hook command already present."""
    merged = json.loads(json.dumps(existing))
    for event, groups in incoming.items():
        target = merged.setdefault(event, [])
        have = {h.get("command") for g in target for h in g.get("hooks", [])}
        for group in groups:
            fresh = [h for h in group.get("hooks", []) if h.get("command") not in have]
            if not fresh:
                continue
            same_matcher = next((g for g in target
                                 if g.get("matcher") == group.get("matcher")), None)
            if same_matcher is not None:
                same_matcher.setdefault("hooks", []).extend(fresh)
            else:
                target.append(dict(group, hooks=fresh))
            have.update(h.get("command") for h in fresh)
    return merged


def install_settings(src_claude, project_claude, report):
    src = src_claude / "settings.json"
    if not src.exists():
        return
    incoming = json.loads(src.read_text(encoding="utf-8")).get("hooks", {})
    dst = project_claude / "settings.json"
    rel = ".claude/settings.json"
    if dst.exists():
        current = json.loads(dst.read_text(encoding="utf-8"))
        merged = dict(current, hooks=merge_hooks(current.get("hooks", {}), incoming))
        if merged == current:
            return
        verb = "merge"
    else:
        merged = {"hooks": incoming}
        verb = "add"
    report.line(verb, rel)
    if not report.dry_run:
        project_claude.mkdir(parents=True, exist_ok=True)
        dst.write_text(json.dumps(merged, indent=2) + "\n", encoding="utf-8")


def install_claude_md(src_claude, project_claude, report):
    src = src_claude / "CLAUDE.md"
    dst = project_claude / "CLAUDE.md"
    if not src.exists():
        return
    if dst.exists():
        return
    # The pack's CLAUDE.md goes to the project root as CLAUDE.md only through /<prefix>-init,
    # which fills it from the profile. Here it is kept as the .claude/ copy the init reads.
    report.line("add", ".claude/CLAUDE.md")
    if not report.dry_run:
        project_claude.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)


def install_pack(name, project, force, report):
    prefix, profile = PACKS[name]
    src = ROOT / "packs" / name
    src_claude = src / ".claude"
    if not src_claude.is_dir():
        sys.exit("pack source not found: {}".format(src_claude))
    project_claude = project / ".claude"

    print("{} (/{}-init)".format(name, prefix))
    copy_tree(src_claude, project_claude, force, report)
    install_settings(src_claude, project_claude, report)
    install_claude_md(src_claude, project_claude, report)
    # The profile is the project's own once it is filled in: never replaced, not even by --force.
    copy_file(src / "profile" / profile, project_claude / profile,
              ".claude/" + profile, False, report)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("project", help="project directory to install into")
    ap.add_argument("packs", nargs="+", metavar="pack",
                    help="{} or all".format(" | ".join(PACKS)))
    ap.add_argument("--force", action="store_true",
                    help="overwrite files that differ from the pack (profile, CLAUDE.md and "
                         "settings.json are never overwritten)")
    ap.add_argument("--dry-run", action="store_true", help="print what would change, write nothing")
    args = ap.parse_args()

    names = list(PACKS) if "all" in args.packs else args.packs
    unknown = [n for n in names if n not in PACKS]
    if unknown:
        sys.exit("unknown pack: {} (expected: {} or all)".format(", ".join(unknown), ", ".join(PACKS)))
    if "sdlc-standard" in names and "migration-standard" in names:
        print("warning: sdlc-standard and migration-standard share hook file names; install "
              "one of them per project.", file=sys.stderr)

    project = Path(args.project).resolve()
    if not project.is_dir():
        sys.exit("not a directory: {}".format(project))

    report = Report(args.dry_run)
    print("Installing into {}{}".format(project, "  (dry run, * = not written)" if args.dry_run else ""))
    for name in dict.fromkeys(names):
        install_pack(name, project, args.force, report)

    print("\n{} added, {} updated, {} kept (differs from the pack; use --force to overwrite)".format(
        len(report.added), len(report.updated), len(report.kept)))
    if not args.dry_run:
        print("Next: open the project in Claude Code and run /{}-init".format(
            PACKS[names[0]][0]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
