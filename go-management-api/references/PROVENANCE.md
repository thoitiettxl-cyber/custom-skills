# Provenance — go-management-api

- Source repo: https://github.com/router-for-me/CLIProxyAPI
- Tag: v8.0.51. Pinned commit: `7cad1cb7df48c6c5ffb7ff0b34ef8198806115bc`.
- Survey date: 2026-11-02. Checkout (read-only, not modified, no code run):
  `~/.cache/checkouts/github.com/router-for-me/CLIProxyAPI`. HEAD verified
  equal to the pinned commit.
- License: MIT (license file head read; paraphrase only). No repo text
  copied at length; no secret values recorded (mechanisms only).
- Sources by tier: T1 explicit guidance (`AGENTS.md` — frozen legacy
  version note only; no management-auth rule stated there); T2
  machine-enforced (route registration gates, middleware wiring);
  T3 history — NOT used; T4 inferred pattern, counts re-run by the
  writer (scopes stated). Researcher tables were leads only; every line
  below was re-verified by grep/read.
- Counts re-run by the writer: `gin.H{"error"` in files under
  `internal/api/handlers/management/` (`*.go`, including tests): 420
  lines; bare-numeric `c.JSON(400/404/500, …)` in the same directory,
  non-test: 113 lines. The two scopes differ (test files included in
  the first count); both are stated here and neither is presented as
  a uniformity proof.

## Evidence table

| Rule | Evidence (file:line at pinned commit) | Tier / scope / confidence | Repo follows? + count |
|---|---|---|---|
| MA-1 | `internal/api/server.go:253-258` (register management routes only if a config/env/local secret exists); `internal/api/server_management.go:213-228` (availability middleware: 404 when disabled) and `:28-29` (group + availability + auth); `internal/api/server_management_v8.go:17-20` (v8 group); `internal/api/server_routes.go:66-67` (data-plane group uses a different auth middleware) and `:54,57` (unauthenticated health + management page) | T2 / CLASS / High | Enforced. Counterexamples: callbacks registered outside the group (still behind availability middleware); health + management page unauthenticated — both listed explicitly in the skill. |
| MA-2 | `internal/api/handlers/management/handler.go:321-354` (middleware: bearer or dedicated header), `:359-361` (5 failures / 30 min constants), `:398-399` (remote requires allow flag), `:402-416` (count + ban), `:427-453` (missing/invalid 401, no key configured 403), `:331-332` (loopback = 127.0.0.1 / ::1 only), `:340-342` (non-Bearer value accepted verbatim), `:390` (ban response leaks remaining time), `:357-358` (shared check reused by non-HTTP callers) | T2 / CLASS / High for the mechanism; Medium for the exact thresholds (hardcoded constants, not config) | Enforced in the one shared check. Limits recorded in the skill: verbatim non-Bearer acceptance, ban-time leak, hardcoded thresholds. |
| MA-3 | `internal/api/handlers/management/config_v8.go:20-38` (ETag / If-Match / 412), `:74-75` (no-store + ETag), `:216-221` (strong ETag from source hash), `:221-243` (If-Match comparison); `internal/api/handlers/management/handler.go:350` (abort with `{"error": …}`); counterexample `internal/api/handlers/management/auth_files_crud.go:44` (free-form error string with `%v`) | T4 / CLASS / Medium | PARTIAL: the `{"error": code}` form dominates (420 lines, scope above) but 113 bare-numeric responses and at least one free-form string break uniformity. ETag/If-Match is config-document-only. |
| MA-4 | `sdk/access/registry.go:11-14` (provider interface), `:30-43` (registration, nil/empty rejected); `sdk/access/manager.go:44-88` (chain loop: not-handled continues, missing/invalid remembered, invalid wins, final fallback no-credentials); `internal/api/server_middleware.go:481-485` (zero providers allows all requests, legacy behaviour) | T2 / CLASS / High | Enforced for the chain. The fail-open default itself is the counterexample the skill calls out: zero providers returns unauthenticated. Per-route variants duplicate the shape rather than sharing one function. |

