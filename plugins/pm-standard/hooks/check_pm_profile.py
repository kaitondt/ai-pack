#!/usr/bin/env python3
"""SessionStart check: is the project-management profile present and usable?

Non-blocking. Reports a missing profile, remaining <...> placeholders, unfilled governance
roles and settings that switch off a safety rule, so a session does not get half-way into a
planning task before discovering the pack is not configured.

Also reports an active change request, since that unblocks edits to baselined documents.
"""
import sys, os, re

ROOT = os.environ.get("CLAUDE_PROJECT_DIR", ".")
PROFILE = os.path.join(ROOT, ".claude", "pm.profile.yaml")
ACTIVE_CR = os.path.join(ROOT, ".claude", ".active_pm_cr")

GOVERNANCE_ROLES = ("sponsor", "client_pm", "project_manager", "technical_lead",
                    "qa_lead", "delivery_manager")


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    if not os.path.exists(PROFILE):
        print("[pm] No .claude/pm.profile.yaml found. The PM Skill Pack is installed but not "
              "configured - run /pm_init before any planning or reporting task.")
        return 0

    with open(PROFILE, encoding="utf-8") as fh:
        text = fh.read()

    problems = []

    # [^>\n] matters: a value like "< 5% first found in UAT" must not pair its "<" with a
    # ">" several lines later and report itself as an unfilled placeholder.
    placeholders = re.findall(r"^\s*([a-z_]+):\s*[\"']?<[^>\n]+>", text, re.MULTILINE)
    if placeholders:
        problems.append("{} unfilled placeholder field(s): {}".format(
            len(placeholders), ", ".join(sorted(set(placeholders))[:8])))

    for role in GOVERNANCE_ROLES:
        if re.search(r"^\s*{}:\s*[\"']?<".format(role), text, re.MULTILINE):
            problems.append("governance.{} is unset - decisions would have no owner "
                            "(DA-01)".format(role))
            break

    if re.search(r"^\s*auto_version_bump:\s*true", text, re.MULTILINE):
        problems.append("document.auto_version_bump is true - versions would bump without an "
                        "explicit instruction (MD-02)")

    m = re.search(r"^\s*change_requires_cr:\s*(\S+)", text, re.MULTILINE)
    if m and m.group(1).strip().lower() not in ("true", "yes"):
        problems.append("baselines.change_requires_cr is not true - baselined documents could "
                        "be edited without a change request (PB-03)")

    base = re.search(r"^\s*baseline_path:\s*[\"']?([^\"'#\n]+)", text, re.MULTILINE)
    work = re.search(r"^\s*working_file:\s*[\"']?([^\"'#\n]+)", text, re.MULTILINE)
    if base and work and base.group(1).strip() == work.group(1).strip():
        problems.append("schedule.baseline_path equals schedule.working_file - every schedule "
                        "variance would be erased on the first re-plan (PB-05)")

    hpd = re.search(r"^\s*hours_per_day:\s*([0-9.]+)", text, re.MULTILINE)
    php = re.search(r"^\s*productive_hours_per_day:\s*([0-9.]+)", text, re.MULTILINE)
    if hpd and php:
        try:
            if float(hpd.group(1)) == float(php.group(1)):
                problems.append("calendar.productive_hours_per_day equals hours_per_day - every "
                                "derived duration will be roughly 19% optimistic (EM-04)")
        except ValueError:
            pass

    alloc = re.search(r"^\s*max_planned_allocation_percent:\s*([0-9]+)", text, re.MULTILINE)
    if alloc and alloc.group(1).strip() == "100":
        problems.append("resource.max_planned_allocation_percent is 100 - the plan has no "
                        "capacity for defects, support or absence (RM-02)")

    if re.search(r"-\s+item:\s*\"\"\s*\n\s+reason:\s*\"\"", text):
        problems.append("scope.out_of_scope has an empty template entry - fill it or remove it")

    if problems:
        print("[pm] Profile loaded with issues:")
        for p in problems:
            print("  - " + p)
        print("  Run /pm_profile_check for the full validation.")

    if os.path.exists(ACTIVE_CR):
        try:
            with open(ACTIVE_CR, encoding="utf-8") as fh:
                cr = fh.read().strip()
        except Exception:
            cr = ""
        if cr:
            print("[pm] Active change request: {} - edits to baselined documents are allowed "
                  "and will be attributed to it. Clear .claude/.active_pm_cr when the CR is "
                  "applied and closed.".format(cr))
    return 0


if __name__ == "__main__":
    sys.exit(main())
