#!/usr/bin/env bash
# FILL: <check-name> — <one-line: everything defined at A must appear at B>
#
# FILL: longer description of the invariant, which direction(s) are enforced,
# and what breaks at runtime when it drifts.
#
# Directions (DIRECTION below; override with --direction or LINKAGE_DIRECTION):
#   a2b   every definition at A must be referenced at B
#   b2a   every reference at B must name a definition at A (no dangling refs)
#   both  a2b and b2a
#
# Escape hatch (a2b only): a definition whose *attached* comment block (the
# contiguous comment lines directly above it, no blank line in between)
# contains "<MARKER>: <reason>" is exempted. The reason is required and is
# echoed in the PASS report.
#
# Scanning B: comments are stripped before references are matched (see
# B_LINE_COMMENT / B_BLOCK_COMMENT), so a reference that exists only in a
# comment, including commented-out code, does NOT count. Stripping is not
# string-aware, and dead code that is not commented out (unreachable
# functions, disabled branches) still counts as a reference.
#
# Test hooks (environment overrides; defaults shown):
#   A_FILE             FILL: file holding the definitions ($REPO_ROOT/...)
#   B_DIR              FILL: tree scanned for references ($REPO_ROOT/...)
#   LINKAGE_DIRECTION  a2b | b2a | both (default: DIRECTION in the config)
#   LINKAGE_DEBUG=1    show Python tracebacks on internal errors
#
# Exit codes: 0 pass · 1 offenders found · 2 usage / misconfiguration /
# internal error (one-line diagnostic on stderr). Exit 1 means only "real
# offenders"; nothing else exits 1.
#
# Remove every placeholder marker (the word FILL followed by a colon) once
# filled, including in these comments; the script refuses to run (exit 2)
# while any remain.

set -euo pipefail

SELF="${BASH_SOURCE[0]}"
CHECK_NAME="$(basename "$SELF" .sh)"
die() { echo "$CHECK_NAME: error: $*" >&2; exit 2; }
usage() { echo "usage: $CHECK_NAME.sh [--direction a2b|b2a|both] [--debug]" >&2; exit 2; }

while [[ $# -gt 0 ]]; do
    case "$1" in
        --direction) [[ $# -ge 2 && -n "$2" ]] || usage; LINKAGE_DIRECTION="$2"; shift 2 ;;
        --debug) LINKAGE_DEBUG=1; shift ;;
        -h|--help) usage ;;
        *) usage ;;
    esac
done

# Unfilled template guard. The pattern is written so this line itself
# does not match.
if fill_line="$(grep -nm1 'FIL[L]:' "$SELF")"; then
    die "unfilled template: placeholder marker remains at line ${fill_line%%:*} of $SELF"
fi

REPO_ROOT="$(cd "$(dirname "$SELF")/../.." && pwd)"
A_FILE="${A_FILE:-$REPO_ROOT/FILL:path/to/definitions}"
B_DIR="${B_DIR:-$REPO_ROOT/FILL:path/to/usages}"
LINKAGE_DIRECTION="${LINKAGE_DIRECTION:-}"
LINKAGE_DEBUG="${LINKAGE_DEBUG:-}"

command -v python3 >/dev/null 2>&1 || die "python3 not found on PATH"
[[ -f "$A_FILE" && -r "$A_FILE" ]] || die "A_FILE is not a readable file: $A_FILE"
[[ -d "$B_DIR" ]] || die "B_DIR is not a directory: $B_DIR"

export A_FILE B_DIR LINKAGE_DIRECTION LINKAGE_DEBUG CHECK_NAME

# Guard: compiles and runs the check body (stdin) so that a syntax error,
# missing env var, unreadable file, or any unexpected exception exits 2 with
# a one-line diagnostic. Only the body's explicit sys.exit(1) means offenders.
PY_GUARD='
import os, sys, traceback
name = os.environ.get("CHECK_NAME", "check")
class Misconfig(Exception):
    pass
def misconfig(msg):
    raise Misconfig(msg)
def env(var):
    v = os.environ.get(var)
    if not v:
        misconfig("environment variable %s is not set" % var)
    return v
try:
    code = compile(sys.stdin.read(), name + ".sh:<python>", "exec")
    exec(code, {"__name__": "__main__", "misconfig": misconfig, "env": env})
except SystemExit as e:
    rc = e.code if isinstance(e.code, int) else (0 if e.code is None else 2)
    sys.exit(rc if rc in (0, 1) else 2)
except Misconfig as e:
    print("%s: error: %s" % (name, e), file=sys.stderr)
    sys.exit(2)
except Exception as e:
    if os.environ.get("LINKAGE_DEBUG"):
        traceback.print_exc()
    print("%s: error: %s: %s" % (name, type(e).__name__, e), file=sys.stderr)
    sys.exit(2)
'

rc=0
python3 -c "$PY_GUARD" <<'PYEOF' || rc=$?
import fnmatch
import os
import re
import sys

