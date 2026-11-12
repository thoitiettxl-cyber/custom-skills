---
name: go-testing-release
description: "Observed conventions for Go tests and releases in a large repo with a build-only CI gate: co-located table tests, httptest fakes with cleanup helpers, deterministic clocks, build-tag variant pairs, ldflags version injection, tag-triggered hand-rolled releases, and generated release notes when no changelog file exists. Use when writing tests or release automation for a Go binary in the same shape. Do not use as a general testing or CI guide — see golang-testing, golang-continuous-integration, and golang-benchmark instead. Priority: golang-testing and golang-continuous-integration govern testing and CI generally; this skill records only where the surveyed repo differs from them or adds a narrower evidenced shape."
---

# Go testing and release: observed conventions, including the contradictions

Observed practice only, at the pinned commit in `references/PROVENANCE.md`. This repo's
CI gate builds only (no test, vet, format, lint, race, or coverage step in any
workflow); its large test corpus runs locally. Nothing here claims a CI-enforced gate.

## Rules

### TR-1. Co-located table tests with named subtests; cross-module tests untagged in one top-level directory

Tests live beside the code under test, as `_test.go` in the same package and directory,
using table-driven cases with a `name` field run as named subtests. Cross-module tests
are the exception: a small top-level `test/` package holds end-to-end scenarios as
ordinary tests, with no build-tag gating in that directory. Parallelism is selective, not the default.

Reason: co-location keeps the test beside the contract it pins; named subtests name the
failing case; one untagged cross-module directory keeps end-to-end scenarios runnable
under plain `go test`.

Check: test files beside sources (1173 `_test.go` files); tables with `name` fields and
`t.Run` calls (2357 hits); 0 files with an `integration` build tag in the top-level
`test/` directory; 10 files in the top-level `test/` directory. An
`integration`-tagged test elsewhere in the tree (external-service
cross-module test) is the WHEN-NOT case below, not a failure of
this rule.

When to apply: Go services whose cross-module tests need no external services or build-
tag gating. When NOT to apply: single-case tests; cases needing different setup/teardown
per case; cross-module tests needing external services (then a build tag or environment
gate is required).

Conflict note (unreconciled, scoped): `golang-testing` rule 2 says integration tests
MUST use `//go:build integration`. This repo does the opposite: 0 such tags, cross-
module tests under plain `go test ./...`. Scoped to repos that deliberately run cross-
module tests untagged; where the tag rule is the project standard, the existing skill
wins.

### TR-2. Fake the boundary with real httptest servers and cleanup-registering helpers; no mock or assertion framework

Fake upstream dependencies with real `httptest` servers, or small hand-written fakes
implementing a narrow interface, driven by per-test helper constructors that take
`*testing.T`, register cleanup with `t.Cleanup`, and use `t.TempDir()` for filesystem
state. No mock-generation framework and no assertion library are used; tests use the
plain `testing` package. Hand-written fakes are not always interface-shaped — several
are concrete doubles wired by field assignment — so the helper-constructor shape is
dominant, not exclusive.

Reason: a real local server exercises the real HTTP path; helpers that own teardown keep
tests from leaking servers and directories.

Check: `httptest` in 322 test files; 0 testify/gomock hits in the module file and the
tree; helpers taking `*testing.T` with `t.Helper()`; `t.Cleanup` and `t.TempDir()` at
helper boundaries, except setup owned by `TestMain` (no `*testing.T` there — explicit
teardown instead); fakes live in `_test.go` files only, or in a shared test-only
package the repo already uses (named as test-only, never imported by non-test code).

When to apply: Go services with HTTP/upstream boundaries in a repo that already uses the
zero-dependency test style. When NOT to apply: non-HTTP boundaries (a hand-written fake
for the narrow interface); failure modes a real server cannot express (a scripted fake
type); a repo that already uses testify — follow `golang-stretchr-testify` instead.

### TR-3. Make time deterministic with an injectable time source or synctest bubbles; treat wall-clock sleeps in timing tests as a smell

Make time deterministic with an injectable time source — a clock
field (`nowFunc func() time.Time`, defaulting to `time.Now`) on the
production type, or a `Clock` interface with a fake implementation —
or `testing/synctest` bubbles for timer/goroutine behaviour,
preferring `synctest.Wait()` over sleeps to drain background
goroutines. A clock field must guard the nil case: a nil clock falls
back to `time.Now()` (the surveyed guard) or the constructor
supplies the default — a zero-value type whose nil clock panics on
use fails this rule. A bubble that never calls `Wait()` is a smell, not a
fail, unless it asserts timer ordering or background-goroutine
completion without otherwise synchronizing it — "otherwise
synchronizing" means a channel receive, a `WaitGroup` wait, or
`synctest.Wait()`, and nothing else counts. This is a minority
pattern (20 `nowFunc` hits; 18 synctest files) against 97
`time.Sleep` hits in test files, and the repo's guidance banning
wall-clock sleeps in timing tests is unenforced. Present the ban as
guidance, never as practice.

Reason: controllable time makes expiry, TTL, and retry tests deterministic instead of
timer-granularity dependent.

