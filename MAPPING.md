# Mapping: the WMS pack → the standard pack

What happened to each part of the original project-specific pack (26 skills, 20 agents,
32 commands, all hardcoded to one WMS migration).

Later additions that have no counterpart in the original are marked **new** and are listed
here too, so the record stays a complete account of the standard pack's contents rather than
only of its derivation.

Sides of the comparison, both in this folder:

- **original** — `.claude/` — the WMS pack as it stands today
- **standard** — `migration-standard/` — the generalised pack

This is a derivation record, not part of the pack itself. It is kept outside
`migration-standard/` so that copying the pack into a project does not carry it along.

---

## Skills

| Original | Became | Note |
|---|---|---|
| `claude_wms_project` | `mig_project` + `migration.profile.yaml` | the hardcoded tech stack, monorepo layout, environment matrix and API convention became profile data |
| `claude_wms_basic_design` | `mig_basic_design` | the fixed "309 deliverables across 7 phases" became a plan derived from the FRD and `paths.bd_categories` |
| `claude_wms_screen_design` | `mig_screen_design` | SD-T01..T36 and SD-UI01..06 generalised into SD-S / SD-F / SD-M / SD-B / SD-L families; the Japanese section names became a language-neutral skeleton |
| `claude_wms_function_design` | `mig_function_design` | FD-SC01, FD-L01..03, FD-SP01/02, FD-PAGE01 → FD-S / FD-P / FD-D / FD-E / FD-L |
| `claude_wms_api_design` | `mig_api_design` | API-SP01/NAME01/ORDER01 → API-S / API-U / API-C / API-E / API-X |
| `claude_wms_batch_design` | `mig_batch_design` | BT-SC01, BT-L01..03, BT-SP01/02 → BT-S / BT-R / BT-E / BT-L; restart/rerun promoted to its own section |
| *(none — DB design was ad hoc)* | `mig_data_design` | **new.** Type-conversion traps and reconciliation were the biggest gap in the original |
| `claude_wms_generate_detailed_design` | `mig_detail_design` | GAP verdict model made explicit; the "decide against legacy, never against the code" rule was implicit before |
| `claude_wms_context_map` | `mig_context_map` | the hardcoded WMS layer graph became "read the repository and emit real paths" |
| `claude_wms_backend`, `_frontend_desktop`, `_frontend_handy` | `mig_implementation` + `rules/<language>/` | stack-specific patterns belong in language rules, not in the migration pack |
| `claude_wms_design_desktop`, `_design_handy` | *(project-specific)* | a UI design system is per-product; adopt as `<key>_design_system` |
| `claude_wms_testing` | `mig_test_design` + `rules/common/testing.md` | the nine viewpoints were extracted and generalised; the parallel-run layer is new |
| `claude_wms_uat_bug` | `mig_uat_bug` | the 3-phase workflow and C1–C8 constraints survived nearly intact — they were already general |
| `claude_wms_change_request` | `mig_change_request` | the 6-phase workflow and both gates survived intact; the WMS locator map and cascade became `paths.*` and `change_request.cascade`, and the classification set was renamed to be surface-neutral (`CR-ITEM` → `CR-FIELD`, `CR-MSG` → `CR-MESSAGE`). **New:** the CR recorded as a traceability ancestor — the original had no register, so CR-sourced behaviour had nothing to anchor to |
| `claude_wms_review_brse_rules` (1272 lines) | `mig_review_framework` | the checklist families and the legacy cross-validation method were kept; the WMS vocabulary tables became profile-referenced dictionaries |
| `claude_wms_translate_rules`, `_translate_testcase_csv` | `mig_translate` | TL-01..TL-08; the CSV-specific column handling folded into TL-05 |
| `claude_wms_env_check`, `_build_verify_local` | `/mig_verify_build` | became a command, since it is a workflow rather than knowledge |
| `claude_wms_sc_fc_autofix`, `_sc_notation_fix`, `_mockup_fix_font_width`, `_mockup_fix_sosa_col` | *(dropped)* | one-off repair scripts for defects specific to that project's document history; a standard pack should prevent these rather than repair them |
| *(none)* | `mig_legacy_analysis` | **new.** The original had an agent but no skill — the four-pass method and the kind-specific heuristics were undocumented |
| *(none)* | `mig_requirements` | **new.** BRD/TSD/FRD existed as three agents with no shared rules |
| *(none)* | `mig_bug_trace` | **new.** `claude_wms_uat_bug` stopped at the direct cause; nothing recorded where a defect entered the chain, which commit introduced it, or why UT/IT let it through to UAT |
| *(none)* | `mig_document_io` | **new.** The original wrote Markdown only, into a structure it defined itself. The client's actual deliverables were Excel forms, reconciled by hand afterwards. Also draws the line the original never had: a legacy document is evidence of intent, never of behaviour (DIO-08) |
| `claude_wms_mockup_fix_font_width`, `_mockup_fix_sosa_col` | `mig_mockup` | the two one-off repair scripts were symptoms: the original produced mockups with no rules and no cross-check, then patched them. The skill replaces both with `fidelity` (as-is / restyled / redesigned) and the X-09 / X-10 checks that make a drifted mockup a finding instead of a repair job |
| *(none)* | `mig_infrastructure` | **new, and the largest gap.** The original pack stopped at code. Coexistence and which system owns the data, data migration judged on reconciliation rather than on completing, the parallel run, cutover and a rollback whose target is a system that never stopped — all of it lived in spreadsheets outside the pack |

