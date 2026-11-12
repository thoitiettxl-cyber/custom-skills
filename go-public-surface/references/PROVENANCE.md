# Provenance — go-public-surface

- Source repo: https://github.com/router-for-me/CLIProxyAPI
- Tag: v8.0.51. Pinned commit: `7cad1cb7df48c6c5ffb7ff0b34ef8198806115bc`.
- Survey date: 2026-11-02. Checkout (read-only, not modified, no code run):
  `~/.cache/checkouts/github.com/router-for-me/CLIProxyAPI`. HEAD verified
  equal to the pinned commit; working tree clean at survey time.
- License: MIT (license file head read; paraphrase only, no long verbatim
  copying). Distilling observed patterns by re-expression is permitted
  under that license; no repo text is copied at length in the skill.
- Sources by tier (per distill-repo-skill): T1 explicit guidance file
  (`AGENTS.md`); T2 machine-enforced (CI/lint/config — none enforces the
  layout rules here; the layout is enforced by the tree itself); T3
  history — NOT used (no history mined; no rule rests on it); T4
  inferred pattern from code, with counts re-run by the writer at the
  pinned commit (scopes stated per row). Researcher tables were treated
  as leads only; every line below was re-verified by grep/read.
- Counts re-run by the writer (scope stated; researcher counts that
  differed were not reused): `find` over `*.go` files — `sdk/` 457,
  `internal/` 1478, `cmd/` 9; no `pkg/` directory exists. Non-test files
  under `sdk/` importing the module's `internal/` packages: 228 import
  lines across 93 files; alias declarations `= internal*`: 88 across 16
  directories; `type X = internal*` declarations: 60. Non-test files
  under `internal/` importing the module's `sdk/` packages: 194.

## Evidence table

| Rule | Evidence (file:line at pinned commit) | Tier / scope / confidence | Repo follows? + count |
|---|---|---|---|
| PS-1 | `go.mod:1` (module path ends `/v8`); `AGENTS.md:25-42` (architecture list incl. `cmd/server/`, `internal/api/`, `sdk/cliproxy/`, `test/`); `cmd/server/main.go:1-5` (thin entrypoint package head); directory counts above; `pkg/` absent | T1 + T4 / CLASS (binary + embeddable core) / High for the shape | Enforced by the tree. Counterexample: the `AGENTS.md` list omits some public sub-packages (see gaps) — the list itself is stale, the shape is not. |
| PS-2 | `sdk/config/config.go:9-11` (aliases over internal config types) and `:52-54` (delegating load functions); `sdk/logging/request_logger.go:8-12` (aliases over internal logging); `sdk/api/options.go:18` (alias over internal server option); counts above; reverse imports 194 files | T4 / UNIVERSAL (public-surface honesty) / High that the facade form and the dependence exist | Enforced as the facade form. CONTRADICTED as self-containment: the public surface is not independent of `internal/` (see gaps). The rule therefore prescribes only the facade form + honest documentation, not self-containment. |
| PS-3 | `go.mod:1` (`/v8` module path); `internal/buildinfo/buildinfo.go:7-14` (dev-default vars, ldflags comment); `cmd/server/main.go:47-49` (dev-default vars) and `:56-58` (`init` copy into shared package); `Dockerfile:17` (ldflags `-X main.*`); `.github/workflows/release.yaml:177,306,430,618,627` (same `-X` flags, 5 sites) | T2 (release workflow + Dockerfile) + T1 (`AGENTS.md:8-17` build commands) / CLASS (built binaries) / High | Enforced in code and CI. Counterexample in docs only (see gaps): doc samples use `/v6` paths against a `/v8` module. |

## REPO-ONLY dropped (not generalized)

- Per-package contents of the public surface (which sub-packages exist
  and what they expose) — project-specific API inventory, not a pattern.
- The guidance file's translator-freeze governance rule
  (`AGENTS.md:44-54`) — repo governance, not a Go pattern.

## Unevidenced / dropped (no rule written)

- "The public surface is self-contained / consumers never import
  internal paths" — CONTRADICTED by PS-2 evidence (228 import lines,
  194 reverse-import files). Dropped as a description; the facade
  form is kept in PS-2.
- "Semantic versioning of the public Go API surface" — no API-stability
  policy, deprecation audit, or compatibility test found. Dropped.
- "Guidance-file layout maps and doc code samples stay current" — not
  evidenced; the map omits public sub-packages and doc samples use a
  stale major version (see gaps). Dropped as a rule.

## Observed gaps (NOT skill rules; do not present as repo practice)

- G1. Public-surface self-containment: `sdk/` depends on `internal/`
  by convention (counts above), and the facade package doc comment
  itself states it re-exports internal types "so external projects can
  embed without importing internal packages" while doing so through
  aliases — the dependence is real and must be documented, not denied.
- G2. Stale guidance map: `AGENTS.md:25-42` lists the layout but omits
  public sub-packages present in the tree (e.g. the auth, plugin-ABI,
  and config public packages). The map must be checked against the
  tree; the repo does not evidence a maintained map.
- G3. Stale doc major version: `docs/sdk-usage.md:8,17-18` and
  `docs/sdk-advanced.md:27-28,85` use `/v6` import paths against a
  `/v8` module, while `examples/` use the correct `/v8` paths. The
  version-injection rule holds in code and fails in docs. No
  docs-version rule was written from this violation.
- G4. Single-source Go pinning: `go.mod:3` says `1.26.10`,
  `release.yaml` hardcodes the same version as an env value, the PR
  and image jobs derive it from `go.mod`, and the `Dockerfile` pins
  only the minor version; no `toolchain` directive (0 hits in
  `go.mod` and workflows). The values agree by luck, not derivation.
  No pinning rule was written; see `go-testing-release` provenance
  for the same gap.

## Fix round 1 (2026-11-02) — dry-run scope fixes, evidence re-checked

- PS-1: embeddable-core definition added (external importer or
  documented public API); single-purpose asset/embed packages
  excluded. Scope decision from dry-run verification against
  castctl 2962686 (`webui/embed.go`, sole importer
  `internal/commands/webui.go:23`) and hey 5626f79b
  (`requester/` exported, sole consumer `hey.go:32`, no library
  docs, no `examples/`). CLIProxyAPI evidence unchanged.
- PS-3: converted to a reference-only pointer to TR-5
  (`go-testing-release`). Deduplication decision: one canonical
  rule (TR-5), no duplicated prescription. The `init`-copy +
  ldflags evidence below still supports TR-5; nothing here
  prescribes version injection anymore.

## Fix round 2 (2026-11-02) — verifier + red-team fixes

- R-11: PS-3 "single copy point" sentence removed; PS-3 now states
  only that version variables live where TR-5 places them. TR-5's
  two-source shape is canonical.
- R-30/R-31: PS-1 "thin" and "catch-all surface" defined by role
  and concern (see SKILL.md); PS-2 alias-vs-real-type decision
  test added (alias only when the type's data lives in
  `internal/`); alias counts stated as evidence, never a target.
