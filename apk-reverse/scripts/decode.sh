#!/usr/bin/env bash
# decode.sh — Unpack an APK: jadx decompile + apktool unpack.
# Adapted from zhaoxuya520/reverse-skill (MIT) — English-only Linux version.
#
# Usage:
#   bash decode.sh <apk_path> [--name <task_name>] [--out <output_dir>]
#                              [--skip-jadx] [--skip-apktool] [--clean]

set -euo pipefail

# ─── Argument parsing ───

APK_PATH=""
TASK_NAME=""
OUT_ROOT=""
SKIP_JADX=false
SKIP_APKTOOL=false
CLEAN=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --name) TASK_NAME="$2"; shift 2 ;;
        --out) OUT_ROOT="$2"; shift 2 ;;
        --skip-jadx) SKIP_JADX=true; shift ;;
        --skip-apktool) SKIP_APKTOOL=true; shift ;;
        --clean) CLEAN=true; shift ;;
        -*) echo "Unknown option: $1"; exit 1 ;;
        *) APK_PATH="$1"; shift ;;
    esac
done

if [[ -z "$APK_PATH" ]]; then
    echo "Usage: $0 <apk_path> [--name <name>] [--out <dir>] [--skip-jadx] [--skip-apktool] [--clean]"
    exit 1
fi

if [[ ! -f "$APK_PATH" ]]; then
    echo "ERR: APK file not found: $APK_PATH"
    exit 1
fi

# ─── Tool detection ───
# NOTE: upstream scripts tried an auto-bootstrap hook here
# (bootstrap-reverse.sh from their repo layout). This deployment keeps
# detection only — install missing tools manually (hints below).

install_hint() {
    case "$1" in
        jadx)    echo "  Install: https://github.com/skylot/jadx/releases" ;;
        apktool) echo "  Install: https://apktool.org/docs/install/" ;;
        frida)   echo "  Install: pip3 install frida-tools   (needs Python 3)" ;;
        adb)     echo "  Install: sudo apt install adb   (Android platform-tools)" ;;
        zipalign|apksigner)
                 echo "  Install: sudo apt install android-sdk-build-tools"
                 echo "  Or: sdkmanager \"build-tools;35.0.0\"" ;;
        keytool|java)
                 echo "  Install: sudo apt install default-jdk" ;;
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

[[ "$SKIP_JADX" != "true" ]] && ensure_tool "jadx"
[[ "$SKIP_APKTOOL" != "true" ]] && ensure_tool "apktool"

# ─── Path resolution ───

APK_BASENAME=$(basename "$APK_PATH" .apk | sed 's/[^A-Za-z0-9._-]/_/g')
TASK_NAME="${TASK_NAME:-$APK_BASENAME}"
OUT_ROOT="${OUT_ROOT:-$(dirname "$APK_PATH")}"
TASK_ROOT="$OUT_ROOT/$TASK_NAME"
JADX_OUT="$TASK_ROOT/jadx"
APKTOOL_OUT="$TASK_ROOT/apktool"

if [[ "$CLEAN" == "true" && -d "$TASK_ROOT" ]]; then
    rm -rf "$TASK_ROOT"
fi

mkdir -p "$TASK_ROOT"

# ─── jadx decompile ───

JADX_EXIT=0
if [[ "$SKIP_JADX" != "true" ]]; then
    rm -rf "$JADX_OUT"
    echo "=== jadx decompile ==="
    jadx -d "$JADX_OUT" "$APK_PATH" || JADX_EXIT=$?
fi

# ─── apktool unpack ───

APKTOOL_EXIT=0
if [[ "$SKIP_APKTOOL" != "true" ]]; then
    rm -rf "$APKTOOL_OUT"
    echo "=== apktool unpack ==="
    apktool d "$APK_PATH" -o "$APKTOOL_OUT" -f || APKTOOL_EXIT=$?
fi

# ─── Summary stats ───

PACKAGE=""
if [[ -f "$APKTOOL_OUT/AndroidManifest.xml" ]]; then
    PACKAGE=$(grep -oP 'package="[^"]*"' "$APKTOOL_OUT/AndroidManifest.xml" 2>/dev/null | head -1 | sed 's/package="//;s/"//')
fi

JAVA_COUNT=0
[[ -d "$JADX_OUT" ]] && JAVA_COUNT=$(find "$JADX_OUT" -name "*.java" | wc -l)

SMALI_DIRS=0
[[ -d "$APKTOOL_OUT" ]] && SMALI_DIRS=$(find "$APKTOOL_OUT" -maxdepth 1 -type d -name "smali*" | wc -l)

SO_COUNT=0
[[ -d "$APKTOOL_OUT" ]] && SO_COUNT=$(find "$APKTOOL_OUT" -name "*.so" | wc -l)

echo ""
echo "═══════════════════════════════════════════"
echo "  APK unpack complete"
echo "═══════════════════════════════════════════"
echo "  task_root=$TASK_ROOT"
echo "  jadx_out=$JADX_OUT"
echo "  apktool_out=$APKTOOL_OUT"
echo "  package=$PACKAGE"
echo "  jadx_exit_code=$JADX_EXIT"
echo "  apktool_exit_code=$APKTOOL_EXIT"
echo "  java_files=$JAVA_COUNT"
echo "  smali_dirs=$SMALI_DIRS"
echo "  so_files=$SO_COUNT"
