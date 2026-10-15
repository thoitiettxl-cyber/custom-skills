#!/usr/bin/env bash
# frida-run.sh — Frida dynamic injection wrapper.
# Adapted from zhaoxuya520/reverse-skill (MIT) — English-only Linux version.
#
# Usage:
#   bash frida-run.sh --package <pkg> --script <js> [--usb] [--spawn]
#   bash frida-run.sh --list-devices
#   bash frida-run.sh --list-processes [--usb]

set -euo pipefail

# ─── Arguments ───

PACKAGE=""
PROCESS=""
REMOTE_HOST="127.0.0.1:27042"
SCRIPT_PATH=""
USB=false
SPAWN=false
PAUSE=false
LIST_DEVICES=false
LIST_PROCESSES=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --package|-p) PACKAGE="$2"; shift 2 ;;
        --process) PROCESS="$2"; shift 2 ;;
        --remote|-H) REMOTE_HOST="$2"; shift 2 ;;
        --script|-l) SCRIPT_PATH="$2"; shift 2 ;;
        --usb|-U) USB=true; shift ;;
        --spawn|-f) SPAWN=true; shift ;;
        --pause) PAUSE=true; shift ;;
        --list-devices) LIST_DEVICES=true; shift ;;
        --list-processes) LIST_PROCESSES=true; shift ;;
        -*) echo "Unknown option: $1"; exit 1 ;;
        *) echo "Unknown argument: $1"; exit 1 ;;
    esac
done

# ─── Tool detection ───
# NOTE: upstream scripts tried an auto-bootstrap hook here
# (bootstrap-reverse.sh from their repo layout). This deployment keeps
# detection only — install missing tools manually (hints below).

install_hint() {
    case "$1" in
        frida)   echo "  Install: pip3 install frida-tools   (needs Python 3)" ;;
    esac
}

ensure_tool() {
    local name="$1"
    if command -v "$name" &>/dev/null; then
        return 0
    fi
    echo "ERR: required tool not found: $name"
    install_hint "$name"
    return 1
}

ensure_tool "frida"

# ─── List devices ───

if [[ "$LIST_DEVICES" == "true" ]]; then
    frida-ls-devices 2>/dev/null || python3 -c "
import frida
for d in frida.enumerate_devices():
    print(f'{d.id}\t{d.type}\t{d.name}')
"
    exit 0
fi

# ─── List processes ───

if [[ "$LIST_PROCESSES" == "true" ]]; then
    if [[ "$USB" == "true" ]]; then
        frida-ps -U
    else
        frida-ps -H "$REMOTE_HOST"
    fi
    exit 0
fi

# ─── Inject and run ───

TARGET="${PACKAGE:-$PROCESS}"
if [[ -z "$TARGET" ]]; then
    echo "Usage: $0 --package <pkg> --script <js> [--usb] [--spawn]"
    echo "  or: $0 --list-devices"
    echo "  or: $0 --list-processes [--usb]"
    exit 1
fi

if [[ -z "$SCRIPT_PATH" || ! -f "$SCRIPT_PATH" ]]; then
    echo "ERR: Frida script not found: ${SCRIPT_PATH:-not specified}"
    exit 1
fi

FRIDA_ARGS=()

if [[ "$USB" == "true" ]]; then
    FRIDA_ARGS+=("-U")
else
    FRIDA_ARGS+=("-H" "$REMOTE_HOST")
fi

if [[ "$SPAWN" == "true" ]]; then
    FRIDA_ARGS+=("-f")
else
    FRIDA_ARGS+=("-n")
fi

FRIDA_ARGS+=("$TARGET")
FRIDA_ARGS+=("-l" "$SCRIPT_PATH")

if [[ "$PAUSE" != "true" ]]; then
    FRIDA_ARGS+=("--no-pause")
fi

echo "=== Frida inject ==="
echo "  target: $TARGET"
echo "  script: $SCRIPT_PATH"
echo "  mode: $([ "$SPAWN" == "true" ] && echo "spawn" || echo "attach")"
echo "  connection: $([ "$USB" == "true" ] && echo "USB" || echo "$REMOTE_HOST")"
echo ""

frida "${FRIDA_ARGS[@]}"
