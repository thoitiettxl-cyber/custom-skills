# Provenance — go-service-lifecycle

- Source repo: https://github.com/router-for-me/CLIProxyAPI
- Tag: v8.0.51. Pinned commit: `7cad1cb7df48c6c5ffb7ff0b34ef8198806115bc`.
- Survey date: 2026-11-02. Checkout (read-only, not modified, no code run):
  `~/.cache/checkouts/github.com/router-for-me/CLIProxyAPI`. HEAD verified
  equal to the pinned commit.
- License: MIT (license file head read; paraphrase only). No repo text
  copied at length in the skill.
- Sources by tier: T1 explicit guidance (`AGENTS.md` — no lifecycle rule
  stated there beyond the timeout policy); T2 machine-enforced (none
  for these rules); T3 history — NOT used; T4 inferred pattern, counts
  re-run by the writer (scopes stated). Researcher tables were leads
  only; every line below was re-verified by grep/read.
- Counts re-run by the writer: `singleflight.Group` references: 15
  lines; files mentioning `singleflight`: 17 (`*.go`, incl. tests);
  `errgroup` hits repo-wide: 0; `sync.WaitGroup` non-test lines under
  `sdk/` + `internal/`: 11 (researcher cited 101 hits repo-wide
  including tests and other trees; the writer's narrower scope is the
  one asserted and is not used as shutdown evidence); `sync.Once`
  non-test lines under `sdk/` + `internal/`: 62 (raw count is NOT
  shutdown evidence — only the cited shutdown sites support SL-5).

## Evidence table

| Rule | Evidence (file:line at pinned commit) | Tier / scope / confidence | Repo follows? + count |
|---|---|---|---|
| SL-1 | `internal/cmd/run.go:45` and `:115` (signal-derived contexts, SIGINT/SIGTERM); `sdk/cliproxy/service_lifecycle.go:68-75` (deferred shutdown on a fresh 30 s timeout context, `:71`), `:257-262` (`Shutdown`, `shutdownOnce.Do`), `:186` (100 ms sleep before "started" print); `sdk/cliproxy/service.go:109-110` (`shutdownOnce` field); `internal/api/server.go:298` (`Start`), `:419` (`Stop`, immediate close, no drain) | T4 / CLASS / Medium | Enforced by structure, not by a check. Counterexamples: HTTP shutdown does not drain (comment at `server.go:417`); readiness is faked with a sleep. The skill states both. |
| SL-2 | `sdk/cliproxy/auth/auto_refresh_loop.go:76-94` (spawn N workers, worker selects on context done), `:58` (wake channel cap 1), `:50-60` (job buffer, config size); `sdk/cliproxy/auth/conductor_refresh.go:26-27` (5 s interval, 16 max concurrency), `:61-62` and `:1630-1636` (config override), `:1668-1688` (fan-out clamped to work count, `WaitGroup`-tracked); `sdk/cliproxy/service_plugins.go:265-275` (per-category cap + `WaitGroup` workers); `internal/config/config.go:101-103` (non-positive means default) | T4 / CLASS / High | Enforced by repetition (5 fan-out/pool sites). Counterexamples: no errgroup anywhere (0 hits); refresh-loop workers are spawned without `WaitGroup` tracking (context-owned, unjoined). Both recorded in the skill. |
| SL-3 | `internal/auth/claude/anthropic_auth.go:44` (group declaration) and `:505` (`.Do` call); same declaration shape in `internal/auth/codex/openai_auth.go:40`, `internal/auth/kimi/kimi.go:60`, `internal/auth/xai/xai.go:26`, `internal/runtime/executor/meta_executor.go:26`, `internal/managementasset/updater.go:48`, `sdk/cliproxy/antigravity_models.go:85`; paired block map `anthropic_auth.go:45-46` | T4 / CLASS / High | Enforced by repetition. The paired negative-cache map means singleflight alone is not the whole mechanism; the skill states that. |
| SL-4 | `internal/api/handlers/management/plugin_store_release.go:16` (capacity constant 2), `:121` (slots channel), `:131-157` (acquire/release `select`: acquire `:132`, release `:155`, `ctx.Done()` `:156`; release exactly once on the acquiring branch, 0 on the done branch); `internal/client/codex/live/tcp_proxy.go:25` (capacity 4), `:314` (validation slots); `internal/pluginhost/adapters_auth.go:32` (decode slots, cap 2); `sdk/cliproxy/antigravity_models.go:87` (probe slots); `sdk/cliproxy/auth/conductor.go:249,262` (weighted semaphore, one exclusion gate, max-int capacity) | T4 / CLASS / Medium | Enforced by repetition for channel semaphores (5+ named-capacity sites). The weighted semaphore appears only for the one exclusion gate — not interchangeable, per the skill. |
| SL-5 | `sdk/cliproxy/service_lifecycle.go:262` (`shutdownOnce.Do`), `:322-342` (ordered stops: watcher cancel, refresh stop, watcher stop, gateway stop, queue stop, server stop; first error kept, rest logged); `sdk/cliproxy/auth/conductor_refresh.go:73-88` (nil-guarded cancel under mutex, then selector stop); `sdk/cliproxy/service_lifecycle.go:71-75` (deferred shutdown logs, does not propagate) | T4 / CLASS / Medium | Enforced in the main shutdown path. Counterexample: stop order is not uniform across the two shutdown paths; the skill requires a documented order per service instead of implying one canonical order. |

