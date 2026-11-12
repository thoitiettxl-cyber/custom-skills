# Golang always-load routing — load the primary Go skill and all applicable secondary skills together at the start of every Go task

This skill embeds the skill-routing logic from `golang-always_0_51dn.mdc` (a Cursor rule, `alwaysApply: true`, globs `**/*.go`, `**/go.mod`, `**/go.sum`, `**/go.work`). It applies to every Go file in the project and to every Go task. There is no Cursor `alwaysApply` mechanism in Muse, so this skill is the enforcement point: when a task touches Go, find this skill first and follow its routing before doing the work.

## How skill names map to this VM

Every `golang-<name>` in the tables below is a local skill installed verbatim from `samber/cc-skills-golang`. Read it at `~/workspace/custom-skills/golang-<name>/SKILL.md`, or find it with `muse.skill_search` by that name. The source file wrote the names as `samber/cc-skills-golang@<name>`; on this VM the local path is the authoritative form.

- Load the primary skill and all applicable secondary skills at the same time, at the start of the task. Do not wait and do not load them one at a time as the work proceeds.
- When you delegate Go work to a subagent, put the skill path in the brief, in the form `Skill: ~/workspace/custom-skills/golang-<name>/SKILL.md — read it first`, for the primary skill and for every applicable secondary skill.
- If a task matches more than one row in the routing table, load the primary and secondary skills for every matching row.

Verified 2026-10-28: all 45 distinct `golang-*` names named in the source file have a local directory under `~/workspace/custom-skills/` with a `SKILL.md`. The 46th installed skill, `golang-how-to`, is not named in the source tables and is not added here.

Not verified on this VM, 2026-10-28: `go`, `gopls`, `godig` and `govulncheck` were not found (`command -v` returned nothing and `go version` failed). The `gopls` and `godig` sections below are preserved from the source file, but no `gopls`, `godig` or `govulncheck` run was made on this VM. Before claiming any of those tools works here, check that the binary exists. If it does not, say so and stop at that step instead of faking its output. Do not install a Go toolchain, `gopls`, `godig` or `govulncheck` on the basis of this skill alone; that needs a separate approval.

The `go-*` skills named in the routing table below (`go-public-surface`, `go-provider-registry`, `go-config-reload`, `go-credential-stores`, `go-management-api`, `go-http-errors`, `go-service-lifecycle`, `go-testing-release`) are NOT part of the samber set above. They are local skills distilled from CLIProxyAPI v8.0.51 (commit `7cad1cb7df48c6c5ffb7ff0b34ef8198806115bc`), installed under `~/workspace/custom-skills/go-*/SKILL.md`, and are not covered by the 2026-10-28 verification of the 45 `golang-*` names. Each `go-*` row states its own narrow trigger; the `golang-*` skill in its Also Load column still governs the general case — load both, and follow the `go-*` skill only inside its stated scope.

## Skill Loading Rules

For each Go task, load the **primary skill** and all applicable **secondary skills** at the same time. Do not wait — load them together at the start.

