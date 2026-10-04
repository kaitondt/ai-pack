#!/usr/bin/env python3
"""PostToolUse check: is the working tree still one slice? (SS-02)

Non-blocking. After each file write, measures the change since the last commit - tracked
diff plus untracked files, minus slices.exclude_from_budget - and, when it passes
slices.max_files or slices.max_changed_lines, tells the model once (and again at double the
budget) so it stops and splits instead of growing the slice.
"""
import sys, json, os, re, subprocess, fnmatch

ROOT = os.environ.get("CLAUDE_PROJECT_DIR", ".")
PROFILE = os.path.join(ROOT, ".claude", "vibe.profile.yaml")
MARKER = os.path.join(ROOT, ".claude", ".slice_warned")

DEFAULT_EXCLUDE = ["vibe/**", "*.lock", "package-lock.json", "pnpm-lock.yaml", "**/migrations/**",
                   "**/__snapshots__/**", "**/*.generated.*"]


def read_scalar(key, default):
    if not os.path.exists(PROFILE):
        return default
    with open(PROFILE, encoding="utf-8") as fh:
        for line in fh:
            m = re.match(r"^\s*{}:\s*[\"']?([^\"'#\s]+)".format(re.escape(key)), line)
            if m:
                return m.group(1)
    return default


def read_list(key, default):
    if not os.path.exists(PROFILE):
        return default
    out, in_block, indent = [], False, 0
    with open(PROFILE, encoding="utf-8") as fh:
        for line in fh:
            m = re.match(r"^(\s*){}:\s*(.*)$".format(re.escape(key)), line)
            if m and not in_block:
                in_block, indent = True, len(m.group(1))
                continue
            if in_block:
                if not line.strip() or line.strip().startswith("#"):
                    continue
                item = re.match(r"^(\s*)-\s+[\"']?([^\"'#]+?)[\"']?\s*$", line)
                if item and len(item.group(1)) >= indent:
                    out.append(item.group(2).strip())
                    continue
                break
    return out or default


def git(*args):
    r = subprocess.run(["git", "-C", ROOT] + list(args), capture_output=True, text=True,
                       encoding="utf-8", errors="replace", timeout=8)
    if r.returncode != 0:
        raise RuntimeError(r.stderr)
    return r.stdout


def excluded(path, patterns):
    p = path.replace("\\", "/")
    for pat in patterns:
        if fnmatch.fnmatch(p, pat) or fnmatch.fnmatch(os.path.basename(p), pat):
            return True
        if pat.startswith("**/") and fnmatch.fnmatch(p, "*/" + pat[3:]):
            return True
        if pat.startswith("**/") and fnmatch.fnmatch(p, pat[3:]):
            return True
    return False


def count_lines(path):
    try:
        with open(os.path.join(ROOT, path), "rb") as fh:
            chunk = fh.read(2_000_000)
        if b"\0" in chunk[:8000]:
            return 0
        return chunk.count(b"\n") + (1 if chunk and not chunk.endswith(b"\n") else 0)
    except Exception:
        return 0


def main():
    try:
        sys.stdin.buffer.read()
    except Exception:
        pass
    if not os.path.exists(PROFILE):
        return 0
    try:
        head = git("rev-parse", "HEAD").strip()
        numstat = git("diff", "--numstat", "HEAD")
        untracked = git("ls-files", "--others", "--exclude-standard").splitlines()
    except Exception:
        return 0

    exclude = read_list("exclude_from_budget", DEFAULT_EXCLUDE)
    files, lines = set(), 0
    for row in numstat.splitlines():
        parts = row.split("\t")
        if len(parts) < 3 or parts[2].startswith(".claude/") or excluded(parts[2], exclude):
            continue
        files.add(parts[2])
        lines += sum(int(x) for x in parts[:2] if x.isdigit())
    for path in untracked:
        if path.startswith(".claude/") or excluded(path, exclude):
            continue
        files.add(path)
        lines += count_lines(path)

    try:
        max_files = int(read_scalar("max_files", "8"))
        max_lines = int(read_scalar("max_changed_lines", "400"))
    except ValueError:
        return 0

    level = 0
    if len(files) > max_files or lines > max_lines:
        level = 1
    if len(files) > 2 * max_files or lines > 2 * max_lines:
        level = 2
    if level == 0:
        return 0

    key = "{}:{}".format(head, level)
    try:
        if os.path.exists(MARKER) and open(MARKER, encoding="utf-8").read().strip() == key:
            return 0
        with open(MARKER, "w", encoding="utf-8") as fh:
            fh.write(key)
    except Exception:
        pass

    msg = ("[SS-02] Slice budget exceeded{}: {} files (max {}), {} changed lines (max {}) since "
           "commit {}. Stop adding to this slice. Either commit what runs now and continue in "
           "the next slice, or split the slice in the intent (/vibe-plan). If the slice truly "
           "cannot be smaller, record why as a DEBT-*.").format(
               " by 2x" if level == 2 else "", len(files), max_files, lines, max_lines, head[:7])
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PostToolUse",
                                             "additionalContext": msg}}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
