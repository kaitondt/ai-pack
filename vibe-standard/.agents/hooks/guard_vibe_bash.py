#!/usr/bin/env python3
"""PreToolUse guard: irreversible commands are run by the human (SB-02).

Blocks shell commands that destroy data or state a git checkpoint cannot restore:
recursive deletes of root/home/cwd, hard resets and cleans over unsaved work, force pushes,
dropping or truncating tables, unscoped DELETEs, ORM/database resets, infrastructure
destroy/apply, package publishing, sudo, and piping downloads into a shell - plus any
pattern listed in security.dangerous_commands in the profile (e.g. the production deploy).

Exit 2 blocks the tool call and returns stderr to the model.
"""
import sys, json, os, re

ROOT = os.environ.get("CLAUDE_PROJECT_DIR", ".")
PROFILE = os.path.join(ROOT, ".claude", "vibe.profile.yaml")

BUILTIN = [
    (r"\brm\s+-(?:[a-zA-Z]*r[a-zA-Z]*f|[a-zA-Z]*f[a-zA-Z]*r)[a-zA-Z]*\s+"
     r"(?:/(?=\s|$)|/\*|~|\$HOME|\*(?=\s|$)|\.\.?(?=\s|$)|\.\./)",
     "recursive delete of root, home, the working directory or its parent"),
    (r"(?i)\bRemove-Item\b[^|;]*-Recurse[^|;]*\s(?:~|\$HOME|\$env:USERPROFILE|[A-Za-z]:\\?|\.\.?)(?=\s|$)",
     "recursive delete of a drive, home or the working directory"),
    (r"\bgit\s+reset\s+(?:\S+\s+)*--hard\b", "git reset --hard discards uncommitted work"),
    (r"\bgit\s+clean\s+(?:\S+\s+)*-[a-zA-Z]*f", "git clean -f deletes untracked files"),
    (r"\bgit\s+checkout\s+(?:--\s+)?\.(?=\s|$)", "git checkout . discards all local changes"),
    (r"\bgit\s+restore\s+\.(?=\s|$)", "git restore . discards all local changes"),
    (r"\bgit\s+stash\s+(?:drop|clear)\b", "dropping stashes deletes saved work"),
    (r"\bgit\s+push\b[^\n;&|]*\s(?:--force(?!-with-lease)|-f)(?=\s|$)", "force push rewrites shared history"),
    (r"(?i)\bdrop\s+(?:database|schema|table)\b", "DROP destroys data"),
    (r"(?i)\btruncate\s+table\b|\bTRUNCATE\s+[\w.\"`]+\s*;", "TRUNCATE destroys data"),
    (r"(?i)\bdelete\s+from\s+[\w.\"`]+\s*(?:;|\"|'|$)", "DELETE without WHERE"),
    (r"\bprisma\s+migrate\s+reset\b", "prisma migrate reset drops the database"),
    (r"--accept-data-loss\b", "--accept-data-loss"),
    (r"\bdrizzle-kit\s+drop\b", "drizzle-kit drop"),
    (r"\b(?:rails|rake)\s+db:(?:drop|reset|purge)\b", "database drop/reset"),
    (r"\bmanage\.py\s+(?:flush|reset_db)\b", "Django database flush"),
    (r"\bsupabase\s+db\s+reset\b", "supabase db reset"),
    (r"\bterraform\s+(?:destroy|apply)\b", "terraform changes real infrastructure"),
    (r"\bpulumi\s+(?:destroy|up)\b", "pulumi changes real infrastructure"),
    (r"\bkubectl\s+delete\b", "kubectl delete"),
    (r"\bhelm\s+(?:uninstall|delete)\b", "helm uninstall"),
    (r"\bdocker\s+(?:system|volume)\s+prune\b", "docker prune deletes volumes/images"),
    (r"\bdocker[- ]compose\s+down\b[^\n;&|]*\s-v\b", "compose down -v deletes volumes"),
    (r"\b(?:npm|pnpm|yarn|bun)\s+publish\b", "publishing a package is irreversible"),
    (r"\b(?:twine\s+upload|cargo\s+publish|gem\s+push)\b", "publishing a package is irreversible"),
    (r"\bsudo\b", "system changes via sudo"),
    (r"\bmkfs\b|\bdd\s+if=|\bFormat-Volume\b", "disk-level write"),
    (r"\bchmod\s+-R\s+777\b", "chmod -R 777"),
    (r"\b(?:curl|wget|iwr|Invoke-WebRequest)\b[^|\n]*\|\s*(?:sudo\s+)?(?:ba|z)?sh\b", "piping a download into a shell"),
    (r":\(\)\s*\{\s*:\|:&\s*\};:", "fork bomb"),
]


def read_list(key):
    """Minimal extraction of a YAML list under `key:` without a yaml dependency."""
    if not os.path.exists(PROFILE):
        return []
    out, in_block, indent = [], False, 0
    with open(PROFILE, encoding="utf-8") as fh:
        for line in fh:
            m = re.match(r"^(\s*){}:\s*(.*)$".format(re.escape(key)), line)
            if m and not in_block:
                rest = m.group(2).split("#")[0].strip()
                if rest.startswith("["):
                    return [unquote(v) for v in re.findall(r"\"(?:[^\"\\]|\\.)*\"|'[^']*'|[^,\[\]\s]+", rest)]
                in_block, indent = True, len(m.group(1))
                continue
            if in_block:
                if not line.strip() or line.strip().startswith("#"):
                    continue
                item = re.match(r"^(\s*)-\s+(.+?)\s*$", line)
                if item and len(item.group(1)) >= indent:
                    out.append(unquote(item.group(2)))
                    continue
                break
    return out


def unquote(v):
    v = v.strip()
    if len(v) >= 2 and v[0] == '"' and v[-1] == '"':
        return v[1:-1].replace("\\\\", "\\").replace('\\"', '"')
    if len(v) >= 2 and v[0] == "'" and v[-1] == "'":
        return v[1:-1]
    return v


def main():
    try:
        data = json.loads(sys.stdin.buffer.read().decode("utf-8"))
    except Exception:
        return 0
    cmd = str(data.get("tool_input", {}).get("command", ""))
    if not cmd:
        return 0

    rules = list(BUILTIN)
    for pat in read_list("dangerous_commands"):
        rules.append((pat, "listed in security.dangerous_commands"))

    for pat, why in rules:
        try:
            hit = re.search(pat, cmd)
        except re.error:
            continue
        if hit:
            sys.stderr.write(
                "[SB-02] BLOCKED: this command is irreversible ({}).\n"
                "  matched: {}\n"
                "Irreversible operations are run by the human. Show the user the exact command, "
                "what it will destroy, and how it could be undone - then ask them to run it "
                "themselves.\n"
                "To abandon a failed attempt, do not reset: commit it to an "
                "'attempt/<slice>-<n>' branch and switch back (/vibe_unstuck).\n".format(
                    why, hit.group(0).strip()))
            return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
