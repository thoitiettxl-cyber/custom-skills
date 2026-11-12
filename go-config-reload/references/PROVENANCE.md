# Provenance — go-config-reload

- Source repo: https://github.com/router-for-me/CLIProxyAPI
- Tag: v8.0.51. Pinned commit: `7cad1cb7df48c6c5ffb7ff0b34ef8198806115bc`.
- Survey date: 2026-11-02. Checkout (read-only, not modified, no code run):
  `~/.cache/checkouts/github.com/router-for-me/CLIProxyAPI`. HEAD verified
  equal to the pinned commit.
- License: MIT (license file head read; paraphrase only). No repo text
  copied at length in the skill.
- Sources by tier: T1 explicit guidance (`AGENTS.md` config section);
  T2 machine-enforced (fsnotify dependency in `go.mod`; watcher package);
  T3 history — NOT used; T4 inferred pattern, counts re-run by the
  writer (scopes stated). Researcher tables were leads only; every line
  below was re-verified by grep/read.
- Counts re-run by the writer: sanitizer methods on the config type:
  14 (`grep 'func (.*Config.*) Sanitize'`, non-test, `internal/config/`);
  `KnownFields` hits repo-wide: 2 lines, 1 non-test site + 1 test-file
  comment; environment lookups in `internal/config/` non-test: 0;
  config-library hits in `go.mod`: 0; `CloneForRuntime` occurrences
  repo-wide non-test: 12 lines = 1 definition + 11 call sites
  (researcher said 12 call sites; the writer's count is 11 + definition
  and is the one asserted); "requires a restart" markers in
  config/service/API code: 1.

## Evidence table

| Rule | Evidence (file:line at pinned commit) | Tier / scope / confidence | Repo follows? + count |
|---|---|---|---|
| CR-1 | `internal/config/config_load.go:157-359` (`LoadConfigOptional`: defaults before unmarshal ~:195-232, `yaml.Unmarshal` at :212, validation, 14 sanitizers at :293-333, normalize + rewrite, source hash at :355); `internal/config/config_normalization.go:50-469` (sanitizers); `internal/config/config_v8.go:972` (sole non-test strict-fields site, legacy path); `internal/config/config_load.go:37-66` (load rewrites: secret hashing + legacy cleanup, failure leaves file untouched) | T4 / CLASS (single-file loader) / Medium (single loader site; defaults mechanism is 1 site + helpers, not a >=5 repeated pattern) | Enforced in the one loader. Loading is NOT read-only: it rewrites the file for secret hashing + legacy cleanup (0600 write). Unknown keys are ignored by the main path; strictness exists only in the legacy path. |
| CR-2 | `internal/watcher/watcher.go:116-120` (debounce constants: 50 ms replace-check, 150 ms config reload, 1 s auth-remove/server-update); `internal/watcher/events.go:29-44` (watch config file + auth dir, event loop) and `:103,112` (blocking sleeps in the handler); `internal/watcher/config_reload.go:31-49` (debounce + serialized apply), `:53-89` (empty ignore, hash gate, parsed hash recorded), `:95-103` (`reloadConfig()` returns `false` on load error without swapping) and `:115-120` (swap under lock, success path only) | T2 + T4 / CLASS / High | Enforced, with the sleep counterexample in the event handler recorded in the skill. |
| CR-3 | `cmd/server/main.go:155` (`--config` flag, default empty); `:256` (`.env` load from working directory, missing tolerated); `:271-335` (environment lookups for store DSNs / home JWT only, in main); `:439-597` (precedence chain: store paths, then flag, then working-directory default); 0 env lookups in loader package; 0 config-library hits in `go.mod` | T4 / CLASS / Medium (precedence chain is entrypoint-specific) | Enforced. The chain order is store > flag — surprising; the skill requires documenting non-obvious orders and does not present "flag always wins" as universal. |
| CR-4 | `sdk/cliproxy/service_config.go:134-171` (commit: validate, clone, swap under write lock, sequence++), `:171-179` (sequence-currency check), `:181-251` (apply under second lock, stale commits dropped, cancellation checks); `sdk/cliproxy/service.go:33-39` (three locks); `internal/api/server_reload.go:42-58` (client-context update clones again, diffs YAML snapshot) | T4 / CLASS / Medium (single implementation of the two-phase pattern) | Enforced for the commit/apply split. Restart-only marking is 1 field only (see gaps) — no marking convention is claimed. |
| CR-5 | `internal/config/clone.go:12-21` (reflect deep-copy) and `:43-52` (Struct case: an un-settable field returns the whole value shared, `if !dst.CanSet() { return v }` at :47-49); 11 call sites + definition (see counts); `sdk/cliproxy/service_config.go:16-24` (`RWMutex` snapshot accessor); `internal/watcher/watcher.go:37-44` (watcher mutexes) | T4 / UNIVERSAL / High | Enforced (clone on handoff). Counterexample: reflect clone shares unexported fields; the skill requires a snapshot-mutation test over exported fields and a separate documented-sharing test for unexported state. |