Check: clock fields or `Clock` interfaces on time-dependent types with
`time.Now` fallback and a nil-clock guard (fallback or constructor
default); tests injecting a fixed clock or fake; `synctest.Test`
bubbles with `synctest.Wait()` where completion must be observed; new
timing tests contain no `time.Sleep` used to "wait for" a goroutine
where a bubble or channel expresses the wait; a bubble asserting
timer ordering without a channel receive, `WaitGroup` wait, or
`synctest.Wait()` fails.

When to apply: types whose behaviour depends on "now" (TTL, expiry,
retry loops, cache eviction). Rate limiting is covered only where
the limit logic is parameterized by time.
When NOT to apply: `synctest` for tests touching real networks,
real filesystems outside `t.TempDir()`, or `t.Parallel()` subtests sharing a bubble;
clock injection on every type — only time-dependent ones; behaviour
whose purpose is measuring time itself (load generators, benchmarks,
latency measurement) — wall-clock waits there are the measurement,
not a smell; do not judge a per-OS clock-function pair under this
rule — that is TR-4's subject.

### TR-4. Split build variants with identical symbol names across build-tag pairs

Split build-variant code with `//go:build` constraints that keep identical symbol names
across variants (a boolean constant under `race` and under `!race`; platform/cgo splits
the same way). Variants live beside the code they vary. Build tags here vary only
platform, cgo, and race detection — never environment selection or test-vs-prod
behaviour.

Reason: identical symbols keep callers tag-agnostic; co-location keeps the pair
reviewable together.

Check: 19 build-tagged files, forming identical-symbol pairs; no `integration`/`e2e`
tag; no environment-based variant; capability stub-vs-real pairs share
identical symbols across tag variants.

When to apply: code that must behave differently under `-race`, cgo, or per-OS;
capability stub-vs-real implementation pairs with identical symbols.
When NOT to apply: feature flags, environment selection, or test-vs-prod behaviour (use
config/flags); a one-branch runtime check when clearer. The
capability-stub exclusion here covers runtime selection only (a
runtime flag choosing stub vs real at run time). Build-time
capability tags — where the tag selects which implementation is
compiled in because the real one pulls in a build-constraining
dependency (CGO/native stack) that must be absent from some builds —
are this rule's subject, not its exception.

### TR-5. Embed version identity with dev defaults (or a documented pinned default), mirrored into one metadata package, injected by every release job [canonical — PS-3 in go-public-surface is a pointer to this rule]

Embed version identity with package-level variables defaulting to dev
values (`dev` / `none` / `unknown`), or to a documented pinned
default provided unstamped builds remain detectable via a separately
stamped field (for example empty commit/date variables). Mirror the
variables into one shared metadata package, copied once in `init`,
when the version is reported from outside the entrypoint package; a
single-entrypoint binary whose version lives only in the entrypoint
package needs no mirror. Inject real values at release-build time
with `-ldflags -X` in every release build job, including container
builds. Local builds always report the defaults — never a guessed
version. Never hardcode a user-facing version string in the
entrypoint, except the single documented pinned default above. The
pinned default is the single stated exception to "never hardcode"
in this skill: it must be documented at the declaration site, and
at least one consumer must distinguish stamped from unstamped
builds (reporting the stamped field alongside the version). No
compile-time check enforces the mirror copy: review must grep for a
second entrypoint without a copy. The surveyed `-X` target is the
entrypoint's variables, while the shared package holds a copy
synced in `init` — two sources that must stay in sync; adding a
second binary entrypoint requires repeating the copy, or the
metadata silently stays at dev defaults.

Reason: dev defaults keep local builds honest; every-job injection keeps release
binaries truthful; the mirror warning prevents silent second-source drift.

Check: dev-default variables, or a documented pinned default with a
separately stamped detectability field, in the entrypoint; the `init`
copy into the shared package wherever the version is reported from
outside the entrypoint package; identical `-X` flags in every release
job and the container build; a second entrypoint repeats the copy
(verified by grep, since no compile-time check enforces it); at
least one consumer distinguishes stamped from unstamped builds; no
hardcoded user-facing version string in the entrypoint except the
single documented pinned default.

When to apply: built binaries, CLIs, or servers with a user-facing
version output (`--version` flag, `version` subcommand, or version
endpoint). When NOT to apply: libraries (no `main` package; expose
version via the module or build-info API); binaries built by consumers
from source needing the version without ldflags; a version constant
in code plus injection — pick one source; version strings embedded
only in protocol metadata (for example a `User-Agent` constant) with
no user-facing version output — a constant is the correct mechanism
there; before the first breaking major version, do not add a `/vN`
module-path suffix (v0/v1 modules have none).

### TR-6. Tag-triggered hand-rolled releases: generated notes, per-platform matrix, final checksums in one workflow

