#!/usr/bin/env python3
"""SessionStart check: is the project profile present and usable?

Non-blocking. Reports a missing profile, remaining <...> placeholders, and settings that
switch off a safety rule, so a session does not get half-way into a phase before
discovering the pack is not configured.
"""
import sys, os, re

PROFILE = os.path.join(os.environ.get("CLAUDE_PROJECT_DIR", "."),
                       ".claude", "sdlc.profile.yaml")
ACTIVE_CR = os.path.join(os.environ.get("CLAUDE_PROJECT_DIR", "."),
                         ".claude", ".active_cr")


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    if not os.path.exists(PROFILE):
        print("[sdlc] No .claude/sdlc.profile.yaml found. "
              "The SDLC Skill Pack is installed but not configured - "
              "run /sdlc_init before starting any phase.")
        return 0

    with open(PROFILE, encoding="utf-8") as fh:
        text = fh.read()

    problems = []

    placeholders = re.findall(r"^\s*([a-z_]+):\s*[\"']?<[^>]+>", text, re.MULTILINE)
    if placeholders:
        problems.append("{} unfilled placeholder field(s): {}".format(
            len(placeholders), ", ".join(sorted(set(placeholders))[:8])))

    if re.search(r"^\s*auto_version_bump:\s*true", text, re.MULTILINE):
        problems.append("document.auto_version_bump is true - versions will bump without "
                        "an explicit instruction (DS-02)")

    m = re.search(r"^\s*baseline_change_requires_cr:\s*(\S+)", text, re.MULTILINE)
    if m and m.group(1).strip().lower() not in ("true", "yes"):
        problems.append("constraints.baseline_change_requires_cr is not true - baselined "
                        "documents can be edited without a change request (BL-02)")

    for _ in re.findall(r"-\s+item:\s*\"\"\s*\n\s+reason:\s*\"\"", text):
        problems.append("scope.out_of_scope has an empty template entry - remove it or fill it")
        break

    for _ in re.findall(r"-\s+path:\s*\"\"\s*\n\s+version:\s*\"\"", text):
        problems.append("constraints.baselined has an empty template entry - remove it "
                        "once the first document is baselined")
        break

    for role in ("business_owner", "product_owner", "architect", "qa_lead", "ops_owner"):
        if re.search(r"^\s*{}:\s*[\"']?<".format(role), text, re.MULTILINE):
            problems.append("stakeholders.{} is unset - decisions have no owner (RS-02)".format(role))
            break

    if problems:
        print("[sdlc] Profile loaded with issues:")
        for p in problems:
            print("  - " + p)
        print("  Run /sdlc_profile_check for the full validation.")

    if os.path.exists(ACTIVE_CR):
        try:
            with open(ACTIVE_CR, encoding="utf-8") as fh:
                cr = fh.read().strip()
        except Exception:
            cr = ""
        if cr:
            print("[sdlc] Active change request: {} - edits to baselined documents are "
                  "allowed and will be attributed to it. Clear .claude/.active_cr when "
                  "the CR is closed.".format(cr))
    return 0


if __name__ == "__main__":
    sys.exit(main())