| Intent | Primary Skill | Also Load |
| --- | --- | --- |
| Design an API, choose a pattern | `golang-design-patterns` | `golang-structs-interfaces`, `golang-naming` |
| Name a type, function, or package | `golang-naming` | `golang-code-style` |
| Handle errors idiomatically | `golang-error-handling` | `golang-safety` (nil-heavy code) |
| Write goroutines, channels, sync | `golang-concurrency` | `golang-context` (if cancellation) |
| Pass deadlines / cancel operations | `golang-context` | `golang-concurrency` (if goroutines) |
| Design structs, embed, use interfaces | `golang-structs-interfaces` | `golang-design-patterns` |
| Database queries and transactions | `golang-database` | `golang-error-handling`, `golang-security` |
| Build a gRPC service | `golang-grpc` | `golang-testing`, `golang-error-handling` |
| Build a GraphQL API | `golang-graphql` | `golang-testing`, `golang-error-handling` |
| Build a CLI command tree | `golang-spf13-cobra` | `golang-cli`, `golang-spf13-viper` (if config) |
| Layer config from flags/env/file | `golang-spf13-viper` | `golang-spf13-cobra` |
| Write tests | `golang-testing` | `golang-stretchr-testify` (if using testify) |
| Apply optimization patterns | `golang-performance` | `golang-benchmark` (measure first) |
| Measure with pprof / benchstat | `golang-benchmark` | `golang-performance` (fix), `golang-troubleshooting` (root cause) |
| Debug a panic or unexpected behavior | `golang-troubleshooting` | `golang-safety`, `golang-benchmark` (if perf-related) |
| Monitor in production | `golang-observability` | `golang-performance` (if SLO breach) |
| Audit security vulnerabilities | `golang-security` | `golang-safety`, `golang-lint` |
| Review formatting and style | `golang-code-style` | `golang-naming`, `golang-lint` |
| Refactor or restructure existing code | `golang-refactoring` | `golang-naming`, `golang-code-style`, `golang-project-layout` |
| Configure golangci-lint | `golang-lint` | `golang-code-style` |
| Write godoc / README / CHANGELOG | `golang-documentation` | `golang-naming` |
| Set up a new project structure | `golang-project-layout` | `golang-design-patterns`, `golang-dependency-injection`, `golang-lint` |
| Set up CI/CD pipeline | `golang-continuous-integration` | `golang-lint`, `golang-security` |
| Choose a library | `golang-popular-libraries` | relevant library-specific skill |
| Look up a package's docs, versions, importers, or CVEs | `golang-pkg-go-dev` | `golang-dependency-management` |
| Navigate, diagnose, or refactor local code | `golang-gopls` | — |
| Adopt new Go language features | `golang-modernize` | `golang-lint` |
| Use samber/lo (slice/map helpers) | `golang-samber-lo` | `golang-data-structures`, `golang-performance` |
| Use samber/oops (structured errors) | `golang-samber-oops` | `golang-error-handling` |
| Use log/slog | `golang-samber-slog` | `golang-observability`, `golang-error-handling` |
| Use dependency injection | `golang-dependency-injection` | `golang-google-wire` or `golang-uber-dig` or `golang-uber-fx` or `golang-samber-do` |
| Structure a Go module with both a binary and an embeddable core (thin entrypoints, one public surface, facade re-exports) | `go-public-surface` | `golang-project-layout`, `golang-naming` |
| Dispatch work to several interchangeable upstream implementations behind one contract, with more than one credential per upstream (manager-owned keyed executor registry, credential selection, bounded failover — not a global registry) | `go-provider-registry` | `golang-dependency-injection`, `golang-structs-interfaces` |
| Load one config document without a config library in a Go server and reload it live (single hand-rolled loader, hash-gated watcher, two-phase apply) | `go-config-reload` | `golang-spf13-viper` (if a layered config library is chosen) |
| Persist renewable credentials to disk in a Go server, refresh them on a schedule, or store an operator secret in config (file modes, atomic replacement, hashed secrets) | `go-credential-stores` | `golang-security` |
| Expose an operator/management surface on the same process as the data plane in a Go server (separate route group, own auth, gating, per-IP failure bans, stable error shape, config ETags) — backend mechanics only; versioning/naming/pagination stay with `api-design`, the client contract with `management-center-webui` | `go-management-api` | — |
| Map errors to HTTP statuses, log requests, or forward streaming responses in a Go HTTP server (typed errors with redaction, status-leveled logging, streaming timeout policy) | `go-http-errors` | `golang-error-handling`, `golang-observability`, `golang-samber-slog` |
| Run a long-running Go daemon or embeddable service that owns background work and must stop cleanly (signal-derived context, worker pool, dedup, semaphores, idempotent ordered shutdown) | `go-service-lifecycle` | `golang-concurrency`, `golang-context`, `golang-design-patterns` |
| Write tests or release automation for a Go binary in the surveyed shape (co-located table tests, httptest fakes, deterministic clocks, build-tag variant pairs, ldflags version injection, tag-triggered hand-rolled releases) | `go-testing-release` | `golang-testing`, `golang-continuous-integration` |

## Competing Clusters — Boundary Lines

Key clusters and their owners:

- **Performance**: `golang-performance` (optimization) · `golang-benchmark` (measurement) · `golang-troubleshooting` (root cause) · `golang-observability` (always-on production)
- **DI**: `golang-dependency-injection` (concepts/decision) · `golang-google-wire` (compile-time) · `golang-uber-dig` (runtime reflection) · `golang-uber-fx` (lifecycle) · `golang-samber-do` (type-safe container)
- **samber/\***: `golang-samber-lo` (finite transforms) · `golang-samber-ro` (reactive streams) · `golang-samber-mo` (monadic types)
- **Errors**: `golang-error-handling` (idioms) · `golang-samber-oops` (structured errors) · `golang-safety` (prevent panics)
- **Style**: `golang-code-style` · `golang-naming` · `golang-lint` · `golang-documentation`
- **CLI**: `golang-cli` (architecture) · `golang-spf13-cobra` (command tree) · `golang-spf13-viper` (config layering)
- **Package lookup**: `golang-pkg-go-dev` (query pkg.go.dev) · `golang-gopls` (navigate local build) · `golang-popular-libraries` (which lib) · `golang-dependency-management` (manage go.mod) · `golang-security` (CVE scan)
- **Gap — type vs arch**: `golang-structs-interfaces` vs `golang-design-patterns`
- **Gap — goroutine vs cancel**: `golang-concurrency` + `golang-context` — load both when cancelling goroutines via context
- **Gap — correctness vs threat**: `golang-safety` (internal bugs) vs `golang-security` (external threats)
- **Gap — features vs rules**: `golang-modernize` (language adoption) vs `golang-lint` (static analysis config)
- **Gap — process vs target rules**: `golang-refactoring` (safe process) vs `golang-naming`/`golang-code-style`/`golang-project-layout`/`golang-design-patterns`/`golang-modernize` (target shape) — load `golang-refactoring` alongside whichever owns the target shape

