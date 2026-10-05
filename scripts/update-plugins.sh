#!/usr/bin/env bash
# Update the AI Pack plugins for every AI CLI installed on this machine.
#
# Only packs that are already installed are updated; nothing new is installed.
# CLIs that are not on PATH are skipped.
#
# Usage:
#   scripts/update-plugins.sh                  # every AI found on PATH
#   scripts/update-plugins.sh claude codex     # only these (claude codex copilot gemini antigravity)
#   DRY_RUN=1 scripts/update-plugins.sh        # print the commands without running them
#
# Claude Code plugins installed with --scope project are updated for the project in the
# current directory: run the script from that project.
#
# Antigravity has no update command, so its plugins are reinstalled from a local clone of
# ai-pack-antigravity: AGY_REPO (default: the antigravity submodule next to this script,
# else ~/ai-pack-antigravity). The clone is pulled first.

set -u

PACKS=(sdlc-standard migration-standard pm-standard vibe-standard)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DRY_RUN="${DRY_RUN:-0}"

if [ -z "${AGY_REPO:-}" ]; then
  if [ -d "$SCRIPT_DIR/../antigravity/plugins" ]; then
    AGY_REPO="$SCRIPT_DIR/../antigravity"
  else
    AGY_REPO="$HOME/ai-pack-antigravity"
  fi
fi

updated=()
failed=()
skipped=()

run() {
  echo "  \$ $*"
  [ "$DRY_RUN" = "1" ] && return 0
  "$@"
}

has() { command -v "$1" >/dev/null 2>&1; }

# Prints the packs whose name appears in the given listing, one per line.
installed_in() {
  local listing="$1" pattern="$2" pack
  for pack in "${PACKS[@]}"; do
    if grep -Eq "${pattern//\{\}/$pack}" <<<"$listing"; then
      echo "$pack"
    fi
  done
}

step() {
  local label="$1"; shift
  if run "$@"; then updated+=("$label"); else failed+=("$label"); fi
}

update_claude() {
  has claude || { skipped+=("claude (not installed)"); return; }
  local listing packs
  listing="$(claude plugin list 2>/dev/null)"
  packs="$(installed_in "$listing" '(^|[^a-z-]){}@ai-pack([^a-z-]|$)')"
  [ -n "$packs" ] || { skipped+=("claude (no ai-pack plugin installed)"); return; }
  run claude plugin marketplace update ai-pack || { failed+=("claude marketplace"); return; }
  for pack in $packs; do step "claude $pack" claude plugin update "$pack@ai-pack"; done
  echo "  -> restart Claude Code to load the new version"
}

update_codex() {
  has codex || { skipped+=("codex (not installed)"); return; }
  local listing packs
  listing="$(codex plugin list 2>/dev/null)"
  packs="$(installed_in "$listing" '^{}@ai-pack[[:space:]]+installed')"
  [ -n "$packs" ] || { skipped+=("codex (no ai-pack plugin installed)"); return; }
  run codex plugin marketplace upgrade ai-pack || { failed+=("codex marketplace"); return; }
  # `marketplace upgrade` does not update installed plugins; adding them again does.
  for pack in $packs; do step "codex $pack" codex plugin add "$pack@ai-pack"; done
  echo "  -> start a new Codex thread"
}

update_copilot() {
  has copilot || { skipped+=("copilot (not installed)"); return; }
  local listing packs
  listing="$(copilot plugin list 2>/dev/null)"
  packs="$(installed_in "$listing" '(^|[^a-z-]){}@ai-pack-copilot')"
  [ -n "$packs" ] || { skipped+=("copilot (no ai-pack plugin installed)"); return; }
  run copilot plugin marketplace update ai-pack-copilot || { failed+=("copilot marketplace"); return; }
  for pack in $packs; do step "copilot $pack" copilot plugin update "$pack"; done
  echo "  -> start a new Copilot session"
}

update_gemini() {
  has gemini || { skipped+=("gemini (not installed)"); return; }
  local listing packs
  listing="$(gemini extensions list 2>/dev/null)"
  packs="$(installed_in "$listing" '(^|[^a-z-]){}([^a-z-]|$)')"
  [ -n "$packs" ] || { skipped+=("gemini (no ai-pack extension installed)"); return; }
  for pack in $packs; do step "gemini $pack" gemini extensions update "$pack"; done
  echo "  -> restart Gemini CLI"
}

update_antigravity() {
  has agy || { skipped+=("antigravity (not installed)"); return; }
  local listing packs
  listing="$(agy plugin list 2>/dev/null)"
  packs="$(installed_in "$listing" '"name":[[:space:]]*"{}"')"
  [ -n "$packs" ] || { skipped+=("antigravity (no ai-pack plugin installed)"); return; }
  if [ ! -d "$AGY_REPO/plugins" ]; then
    failed+=("antigravity (no clone at $AGY_REPO; set AGY_REPO or git clone https://github.com/kaitondt/ai-pack-antigravity)")
    return
  fi
  run git -C "$AGY_REPO" pull --ff-only || { failed+=("antigravity pull"); return; }
  for pack in $packs; do
    if run agy plugin uninstall "$pack" && run agy plugin install "$AGY_REPO/plugins/$pack"; then
      updated+=("antigravity $pack")
    else
      failed+=("antigravity $pack")
    fi
  done
  echo "  -> restart Antigravity; IDE or project-only copies (.agents/plugins/) must be re-copied by hand"
}

targets=("$@")
[ ${#targets[@]} -gt 0 ] || targets=(claude codex copilot gemini antigravity)

for ai in "${targets[@]}"; do
  case "$ai" in
    claude|codex|copilot|gemini|antigravity)
      echo "== $ai"
      "update_$ai"
      ;;
    *)
      echo "Unknown AI: $ai (expected: claude codex copilot gemini antigravity)" >&2
      exit 2
      ;;
  esac
done

echo
echo "Updated : ${#updated[@]}"
for x in "${updated[@]}"; do echo "  + $x"; done
if [ ${#skipped[@]} -gt 0 ]; then
  echo "Skipped : ${#skipped[@]}"
  for x in "${skipped[@]}"; do echo "  - $x"; done
fi
if [ ${#failed[@]} -gt 0 ]; then
  echo "Failed  : ${#failed[@]}"
  for x in "${failed[@]}"; do echo "  ! $x"; done
  exit 1
fi
echo
echo "Then, in each project: run /<prefix>-profile-check (see 'After updating' in each AI's README)."