## REPO-ONLY dropped (not generalized)

- Per-account probe workers with a queued successor — credential-
  catalog refresh design specific to this repo; the generalizable
  part is SL-2.
- Payload-configuration ordering, translator write restrictions,
  plugin `.so` loading, management-asset updater, TUI, discovery,
  relay sessions — product features or separate domains.

## Unevidenced / dropped (no rule written)

- Goroutine-leak detection: no leak-detection library usage found
  (0 hits). Not claimed; `golang-testing` owns the prescription.
- Coverage enforcement, `go vet` / lint enforcement, race detector
  in CI: 0 hits in workflows. Not claimed as repo practice; see
  `go-testing-release` provenance.
- Context-stored-in-struct audit: a targeted grep returned only
  function parameters; no rule claimed. `golang-context` owns the
  prescription.
- "Shutdown drains active connections" — CONTRADICTED (immediate
  close). Dropped; SL-1 states stop-promptly semantics.
- "Readiness is signalled" — CONTRADICTED (sleep before print).
  Dropped as a pattern; recorded as a counterexample.
- No T3 history rule is written; no history was mined. The manual
  dependency-bump observation in the research is history-only and
  was not turned into a rule.

## Observed gaps (NOT skill rules)

- G1. Raw `sync.Once` counts (62 in the writer's scope) are mostly
  unrelated lazy init, not shutdown evidence. Only the cited
  shutdown sites support SL-5.
- G2. Refresh-loop workers are unjoined and context-owned only; if
  the context is never cancelled they are never joined.
- G3. No errgroup usage anywhere; fan-out errors surface via result
  slots or logging. The skill does not present errgroup as the
  repo's pattern.

## Fix round 1 (2026-11-02) — dry-run scope fixes, evidence re-checked

- SL-1: pair requirement scoped per long-running command in CLI
  dispatch models; WHEN-NOT reworded from "short-lived CLIs" to
  one-shot commands (a single `Run()` that returns, no serve
  loop, no restart), however long one run lasts. Verified
  against castctl 2962686 (`cmd/castctl/main.go:35-37`
  signal-derived context; per-command shutdown at
  `internal/commands/webui.go:246-249`, `internal/keeper/run.go:51-64`)
  and hey 5626f79b (`hey.go:240-251` signal + `-z` timer around
  one `Run()`). The single-pair evidence below still supports
  the service case.
- SL-3: cross-process single-flight guards (owner files/flocks)
  named as a distinct, unrelated mechanism. Verified against
  castctl (`internal/keeper/run.go:164` `AcquireSingleFlight`
  vs 0 `singleflight` hits).
- SL-4: WHEN bounded to 2–16 permits in a long-running service;
  fixed worker fan-out (SL-2's shape) and stop-signal channels
  excluded. Verified against hey (`-c` default 50,
  `hey.go:54`; fan-out `requester/requester.go:235-265`;
  `stopCh` stop-signal at `requester.go:96,113`). The
  named-capacity evidence below still supports the scoped rule.
- SL-5: mutex-guarded flag idempotence accepted for closables
  reconfigured after close; `sync.Once` required only for
  terminal shutdown. Verified against castctl
  (`internal/pluginhost/host.go:329-360` applyMu-serialized
  close + `ApplyConfig`; `internal/outbound/manager.go:568-578`
  flag-guarded close). The `shutdownOnce` evidence below still
  supports the terminal-shutdown form.

## Fix round 2 (2026-11-02) — verifier + red-team fixes, evidence re-checked

- F-V4: SL-4 slots citation corrected to `:131-157`
  (acquire `:132`, release `:155`, `ctx.Done()` `:156`).
- R-2: SL-4 release is exactly once on the acquiring branch,
  0 on the `ctx.Done` branch; the weighted gate is whole-store
  exclusion, not a permit budget.
- R-24: SL-1 one-shot decision test stated in the body
  (no serve loop, never re-entered); Background shutdown
  context reconciled with `WithoutCancel` in the Priority
  note (entrypoint lifetime vs request continuation).
- R-25: SL-2 dirty-before-wake ordering stated (dirty set
  recorded before the wake send; a dropped wake is safe only
  because the dirty set persists); pool clamped to work count;
  unjoined workers are a recorded gap (G2) — cancel first,
  do not close shared resources synchronously. SL-3
  package-level group allowed only for a package's single
  operation family.
- R-26: SL-5 Check accepts `Once` for terminal shutdown OR
  mutex-guarded flag for reconfigurable closables, keyed by
  kind; stop order must name feed-before-consumer order.
