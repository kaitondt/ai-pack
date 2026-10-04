#!/usr/bin/env python3
"""PreToolUse guard: no secrets in files, no writes to protected paths (SB-01).

Two protections:
  1. security.protected_paths globs -> always denied (generated / vendored code).
  2. Content being written that contains a recognisable credential -> denied, unless the
     target is one of security.env_files (gitignored local env files). .env.example is never
     exempt: it holds names, not values.

Exit 2 blocks the tool call and returns stderr to the model.
"""
import sys, json, os, re, fnmatch

ROOT = os.environ.get("CLAUDE_PROJECT_DIR", ".")
PROFILE = os.path.join(ROOT, ".claude", "vibe.profile.yaml")

DEFAULT_ENV_FILES = [".env", ".env.local", ".env.development.local", ".env.test.local"]
DEFAULT_PROTECTED = ["**/*.generated.*"]

SECRETS = [
    ("AWS access key", r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b"),
    ("GitHub token", r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{36,}\b"),
    ("GitHub fine-grained token", r"\bgithub_pat_[A-Za-z0-9_]{50,}"),
    ("Anthropic API key", r"\bsk-ant-[A-Za-z0-9_\-]{20,}"),
    ("OpenAI-style API key", r"\bsk-(?:proj-|svcacct-)?[A-Za-z0-9_\-]{32,}"),
    ("Stripe live key", r"\b(?:sk|rk)_live_[A-Za-z0-9]{20,}"),
    ("Slack token", r"\bxox[abprs]-[A-Za-z0-9-]{10,}"),
    ("Google API key", r"\bAIza[0-9A-Za-z_\-]{35}\b"),
    ("SendGrid key", r"\bSG\.[A-Za-z0-9_\-]{22}\.[A-Za-z0-9_\-]{43}\b"),
    ("private key", r"-----BEGIN (?:RSA |EC |DSA |OPENSSH |PGP |ENCRYPTED )?PRIVATE KEY-----"),
]

# name = "long random value" - only when the value looks random, not like a placeholder.
GENERIC = re.compile(
    r"(?i)\b(api[_-]?key|secret(?:[_-]?key)?|access[_-]?token|auth[_-]?token|client[_-]?secret"
    r"|private[_-]?key|password|passwd)\b[\"']?\s*[:=]\s*[\"']([^\"'\s]{16,})[\"']")
PLACEHOLDER = re.compile(
    r"(?i)your|example|change.?me|placeholder|xxx|dummy|fake|sample|redacted|replace|<|\$\{"
    r"|process\.env|os\.environ|getenv|env\(|\*\*\*|test_|_test|todo")

# Documented example keys (AWS's AKIAIOSFODNN7EXAMPLE) and deliberately fake fixtures.
OBVIOUS_FAKE = re.compile(r"(?i)example|fake|dummy|xxxxx|00000000|placeholder")

CONN = re.compile(r"\b(?:postgres(?:ql)?|mysql|mariadb|mongodb(?:\+srv)?|redis|amqp)://"
                  r"[^\s:/@]+:([^\s@/]{6,})@([^\s/:?]+)")
LOCAL_HOSTS = re.compile(r"(?i)^(?:localhost|127\.0\.0\.1|0\.0\.0\.0|db|database|postgres|mysql"
                         r"|mongo|mongodb|redis|rabbitmq|host\.docker\.internal)$")


def read_list(key, default):
    if not os.path.exists(PROFILE):
        return default
    out, in_block, indent = [], False, 0
    with open(PROFILE, encoding="utf-8") as fh:
        for line in fh:
            m = re.match(r"^(\s*){}:\s*(.*)$".format(re.escape(key)), line)
            if m and not in_block:
                rest = m.group(2).split("#")[0].strip()
                if rest.startswith("["):
                    vals = [v.strip().strip("\"'") for v in rest.strip("[]").split(",")]
                    return [v for v in vals if v] or default
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


def matches(path, pattern):
    p = path.replace("\\", "/")
    pat = pattern.replace("\\", "/")
    if fnmatch.fnmatch(p, pat) or fnmatch.fnmatch(p, "*/" + pat.lstrip("/")):
        return True
    if pat.startswith("**/") and fnmatch.fnmatch(os.path.basename(p), pat[3:]):
        return True
    if pat.endswith("/**"):
        base = pat[:-3].lstrip("./")
        return ("/" + base + "/") in ("/" + p.lstrip("/")) or p.lstrip("./").startswith(base + "/")
    return False


def written_text(tool_input):
    parts = [tool_input.get("content", ""), tool_input.get("new_string", "")]
    for e in tool_input.get("edits", []) or []:
        if isinstance(e, dict):
            parts.append(e.get("new_string", ""))
    return "\n".join(str(p) for p in parts if p)


def find_secret(text):
    for name, pat in SECRETS:
        for m in re.finditer(pat, text):
            if not OBVIOUS_FAKE.search(m.group(0)):
                return name, m.group(0)
    for m in GENERIC.finditer(text):
        val = m.group(2)
        if PLACEHOLDER.search(val):
            continue
        if re.search(r"[A-Za-z]", val) and re.search(r"[0-9]", val):
            return "hardcoded {}".format(m.group(1)), val
    for m in CONN.finditer(text):
        if not LOCAL_HOSTS.match(m.group(2)) and not PLACEHOLDER.search(m.group(1)):
            return "database URL with password", m.group(0)
    return None


def redact(s):
    s = s.strip()
    return s[:6] + "..." + "*" * 6 if len(s) > 8 else "***"


def main():
    try:
        data = json.loads(sys.stdin.buffer.read().decode("utf-8"))
    except Exception:
        return 0
    ti = data.get("tool_input", {}) or {}
    fp = str(ti.get("file_path", ""))
    if not fp:
        return 0
    norm = fp.replace("\\", "/")

    for pattern in read_list("protected_paths", DEFAULT_PROTECTED):
        if matches(norm, pattern):
            sys.stderr.write(
                "[vibe] BLOCKED: {} matches protected path '{}' (security.protected_paths).\n"
                "Generated or vendored files are not hand-edited. Change the generator's input "
                "and regenerate, or ask the user to change the profile if this path should be "
                "writable.\n".format(fp, pattern))
            return 2

    base = os.path.basename(norm)
    env_files = read_list("env_files", DEFAULT_ENV_FILES)
    if base in env_files and not base.endswith(".example"):
        return 0

    hit = find_secret(written_text(ti))
    if hit:
        sys.stderr.write(
            "[SB-01] BLOCKED: the content for {} contains what looks like a credential: {} ({}).\n"
            "Secrets never go into source, tests, docs or .env.example. Read it from an "
            "environment variable, put the real value only in a gitignored env file ({}), and "
            "add the variable NAME to .env.example.\n"
            "For a test fixture use an obviously fake value (e.g. 'sk_test_FAKE').\n"
            "If this was a real key that has been pasted into the conversation, tell the user "
            "to rotate it.\n".format(fp, hit[0], redact(hit[1]), ", ".join(env_files)))
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