Drive releases from git tags: pushing a tag creates or updates the release, generates
notes from the commit range since the previous tag merged with generated release notes,
builds a per-OS/arch asset matrix, uploads every asset, then regenerates and uploads a
checksums file over the final asset set. Keep the trigger, matrix, and checksum step in
one workflow file. Two caveats: the binary trigger matches any tag while the image
trigger matches version tags only — scope the trigger to the version-tag pattern, or
gate an unscoped trigger downstream with a version-format predicate that runs before
any build/upload step; do not copy the mismatch; and checksum refresh steps inside
build jobs tolerate failure, while the final publish step runs always and exits cleanly
with no archives — both surveyed shapes are recorded flaws, not patterns: a
final-checksums step that can exit cleanly with no archives fails this rule. Only a
success-only final-checksums step with a fail-closed archive-count check is compliant:
it runs only when the build/upload jobs succeeded, and fails the workflow when the
downloaded archive set is empty or smaller than the matrix. Artifact-storage exhaustion is a legitimate
reason for a hand-rolled `gh` pipeline instead of artifact storage; name it when
that tradeoff is made.

Reason: one workflow keeps trigger, matrix, and checksums consistent; generated notes
tie the release record to the tag range; final checksums cover the asset set as
published.

Check: one workflow file holding trigger, matrix, and checksums; notes generated from
the tag range; checksums regenerated over the final downloaded asset set by a
success-only step with a fail-closed archive-count check (an
always/best-effort final step fails); the trigger
pattern matches only version tags, or an unscoped trigger is gated by a version-format
predicate that runs before any build/upload step.

When to apply: multi-platform distributed binaries where releases are driven by a
GitHub-Actions workflow and a hand-rolled pipeline is deliberately chosen over a
release tool. When NOT to apply: libraries (a tag is the module version; no assets);
single-platform tools (matrix/checksum machinery is disproportionate); releases
needing human approval (this pipeline publishes on tag push with no approval gate);
releases driven by `Makefile`/scripts outside Actions — apply the
trigger/matrix/checksum properties pipeline-agnostically and say which pipeline owns
them; do not demand a workflow file.

Conflict note: `golang-continuous-integration` makes GoReleaser own release pipelines.
This repo uses hand-rolled `gh` plus a matrix. This rule does not present hand-rolled
scripts as preferred — state the tradeoff (full control, full maintenance) when
choosing. Where a project already uses GoReleaser, that skill governs.

### TR-7. When no changelog file exists, generated release notes are the changelog; keep commit subjects user-facing

If the repo has no changelog file, the release notes are the changelog: generate them at
tag time from commit subjects over the tag range, excluding purely internal prefixes
(the surveyed filter excludes `docs:` and `test:` subjects), and therefore keep commit
subjects user-facing and area-prefixed. Platform-generated notes (for example
`--generate-notes` or the platform's generate-notes API) are a compliant alternative
to workflow-assembled notes; the prefix filter is required only when notes are
assembled from raw commit subjects. Nothing in CI enforces the subject convention —
subjects are conventional by habit, and a non-conforming subject lands in the notes
verbatim. If a `CHANGELOG.md` exists, this rule does not apply.

Reason: with no changelog file, the tag-time notes are the only user-facing change
record; prefix filtering keeps internal churn out of it.

Check: no `CHANGELOG.md` in the repo; the release workflow generates notes from the tag
range by one of the two mechanisms — platform-generated notes, or workflow-assembled
notes with the prefix filter when raw subjects are used; subjects in the range are
area-prefixed; a curation step for sensitive subjects exists (hand review before
publish, or an exclusion list) — history with sensitive subjects and no curation
fails this rule.

When to apply: binary repos without a changelog file whose releases are published from
tags (for example GitHub Releases). When NOT to apply: a maintained
`CHANGELOG.md` exists (then `update-changelog` owns the record); history containing
internal or security-sensitive subjects (curate notes by hand); libraries; repos with
no tag-published release process — this rule does not apply there; do not invent one.

## Priority vs existing skills

- `golang-testing`: test mechanics (tables, tags, HTTP testing, synctest, fuzzing,
  goleak, coverage). This skill adds only the measured evidence and three contradictions
  (integration tag, no goleak, no coverage bar). `golang-stretchr-testify`: assert/mock
  APIs; when testify is present it governs over this zero-testify counterpart. `tdd`:
  the red-green loop (unaffected). `golang-benchmark`: measurement methodology (the
  surveyed repo adds nothing beyond co-located benchmarks). - `golang-continuous-
  integration`: `-race`/lint in CI, GoReleaser, coverage, dependency bots. This skill
  records the surveyed repo as the counterexample on each. Where that skill prescribes a
  gate, it governs new projects; this skill does not weaken it. - `golang-dependency-
  management`: versioning, MVS, major-version suffix, govulncheck (this skill adds only
  the ldflags mirror warning and the generated-notes precondition). Version ownership,
  in one sentence: TR-5 owns injection mechanics (ldflags targets, mirror, every-job
  injection), `golang-cli` owns the flag/output shape (`--version`), and
  `golang-dependency-management` owns the `/vN` module path. `golang-cli`:
  version embedding (this skill adds only the every-job injection check). `golang-
  documentation` / `update-changelog`: changelog format/content; TR-7 applies only when
  no changelog file exists. `golang-lint`: lint config; the surveyed repo has none, so
  do not cite it as lint practice.
