---
name: codemode
description: Run model-written JavaScript in a QuickJS sandbox (worker thread) with 4 system tools read/write/exec/mcp. Use when you need to combine many read-write-run-command-call-MCP steps into a single script instead of calling individual tools — nested tool calls do not enter LLM context, only output and return value do.
---

# Codemode — combining many file read/write, shell run, and MCP call steps into one JS script in a sandbox

The system has codemode registered by default: run model-written JS in the QuickJS VM
(WebAssembly), whose only capability is calling tools injected from the host.
Based on `@earendil-works/pi-codemode@1.2.0` (exact pin). Code at `~/workspace/codemode/`,
binary at `~/.local/bin/codemode`, state at `~/.config/codemode/store.json`.
Public repo: `thoitiettxl-cyber/muse-codemode` (with `smoke.sh` — 10 checks).
Everything lives under `~`, so per AGENTS.md:62 it survives a VM replace (home is a separate btrfs volume mounted at `/home/hatch`).

## When to use instead of individual tool calls

- Need a **multi-step chain** (read file → process → write file → run command → call MCP) where each step
  depends on the previous step's result: write one script, run it once, receive only output + return value.
- Need **loops / branching / try-catch** around tool calls without spending many LLM turns.
- Do NOT use when only 1-2 simple tool calls are needed — calling them directly is faster.

## Usage

```bash
codemode script.js              # run a script from a file
echo 'return 1+1' | codemode    # or from stdin
codemode --declarations         # print TypeScript declarations of the 4 tools (always true to the code)
codemode --json script.js       # machine-readable JSON output
codemode --timeout-ms 120000 script.js
codemode --no-store script.js   # do not use the persistent store()
```

A script is the body of an async function: top-level `await` and `return` work.
The first line may be: `// @options: {"max_output_tokens": 2000, "timeout_ms": 30000}`
(`timeout_ms` is a hard deadline for the whole script, `max_output_tokens` truncates output).

Inside a script: `tools.read/write/exec/mcp`, `ALL_TOOLS`, `text()`, `image()`,
`console.*`, `exit()`, `store(key, value)` / `load(key)` (persist across runs).

Exit codes: 0 ok, 1 script error, 2 timeout, 3 aborted, 4 sandbox/host error,
5 bad `// @options:` line, 6 usage error.

## Default tools (see `codemode --declarations` for the latest version)

- `read({path, encoding?, maxBytes?})` — read a file under `$HOME` (relative paths resolve from `$HOME`).
- `write({path, content, encoding?})` — write a file under `$HOME`, creating parent directories automatically.
- `exec({command, args?, cwd?, timeoutMs?, shell?, maxOutputBytes?})` — run a command;
  **always has a timeout** (default 30s, max 120s); a hanging command is SIGKILLed and reported as an error;
  `cwd` defaults to `$HOME` and must be under `$HOME`; `shell:true` to use pipes/globs via bash.
- `mcp({server, name, args?, timeoutMs?})` — call an MCP tool over a **persistent session**
  (connect once per run, reuse for every call — multi-step workflows keep
  server-side state between calls); servers: openai-docs, xai-docs,
  anthropic-docs, context7, exa, firecrawl, inspo.

Every path in `read`/`write`/`exec.cwd` is blocked if it escapes `$HOME`.

## Sample scripts

```js
// read package.json, count dependencies, write a report, return the count
const src = await tools.read({ path: "workspace/codemode/package.json" });
const deps = Object.keys(JSON.parse(src).dependencies ?? {});
const out = await tools.write({
  path: "workspace/codemode/deps.txt",
  content: deps.join("\n") + "\n",
});
text(`wrote ${out.bytes} bytes`);
const ls = await tools.exec({ command: "ls", args: ["workspace/codemode"] });
text(ls.stdout);
return deps.length;
```

```js
// call MCP: look up quickjs docs via context7 (resolve libraryId first, separate 20s timeout)
const lib = await tools.mcp({
  server: "context7",
  name: "resolve-library-id",
  args: { query: "QuickJS memory limit", libraryName: "quickjs" },
  timeoutMs: 20000,
});
text(String(lib).slice(0, 500)); // pick a libraryId (form "/org/project") from the result
const doc = await tools.mcp({
  server: "context7",
  name: "query-docs",
  args: { libraryId: "/quickjs-ng/quickjs", query: "QuickJS memory limit" },
  timeoutMs: 20000,
});
text(doc.slice(0, 500));
return "done";
```

## Notes

- Script error (uncaught throw, tool rejection) → `result.ok=false`, CLI exit 1, stderr has a `codemode.js:<line>` stack.
- Script hanging without calling a tool (infinite loop) → `timeout` failure, worker terminated, runner does not hang.
- `store()`/`load()` save to `~/.config/codemode/store.json`; use `--no-store` to disable.
- Limits: the QuickJS VM is an interpreter (heavy computation is slower than V8); no timers/fetch/process/require in scripts — all I/O goes through tools.
