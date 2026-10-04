#!/usr/bin/env python3
"""SessionStart check: is the migration profile present and usable?

Non-blocking. Reports missing profile, remaining <...> placeholders, and an unsafe
legacy.readonly setting, so a session does not get half-way into a phase before
discovering the pack is not configured.
"""
import sys, os, re

PROFILE = os.path.join(os.environ.get("CODEX_PROJECT_DIR", "."),
                       ".codex", "migration.profile.yaml")


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    if not os.path.exists(PROFILE):
        print("[mig] No .codex/migration.profile.yaml found. "
              "The Migration Skill Pack is installed but not configured — "
              "run /mig_init before starting any phase.")
        return 0

    with open(PROFILE, encoding="utf-8") as fh:
        text = fh.read()

    problems = []

    placeholders = re.findall(r"^\s*([a-z_]+):\s*[\"']?<[^>]+>", text, re.MULTILINE)
    if placeholders:
        problems.append("{} unfilled placeholder field(s): {}".format(
            len(placeholders), ", ".join(sorted(set(placeholders))[:8])))

    m = re.search(r"^\s*readonly:\s*(\S+)", text, re.MULTILINE)
    if m and m.group(1).strip().lower() not in ("true", "yes"):
        problems.append("legacy.readonly is not true — the read-only safety model is off")

    if re.search(r"^\s*auto_version_bump:\s*true", text, re.MULTILINE):
        problems.append("document.auto_version_bump is true — versions will bump without "
                        "an explicit instruction (DS-02)")

    for entry in re.findall(r"-\s+id:\s*\"\"\s*\n\s+reason:\s*\"\"", text):
        problems.append("legacy.excluded has an empty template entry — remove it or fill it")
        break

    if problems:
        print("[mig] Profile loaded with issues:")
        for p in problems:
            print("  - " + p)
        print("  Run /mig_profile_check for the full validation.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
