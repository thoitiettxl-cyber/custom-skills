# Real-world experience — evolving with each use of subagent-orchestration

Each lesson: date, task, what happened, evidence, rule drawn. Only lessons with real evidence.

## 2026-10-15 — Reverse-skill investigation

- **Trust only code, ignore comments:** when surveying an unfamiliar repo, grep executable code first, read docs afterwards only to cross-check. Result: 45 skills, only 1 with real Android code (`apk-reverse`); `mobile-reverse` had 0 code files even though its docs fully described Frida/Objection/MSTG.
- Define "executable file" in the brief (excluding `.md` files containing snippets from the count).
- Rule "match → verify context → only then count": a grep hit is not enough — false positive (variable `index` matching "android" in `review_case.py`).
- Cross-checking doc-vs-manifest versions is a cheap technique for detecting drift (SKILL.md said jadx 1.5.5 vs manifest pin 1.5.6).
- `mkdir -p` before redirecting `gh api` output — otherwise it fails silently, creating an empty file.

## 2026-10-16 — Diagnostic v2 SpoofX

- **An outside reviewer catches question-framing errors, not just answer errors:** 9 feasibility questions asked "can it be done" but missed "does doing that change the measured result". Boss pointed out questions 1,2,3,6 were framed wrong → a supplementary review round had to be rewritten with 8 corrected questions. Rule: have a reviewer approve the questions before agents run.
- **Read-only subagents cannot confirm runtime:** 3 parallel agents gave detailed results with file:line, but only proved "what the code does", not "what the framework/runtime does". Boss required every conclusion to carry `[STATIC]`/`[NEEDS-MEASUREMENT]`. Rule: mandatory labels on every investigation report.
- **Set interpretation criteria before measuring:** a 6-row table (mismatch@t0+t2s=F1, mismatch@t0+match@t2s=late, target runs first=needs restart, torn read, P3 type excluded, read-back meaningless) was settled before building the APK. Rule: no post-hoc justification after numbers exist.
- **Brief states the evidence format explicitly:** a brief requiring "[STATIC]/[NEEDS-MEASUREMENT] + file:line" produced far better-structured reports than a vague brief. Rule: write the evidence format in the brief itself, do not let the agent choose it.
- **Review the real diff, not the agent's words:** an agent reported "logs only, no logic change" but Boss required seeing the full git diff before approving — self-reporting is not evidence. Rule: the approve gate takes a diff + hunk classification, not a summary.
- **Define permitted hunk types in advance:** for a "logs only" change, 4 hunk types were accepted: LOG / LOCAL-TS / EXECUTOR / TOGGLE. Any hunk editing an original line, changing write order, or changing return/exception flow is listed separately as a violation. Rule: put a hunk whitelist in the implement brief.
- **Self-tests must go through the exact path needing proof:** hashing a fixed string only proves the sha function is correct, not that both sides use the same canonical form. A fixed fixture must be added going through the canonical function on both sides. Rule: test what is in doubt, not what is already certain.
- **A control group can "heal" the bug:** a fresh pull on the writer side can fix staleness → FAIL(A) < FAIL(C) means read-back is medicine, not a measuring stick. Rule: pre-register the interpretation for the case where the measurement changes the result, before numbers exist.
- **State what a sample size can prove:** 0 errors/20 runs only rules out error rates above ~14% (95%), it does not prove the bug is gone. Rule: reports state statistical limits, no overclaiming.

## 2026-10-16 — Sing-box: measure before fixing

- **Verify a hypothesis with a raw sample table before changing code:** suspecting the password "rotates every exec" (short TTL) → probing 908 domains consecutively (~1h) with a single credential: 908/908 CONNECT 200, 0× 407 → hypothesis WRONG, the password is stable. Evidence: `~/workspace/apk-domains/egress-probe-full.tsv` (908 lines).

## 2026-10-17 — Sing-box watchdog: log trigger and live test