## REPO-ONLY dropped (not generalized)

- Per-section config names and per-upstream sanitizer contents —
  domain sections; the loader ordering is kept, the section names
  are not.
- Control-plane config forcing and remote catalog sources — separate
  deployment domain; sequence-gating is kept in CR-4.
- The watcher/auth-delta queue contract beyond the reload trigger —
  credential-store domain, covered in `go-credential-stores`.

## Unevidenced / dropped (no rule written)

- "Strict config validation rejects unknown fields" — CONTRADICTED
  (plain unmarshal in the main path; 1 legacy strict site). Dropped
  as stated; CR-1 states the observed policy honestly.
- "Hot reload applies ALL config fields except documented restart-only
  ones" — CONTRADICTED (1 restart-only marker; listener built once
  in `internal/api/server.go:267-271`). Dropped; CR-2/CR-4 scope
  reload to incrementally applicable fields.
- "Config reload is atomic w.r.t. in-flight requests" — no evidence of
  request draining or in-flight pinning to a config generation.
  Dropped.
- "Load never mutates the file" — CONTRADICTED (secret hashing +
  legacy cleanup rewrite). Dropped; CR-1 records the rewrite.

## Observed gaps (NOT skill rules)

- G1. Restart-only marking: only `TrustedProxies`
  (`internal/config/config.go:30-32`) carries a restart marker.
  Bind host/port and TLS have no reload/restart annotation, and the
  listener is built once. No annotation convention is presented as
  repo practice.
- G2. Load-time file rewrite: loading hashes a plaintext secret and
  drops conflicting legacy fields. Any project copying the loader
  must decide explicitly whether load may mutate the file.
- G3. Sleep in the event handler (`events.go:103,112`) contradicts
  the debounced-async pattern elsewhere in the watcher. Recorded as
  a counterexample, not a pattern.
- G4. Single-source Go pinning is not followed (see
  `go-public-surface` provenance G4). No pinning rule is written.

## Fix round 1 (2026-11-02) — dry-run scope fixes, evidence re-checked

- CR-1: strict-reject variant added (documented strict policy:
  sanitizer-drop does not apply; whole load fails). Verified
  against castctl 2962686 (`internal/profile/config.go:222-228`
  unknown-key rejection; `docs/config.md` strictness). The
  defaults/hash evidence below still supports the rule; the
  strict variant exempts only the sanitizer-drop clause.
- CR-3: Check narrowed from package level to the parse/load
  function and its callees, excluding caller-side resolution.
  The 0-env-lookup evidence below (package-wide 0) still
  supports the narrower check. Verified against castctl
  (`internal/profile/configlocation.go:88-167` resolution vs
  `config.go:213` parse function).
- CR-4: cross-reference to CR-5 added for the clone discipline
  (one clone function, two stages). No prescription changed.
- CR-5: "reload" defined as replacing a stored in-process
  snapshot; re-parse-per-request / explicit re-read with no
  stored snapshot excluded. Verified against castctl
  (`internal/webui/store.go:71-84` re-parse per request;
  `internal/conn/conn.go:175-181` explicit `Reload`).

## Fix round 2 (2026-11-02) — verifier + red-team fixes, evidence re-checked

- F-V2: CR-5 un-settable citation corrected to the Struct case
  `clone.go:43-52` (`:47-49`). F-V3: CR-2 keep-old citation
  corrected to `reloadConfig()` `:95-103` + success-only swap
  `:115-120`.
- R-5: CR-1 drop-silence recorded (no log/metric/record names a
  dropped entry; the one `Warnf` in the sanitizer file is an
  unrelated fallback). R-18: hash-gate recovery is next-event
  retry only (last-applied hash updated on success at
  `config_reload.go:80-92`); mutex+hash ordering and empty-read
  scoping added. R-19: clone-test split — exported-field test
  evidenced by `internal/config/clone_test.go:65-102` (mutate
  original, clone unaffected); unexported sharing is a separate
  documented test. R-34: CR-3 check narrowed to the function
  itself + named helpers (0 env lookups in `internal/config/`
  non-test, re-verified).
