# Provenance — go-http-errors

- Source repo: https://github.com/router-for-me/CLIProxyAPI
- Tag: v8.0.51. Pinned commit: `7cad1cb7df48c6c5ffb7ff0b34ef8198806115bc`.
- Survey date: 2026-11-02. Checkout (read-only, not modified, no code run):
  `~/.cache/checkouts/github.com/router-for-me/CLIProxyAPI`. HEAD verified
  equal to the pinned commit.
- License: MIT (license file head read; paraphrase only). No repo text
  copied at length; no secret values recorded (mechanisms only).
- Sources by tier: T1 explicit guidance (`AGENTS.md:54-61` — gofmt,
  no process-killing log calls, no panics in handlers, timeout policy,
  sleep guidance); T2 machine-enforced (middleware registration,
  status-mapping function); T3 history — NOT used; T4 inferred pattern,
  counts re-run by the writer (scopes stated). Researcher tables were
  leads only; every line below was re-verified by grep/read.
- Counts re-run by the writer (non-test `*.go` under `sdk/` + `internal/`
  unless stated): `%w` uses: 1053 lines; `StatusCode() int`: 34
string lines containing `StatusCode() int`, of which 21 are true
`func … StatusCode() int` definitions (23 match the `func` form,
including 2 false positives `HTTPStatusCode` and
`effectiveStatusCode`); `log.Fatal`/`log.Fatalf`: 0; `log/slog` imports: 0;
  `logrus` lines: 261 (researcher said 343 hits/300 files; the writer's
  scope differs and is the one asserted); `ForwardStream` call sites:
  6 + 1 definition.

## Evidence table

| Rule | Evidence (file:line at pinned commit) | Tier / scope / confidence | Repo follows? + count |
|---|---|---|---|
| HE-1 | `internal/clienterror/client_error.go:40-64` (status mapping: `StatusCode()` via `errors.As`, 413, 499, 504, 0 unknown); `:75-130` (separate upstream-fault sniffing layer, incl. substring match); `sdk/api/handlers/handlers_errors.go:17-19` (status via the mapping function); `sdk/cliproxy/auth/errors.go:109` and `sdk/pluginabi/types.go:182` (true `StatusCode() int` definitions) | T4 / UNIVERSAL / High for the interface pattern; Medium for "no string matching" (the sniffing layer coexists) | Enforced as the primary path. The sniffing layer is upstream-body classification, not local status mapping, and is labelled as such in the skill. Count: 21 true `func … StatusCode() int` definitions in non-test `*.go` under `sdk/` + `internal/` (34 string lines containing `StatusCode() int`; 23 match `func …StatusCode() int`, including 2 false positives `HTTPStatusCode` and `effectiveStatusCode`). `HTTPStatusCode` at `sdk/access/errors.go:51` is a different method, not `StatusCode()` evidence. |
| HE-2 | `%w` count above; `sdk/cliproxy/auth/errors.go:51-60` (typed error: code, message, retryable, HTTP status) and `:140-178` (`Unwrap` :160, `As` :167, `Is` :178); `internal/logging/diagnostic.go:27-47` (bounded diagnostic: truncates a 600-rune scan prefix first at :31, then redacts at :42-44, then truncates to 300 at :46 — truncate→redact→truncate, NOT the clean form); `sdk/api/handlers/openai/openai_responses_handlers.go:1197-1230` (clean `truncate(redact(…))` at :1203, 1225); chain breaks: `internal/api/server.go:306,325,378,381,403` and `internal/auth/claude/token.go:79` (`%v` wraps) | T4 / UNIVERSAL / High for wrapping + typed errors; Medium for redaction completeness (regex/key-name based) | PARTIAL: wrapping dominates but chain-breaking `%v` wraps exist in startup paths. Redaction completeness is not claimed. The diagnostic helper does NOT satisfy redact-before-final-truncate; only the responses-handler form does. |
| HE-3 | `internal/logging/global_logger.go:146-152` (shared logger setup, custom formatter, caller reporting); `internal/util/util.go:60-69` (debug iff debug flag, else info); `internal/logging/gin_logger.go:41-114` (request line, id only for data-plane paths, status-leveled line, health suppression, recovery); `internal/logging/requestid.go:18-22,40-65` (UUIDv7, short id = last 8 chars, context storage); `internal/util/provider.go:227-240` (header masking: authorization/api-key/apikey/token/secret substrings) and `:280-295` (query masking: key/value/api-key/apikey/api_key/token/secret); `internal/logging/gin_logger.go:44-50,97` (request line logs the raw path verbatim, only the query masked; OAuth query blanked); `internal/api/server.go:173-176,190` (middleware order); `internal/misc/credentials.go:21` (`fmt.Printf` bypass, path only) | T2 + T4 / CLASS / High for structure/levels/id; Medium for "never logs secrets" (masking is key-name based) | Enforced: 0 process-killing log calls, 0 structured-logger imports. The logger is text, not JSON; no tracing was found in the surveyed logging files. The short id is used in the log formatter and file names, while the request line carries the full id in a field. |
| HE-4 | `internal/api/server.go:267-271` (main server: only `ReadHeaderTimeout` = sniff deadline); `internal/api/protocol_multiplexer.go:17` (sniff deadline 10 s); `internal/api/server.go:138,254,260` (management + data-plane routes share the one engine); `internal/auth/claude/oauth_server.go:92-93` and `internal/auth/codex/oauth_server.go:91-92` (local callback servers: 10 s read/write) | T1 / CLASS / High | Enforced for the streaming-only main listener. The main engine serves mixed listeners; the mixed-listener combination is a recorded gap (separate listeners, or leave unscoped) — the "match, do not stack" sub-claim is DROPPED (no evidenced handler-level body deadline for mixed listeners). |
| HE-5 | `sdk/api/handlers/stream_forwarder.go:119-163` (shared loop: disconnect cancel, data/errors/keep-alive select), `:164-196` (terminal error once + flush + cancel), `:219-247` (error channel + keep-alive); 6 call sites (handlers for three protocol families); keep-alive interval config-derived with zero default (`stream_forwarder.go:151-154`, default at `sdk/api/handlers/handlers.go:58-60`, `defaultStreamingKeepAliveSeconds = 0` at :59); SSE comment keep-alive at `stream_forwarder.go:147`; flush-error handling at `:127-137,182-184` | T2 / CLASS / High | Enforced by the shared helper at 6 call sites. Counterexample: the zero keep-alive default silently disables keep-alives; the skill requires a non-zero default. WebSocket paths use separate handlers, not this loop. |

