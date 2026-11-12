# Provenance — go-provider-registry

- Source repo: https://github.com/router-for-me/CLIProxyAPI
- Tag: v8.0.51. Pinned commit: `7cad1cb7df48c6c5ffb7ff0b34ef8198806115bc`.
- Survey date: 2026-11-02. Checkout (read-only, not modified, no code run):
  `~/.cache/checkouts/github.com/router-for-me/CLIProxyAPI`. HEAD verified
  equal to the pinned commit.
- License: MIT (license file head read; paraphrase only). No repo text
  copied at length in the skill.
- Sources by tier: T1 explicit guidance (`AGENTS.md` — no provider-registry
  rule stated there; the rules are T4); T2 machine-enforced (none for
  these rules); T3 history — NOT used; T4 inferred pattern, counts
  re-run by the writer (scopes stated). Researcher tables were leads
  only; every line below was re-verified by grep/read.
- Counts re-run by the writer: key-method implementations in the
  implementation directory: 13; `New*Executor` constructors: 17;
  `RegisterExecutor(` non-test call sites repo-wide: 17; `func init()`
  in the executor implementation directory: 0; `func init()` across the
  translator packages: 26; optional-capability assertion sites: 7
  (re-verified by reading the cited sites).

## Evidence table

| Rule | Evidence (file:line at pinned commit) | Tier / scope / confidence | Repo follows? + count |
|---|---|---|---|
| PR-1 | `sdk/cliproxy/auth/conductor.go:17-36` (6-method interface: key, unary, streaming, refresh, token count, raw-request injection); `:38-66` (small optional interfaces: key-config view, auth preparer, session closers/sharer); `sdk/cliproxy/auth/conductor_execution.go:123,240` (dispatch through manager execute methods) | T4 / CLASS (multi-upstream dispatch) / High | Enforced. 13 key-method implementations, 17 constructors. No dispatch path bypasses the interface in the sampled loops. Asymmetry noted: the raw-request injection method mixes a transport concern into the executor contract. |
| PR-2 | `sdk/cliproxy/auth/conductor.go:178` (map field on the manager); `sdk/cliproxy/auth/conductor_lifecycle.go:37-71` (register: trim, empty/nil rejected silently, last-wins, reschedule, close replaced sessions unless sharing declared); `:74-83` (unregister: lowercase + trim) | T4 / CLASS / High | Enforced. Note the normalization asymmetry: register trims only, unregister lowercases and trims, and lookup trims — the rule states the observed behaviour and requires checking that registration took effect; it does not claim uniform normalization. |
| PR-3 | `sdk/cliproxy/service_executors.go:261-340` (per-credential switch with 10+ cases and a `default` compatibility branch); `:241-259` (per-credential loop with dedup guards); `func init()` counts above | T4 / CLASS / High | Enforced for executors; the opposite (init-registration) is enforced for conversion packages — split by extension-point kind. Counterexample: the `default` branch silently maps any unknown key to a compatibility implementation (fail-open); the skill flags it, it does not copy it. |
| PR-4 | `sdk/cliproxy/auth/conductor.go:107-109` (`Selector` interface, `Pick` over loaded candidates); `sdk/cliproxy/auth/selector.go:33,40,72` (two stateful strategies holding mutexes — `RoundRobinSelector` :33-37, `WeightedRoundRobinSelector` :40-44 — and the stateless `FillFirstSelector`, an empty struct with no mutex, at :72) and `:912` (affinity decorator wrapping a fallback); `sdk/cliproxy/service_config.go:101-121` (config strategy string to selector, affinity applied last); `sdk/cliproxy/auth/conductor_selection.go:426` (`SetSelector`) | T4 / CLASS / High | Enforced. Only the two stateful selectors hold mutexes; `FillFirstSelector` is stateless. |
| PR-5 | `sdk/cliproxy/auth/conductor_execution.go:522-583` (tried-set, pick-excluding-tried, result recording after each attempt); `:123-218,240-292` (retry loops); `sdk/cliproxy/auth/conductor_cooldown.go:889` (result-recording method); `sdk/cliproxy/auth/conductor_lifecycle.go:20-35` (retry config clamps negatives to 0); `internal/config/config.go` retry knobs applied in `sdk/cliproxy/service_config.go:253-275` | T4 / CLASS / High | Enforced. Counterexample: three parallel loop bodies duplicate the tried-set logic (unary, count, stream) and can drift; the skill requires reviewing all three. |
| PR-6 | `sdk/translator/registry.go:30-52` (`Registry.Register` / `RegisterRequestEnvelope`), `:371-390` (package default registry, `Default()`, package `Register` delegating); format constants in `sdk/translator/format.go`; `init()` registration in conversion packages (e.g. `internal/translator/antigravity/openai/chat-completions/init.go:9`); external registration in `examples/custom-provider/main.go:52` | T4 / CLASS / High | Enforced, in tension with the DI ban (see skill conflict note). The global default is mutable package state; the rule requires the constructible registry for tests. No aggregate registration count is asserted (researcher and writer counts differed by scope). |