## Commands

32 → 30. The consolidation:

| Original | Became |
|---|---|
| `generate_brd`, `generate_tsd`, `generate_frd` | `/mig_generate_requirements [brd\|tsd\|frd]` |
| `generate_basic_design`, `generate_batch_design`, `generate_prototype` | `/mig_generate_basic_design [category\|module]` |
| `review_screen_design`, `review_function_design`, `review_api_design`, `review_batch_design`, `review_report_design`, `review_file_design`, `review_brse_rules` | `/mig_review_design [target]` — one command, families selected by the profile |
| `generate_test` | `/mig_generate_test [ut\|it\|both] MODULE` |
| `uat_bug`, `uat_investigate`, `uat_fix`, `uat_report` | `/mig_uat_investigate`, `/mig_uat_fix`, `/mig_uat_report` (the umbrella command was redundant with the skill) |
| `cr`, `cr_analyze`, `cr_design`, `cr_implement`, `cr_report` | `/mig_cr_analyze`, `/mig_cr_design`, `/mig_cr_implement`, `/mig_cr_report` — the umbrella `cr` command dropped for the same reason as `uat_bug` |
| `verify_build_local` | `/mig_verify_build` |
| `security_review` | folded into `/mig_review_commit` + `rules/common/security.md` |
| *(none)* | `/mig_init`, `/mig_profile_check`, `/mig_trace_check` — **new**, and the three that make the pack reusable |
| *(none)* | `/mig_trace_bug` — **new**, the entry point for `mig_bug_trace` |

## Agents

20 → 9. The original had one agent per design category (`bd_screen_design`,
`bd_function_design`, `bd_api_design`, `bd_db_design`, `bd_report_design`,
`bd_batch_design`, `bd_architecture`). They differed only in which skill they loaded and
which directory they wrote to — both now profile data — so they collapsed into
`mig_bd_designer`, dispatched by `mig_bd_orchestrator`.

`mig_cr_engineer` is the one agent with no counterpart in the original: the WMS pack ran
its change requests from commands alone, so nothing carried the two-gate discipline into a
delegated session.

## Things that were fixed, not just moved

| Issue in the original | Fix |
|---|---|
| `rules/web/*.md` extended `rules/common/*.md`, which did not exist | `rules/common/` shipped: coding-style, patterns, security, testing, performance, hooks |
| Absolute machine paths in a skill (`/Users/ntq/Project/...`) | all paths resolve from the profile |
| Deliverable counts hardcoded and inconsistent (309 in one file, 351 in another, 315 in a third) | counts derived from the FRD at plan time |
| `pnpm generate:types` referenced in one skill, documented as non-existent in another | LR-04 / CM-01: verify the generator exists before relying on it |
| Phase status baked into an agent ("04.DB設計 — DONE, skip") | status is the traceability register's job, not an agent's |
| Traceability implied but never recorded | explicit register, orphan detection, gate assertions |
| A change request could authorise behaviour with no anchor and leave no trace of it | the CR id is the ancestor in the register (TR-02); a `CR-*` ancestor with no report on disk is Critical |
| No-invention rule stated in one skill among many | promoted to `rules/migration/no-invention.md`, loaded for every task |
| All 19 agents declared `model: sonnet` while the team actually ran opus at high effort | `model: opus` in every agent, driven by `execution.agent_model`; `/mig_profile_check` flags drift between the profile and the agent files |