## REPO-ONLY dropped (not generalized)

- The frozen legacy management surface (v0, deprecated per guidance)
  — kept only as the "frozen legacy version" example; not a pattern
  to copy.
- Plugin interceptors, control-plane heartbeat/cluster dispatch,
  protocol multiplexer, per-provider quota parsing — separate
  domains.
- TURN/ICE secret preservation on config round-trip — narrow
  config-domain behaviour; the general rule is MA-3.

## Unevidenced / dropped (no rule written)

- Rate limiting on management endpoints: only the per-IP failure ban
  (MA-2) found. Dropped.
- "All management errors share one shape" — CONTRADICTED in part
  (113 bare-numeric + free-form string). Dropped as stated; MA-3 is
  scoped as partial with the audit requirement.
- "Management auth is uniform across all entry points" — the shared
  check is reused by one non-HTTP caller; broader uniformity was not
  surveyed. Not claimed beyond the cited reuse.
- No T3 history rule is written; no history was mined.

## Observed gaps (NOT skill rules)

- G1. The fail-open zero-provider default is legacy behaviour with a
  code comment, not a deliberate policy statement. Projects copying
  the chain must decide explicitly.
- G2. The ban response reveals remaining ban time, and non-Bearer
  Authorization values are accepted verbatim. Both are recorded in
  the skill as review items, not as recommended behaviour.
- G3. The error shape is not uniform (see MA-3 counts). Uniformity
  requires an audit pass over the handler set.

## Fix round 1 (2026-11-02) — dry-run scope fixes, evidence re-checked

- MA-1: server-absent-when-secret-absent named as satisfying the
  hiding requirement. Verified against castctl 2962686
  (`internal/commands/webui.go:30-33`, `internal/webui/server.go:150-164`).
- MA-2: Bearer-only acceptance added as a compliant stricter
  variant of the two-form clause. The proposed loopback ban
  omission was REJECTED: the surveyed code counts failures and
  bans per IP for all clients including loopback
  (`AuthenticateManagementKey`, `handler.go:359-453`: the ban
  check and `fail()` run before the `localClient` branch; the
  local branch only adds an extra accepted credential). The ban
  clause therefore stays unconditional, including loopback-only
  surfaces. Verified against castctl (Bearer-only check at
  `internal/webui/server.go:311-333`; 0 ban/ratelimit hits in
  `internal/webui/`; loopback validation at
  `internal/profile/webui.go:173-207`) — castctl's ban absence
  remains a recorded gap under the unmodified clause, not a
  design break.
- MA-3: prior-contract scope added (existing shipped nested
  envelope + body-hash concurrency contract: record the
  divergence, do not retrofit). Verified against castctl
  (`internal/webui/server.go:536-548` nested envelope;
  body `sha256` + 409 at `internal/webui/handlers.go:1219-1246`;
  frontend pins at `webui/src/pages/ConfigPage.tsx:86,139,149`).
  The flat-shape/ETag evidence below still supports the rule
  for surfaces with no prior contract.

## Fix round 2 (2026-11-02) — verifier + red-team fixes, evidence re-checked

- F-V8: Priority misattribution removed — `management-center-
  webui` (read in full, 0 `ETag`/`If-Match` hits) owns no
  ETag/`If-Match` behaviour; MA-3's contract rests on
  surveyed-repo backend evidence alone.
- R-4: MA-2 verbatim acceptance and ban-time leak are now
  Check failures, not review items (`handler.go:340-342`,
  `:390` are the surveyed flaws).
- R-6: MA-4 zero-provider fail-open is no longer curable by
  comment: the branch (and the nil-manager pass-through at
  `server_middleware.go:504-511`) fails the Check; final
  status is 401 for both missing and invalid
  (`sdk/access/errors.go:70-76`).
- R-20: MA-1 not-start variant scoped to management-only
  servers; health/liveness callbacks stay ungated.
- R-21: MA-3 exemption split per half (envelope vs
  concurrency); "dominates" removed as a Check criterion —
  enumeration with disposition is the check.
