import os
import shutil

packs = ["sdlc-standard", "migration-standard", "pm-standard", "vibe-standard"]

for pack in packs:
    src_dir = os.path.join(pack, ".claude")
    dest_dir = os.path.join(pack, ".agents")
    
    if os.path.exists(src_dir):
        if os.path.exists(dest_dir):
            shutil.rmtree(dest_dir)
            
        shutil.copytree(src_dir, dest_dir)
        print(f"Copied {src_dir} to {dest_dir}")
        
        claude_md = os.path.join(dest_dir, "CLAUDE.md")
        gemini_md = os.path.join(dest_dir, "GEMINI.md")
        if os.path.exists(claude_md):
            os.rename(claude_md, gemini_md)
            print(f"Renamed CLAUDE.md to GEMINI.md in {pack}")
            
        plugin_json_path = os.path.join(dest_dir, "plugin.json")
        with open(plugin_json_path, "w", encoding="utf-8") as f:
            f.write(f'''{{
  "name": "{pack}",
  "description": "{pack} migrated to Gemini Antigravity format"
}}''')
        print(f"Created plugin.json in {pack}/.agents")
