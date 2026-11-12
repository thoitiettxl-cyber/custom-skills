# Provenance — go-testing-release

- Source repo: https://github.com/router-for-me/CLIProxyAPI
- Tag: v8.0.51. Pinned commit: `7cad1cb7df48c6c5ffb7ff0b34ef8198806115bc`.
- Survey date: 2026-11-02. Checkout (read-only, not modified, no code run):
  `~/.cache/checkouts/github.com/router-for-me/CLIProxyAPI`. HEAD verified
  equal to the pinned commit.
- License: MIT (license file head read; paraphrase only). No repo text
  copied at length in the skill.
- Sources by tier: T1 explicit guidance (`AGENTS.md:9-15` gate commands,
  `:54-61` conventions); T2 machine-enforced (workflows — build-only
  gate, release workflow, Dockerfile); T3 history — NOT used for any
  rule (commit counts and recent-history observations in the research
  were not relied on; TR-7 rests on the workflow + the absence of a
  changelog file, not on history); T4 inferred pattern, counts re-run
  by the writer (scopes stated). Researcher tables were leads only;
  every line below was re-verified by grep/read.
- Counts re-run by the writer (`grep -rn`, `*.go`, whole repo unless
  stated): `_test.go` files: 1173; `t.Run(` hits: 2357; files with
  `func Test`: 1149; `t.Parallel()` hits: 656 (researcher said 662;
  the writer's count is asserted); `httptest` test files: 322;
  `t.Helper()`: 734; `t.Cleanup`: 1554 (researcher said 1574; the
  writer's count is asserted); `t.TempDir()`: 656; `nowFunc` hits:
  20; `time.Sleep` in test files: 97; files importing
  `testing/synctest`: 18 (researcher said 5; the writer's broader
  scope is asserted); files with `//go:build`: 19, breakdown:
  5 windows, 4 `cgo && (linux||darwin||freebsd)`, 2
  `windows || (cgo && …)`, 2 race, 2 !race, 1 cgo, 1 !windows,
  1 `!cgo && !windows`, 1 `!cgo`; `go:build integration`: 0;
  testify in `go.mod`: 0; `errgroup`: 0; workflow hits for
  `go test` / `go vet` / `golangci` / `-race`: 0.

## Evidence table

| Rule | Evidence (file:line at pinned commit) | Tier / scope / confidence | Repo follows? + count |
|---|---|---|---|
| TR-1 | `internal/cache/signature_cache_test.go:322-338` (table with `name`, `t.Run`, plain `testing`, no assertion library); `test/` listing: 10 `*_test.go` files; build-tag census above; counts above | T4 / UNIVERSAL for co-location + tables; CLASS for the untagged top-level shape / High | Enforced by overwhelming repetition. Parallelism selective (656 vs 2357). Contradicts the `golang-testing` integration-tag rule — recorded in the skill. |
| TR-2 | `internal/runtime/executor/codex_executor_auth_test.go:44,59` (mock-server helper, `httptest` servers); `internal/api/server_test.go:610-625` (`newTestServer*` helpers with `t.Helper`, `t.TempDir`); `internal/api/handlers/management/test_main_test.go:10-13` (`TestMain` sets test mode; 1 of 2 `TestMain` functions repo-wide per research, not re-counted); counts above; `testdata/` exists in 5 directories but only 11 test files reference it (researcher count, not re-run — not asserted as a rule count) | T4 / CLASS / High | Enforced by repetition. Hand-written fakes are not always interface-shaped (concrete doubles wired by field assignment exist); the skill states the dominant shape, not exclusivity. |
| TR-3 | `internal/api/handlers/management/plugin_store_release.go:37,40-43` (`nowFunc` field, `time.Now` fallback); `internal/pluginstore/github_rate_limit.go:51,64-65` (same shape); `internal/api/handlers/management/plugin_store_release_test.go:118` (fixed-time injection); `internal/api/handlers/management/auth_files_patch_fields_test.go:857` (`synctest.Test` + `synctest.Wait`); `AGENTS.md:61` (sleep guidance + controllable-clock preference) | T1 + T4 / CLASS / Medium | PARTIAL / aspirational for the ban; enforced at small scale for the two mechanisms (20 `nowFunc` hits, 18 synctest files vs 97 sleeps). The skill presents the minority pattern + guidance, never the ban as practice. |
| TR-4 | `internal/translator/codex/claude/race_enabled_test.go:1-5` and `race_disabled_test.go:1-5` (identical `raceDetectorEnabled` const, `true`/`false`); same pair under `sdk/api/handlers/openai/`; build-tag census above | T4 / CLASS / Medium | Enforced at small scale (19 files). No integration/env tags exist; the skill does not generalize tags into environment switching. |
| TR-5 | `cmd/server/main.go:47-49` (dev-default vars), `:56-58` (`init` copy into shared package), `:86,104` (printed via shared package); `internal/buildinfo/buildinfo.go:7-14` (shared vars, ldflags comment); `.github/workflows/release.yaml:177,306,430,618,627` (5 `-X` flag sites) + `Dockerfile:13-17` (ARG defaults + same `-X` flags) | T2 / CLASS / High | Enforced by CI. Two-source sync warning recorded (entrypoint vars + shared-package copy). |
| TR-6 | `.github/workflows/release.yaml:4-7` (tag trigger `'*'`), `:17-91` (prepare-release: previous-tag range, `git log` subjects filtered `docs:`/`test:`, generated notes, create/edit release), `:94-690` (build matrix jobs), `:691-717` (final checksums: `if: always()`, regenerate over downloaded assets, upload; exits 0 when no archives); `continue-on-error: true` at `:206,342,461,662` (per-job checksum-refresh steps, NOT the final publish job); `.github/workflows/docker-image.yml:5-6` (image trigger `v*` only) | T2 / CLASS / Medium | Enforced by CI for the binary release, with the trigger mismatch recorded. The always/best-effort final step is a RECORDED FLAW, not a compliant shape: only a success-only final step with a fail-closed archive-count check complies. No draft/prerelease distinction and no attestation step found. Hand-rolled, not GoReleaser — recorded as a tradeoff, not a preference. |
| TR-7 | `CHANGELOG.md`: ABSENT (verified by listing); `.github/workflows/release.yaml:60-75` (notes generated from tag-range subjects, prefix filter, merged with generated notes). No commit-history claim is relied on; the subject convention's lack of enforcement (no commitlint config found) is recorded in the skill. | T2 / CLASS / Medium | Enforced by CI as the only user-facing change record. The subject convention is unenforced habit, not a gate. |

## REPO-ONLY dropped (not generalized)

- Plugin `.so` loading, GLIBC ceiling check, no-plugin variants,
  FreeBSD no-plugin build — distribution specifics; the generalizable
  part is TR-6's matrix + checksums.
- Per-account probe workers, translator architecture rules, TUI,
  discovery, relay sessions — product features or other domains.
- `config-version` / module-path `/v8` as a standalone rule —
  owned by `golang-dependency-management`; not re-derived.
- Refresh-model-catalogs pre-build step in every build job —
  repo-specific generated-catalog step, not a general Go gate.

## Unevidenced / dropped (no rule written)

- Fuzzing as a general practice: only 2 `func Fuzz` found (both
  differential against a reference). Below the >=5 bar. Dropped.
- Benchmarks as a separate discipline: 90 `func Benchmark`
  (researcher count, not re-run), no benchmark step in CI. Owned by
  `golang-benchmark`. Dropped, no new rule.
- Goroutine-leak detection: no leak-detection usage (0 hits).
  Dropped; `golang-testing` owns it.
- Coverage enforcement: 0 coverage hits in workflows. Dropped; no
  coverage bar claimed.
- `go vet` / lint enforcement: 0 hits in CI; no lint config. The
  T1 `gofmt` requirement is unenforced (T2 wins). Not presented as
  repo practice.
- Race detector in CI: 0 `-race` hits in workflows, despite race
  build-tag pairs. Not claimed; `golang-continuous-integration`
  requires `-race` and this repo is the counterexample.
- Dependency-update automation: no bot config; updates appear as
  manual commits (history-only observation, not relied on). No
  "manual bumps" policy prescribed.
- Single-source Go pinning (V3 in the research): CONTRADICTED —
  `go.mod:3` (`1.26.10`), `release.yaml:14` hardcoded `GO_VERSION:
  '1.26.10'`, PR/Docker jobs derive from `go.mod`, `Dockerfile:1`
  pins `golang:1.26-bookworm` only, no `toolchain` directive (0
  hits). Dropped as a rule; recorded here as a gap only.
- Sleep ban as enforced practice: CONTRADICTED (97 sleeps in test
  files; no enforcement). Dropped; TR-3 states guidance + minority
  pattern.
- "Tests are CI-gated": CONTRADICTED — T1 lists `go test ./...`
  (`AGENTS.md:13`) but no workflow runs any test command (0 hits).
  T2 wins. Recorded here; no rule presents `go test` as a CI gate
  of this repo.
- "Formatting is CI-checked": CONTRADICTED — T1 requires `gofmt`,
  no format/lint check exists. Whether the tree is gofmt-clean was
  not measured (no formatter run). Not claimed.

## Observed gaps (NOT skill rules)

- G1. CI strictness is LOW (build-only gate) despite a large test
  corpus (1173 test files). Confidence in distilled rules is
  therefore capped: patterns are widely repeated (T4) but not
  machine-enforced (T2), except where a workflow enforces them.
- G2. Go version pinning is split across three mechanisms that
  happen to agree (see dropped V3 above). Silent future drift is
  the failure mode.
- G3. Release triggers disagree (`'*'` vs `v*`); a non-version tag
  produces binaries without images.
- G4. The final checksums step is best-effort (always runs, exits 0
  with no archives); per-job checksum refresh steps tolerate
  failure. Checksums are not a release gate here.

## Fix round 1 (2026-11-02) — dry-run scope fixes, evidence re-checked

- TR-3: injectable time source widened to a `nowFunc` field or a
  `Clock` interface + fake; measurement-of-time behaviour
  (load generators, benchmarks, latency measurement) excluded;
  per-OS clock-function pairs assigned to TR-4; a bubble that
  never calls `synctest.Wait()` is a smell, not a fail, unless
  it asserts timer ordering or background-goroutine completion.
  Verified against castctl 2962686 (`Clock` interfaces at
  `internal/keeper/clock.go:32`, `internal/gateway/clock.go:19`;
  7 synctest files, 0 `synctest.Wait()` hits; 0 `nowFunc` hits)
  and hey (`requester.go:208-216` QPS ticker,
  `requester_test.go:48-73` `TestQps` wall-clock measurement,
  `now_other.go:24`/`now_windows.go:24` per-OS pair). The
  `nowFunc`/synctest evidence below still supports the rule;
  `synctest.Wait()` is well evidenced in the surveyed repo (66
  hits in `_test.go` files), so it stays a strong preference,
  softened only from fail to smell. The per-OS pair is TR-4's
  subject, not TR-3's.
- TR-4: capability stub-vs-real tag pairs exempted from the
  feature-flag WHEN-NOT. Verified against castctl
  (`internal/keeper/export_cdp.go:56,69` vs
  `export_stub.go:19,26`, `with_chromedp`; capability tags in
  `cmd/castctl/main.go:13-16`). The race/cgo/platform pair
  evidence below still supports the scoped rule.
- TR-5: CANONICAL version-injection rule (PS-3 in
  `go-public-surface` is now a pointer to this rule; the
  duplication is resolved to this single rule). Trigger scoped
  to user-facing version output; protocol-only identifiers
  (e.g. a `User-Agent` constant) excluded; documented pinned
  default admitted when unstamped builds stay detectable via a
  separately stamped field; mirror required only when the
  version is reported from outside the entrypoint package.
  Verified against castctl (`internal/commands/commands.go:58-66`
  pinned `0.6.1` + empty `Commit`/`BuildDate`; `-X` in both
  release jobs, `release.yaml:306,459`; no metadata mirror, no
  second entrypoint) and hey (`hey.go:38` `heyUA` constant, no
  version flag/output; plain `go build` everywhere). The
  dev-default/`init`-copy/ldflags evidence below still supports
  the canonical rule; the pinned-default and mirror-exemption
  scopings are dry-run-derived, not surveyed-repo shapes.
- TR-6: success-only final checksums with a fail-closed
  archive-count check admitted as a compliant stricter variant;
  trigger scoped to version tags OR gated by a version-format
  predicate before any publish/upload step; Actions-workflow
  scope stated (Makefile/script releases apply the properties
  pipeline-agnostically); artifact-storage exhaustion named as
  a legitimate reason for hand-rolled `gh` pipelines. Verified
  against castctl (success-only predicate + exactly-4 check,
  `release.yaml:47,50-60,508-556`; `--generate-notes` at `:178`;
  quota-exhausted header `:30-34`) and hey (`Makefile:4-11`
  multi-platform `go build` + `gsutil` upload; CI-only
  `.github/workflows/go.yml`). The always/best-effort evidence
  below still supports the best-effort variant; the
  success-only variant is the stricter dry-run-derived shape.
  (Fix round 2 correction: the always/best-effort shape is a
  recorded flaw, not a compliant variant — only the
  success-only + fail-closed count check complies.)
- TR-7: platform-generated notes (`--generate-notes`) admitted
  as compliant; prefix filter required only for raw-subject
  assembly; scoped to repos with a tag-published release
  process. Verified against castctl (no `CHANGELOG.md`;
  `--generate-notes` at `release.yaml:178`; no prefix filter,
  no `.github/release.yml`) and hey (no `CHANGELOG.md`;
  `Makefile:4-11` upload-only, no notes step, no release
  workflow). The tag-range + prefix-filter evidence below
  still supports the workflow-assembled form.

## Fix round 2 (2026-11-02) — red-team fixes, evidence re-checked

- R-3: TR-1 Check scoped to the top-level `test/` directory;
  an `integration`-tagged external-service test elsewhere is
  the WHEN-NOT case, not a failure.
- R-10: TR-6 best-effort/always DROPPED as compliant — the
  surveyed final step (`release.yaml:691-717`, `if: always()`,
  exit 0 with no archives) is a recorded flaw; only
  success-only + fail-closed archive-count check complies;
  the version predicate must run before any build/upload step.
- R-12: TR-5 pinned default is the single stated exception to
  "never hardcode", documented at declaration, with a
  separately stamped field and at least one consumer
  distinguishing stamped from unstamped; no compile-time
  enforcement — review greps for a second entrypoint without
  a copy.
- R-27: TR-2 Check scoped to zero-dependency-style repos;
  shared test-only fake packages allowed; `TestMain` setup
  carve-out (no `*testing.T` there).
- R-28: TR-3 nil-clock guard required, citing the evidenced
  guard (`plugin_store_release.go:40-44`); "otherwise
  synchronizing" defined as channel receive / `WaitGroup`
  wait / `synctest.Wait()`. TR-4 capability exemption
  restated: runtime selection only; build-time capability
  tags are the rule's subject.
- R-29: TR-7 Check gates the mechanism (prefix filter or
  platform generation) and requires a sensitive-subject
  curation step.
- R-35: Priority gains the ONE version-ownership sentence
  (TR-5 injection mechanics; `golang-cli` flag/output
  shape; `golang-dependency-management` `/vN` module path).
