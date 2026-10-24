# Optimal subagent orchestration process — v1 (history)

## Overview
3-phase pattern proven on SpoofX (3 researchers → 1 writer → 2 reviewers, all PASS):
```
Phase 1: RESEARCH (parallel) → Phase 2: IMPLEMENT (sequential) → Phase 3: REVIEW (parallel)
```

## Phase 1: Research (parallel)

**When parallel works:** subtasks are independent, do not edit the same file, output is documentation (not code).

**Sample brief for each agent:**
```
Task: <one sentence, specific>
Skill: <SKILL.md path — must read before working>
Context:
- Repo: <path, branch>
- Related files: <3-5 files, not the whole repo>
- Existing pattern: <sample file to follow>
Constraints:
- <relevant rules, only the necessary ones>
- <specific prohibitions>
Output: <format + output file path>
Non-goals: <explicit list of what NOT to do>
```

**Principles:**
- Each agent outputs to its own markdown file (does not edit the repo)
- If evidence is insufficient: the agent must say what it needs, must not guess
- At most 3-4 agents in parallel (more is hard to track)

## Phase 2: Implement (sequential — 1 writer)

**Why sequential:** avoid conflicts when multiple agents edit the same file/area.

**Sample brief:**
```
Task: <implement from the research packages>
Skill: <the repo's implement skill>
Inputs: <list of research outputs from Phase 1>
Existing code: <sample files to follow>
Rules: <mandatory rules>
What to do: <specific steps>
Constraints:
- <coding conventions>
- <prohibitions>
- Edit only: <list of permitted files>
Output: <edited files, uncommitted> + summary markdown
Non-goals: commit, push, PR, build, test on device
```

**Principles:**
- The writer does NOT decide scope itself — it implements only what Phase 1 has fully researched
- If a research item is in DRAFT state → the writer skips it, stating the reason clearly
- Output is uncommitted — the parent decides on merging after review

## Phase 3: Review (parallel)

**2 reviewer types running in parallel:**
1. **Technical reviewer**: wiring, patterns, conventions, correctness
2. **Safety reviewer**: security, privacy, charter boundaries

**Sample brief:**
```
Role: <reviewer role>
Spec: <path to reviewer spec if any>
What to review: <git diff or list of files>
Checklist: <specific items from the spec>
Output: Verdict PASS/FAIL + issues with file:line, written to markdown
Non-goals: editing code, committing
```

**Principles:**
- Reviewers are read-only (do not edit files)
- Both must PASS before merging
- Non-blocking warnings are recorded but do not block

## Checklist for applying to a new repo

When bringing this pattern to another repo, determine:

1. **Skills**: does the repo have skills for research/implement/review? If not, write more detailed briefs to compensate.
2. **Reviewers**: are there reviewer specs? If not, define the checklist manually in the brief.
3. **Rules**: read the repo's AGENTS.md + rules, extract the mandatory points into the brief.
4. **Phases**: can the task be split into research/implement/review? If the task is simple (1 file, clear), merge Phase 1+2.
5. **Parallel**: are the subtasks independent? Do they edit the same file?

## Anti-patterns

1. **Giving the whole repo to an agent** → context too large, slow, many errors
2. **Multiple writers at once** → conflicts, hard to review
3. **Skipping Phase 1** → the writer guesses instead of relying on evidence
4. **Skipping Phase 3** → safety errors slip into code
5. **Vague brief** → the agent works in the wrong direction, must redo
6. **No limits on editable files** → the agent edits sprawlingly outside scope
