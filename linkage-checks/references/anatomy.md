# Check anatomy

The 7 structural elements every linkage check script carries. The scaffold
template (`assets/check-template.sh`) implements all of them; keep them when
hand-writing.

1. **Bash wrapper** — `#!/usr/bin/env bash` + `set -euo pipefail`. No logic
   here beyond path resolution; the real work is embedded Python (better
   regexes, testable parsing).
2. **Repo-root resolution** — `REPO_ROOT` derived from the script's own
   location (`dirname "${BASH_SOURCE[0]}"`), never from cwd. The script must
   work when invoked from anywhere.
3. **Env overrides (test hooks)** — every repo-specific input path comes
   from an environment variable with a sensible default. This is what makes
   the check testable against fixture trees without touching the real repo.
   Document each override in the header comment.
4. **Parse A** — extract the definition set. Fail with exit 2 if *zero*
   definitions parse: a check that silently parses nothing passes vacuously
   and is worse than no check.
5. **Scan B** — collect the reference set. Walk the tree; match the exact
   reference syntax (verified against real code in step 2 of the workflow).
   The template strips comments first (line + optional block syntax,
   preserving line numbers), so commented-out references do not count;
   uncommented dead code still does. Direction is explicit (`a2b`, `b2a`,
   `both`): `b2a` reports references at B with no definition at A.
6. **Escape hatch** — a marker (`NO_<X>: <reason>`) in a comment *directly
   attached* to the definition. The reason is required and echoed in the
   PASS report. Scope it tightly: a marker "anywhere in the file" silently
   disables the check (caught in production once — reviewer found it with a
   fixture). "Attached" = the contiguous comment lines directly above the
   definition; a blank or code line ends the block.
7. **Report + exit codes** — `0` pass (`PASS: <n> ...`), `1` offenders
   (list every offender on stdout), `2` usage/misconfiguration (stderr).
   `1` must mean *only* offenders. The template runs the embedded Python
   under a guard so a missing file, unset env var, unfilled `FILL:` marker,
   bad flag, syntax error or any unexpected exception exits `2` with one
   diagnostic line (traceback only with `LINKAGE_DEBUG=1`).
   CI greps the PASS line; humans read the offender list.

## Wiring
Add `bash scripts/checks/<name>.sh` and
`bash scripts/checks/tests/fixtures/<name>/run-fixtures.sh` to the repo's
native validation owner (existing test script / task target / checks job).
Editing CI or hooks is a separate, authorized change. If CI is wired,
confirm a real run's log prints the PASS line — "the step exists in YAML" is
not evidence.