- **A log-scan trigger must follow byte offsets, not tail N:** the watchdog only considers lines newer than the offset in `.authfail-offset` (reset on rotate; first run only baselines, does not act). Without an offset → rescanning old lines → restart loop.
- **Prove a log chain with a deliberately broken instance, never live:** the `authentication required` trigger was proven with a temporary instance set to a wrong password — never tested on the live tunnel.
- **A long-lived parent process freezes env:** run.sh's env was frozen at start (proven via /proc: run.sh pid 27410 sha8 `1f4cf5f2` vs fresh shell `601243fd`) → when triggered, kill run.sh (not just the child) then respawn to get fresh env.
- **Live testing caught 2 bugs static review missed** (fixed in the same commit): (1) the watchdog shared `.watchdog.lock` with run.sh — run.sh holds the lock for its whole life, so the watchdog's `flock -n` always failed, exiting silently and never checking; fix: a separate lock `.watchdog-wd.lock`. (2) `sleep 3` after kill was not enough — the leftover sing-box child inherited the lock fd from run.sh, so the new instance hit "another instance holds the lock"; fix: a wait loop of up to 20s until both run.sh and the child are fully dead.

## 2026-10-17 — Linkage survey: red-team catches a real bug

- **Outside review before applying catches real bugs:** red-team caught 2 real errors — 7 scripts forgot to strip `//` on side A, causing false reports; one check's regex wrongly matched a class name. Rule: keep an independent review gate before applying; the reviewer reads diff/code, not summaries.

## 2026-10-17 — Security audit run-1: verify discipline and reporting

- **Isolate held-out data by structure, not by instruction:** recall item creatorPackage was independently rediscovered by hunter h-u03 → recall 1/1. Evidence: clean worktree detached at d08d2e9, 0 untracked files; the held-out list lived only in the parent-side PLAN.md, not in the snapshot; the hunter brief contained no plan content; the "commit = known finding" mapping was never committed to the repo.
- **Quote status definitions verbatim when reporting:** having reported "16/16 complete / 100% trust-boundary", it had to be corrected to 12/16 = 75% after re-reading HUNTING.md (`candidate` ≠ `covered`; covered requires "no candidate").
- **Finalize the artifact before the verifier sees it:** reworking findings 1-2 (attacker model, precondition, severity) inline BEFORE spawning Phase-5 → all 3 verifiers returned "verified" in the first round, costing no replacement round.
- **An independent verifier produces new evidence:** v-fp5 (which had never seen the candidate) not only confirmed but found a specific spoof mechanism (`createPackageContext`) + discovered the receiver never reads `creatorUid` (grep across the repo: 0 references).
- **Order violations must be recorded:** spawning v-fp5 before sending the breakdown (against Boss's condition) → recorded in run-notes.md immediately per Boss's order, not quietly let pass.
- **Spend ledger per invocation:** ceiling 25→31, each spawn numbered (26/31, 27/31…), total stopping at 29/31.

## Changelog (design, unverified)

### 2026-10-17 — v2: verify/report discipline from audit run-1 + sing-box watchdog lessons

- **v2 replaces 5.3 (reset baseline, not a downgrade):** the 5.x line was incremental steps from v5 (Floor/Target); v2 is a new baseline unifying everything — read v2 instead of all earlier 5.x versions.
- lessons.md: 6 audit lessons (held-out isolation, quoting status definitions, finalize before verify, independent verifier, recording order violations, spend ledger) + measure-before-fix (password rotation) + offset-based log trigger + broken-instance log-chain proof + frozen env + 2 live-test bugs + red-team catching real bugs.
- SKILL.md: added spend ledger + quoting definitions (Phase 0), structural held-out isolation (Phase 1), verifier independence + finalize-before-verify (Phase 3). The verify→propose→approve→live test→commit gate is unchanged.

### 2026-10-16 — Floor/Target for hard goals

- **A hard goal needs Floor/Target split to avoid conflicting with the stop rule:** a single threshold that is both an "ambitious target" and a stop condition forces the agent either to quit early or to loosen the metric to "reach" it. v5 splits into Floor (only this level decides pass/fail and the 3-round / no-improvement / Boss-decides loop) and Target (hard but feasible, put in the brief as the achievable level). Rule: reaching Floor without Target → PASS — the agent reports evidence about the blocking point, forbidden to change how it measures; an external verifier enforces this.

### 2026-10-16 — 5.1: Floor replaces threshold, TDD block added in Phase 2, general.md becomes v1 history.

### 2026-10-16 — 5.2: refactor becomes a Phase 3 finding, test files go into the whitelist.

### 2026-10-16 — 5.3: Phase 2 points to the tdd skill.
