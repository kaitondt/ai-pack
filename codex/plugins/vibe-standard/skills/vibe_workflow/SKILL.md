---
name: vibe_workflow
description: "Route a vibe pack task to the correct lifecycle workflow. Use when the user asks to start, plan, build, test, review, release, report, or assess work governed by this pack."
---

# vibe workflow router

1. Read `.codex/vibe.profile.yaml`. If it is missing, stop and ask the user to adopt the pack by copying the profile template from this plugin and its generated `AGENTS.md` into the repository root.
2. Load `vibe_project` first, then the phase/area skill it routes to.
3. Treat legacy slash-command names as workflow aliases, not literal Codex commands. Their source procedures are in `references/commands/`.
4. Follow the profile, invariant rules, and evidence/reporting requirements; do not invent project values.

Legacy workflow aliases: `/vibe_build` · `/vibe_debt` · `/vibe_fix` · `/vibe_graduate` · `/vibe_handoff` · `/vibe_init` · `/vibe_intent` · `/vibe_park` · `/vibe_plan` · `/vibe_product` · `/vibe_profile_check` · `/vibe_refine_skill` · `/vibe_resume` · `/vibe_review` · `/vibe_scaffold` · `/vibe_security_check` · `/vibe_ship` · `/vibe_status` · `/vibe_unstuck` · `/vibe_verify`
