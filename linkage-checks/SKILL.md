---
name: linkage-checks
description: "Turn 'defined in A, must appear in B' invariants into CI check scripts. Use when a repo has definition/usage pairs that drift silently (toggles without UI rows, modules without registry keys, JNI names, i18n keys, routes, permissions). Scaffolds bash+python check scripts (A→B, B→A or both) with escape hatches, a self-running fixture test, and guidance for wiring into the repo's native validation."
---

# Checking linkage: turning the invariant "defined in A must appear in B" into a check script — use when a repo has definition/usage pairs that drift silently (toggle, JNI, i18n key, route, permission)

A **linkage** is an invariant of the form: *everything defined at site A must
appear at site B*. When it breaks silently, the bug is invisible until runtime:
a toggle with no UI row, a module with no registry key, a native function
whose Kotlin declaration was renamed, an i18n key with no translation.

This skill turns each linkage into a small CI check script that fails loudly
on drift, so human reviewers stop spending eyes on what a machine can verify.

## Workflow

### 1. Identify pairs
Survey the repo and list candidate A↔B pairs (see `references/pair-catalog.md`
for common ones). Pick pairs where drift is a **real bug**, not trivia. For
each pair, write down:
- **A (definition site)**: file(s), exact syntax of a definition.
- **B (appearance site)**: file(s), exact syntax of a reference.
- **Direction**: A→B (every A must appear in B), B→A, or both.

### 2. Verify the mechanism first
Read both sides before writing any check. Confirm the extraction you plan is
reliable on the real code — not on your memory of how it "should" look.
(Lesson from production: a JNI check written against assumed `Java_*` naming
would have missed every `RegisterNatives` entry. The writer read the
registration code first, then designed the check.)

If extraction is unreliable (dynamic names, string-built keys), **do not**
force the check — document the pair as deferred with reasons.

### 3. Scaffold
```
bash bin/new-linkage-check <check-name> [--repo DIR]
```
Generates `scripts/checks/<check-name>.sh` from the template plus
`scripts/checks/tests/fixtures/<check-name>/` with `run-fixtures.sh` and
`pass/`, `fail/`, `exempt/` (each with `README.md` and `fixture.env`, plus
`fail/EXPECT_OFFENDER` and `exempt/EXPECT_EXEMPT`). Fill every `FILL:`
marker: the config block (things, marker, `DIRECTION`, A/B regexes, B globs,
B comment syntax), defaults, header docs. The check and the runner refuse to
run (exit 2) while any marker remains.

- **Direction** is explicit: `DIRECTION = "a2b" | "b2a" | "both"` in the
  config; override per run with `--direction` or `LINKAGE_DIRECTION`.
  `b2a` reports dangling references at B (with `file:line`).
- **Scanning B strips comments** (`B_LINE_COMMENT`, optional
  `B_BLOCK_COMMENT`) before matching, so a reference that exists only in a
  comment or in commented-out code does **not** count. Stripping is not
  string-aware, and uncommented dead code (unreachable functions, disabled
  branches) still counts. Set both to `None` to match raw text.
- **Escape hatch** (a2b): `<MARKER>: <reason>` anywhere in the contiguous
  comment block directly above the definition (multi-line blocks OK; a blank
  line ends the block). A marker without a reason is misconfiguration.

### 4. Self-test with fixtures
- **pass/**: faithful miniature of the real tree → exit 0, prints PASS.
- **fail/**: one synthetic offender → exit 1, names it (`EXPECT_OFFENDER`).
- **exempt/**: offender carrying the escape-hatch marker → exit 0, listed
  as exempt (`EXPECT_EXEMPT`).
Point each `fixture.env` at its miniature tree (`{fixture}` = that dir), then:
```
bash scripts/checks/tests/fixtures/<check-name>/run-fixtures.sh
```
It must print `PASS: 3 fixtures`. Then break a fixture on purpose (e.g. add
a reference to the fail offender) and confirm the runner goes red (exit 1).
A check that cannot demonstrate catching an offender is not done.

### 5. Wire into the repo's native validation
Find the repo's existing validation owner (test script, Makefile/task
target, the job that already runs other checks) and add both commands there,
invoked via `bash` so lost exec bits never matter:
```
bash scripts/checks/<check-name>.sh
bash scripts/checks/tests/fixtures/<check-name>/run-fixtures.sh
```
The scaffold does not edit CI or hooks. If you do wire CI (with
authorization), report it as "wired" only after a real run's log shows the
PASS line; a step in YAML is not evidence it runs.

## Check anatomy
Every generated script follows the same 7 elements (see
`references/anatomy.md`): bash wrapper, repo-root resolution, env overrides
for testability, embedded Python (parse A / scan B / compare), escape hatch,
PASS/FAIL report, exit codes (`0` pass · `1` offenders · `2` usage/misconfig/
internal error). Exit `1` means *only* real offenders: missing inputs, unset
env, unfilled `FILL:` markers, bad flags, a Python syntax error or any
unexpected exception all exit `2` with a one-line stderr diagnostic
(`LINKAGE_DEBUG=1` adds the traceback).

## Output contract
- One script per pair: `scripts/checks/<name>.sh`, invoked via `bash`
  (the exec bit is set but never relied on).
- stdout ends with `PASS: <n> ...` or `FAIL: <offenders...>`; stderr for
  misconfiguration.
- Fixtures and `run-fixtures.sh` live under `scripts/checks/tests/fixtures/<name>/`
  so the next agent can re-verify with one command.

## Operating rules
1. **Verify, don't guess** the extraction — read both sites first.
2. Every check **must** have an escape hatch (`NO_<X>: <reason>`); the reason
   is required and echoed in the PASS report. An escape hatch with wrong scope
   silently disables the check — the self-test must cover it.
3. Env-var overrides for all repo-specific paths (testability is not optional).
4. One pair per script. A script checking two pairs is two scripts.
5. If a pair proves too noisy, defer it **in writing** with the concrete
   false-positive causes — never ship a check you don't trust.

## Inside a Harness repo
If the repo's `AGENTS.md` contains a `<!-- WORKFLOW:BEGIN -->` block, this
skill only supplies the mechanism; `~/workspace/harness/patterns/encoding-invariants.md`
governs the rule:
- The linkage rule must come from **accepted authority** (an accepted doc or
  explicit owner decision); cite its path and exact rule in the check header.
  Do not derive an invariant from code patterns, conventions, tests or
  defaults: "every toggle currently has a UI row" is not authority.
- Integrate into the repo's **native validation owner**; do not modify CI,
  hooks, or branch protection without separate authorization.
- The fixture pass/fail pair is the positive/negative proof that pattern asks for.
- Report enforcement levels **separately**: local validation (run? passed?),
  optional hook, CI invocation found/absent (and verified run status only if
  observed), branch protection verified/unverified.
