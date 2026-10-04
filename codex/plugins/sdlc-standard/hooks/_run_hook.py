#!/usr/bin/env python3
"""Run a pack guard only after a Codex project has opted in with its profile."""
import os
import subprocess
import sys

profile, script = sys.argv[1], sys.argv[2]
always = "--always" in sys.argv[3:]
here = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(here)
project = os.environ.get("CODEX_PROJECT_DIR", os.getcwd())
stdin = sys.stdin.buffer.read() if not sys.stdin.isatty() else b""
if not os.path.exists(os.path.join(project, ".codex", profile)) and not always:
    raise SystemExit(0)
if always:
    print("[{}] plugin root: {}".format(profile.split(".")[0], root))
env = dict(os.environ, CODEX_PROJECT_DIR=project, PLUGIN_ROOT=root,
           CLAUDE_PROJECT_DIR=project, CLAUDE_PLUGIN_ROOT=root)
raise SystemExit(subprocess.run([sys.executable, os.path.join(here, script)], input=stdin, env=env).returncode)
