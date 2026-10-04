import os
import json
import re

packs = ["sdlc-standard", "migration-standard", "pm-standard", "vibe-standard"]

for pack in packs:
    settings_path = os.path.join(pack, ".claude", "settings.json")
    if not os.path.exists(settings_path):
        continue
        
    with open(settings_path, "r", encoding="utf-8") as f:
        settings = json.load(f)
        
    if "hooks" not in settings:
        continue
        
    claude_hooks = settings["hooks"]
    gemini_hooks = {}
    
    # 1. Map SessionStart to PreInvocation
    if "SessionStart" in claude_hooks:
        pre_inv_handlers = []
        for group in claude_hooks["SessionStart"]:
            for h in group.get("hooks", []):
                cmd = h.get("command", "")
                cmd = re.sub(r'\$CLAUDE_PROJECT_DIR/\.claude/hooks/', './hooks/', cmd)
                pre_inv_handlers.append({
                    "type": "command",
                    "command": cmd,
                    "timeout": h.get("timeout", 10)
                })
        if pre_inv_handlers:
            gemini_hooks["PreInvocation"] = pre_inv_handlers

    # 2. Map PreToolUse
    if "PreToolUse" in claude_hooks:
        pre_tool_groups = []
        for group in claude_hooks["PreToolUse"]:
            matcher = group.get("matcher", "*")
            # Map Claude Write|Edit to Gemini file writing tools
            if "Write" in matcher or "Edit" in matcher:
                matcher = "write_to_file|multi_replace_file_content|replace_file_content"
            
            new_hooks = []
            for h in group.get("hooks", []):
                cmd = h.get("command", "")
                cmd = re.sub(r'\$CLAUDE_PROJECT_DIR/\.claude/hooks/', './hooks/', cmd)
                new_hooks.append({
                    "type": "command",
                    "command": cmd,
                    "timeout": h.get("timeout", 10)
                })
                
            pre_tool_groups.append({
                "matcher": matcher,
                "hooks": new_hooks
            })
        if pre_tool_groups:
            gemini_hooks["PreToolUse"] = pre_tool_groups

    if gemini_hooks:
        hooks_json_content = {
            "pack-hooks": gemini_hooks
        }
        
        hooks_json_path = os.path.join(pack, ".agents", "hooks.json")
        with open(hooks_json_path, "w", encoding="utf-8") as f:
            json.dump(hooks_json_content, f, indent=2)
        print(f"Created {hooks_json_path}")
