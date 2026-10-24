---
name: native-web-search
description: "Quick web-research pattern: separate the query from its purpose, get a concise summary with full source URLs per finding. Use when you need fast internet research with explicit URLs and disagreements called out."
---

# Fast web search following the query + purpose pattern — use when you need quick research, a concise summary with full source URLs for each finding

(The original came with `search.mjs` running on the Pi runtime — dropped by Boss's decision.
This skill keeps only the pattern, mapped onto this system's search tools.)

## Pattern

Keep two things separate in every research pass:

- **query**: what to find (e.g. "latest python release")
- **purpose**: why it is needed (e.g. "update dependency notes") — the purpose decides
  which information is worth keeping and which to drop.

## How to run on this system

- Quick research: `browser.search`, setting a suitable `verticals`
  (`news`, `sports`, `weather`, `finance`, `datetime`).
- Deep research, needing cross-checking across many sources: `browser.deep_research`.
- Fallback when needed: Exa / Firecrawl via MCP.

## Output expectations

Every research result following this pattern must have:

- 3–7 key findings; each finding consists of: a title, why it matters **for
  the stated purpose**, and a full canonical URL (`https://...`)
- wherever sources disagree, name the disagreement explicitly, do not hide it
- end with a short recommendation: which source(s) to trust first

## Sample prompt (when handing research to a subagent or another model)

```
Search the internet for: <query>

Purpose: <purpose>

Return a concise research summary with:
- 3 to 7 key findings
- for every finding: title, why it matters for this purpose, and a full canonical URL (https://...)
- if multiple sources disagree, call that out
- finish with a short recommendation on which source(s) to trust first.
```

## Notes

- Every finding must carry a real, readable URL — do not invent URLs to fill gaps.
- Clearly distinguish "read from a source" from "inference" (see skill `verify-before-claiming`).
