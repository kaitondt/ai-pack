#!/usr/bin/env python3
"""SessionStart check: is the migration profile present and usable?

Non-blocking. Reports missing profile, remaining <...> placeholders, an unsafe
legacy.readonly setting, and the change request recorded in .claude/.active_cr, so a
session does not get half-way into a phase before discovering the pack is not configured
or that a CR is still open.
"""
import sys, os, re

PROFILE = os.path.join(os.environ.get("CLAUDE_PROJECT_DIR", "."),
                       ".claude", "migration.profile.yaml")
ACTIVE_CR = os.path.join(os.environ.get("CLAUDE_PROJECT_DIR", "."),
                         ".claude", ".active_cr")


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    if not os.path.exists(PROFILE):
        print("[mig] No .claude/migration.profile.yaml found. "
              "The Migration Skill Pack is installed but not configured — "
              "run /mig-init before starting any phase.")
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
        print("  Run /mig-profile-check for the full validation.")

    if os.path.exists(ACTIVE_CR):
        try:
            with open(ACTIVE_CR, encoding="utf-8") as fh:
                cr = fh.read().strip()
        except Exception:
            cr = ""
        if cr.upper() == "PENDING":
            print("[mig] A change request is open with no id yet (.claude/.active_cr = PENDING). "
                  "Its documents can be edited but not committed until the client's CR id is "
                  "written to the marker.")
        elif cr:
            print("[mig] Active change request: {} - commits touching "
                  "change_request.governed_paths must carry this id. /mig-cr-report clears "
                  ".claude/.active_cr when the CR is closed.".format(cr))
    return 0


if __name__ == "__main__":
    sys.exit(main())
