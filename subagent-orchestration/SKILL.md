---
name: subagent-orchestration
description: Orchestrate subagents optimally — outcome-first (Phase 0), depth/range research, implement, review, iterate to metric. Use when delegating multi-agent work.
version: "2"
---

# Orchestrating subagents optimally

v2 — following Felix Rieseberg "How to be more ambitious": Altitude/Depth/Range.

## Phase 0: Outcome (Altitude)

Ask before every task: **what is the outcome, not what is the task.**

- Outcome / Metric + Floor + Target / Verifier (a tool the agent runs itself, not self-assessment) / Interpretation (settled BEFORE running)
  - **Floor** <number>: below this = FAIL; only the Floor decides pass/fail and the loop (3 rounds / no improvement / Boss decides).
  - **Target** <number, deliberately hard but feasible>: put it in the agent's brief, stated as achievable.
  - Reaching Floor but not Target → done (PASS). The agent reports blocking-point evidence, does not change how it measures.
- **Readiness check:** does the agent have enough data, environment, and tools to reproduce and verify itself? If not → build that first.
- **Spend ledger:** When Boss sets an invocation/cost ceiling: number each invocation against the approved ceiling (recon N, hunting M, validation K…); send the breakdown + max cost per step BEFORE running. Violating the order → record it in the run notes immediately, do not quietly let it pass.
- **Status reporting:** quote definitions verbatim from the ledger/skill (e.g. `candidate` ≠ `covered`); a critic's `stop=true` is only a gap check, not evidence of coverage.

## Pattern

```
Phase 0: OUTCOME → Phase 1: RESEARCH (parallel) → Phase 2: IMPLEMENT (1 writer)
→ Phase 3: REVIEW (parallel) → Live test → [repeat if metric < Floor]
```

Syntax on Muse: `subagent.spawn {message: "<brief>"}` (async, result returns later; manage with `subagent.list/send/resume/close`).

## Phase 1: Research (parallel)

Independent subtasks, not editing the same file, output is documentation.

**Depth — ask before writing the brief:** what would a top expert do that I have not asked for; what raw data do they start from; what method/tools do they use; what (not you or me) proves the result right.

**Range — pick agents by verb:** turn nouns into verbs ("make a busy person believe the causal story in 30 minutes" instead of "the deck"). Each agent = one domain + 1 red-team. Rule: the agent **DOES** what the expert does, does not role-play a writing voice.

**Sample brief:**
```
Outcome: <Phase 0> | Metric: <number> | Floor: <FAIL line> | Target: <hard but feasible>
Task: <one sentence> | Skill: <SKILL.md — read first>
Context: <repo, branch, 3-5 files, sample pattern>
Challenge: <assumption to check against raw data>
Discover: <odd signals / blind spots found in raw data; must validate on held-out data the agent has not seen, otherwise tag [NEEDS-MEASUREMENT]>. Use only when the task has raw data (logs, crashes, metrics); otherwise "Discover: N/A". Do not invent findings to fill gaps.
Constraints: <rules + prohibitions> | Output: <format + path> | Non-goals: <explicit>
```

**Principles:** separate output file, do not edit the repo · missing evidence → say what is needed, do not guess · at most 3-4 in parallel · review the question framing before running · conclusions tagged `[STATIC]`/`[NEEDS-MEASUREMENT]` + file:line · held-out data isolated by structure (separate worktree, brief containing no plan content), not by an instruction saying "don't look".

## Phase 2: Implement (1 writer)

Avoid conflicts when editing the same file. Add Outcome + Metric at the top of the brief. Implement only finished research (DRAFT → skip, record the reason). Not committed yet — parent decides after review. Non-goals: commit, push, PR, build.

- TDD (only when the task has testable code logic; log-only/config changes are skipped): Details (seam, mocking, anti-patterns, examples): read skill `tdd`.
  - Seam: settled in advance, Boss approves; for each seam record "catches / misses".
  - Each round: 1 seam → 1 red test → minimal code → green.
  - Expected = literal/worked example with a solution/spec; forbidden to recompute it using the code's logic.
  - Writer does not refactor. Refactor proposals become findings in Phase 3; parent decides after review. The seam's "misses" part → [NEEDS-MEASUREMENT]. The live test gate is still mandatory.
  - Test files are on the list of files allowed to be edited, declared in the brief.

## Phase 3: Review (parallel)

1. Technical 2. Safety 3. Red-team (adversarial — find ways to break it). Read-only; all must PASS before merging.
- Independent verifier brief: "you did not do the previous step — verify the record, not the agent's words". Independence produces new evidence (the verifier finds a mechanism + blind spots the hunter missed), not just a stamp.
- Finalize the artifact BEFORE the verifier sees it: verifying a version already known stale wastes a whole verifier round.

## Gate: verify → propose → approve → live test → commit

For fixes touching runtime/framework: Verify (file:line, `[STATIC]`/`[NEEDS-MEASUREMENT]`) → Propose (diff, not yet edited) → Approve (Boss approves) → Live test (measure against criteria set BEFORE) → Commit. **Approve the diff, not the summary** — inspect against criteria checkable by machine. Do not skip the live test because "the logic is already right".

## Loop after live test

`metric >= Floor → done` · `metric < Floor → back to Phase 1 with new evidence`. Stop: N rounds (default 3) / no improvement / Boss decides.

## Checklist for a new repo

No skills → write more detailed briefs to compensate. No specs → define the checklist in the brief. Simple task → merge Phase 1+2. Quote mandatory rules from AGENTS.md into the brief.

## Anti-patterns

Giving the whole repo to an agent · multiple writers · skipping Phase 0 (right task, wrong outcome) · skipping Phase 1 (guessing instead of evidence) · skipping Phase 3 · vague brief · no file limits · agent evaluating itself.

## Details

- [references/general.md](references/general.md) — v1 (history)
- [references/lessons.md](references/lessons.md) — real-world experience