## REPO-ONLY dropped (not generalized)

- Per-implementation internals (transports, refresh flows, streaming
  executors, payload-translation ordering) — domain logic for
  upstream proxying, not a transferable pattern.
- Per-upstream config sections and model-catalog registries — domain
  sections; the transferable part (per-section sanitize) is in
  `go-config-reload`.
- Control-plane integration and plugin-ABI versioning — separate
  domains; the sequence-gated apply is in `go-config-reload`.

## Unevidenced / dropped (no rule written)

- "Executor registration is thread-safe for concurrent register +
  dispatch" — locking exists but no race test or lock-ordering proof
  was examined. Dropped.
- "Global default registry is safe for tests" — CONTRADICTED by
  mutability; the rule requires the constructible form for tests.
- No T3 history rule is written; no history was mined.

## Observed gaps (NOT skill rules)

- G1. Silent registration rejection: nil/empty-key executors are
  ignored without an error (`conductor_lifecycle.go:38-43`). The
  skill requires checking effect; it does not present silent-ignore
  as a recommended design.
- G2. Key normalization is not uniform across register/unregister/
  lookup (see PR-2). No "normalize everywhere" rule is presented as
  repo practice; the asymmetry is recorded here.
- G3. Global default registry vs DI ban: unresolved tension, scoped
  in the skill to declarative conversion tables with an injectable
  alternative. Outside that scope the existing DI skill wins.

## Fix round 1 (2026-11-02) — dry-run scope fixes, evidence re-checked

- PR-2: plugin hosts excluded unless they expose executor-style
  `Register`/`Unregister`. Verified against castctl 2962686
  (`internal/pluginhost/host.go:119` keyed `loaded` map,
  `ApplyConfig` at `:360-369`, no `Register`/`Unregister` API).
  Evidence below unchanged.
- PR-3: scoped to service/executor wiring the project owns; CLI
  dispatch tables with a fixed order list and dependency-owned
  registries excluded. Verified against castctl
  (`internal/commands/commands.go:751-760` table + `commandOrder`,
  11 `init()` functions in `internal/commands/`; sing-box
  registry consumed at `internal/outbound/manager.go:43-48,243`).
  The surveyed switch evidence below still supports the scoped
  rule (executor wiring in `service_executors.go`).

## Fix round 2 (2026-11-02) — verifier + red-team fixes, evidence re-checked

- F-V1: PR-4 `Selector` citation corrected to `conductor.go:107-109`
  (`:110-113` is `PluginScheduler`). F-V10: PR-4 softened — only
  the two stateful selectors hold mutexes; `FillFirstSelector`
  (`selector.go:72`) is stateless.
- R-1: PR-3/PR-6 collision resolved with one decision test (pure
  constant-keyed entries + constructible registry); evidenced by
  `sdk/translator/registry.go:22-52,371-390` (`NewRegistry`,
  package default) and the pure-function `init()` registrations
  (26 files, e.g. `internal/translator/antigravity/openai/
  chat-completions/init.go:9`).
- R-7: PR-2 lookup exists — `Executor(provider) (ProviderExecutor,
  bool)` at `sdk/cliproxy/auth/conductor_selection.go:1769`;
  same-instance no-close at `conductor_lifecycle.go:62-64`, close
  after unlock at `:56` / `:68-70`. The reviewer's "no lookup"
  sub-claim is refuted by that method.
- R-13: PR-1 composition form is per `golang-structs-interfaces`
  (read in full); the surveyed flat 6-method interface is kept
  only scoped to the dispatch case with all six behaviours real.
- R-14: PR-5 zero meanings verified: per-round cap 0 = no cap
  (`conductor_execution.go:532`, `> 0` gate); retry 0 = no round
  beyond the first attempt (limit compared at
  `conductor_selection.go:1177,1322,1420`).