# ---- Configure the pair --------------------------------------------------
THINGS = "FILL:things"         # plural noun for reports, e.g. "feature toggles"
WHERE = "FILL:where"           # e.g. "an editor UI row"
MARKER = "FILL:NO_X"           # escape-hatch marker, e.g. "NO_UI_ROW"
DIRECTION = "FILL:a2b|b2a|both"  # default direction (see header)
A_DEF_RE = r"FILL:"            # matched per line of A; group 1 = defined name
A_COMMENT_RE = r"^\s*#"        # a comment line at A (for hatch blocks)
B_GLOBS = ("FILL:*.ext",)      # basenames scanned under B_DIR
B_REF_RE = r"FILL:"            # matched in comment-stripped B; group 1 = name
B_LINE_COMMENT = r"#"          # line-comment leader at B (regex); None = keep
B_BLOCK_COMMENT = None         # (open_re, close_re), e.g. (r"/\*", r"\*/")
# --------------------------------------------------------------------------

direction = os.environ.get("LINKAGE_DIRECTION") or DIRECTION
if direction not in ("a2b", "b2a", "both"):
    misconfig("direction must be a2b, b2a or both (got %r)" % direction)
a_file = env("A_FILE")
b_dir = env("B_DIR")


def attached_comment_block(lines, i):
    """Contiguous comment lines directly above lines[i] (stops at blank or
    non-comment line), so a marker elsewhere in the file never applies."""
    block = []
    j = i - 1
    while j >= 0 and re.match(A_COMMENT_RE, lines[j]):
        block.append(lines[j])
        j -= 1
    return block


def exempt_reason(lines, i):
    for line in attached_comment_block(lines, i):
        m = re.search(re.escape(MARKER) + r":\s*(\S.*?)\s*$", line)
        if m:
            return m.group(1)
        if re.search(re.escape(MARKER) + r"\b", line):
            misconfig("%s:%d: %s marker without a reason" % (a_file, i + 1, MARKER))
    return None


def parse_a(src):
    """Produce [{"name", "line", "exempt_reason"}]. Replace for multi-line
    definition syntax, but keep the attached-block hatch scope."""
    lines = src.splitlines()
    out = []
    for i, line in enumerate(lines):
        m = re.search(A_DEF_RE, line)
        if m:
            out.append({"name": m.group(1), "line": i + 1,
                        "exempt_reason": exempt_reason(lines, i)})
    return out


def strip_comments(text):
    """Blank out comments, preserving line numbers."""
    if B_BLOCK_COMMENT:
        op, cl = B_BLOCK_COMMENT
        text = re.sub(op + r".*?" + cl,
                      lambda m: "\n" * m.group(0).count("\n"), text, flags=re.S)
    if B_LINE_COMMENT:
        text = re.sub(r"(^|\s)" + B_LINE_COMMENT + r".*$", r"\1", text,
                      flags=re.M)
    return text


def scan_b(root):
    """Produce {name: ["relpath:line", ...]} for references under root."""
    refs = {}
    for dirpath, dirnames, files in os.walk(root):
        dirnames.sort()
        for fn in sorted(files):
            if not any(fnmatch.fnmatch(fn, g) for g in B_GLOBS):
                continue
            path = os.path.join(dirpath, fn)
            with open(path, encoding="utf-8", errors="replace") as f:
                text = strip_comments(f.read())
            rel = os.path.relpath(path, root)
            for m in re.finditer(B_REF_RE, text):
                ln = text.count("\n", 0, m.start()) + 1
                refs.setdefault(m.group(1), []).append("%s:%d" % (rel, ln))
    return refs


with open(a_file, encoding="utf-8") as f:
    defs = parse_a(f.read())
if not defs:
    misconfig("no definitions parsed at site A (%s); A_DEF_RE wrong?" % a_file)
refs = scan_b(b_dir)
names = {d["name"] for d in defs}

missing, exempted, dangling = [], [], []
if direction in ("a2b", "both"):
    for d in defs:
        if d["name"] in refs:
            continue
        if d["exempt_reason"]:
            exempted.append((d["name"], d["exempt_reason"]))
        else:
            missing.append(d)
if direction in ("b2a", "both"):
    dangling = sorted((n, locs) for n, locs in refs.items() if n not in names)

if missing or dangling:
    if missing:
        print("FAIL: %d %s without %s:" % (len(missing), THINGS, WHERE))
        for d in sorted(missing, key=lambda d: d["name"]):
            print("  - %s (%s:%d)" % (d["name"], os.path.basename(a_file), d["line"]))
    if dangling:
        print("FAIL: %d references at B to undefined %s:" % (len(dangling), THINGS))
        for n, locs in dangling:
            print("  - %s (%s)" % (n, ", ".join(locs)))
    sys.exit(1)

print("PASS: %d %s, %d referenced names at B (direction %s); %d marked %s, 0 offenders"
      % (len(defs), THINGS, len(refs), direction, len(exempted), MARKER))
for n, reason in sorted(exempted):
    print("  exempt: %s (%s)" % (n, reason))
PYEOF
# Anything other than 0/1 from the interpreter is misconfig/internal error.
case "$rc" in 0|1) ;; *) rc=2 ;; esac
exit "$rc"