## REPO-ONLY dropped (not generalized)

- Plugin interceptor hook order — plugin-framework design, not a
  general HTTP pattern.
- Protocol multiplexer (transport sniffing on one listener) —
  deployment-specific transport trick.
- Per-protocol handler internals and upstream JSON pass-through
  details — the pass-through behaviour is noted in HE-2 only as a
  redaction boundary.

## Unevidenced / dropped (no rule written)

- Structured (JSON) logging / OpenTelemetry tracing: logger is a
  custom text formatter; `log/slog` = 0; no tracing found in
  surveyed logging files. HE-3 is NOT presented as a
  structured-logging rule.
- Honouring a client-supplied request id: ids are server-generated
  for data-plane paths only; no incoming-header honouring found.
  Dropped.
- Request-id propagation to upstream providers: a separate trace id
  exists but its upstream propagation was not verified. Not claimed.
- "No secret can leak via logs": masking is key-name/regex based; no
  allowlist audit run. Not claimed.
- "All config hot-reloads" / timeout-after-connect as a general rule:
  out of this skill's domain; the timeout rule is HE-4 only, with
  its stated exceptions.

## Observed gaps (NOT skill rules)

- G1. Chain-breaking `%v` wraps in server startup paths (files in
  HE-2). The chain is dominant, not unbroken.
- G2. Zero keep-alive default silently disables keep-alives.
- G3. The sniffing layer (substring/body-code classification) coexists
  with the typed status mapping; merging the two layers into one
  "no string matching" claim would be false.

## Fix round 1 (2026-11-02) — dry-run scope fixes, evidence re-checked

- HE-1: typed-error constructors centralizing status + code
  accepted as the mapping function; the `StatusCode()` form is
  required only where status travels in the error value across
  the handler boundary. Verified against castctl 2962686 (0
  `StatusCode() int` definitions; `apiError` constructors at
  `internal/webui/server.go:510-548`; `ExitCode()` CLI analogue
  at `internal/profile/errors.go:148-153`). The
  `StatusCode()`-via-`errors.As` evidence below still supports
  the handler-boundary form.
- HE-2: WHEN narrowed to the server handler boundary; errors
  rendered only from allowlisted fields (no untrusted text)
  satisfy the redact-before-truncate intent with no truncate
  step. Verified against castctl (`GatewayError` allowlist
  summaries at `internal/conn/errors.go:169-192`; `%v`
  chain-breaks at `internal/commands/webui.go:383,386,424,427`).
  The redact-then-truncate evidence below still supports the
  rule where untrusted text can reach the rendered string.
  Hey wording-risk also closed: the handler-boundary WHEN
  keeps terminal/display-only CLI output out of this rule
  (hey `report.go:95-97`).
- HE-3: the no-process-killing-log-call clause split out as a
  logger-independent clause applying in server code whatever
  the logger. Evidence: 0 such calls in surveyed non-test
  server code (see evidence table). Verified against castctl
  (0 such calls in server code).

## Fix round 2 (2026-11-02) — verifier + red-team fixes, evidence re-checked

- F-V5: HE-1 example replaced (`pluginabi/types.go:182`);
  `HTTPStatusCode` at `sdk/access/errors.go:51` is a different
  method; count corrected to 34 string lines / 21 true
  definitions.
- F-V6: HE-2 ordering corrected (diagnostic helper is
  truncate→redact→truncate; clean form is the responses
  handler); `Is` range corrected to `:140-178`.
- F-V7: HE-5 default path completed (`handlers.go:58-60`,
  `:59` is the zero default).
- R-9: HE-4 "match, do not stack" DROPPED — no evidenced
  handler-level body deadline for mixed listeners; mixed
  listeners fail the Check (separate, or record the gap).
- R-22: HE-1 unknown→0 with caller fallback; 499 flagged
  non-standard; typed detection named; ONE status source
  (no direct field reads outside mapper/constructors).
- R-23: HE-2/HE-3 key lists named; path-verbatim gap
  stated; pass-through call sites must name their redacting
  caller; trust boundary defined per `golang-error-handling`.
- R-36: HE-5 keep-alive default must be stated in seconds
  and > 0 (no value prescribed — gap); single terminal
  marker shared; flush error cancels, no retry, no double
  terminal write.
