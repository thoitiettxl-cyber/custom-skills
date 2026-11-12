---
name: go-public-surface
description: "Observed conventions for a Go module with an embeddable core: thin entrypoints, an internal implementation, one public surface, and facade re-exports. Use when a Go project has both a binary and code other modules embed, or when reviewing whether a public package really stands alone. Do not use for a single-purpose binary with no embeddable core, for a pure library with no binary, or for general package layout and naming — see golang-project-layout and golang-naming instead. Version identity is owned by go-testing-release (TR-5); this skill states no version rule of its own. Priority: this skill narrows golang-project-layout for the embeddable-core case only; layout, naming, and module-version rules there still govern."
---

# Go public surface: observed conventions for an embeddable core

Observed practice only, at the pinned commit in `references/PROVENANCE.md`.
"Public surface" here means the packages outside the project that embedders
import. Nothing in this skill claims the surveyed public surface is
self-contained: it is not (see rule PS-2 and the gap note in PROVENANCE.md).

## Rules

### PS-1. Use at most two code surfaces plus thin entrypoints

Keep every binary entrypoint a thin `main` package: flag parsing,
dependency wiring, and one call into the service — no business
logic, no retries, no config parsing beyond flags. Put the
implementation under
`internal/`. Put the embeddable surface under one top-level directory.
Do not add a third catch-all surface alongside them: a catch-all
surface is a second public directory holding unrelated public
packages with no single concern. A single-concern public directory,
and a single-purpose asset/embed package, are not catch-alls.

Reason: one public directory makes the embeddable contract findable; a
second public directory splits it without a boundary between the two.

Check: `find cmd internal <public-dir> -name '*.go' | wc -l` per directory;
`ls` shows exactly one public directory besides `cmd/` and
`internal/`, holding one concern; the `main` package contains only
wiring (flags, composition, one service call). The surveyed repo has
`cmd/` (9 Go files), `internal/` (1478 Go files), and one public directory
(457 Go files), and no `pkg/` directory.

When to apply: a project with a binary plus an embeddable core.
An embeddable core means a top-level package imported by at least one
module outside this repo, or documented in the repo as a public API
for embedders. Mere exportability is not enough: an exported package
imported only by this module's own binaries is not an embeddable core
for this rule.
When NOT to apply: a single-purpose binary with no embeddable core (then
`cmd/` + `internal/` alone is enough); a pure library (no `cmd/` needed);
a project that already publishes its public API from a different single
directory — do not rename it to match this skill; single-purpose
asset/embed packages (one file, imported only to expose embedded bytes,
no API of their own) — they are not surfaces for this rule.

### PS-2. Re-export internal types only through facade packages, and say so

When a public package exposes a type owned by `internal/`, expose it
through a facade: a type alias plus delegating functions in one facade
package per concern, in the public directory. Use an alias only when
the type's data lives in `internal/` and callers must pass the same
value identity across the boundary; when the public package can define
the type without depending on `internal/` state, define a real public
type instead. Never tell consumers to
import `internal/` directly. State in the facade package's doc comment
that it re-exports internal types of the same module, so embedders know
the public surface depends on the module's internal packages.

Reason: an alias keeps one type identity, so callers pass the same value
across the boundary; hiding the dependence misleads embedders about what
they can build without the implementation.

Check: `grep -rn '= internal' <public-dir> --include='*.go'` lists the
aliases (88 alias declarations across 16 directories in the surveyed
repo, 228 import lines of the module's `internal/` packages from
non-test files under the public directory, 60 of them `type X = internal*`
declarations); the alias counts are evidence that the pattern is
present, never a target — adding aliases to raise a count fails this
rule; each facade package doc comment names the re-export.
Also check the reverse direction: 194 non-test files under `internal/`
import the public surface, so the boundary is conventional, not enforced.

When to apply: a single-module project whose public packages must expose
internal types and accepts that dependence by convention.
When NOT to apply: when external consumers must build without the
implementation — then split into two modules instead of aliasing; when a
real public type can be defined in the public package — prefer it over
an alias (aliases are for compatibility, not a design goal).

### PS-3. Version identity is owned by TR-5 (reference — no separate prescription here)

Do not write a second version-injection rule in this skill. Version
identity — dev defaults, the metadata-package copy, and ldflags
injection in every release job — is stated once, as TR-5 in
`go-testing-release`, with its scope (user-facing version output,
pinned-default variant, single-entrypoint mirror exemption). This
skill adds nothing to it. When injection is in place, the version
variables live only where TR-5 places them (entrypoint variables,
plus the shared-package copy synced in `init` where TR-5 requires a
mirror). This pointer states no copy-point claim of its own: TR-5's
two-source shape (entrypoint variables + shared-package copy) is
the whole statement.

Check: no version prescription in this skill beyond this pointer;
version variables live only where TR-5 places them.

When to apply: exactly TR-5's.
When NOT to apply: exactly TR-5's. A version string
embedded only in protocol metadata (for example a `User-Agent`
constant) with no user-facing version output is not governed by
TR-5 either; a constant is the correct mechanism there.

## Priority vs existing skills

- `golang-project-layout` owns `cmd/`/`internal/`/`pkg/` conventions and
  module naming. This skill adds only the embeddable-core surface and
  the facade form; do not restate its layout rules from here.
- `golang-cli` owns version/build-info embedding and exit codes.
  Version injection itself is owned by TR-5 (`go-testing-release`);
  this skill adds nothing to it beyond the PS-3 pointer.
- `golang-dependency-management` owns module versioning and the
  major-version suffix. This skill does not re-own it.
- `golang-structs-interfaces` owns interface and type boundaries. The
  facade-alias warning here is the public-surface instance of that
  boundary question, not a replacement for it.

## What this skill does not claim

- It does not claim the surveyed public surface is self-contained or
  that consumers never import `internal/` paths. The evidence shows the
  opposite; see PROVENANCE.md, Observed gaps.
- It does not claim guidance-file layout maps or doc code samples stay
  current. Both were stale at the pinned commit; see PROVENANCE.md.
