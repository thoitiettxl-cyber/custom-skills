# Provenance — go-credential-stores

- Source repo: https://github.com/router-for-me/CLIProxyAPI
- Tag: v8.0.51. Pinned commit: `7cad1cb7df48c6c5ffb7ff0b34ef8198806115bc`.
- Survey date: 2026-11-02. Checkout (read-only, not modified, no code run):
  `~/.cache/checkouts/github.com/router-for-me/CLIProxyAPI`. HEAD verified
  equal to the pinned commit.
- License: MIT (license file head read; paraphrase only). No repo text
  copied at length; no secret values recorded anywhere (mechanisms only).
- Sources by tier: T1 explicit guidance (`AGENTS.md` — no credential-store
  rule stated there); T2 machine-enforced (type-level store interface;
  bcrypt hashing on load); T3 history — NOT used; T4 inferred pattern,
  counts re-run by the writer (scopes stated). Researcher tables were
  leads only; every line below was re-verified by grep/read.
- Counts re-run by the writer: `MkdirAll … 0700` non-test hits under
  `sdk/` + `internal/`: 38; `SaveTokenToFile` implementations: 8 (7 real
  + 1 empty no-op), of which 4 use plain `os.Create` (4 files listed
  below) and 3 replace atomically; refresh-lead registrations: 9
  (2 returning nil, per the cited files).

## Evidence table

| Rule | Evidence (file:line at pinned commit) | Tier / scope / confidence | Repo follows? + count |
|---|---|---|---|
| CS-1 | `sdk/cliproxy/auth/store.go:6-19` (interface + contract comments: no synchronous manager mutation, no re-entrant load during save, metadata merge on non-fatal save errors); `sdk/auth/manager.go:52-69` (login, then persist; nil store returns record unpersisted); `:37-45` (register keyed by provider string, duplicate silently replaces) | T2 / CLASS / High for the interface shape; Medium for the no-reentrancy contract (comment-only) | Enforced by type: file store plus database/object/git backends implement the same shape. No second persistence interface found in the same package. |
| CS-2 | `sdk/auth/filestore.go:104` (`MkdirAll` `0o700`), `:140,152` (`OpenFile`/`WriteFile` `0o600`); `internal/auth/codex/token.go:77` (`Chmod(0o600)` on temp file); `internal/config/config_load.go:55` (`WriteFile` `0600`); plain-create writers: `internal/auth/claude/token.go:89`, `internal/auth/kimi/token.go:117`, `internal/auth/xai/token.go:52`, `internal/auth/vertex/vertex_credentials.go:69` | T4 / UNIVERSAL / Medium | PARTIAL / contradicted in part: the store writer sets modes; 4 of 7 real writers rely on the umask. The rule is scoped to the subset that sets modes, with the audit requirement for the rest. Mode-on-create applies only at creation; an existing group-readable file keeps its mode. |
| CS-3 | `internal/auth/codex/token.go:62-98` (temp file in same dir, `Chmod(0o600)`, rename, deferred temp removal) and `:45` (inter-process lock wrapper); `internal/auth/meta/meta.go:198-211` (temp + rename, no explicit chmod — relies on temp default); `internal/pluginhost/auth_provider.go:1193` (shared atomic-write helper: temp + rename); `internal/auth/codex/filelock_unix.go:13-22` (flock on a `0600` lock file) | T4 / CLASS / Medium | Aspirational-only as a repo-wide rule: 3 of 7 real writers replace atomically; 4 write directly. No shared helper is used by all writers. The rule is scoped to the checked writers. |
| CS-4 | `sdk/auth/interfaces.go:12,25-29` (refresh sentinel, `Authenticator` with `RefreshLead()`); `sdk/auth/refresh_registry.go:9-18` (9 registrations); lead examples `sdk/auth/claude.go:34-35` (4h) and `sdk/auth/antigravity.go:30-31` (30m); nil-lead opt-outs `sdk/auth/devin.go:39-41`, `sdk/auth/meta.go:32-33`; `sdk/cliproxy/auth/conductor_refresh.go:1120-1141` (401 refresh before fallback) and `:1295-1314` (terminal grant to requires-sign-in); substring classification `:1071-1084` | T2 / CLASS / High for lead-time + 401-refresh; Medium for terminal-classification completeness | Enforced, with legitimate nil-lead opt-outs. Terminal detection partly matches message substrings — recorded as a fragility, not hidden. |
| CS-5 | `internal/config/config_load.go:72-94` (hash-if-plaintext, rewrite file, reject residual plaintext copies); `internal/config/config_validation.go:71-74` (bcrypt, default cost); `internal/api/handlers/management/handler.go:450-453` (hash comparator) and `:438,445` (constant-time compare for local/env secrets) | T2 / CLASS / High | Enforced after first load. Limits: plaintext accepted at the input boundary; env/local secrets compared as stored plaintext in constant time; three accepted sources, so rotation must cover all three. |