## Code Navigation with gopls

`gopls` gives semantic code intelligence for Go — go-to-definition, find references, diagnostics, package API, symbol search, refactoring. See the `golang-gopls` skill at `~/workspace/custom-skills/golang-gopls/SKILL.md` for the three ways to reach it (MCP server, native LSP tool, CLI), capability matrix, and efficient workflows.

`gopls` only reasons about code present and resolvable in your local build: workspace plus every dependency exactly as pinned in `go.sum` (including `replace` directives). For facts not tied to your local build — version history, licenses, ecosystem-wide importers, a package you haven't added yet — use `golang-pkg-go-dev` (`godig`).

## `godig` vs gopls vs Context7 vs govulncheck

| Task | Tool |
| --- | --- |
| Find where a symbol is defined in your repo | `gopls` |
| Understand a file's intra-package deps | `gopls` |
| Jump into a dependency's exact resolved source (incl. forks/replace) | `gopls` |
| Find every call site in your code referencing a dep's symbol | `gopls` |
| Get compiler diagnostics right after an edit | `gopls` |
| Check if current build reaches a known vulnerability (mid-edit) | `gopls` |
| Rename, extract, inline, or refactor local code | `gopls` |
| Whole-tree vulnerability audit (CI, periodic sweep) | `govulncheck` |
| List available versions of a published package | `godig` |
| Check known CVEs for a package/version not yet added | `godig` |
| See exported symbols/signatures of a published package | `godig` |
| Get runnable code examples for a symbol | `godig` |
| Read a package's rendered README/docs | `godig` |
| See who imports a package across public ecosystem | `godig` |
| Search for a package or library candidate | `godig` |
| Check a package's or module's license | `godig` |
| Get docs for non-Go lib or Go module not on pkg.go.dev | Context7 |

## Categories at a Glance

| Category | Skills |
| --- | --- |
| Code Quality | `golang-code-style` `golang-documentation` `golang-error-handling` `golang-lint` `golang-naming` `golang-safety` `golang-security` `golang-structs-interfaces` |
| Architecture & Design | `golang-concurrency` `golang-context` `golang-data-structures` `golang-database` `golang-dependency-injection` `golang-design-patterns` `golang-modernize` `golang-refactoring` |
| QA & Performance | `golang-benchmark` `golang-observability` `golang-performance` `golang-testing` `golang-troubleshooting` |
| Project Setup | `golang-cli` `golang-continuous-integration` `golang-dependency-management` `golang-gopls` `golang-pkg-go-dev` `golang-popular-libraries` `golang-project-layout` `golang-stay-updated` |
| APIs | `golang-graphql` `golang-grpc` `golang-swagger` |
| Dependency Injection | `golang-dependency-injection` `golang-google-wire` `golang-uber-dig` `golang-uber-fx` `golang-samber-do` |
| Frameworks | `golang-spf13-cobra` `golang-spf13-viper` |
| samber/\* | `golang-samber-do` `golang-samber-hot` `golang-samber-lo` `golang-samber-mo` `golang-samber-oops` `golang-samber-ro` `golang-samber-slog` |
| Testing | `golang-stretchr-testify` `golang-testing` |

## Available connectors

- [Golang Always](~/workspace/custom-connectors/custom.golang-always/CONNECTOR.md) for the connector listing that points at this routing skill; it carries the same tables and no API, credential or helper.

- Use `muse.connector_search` to find other connectors and `muse.skill_search` to find related skills.

- If nothing here fits, look on the web for a maintained API or MCP server and set it up with [Custom Connectors and MCPs](/opt/muse/skills/custom-connector-setup/SKILL.md), or build a custom connector.
