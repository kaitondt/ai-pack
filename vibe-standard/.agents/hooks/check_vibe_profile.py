#!/usr/bin/env python3
"""SessionStart: load the project's memory into the first turn (SC-02).

Non-blocking. Prints:
  - whether the profile exists and is usable (stage, placeholders)
  - reality-vs-stage and .env hygiene warnings
  - the working tree and branch state
  - open debt and bug counts
  - the head of STATE.md, so the session starts from the handoff instead of from nothing
"""
import sys, os, re, subprocess

ROOT = os.environ.get("CLAUDE_PROJECT_DIR", ".")
PROFILE = os.path.join(ROOT, ".claude", "vibe.profile.yaml")
STAGES = ("spike", "prototype", "mvp", "production")
STATE_LINES = 45


def scalar(text, key, default=""):
    m = re.search(r"^\s*{}:\s*[\"']?([^\"'#\n]*?)[\"']?\s*(?:#.*)?$".format(re.escape(key)),
                  text, re.MULTILINE)
    return m.group(1).strip() if m else default


def md_path(text, key, default):
    m = re.search(r"^\s*{}:\s*[\"']?([^\"'#\n]+\.md)".format(re.escape(key)), text, re.MULTILINE)
    return m.group(1).strip() if m else default


def git(*args):
    try:
        r = subprocess.run(["git", "-C", ROOT] + list(args), capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=8)
        return r.stdout if r.returncode == 0 else None
    except Exception:
        return None


def read(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return fh.read()
    except Exception:
        return None


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    text = read(PROFILE)
    if text is None:
        print("[vibe] No .claude/vibe.profile.yaml found. The Vibe Skill Pack is installed but "
              "not configured - run /vibe_init before building anything.")
        return 0

    issues = []
    stage = scalar(text, "stage")
    if stage not in STAGES:
        issues.append("stage is '{}' - must be one of {}".format(stage or "missing", ", ".join(STAGES)))

    ph = sorted(set(re.findall(r"^\s*([a-z_]+):\s*[\"']?<[^>]+>", text, re.MULTILINE)))
    if ph:
        issues.append("{} unfilled field(s): {}".format(len(ph), ", ".join(ph[:8])))

    if scalar(text, "public_url").lower() == "true" and stage in ("spike", "prototype"):
        issues.append("product.public_url is true at stage '{}' - mvp security applies (SB-07)".format(stage))

    gi = read(os.path.join(ROOT, ".gitignore")) or ""
    if not re.search(r"^\s*/?\.env(\*|\.\*|\s*$)", gi, re.MULTILINE):
        issues.append(".gitignore does not ignore .env files (SB-01)")

    if issues:
        print("[vibe] Profile issues:")
        for i in issues:
            print("  - " + i)
        print("  Run /vibe_profile_check for the full validation.")

    branch = (git("branch", "--show-current") or "").strip()
    status = git("status", "--porcelain")
    head = (git("log", "-1", "--format=%h %s") or "").strip()
    line = "[vibe] stage: {} · branch: {} · HEAD: {}".format(stage or "?", branch or "?", head or "?")
    if status is not None:
        n = len([l for l in status.splitlines() if l.strip() and ".claude/.slice_warned" not in l])
        line += " · tree: {}".format("clean" if n == 0 else "{} uncommitted change(s)".format(n))
    print(line)
    if branch.startswith("attempt/"):
        print("[vibe] On an attempt/ branch - this holds a failed attempt (SS-05). "
              "Switch back before building.")
    if branch.startswith("spike/"):
        print("[vibe] On a spike/ branch - throwaway code; never merge it as-is.")

    debt = read(os.path.join(ROOT, md_path(text, "debt", "vibe/debt.md")))
    if debt:
        rows = [r for r in debt.splitlines() if re.match(r"^\|\s*DEBT-\d+", r)]
        open_rows = [r for r in rows if re.search(r"\|\s*open\s*\|?\s*$", r)]
        sec = [r for r in open_rows if re.search(r"\|\s*security\s*\|", r)]
        if open_rows:
            print("[vibe] Debt: {} open ({} security).".format(len(open_rows), len(sec)))

    bugs = read(os.path.join(ROOT, md_path(text, "bugs", "vibe/bugs.md")))
    if bugs:
        n = len(re.findall(r"^BUG-\d+\s*·[^\n]*·\s*open\b", bugs, re.MULTILINE))
        if n:
            print("[vibe] Open bugs: {}.".format(n))

    state = read(os.path.join(ROOT, md_path(text, "state", "vibe/STATE.md")))
    if state:
        lines = state.splitlines()
        print("[vibe] Handoff from STATE.md (read before acting; report if git disagrees):")
        print("\n".join(lines[:STATE_LINES]))
        if len(lines) > STATE_LINES:
            print("  ... ({} more lines in STATE.md)".format(len(lines) - STATE_LINES))
    elif stage in ("prototype", "mvp", "production"):
        print("[vibe] No STATE.md - the next session will start blind. Write one with /vibe_handoff.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