## REPO-ONLY dropped (not generalized)

- Per-upstream login flows (device flow, browser callback servers,
  token endpoints, field names) — provider-specific; the generalizable
  parts are CS-1/CS-4/CS-5.
- Cooldown/quota scheduler semantics — tied to the proxy's
  load-balancing model.
- Protocol multiplexer, control-plane integration, plugin mechanics —
  separate domains.

## Unevidenced / dropped (no rule written)

- Encryption at rest for credential files: no evidence found —
  credential files are plaintext JSON protected only by modes. Do not
  claim encryption. No rule written.
- Rotation of data-plane keys: no rotation mechanism found; only
  credential refresh (CS-4) and operator-secret hashing (CS-5).
  Dropped.
- Rate limiting on management endpoints: only the per-IP failure ban
  (in `go-management-api`) found; no token-bucket limiter evidenced.
  Dropped.
- Secret redaction completeness: masking is key-name/regex based; no
  allowlist audit was run. "No secret can leak" is NOT claimed.
- "0600/atomic as repo-wide practice" — CONTRADICTED by the 4
  direct writers. Dropped as a repo-wide claim; CS-2/CS-3 are scoped
  to the subsets that follow them, with counts.

## Observed gaps (NOT skill rules)

- G1. Four token-file writers rely on the umask (files in CS-2).
  A project adopting CS-2 must audit all writers, not just the
  store's own writer.
- G2. No shared atomic-write helper is used by all writers; the
  atomic pattern exists in 3 writers in two different helper forms.
- G3. The management secret has three accepted sources (config hash,
  env, local password). Rotation covering only the config hash leaves
  the other two live.

## Fix round 1 (2026-11-02) — dry-run scope fixes, evidence re-checked

- CS-1: WHEN-NOT sharpened (one credential file, one writer
  function, no second backend planned: no store interface
  required; document the single-writer invariant). Verified
  against castctl 2962686 (`internal/profile/cookies.go:49`
  `WriteCookiesFile`, call sites in `authimport.go:89`,
  `webui.go:381,423`, `keeper/tick.go:465`; no second backend).
- CS-4: session keepers that re-authenticate (browser re-export)
  rather than refresh tokens named out of scope. Verified
  against castctl (`internal/keeper/export_cdp.go`; 401/403
  mapping to `*AuthError`, never retried,
  `internal/conn/errors.go:16`). Refresh evidence below
  unchanged.
- CS-5: single-source scoping added (rotation trivially
  satisfied by listing the one source; residual-copy rejection
  only where the format admits a second copy). Verified against
  castctl (`internal/profile/webui_secret.go:13-56`, one token
  source, 0 fallbacks). The three-source evidence below still
  supports the multi-source rule.

## Fix round 2 (2026-11-02) — red-team fixes, evidence re-checked

- R-8: CS-5 hash named (bcrypt, `config_validation.go:71-74`,
  `bcrypt.DefaultCost`; Argon2id per `golang-security`, read in
  full); rewrite required atomic via CS-3 (surveyed direct
  `WriteFile` at `config_yaml.go:138` is the counterexample);
  fallback scoped to never-persisted runtime values.
- R-15: CS-1 merge/replace discipline quoted from the store
  contract comment (`store.go:9-15`); reentrancy stated as
  comment-only, review-read; unpersisted record distinguished
  by the empty persisted-path return (`manager.go:67-69` vs
  `:159`).
- R-16: CS-3 lock semantics named `flock(2)` from
  `filelock_unix.go:13-22` (descriptor-held, released on
  process death); existence locks fail the rule.
- R-17: CS-4 lead typed `*time.Duration`
  (`interfaces.go:28`) — nil vs zero distinct; status/code
  checks precede substring fallback (`conductor_refresh.go:
  1071-1077`).
- R-33: CS-2 enumeration method stated (grep write call sites
  across the module, classify every hit).
