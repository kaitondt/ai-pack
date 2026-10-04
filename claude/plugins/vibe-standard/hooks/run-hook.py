#!/usr/bin/env python3
"""Plugin hook launcher: python run-hook.py <profile-file> <hook-script> [--always]

Without --always the hook is skipped (exit 0) unless .claude/<profile-file> exists in the
project. With --always (SessionStart) it also prints the plugin root so commands can find
the pack's templates.
"""
import os
import subprocess
import sys


def main():
    profile, script = sys.argv[1], sys.argv[2]
    always = "--always" in sys.argv[3:]
    here = os.path.dirname(os.path.abspath(__file__))
    root = os.path.dirname(here)
    project = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
    stdin = sys.stdin.buffer.read() if not sys.stdin.isatty() else b""

    if not os.path.exists(os.path.join(project, ".claude", profile)):
        if not always:
            return 0
    if always:
        print("[{}] plugin root: {}".format(profile.split(".")[0], root))
        sys.stdout.flush()

    env = dict(os.environ, CLAUDE_PROJECT_DIR=project, CLAUDE_PLUGIN_ROOT=root)
    proc = subprocess.run([sys.executable, os.path.join(here, script)],
                          input=stdin, env=env)
    return proc.returncode


if __name__ == "__main__":
    sys.exit(main())
