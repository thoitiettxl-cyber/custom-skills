# custom-skills

Custom skills for [Muse](https://muse.ai) — reusable playbooks for coding,
debugging, research, media pipelines, and agent orchestration.

Each skill lives in its own directory with a `SKILL.md` describing when and
how to use it:

- `api-design` — API design patterns
- `cli-creator` — scaffold CLIs
- `code-review` — review code against standards and spec
- `codebase-design` — deep-module design, seams, testability
- `codemode` — bundle shell/file/MCP steps into one JS sandbox script
- `commit` — commit message format
- `diagnosing-bugs` — hard-bug and perf-regression diagnosis loop
- `domain-modeling` — glossary + ADR modeling
- `ghidra` — binary analysis via Ghidra headless
- `github` — GitHub workflows
- `grill-with-docs` — grill a plan while producing docs
- `grilling` — ruthless stress-test of a plan or idea
- `heal` — self-healing for the Hatch VM
- `improve-codebase-architecture` — architecture review with visual HTML report
- `librarian` — shared cache checkout management
- `linkage-checks` — turn definition/usage invariants into check scripts
- `mcp-builder` — MCP server development guide
- `mcp-client` — MCP client wrapper
- `native-web-search` — fast query+purpose web research pattern
- `search-playbook` — search routing: need → lookup channel
- `subagent-orchestration` — coordinate subagents efficiently
- `summarize` — summarization conventions
- `tdd` — red → green test-first at chosen seams
- `technical-scoping-workflow` — technical scoping: baseline → gaps → phases
- `tmux` — tmux workflows
- `update-changelog` — changelog process
- `uv` — uv quick reference
- `verify-before-claiming` — verify against primary sources before asserting

## Layout convention

Skills are indexed by their `SKILL.md` H1 line, which is written in
Vietnamese as a one-line summary of purpose + trigger (the search index uses
the H1 and ignores the frontmatter `description:`).

## License

MIT — see [LICENSE](LICENSE).
