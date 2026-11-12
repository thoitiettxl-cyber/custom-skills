---
name: go-provider-registry
description: "Observed conventions for a keyed registry of upstream executors with separate credential selection, bounded failover, and a format-conversion registry. Use when a Go service dispatches work to several interchangeable upstream implementations behind one contract, with more than one credential per upstream. Do not use for one upstream, one credential, a single call style, or general interface and DI design — see golang-structs-interfaces, golang-dependency-injection, and codebase-design instead. Priority: golang-dependency-injection governs service wiring and forbids global registries; this skill's manager-owned registry and its narrow conversion-table exception are scoped inside that rule, never above it."
---

# Go provider registry: executors, selection, and conversion tables

Observed practice only, at the pinned commit in `references/PROVENANCE.md`.
"Provider" means one interchangeable upstream implementation, keyed by a
normalized string. "Credential" means one usable identity for a provider.
Rules state the surveyed repo's shape; where the repo's shape conflicts
with an existing skill, the rule says so and scopes itself.

## Rules

### PR-1. One executor interface, owned by the consumer-facing package

Define one interface per upstream family with: a normalized string key
method, unary execution, streaming execution, credential refresh, token
counting, and credential injection for raw requests. Compose it from
small single-capability interfaces (one per behaviour above) embedded
into the executor contract, per `golang-structs-interfaces`. Keep the
interface in the package that dispatches through it; put
implementations elsewhere. Extend the core contract only through small
optional interfaces probed by type assertion, one capability each. A
behaviour the executor does not have is omitted from its composed
contract — never implemented as a no-op stub (a no-op refresh
returning nil, or a counting stub returning 0, masks expiry and
corrupts quota accounting downstream).

Reason: one contract lets dispatch, selection, and failover stay uniform
across implementations; optional interfaces keep rare capabilities from
bloating the core contract.

Check: the interface has the six methods, composed from small
interfaces or, for the surveyed flat form, scoped to the dispatch
case with all six behaviours real (0 no-op refresh/counting stubs);
dispatch goes through the
manager's execute methods, never around the interface; optional
interfaces are probed by assertion at the call sites that need them
(7 assertion sites in the surveyed repo; 13 key-method implementations
and 17 constructors in the implementation directory).

When to apply: several interchangeable implementations plus third-party
extenders, with both unary and streaming call styles.
When NOT to apply: one implementation and no third-party extenders
(a concrete type is simpler); only one call style (use a smaller
interface plus an optional streaming capability interface); no
refresh endpoint or no token counting (omit that behaviour from
the composed contract; see above); do not put
implementation-specific fields on the shared interface — use per-call
options/metadata.

Conflict note: this is a 6-method interface. `golang-structs-interfaces`
says keep interfaces to 1-3 methods and compose larger ones. The
6-method shape is scoped to this case only — many implementations
behind one dispatch path — and does not override the small-interface
rule elsewhere. Do not cite this rule to justify a large interface in
general code.

### PR-2. Manager-owned keyed registry with last-wins replacement

Hold implementations in a keyed map owned by a manager type (not a
package-level variable). `Register` replaces by key; `Unregister`
removes by key; registration is explicit and idempotent. Replacing an
implementation closes the old one's sessions unless it declares
session-sharing with the replacement, or the replacement is the same
instance (re-registering the same instance closes nothing). The
close of replaced sessions happens only after the registry lock is
released. Rejected registrations (nil, or empty key) return without
an error in the surveyed code — callers must not rely on silence to
mean success; check registration took effect through the manager's
executor lookup, which reports whether a key is registered.

Reason: manager ownership keeps the registry testable and replaceable;
closing replaced sessions prevents work from continuing against a
discarded implementation.

Check: one map field on the manager; register/unregister are manager
methods; replacement closes sessions unless sharing is declared or
the instance is identical, and the close runs after unlock;
registration is verified via the executor lookup after the call;
`grep -rn 'RegisterExecutor('` shows the call sites are explicit wiring,
plugin-host, service, and example sites (17 non-test sites).

When to apply: a closed set of implementations wired at startup or on
reload, where at most one implementation serves a key.
When NOT to apply: two implementations must coexist under one key (use
key + variant/priority instead); sessions are owned outside the
implementation (closing is then the owner's job); service wiring in
general — `golang-dependency-injection` governs that, and its ban on
global registries and package-level service locators still applies.
This registry is manager-owned, never global; plugin hosts are out
of scope unless they expose executor-style `Register`/`Unregister` —
a host with `ApplyConfig` replace/close semantics is judged by the
host's own lifecycle rules, not this one.

### PR-3. Wire built-ins explicitly; reserve self-registration for open extension points

Wire built-in implementations explicitly in the composition root with a
per-credential switch: normalize the key, construct the implementation,
register it. Do not rely on `init()` self-registration for built-ins.
`init()` registration passes the decision test below, and only then:
every registered entry is a pure function value keyed by an explicit
constant, needing no configuration, endpoint, or credential; a
constructible registry exists alongside the package default; and
tests use the constructible registry, never the default. An entry
needing configuration fails the test and is wired explicitly
instead. Do not add a `default` branch that
silently accepts unknown keys in a fail-closed system; reject or skip
with a log instead. This rule governs service/executor wiring the
project owns. It does not govern CLI dispatch tables with a fixed
order list, or registries owned by a dependency (whose registration
mechanism the project inherits, not chooses).

Reason: an explicit switch makes the built-in set reviewable and makes
an unknown key visible; self-registration hides both.

Check: 0 `init()` functions in the implementation directory vs 26
across the conversion packages in the surveyed repo — the two
patterns split by the decision test in the body (pure constant-keyed
entries plus a constructible registry), not by a label. The surveyed
switch has a fail-open
`default` branch mapping any unknown key to a compatibility
implementation; flag that shape in review, do not copy it silently.

When to apply: a closed built-in set wired at startup; a conversion
matrix passing the PR-6 decision test is the contrasting case.
When NOT to apply: the implementation set is genuinely open-ended at
runtime (plugins loaded from disk — use the registry plus a plugin host
form instead); CLI dispatch tables with a fixed order list; registries
owned by a dependency.

### PR-4. Separate credential selection from execution

Define a `Selector` interface that picks one credential from candidates
already loaded. Choose the strategy from configuration when the
strategy is first selected from config, before the first pick;
implement stateful affinity as a decorator wrapping a stateless
selector. Affinity is keyed by session identity (the surveyed
decorator extracts a session id); keying affinity by provider alone
collapses per-credential affinity and fails this rule. The selector performs no I/O and no credential refresh. All
mutable selection state and its lock live inside the selector, never in
the caller; a stateless selector holds no lock.

Reason: selection is a pure choice over loaded candidates; mixing
refresh or I/O into it couples scheduling to transport and hides
failure modes.

Check: one `Pick` method taking candidates; config maps a strategy
string to a selector; the affinity type wraps a fallback selector and
is keyed by session identity; the stateful selectors hold a mutex and their own state maps.

When to apply: more than one credential per provider, with more than
one selection strategy.
When NOT to apply: exactly one strategy will ever exist (a single
`Pick` function is enough); the selector would need I/O to choose
(then load candidates first and keep the selector pure).

### PR-5. Isolate failures per credential within a bounded round

Dispatch tracks a tried-set per attempt so a failed credential is never
retried in the same round. Every outcome is reported to a single
result-recording method that drives cooldown/quota state. Retry rounds
and the per-round credential cap are bounded by configuration, with
negative values clamped to zero at the setter. Clamped zero has a
fixed meaning, stated wherever the setter is used: zero retry rounds
means no round beyond the first attempt; a zero per-round cap means
no cap. The surveyed setter clamps silently — a negative value
reaching it is a config error; surface it at validation, do not rely
on the clamp to hide a typo. Review must check every parallel loop
body: the surveyed dispatch duplicates the tried-set logic across
unary, count, and streaming loops, which drift independently — a
change to tried-set handling that touches only one loop body fails
review.

Reason: without a tried-set, one bad credential consumes every retry;
without a single result sink, cooldown state diverges from outcomes.

Check: a `tried` set consulted before each pick; one result method
called after each attempt; retry configuration clamped at the setter
with the zero meanings above stated; a tried-set change touches all
three loop bodies in the same change.

HARDENING NOTE (not a rule, not checked): extracting the tried-set
handling into one shared helper removes the drift source; per
`golang-design-patterns`, avoid repetitive code. The surveyed code
does not do this; the note is a recommendation, not surveyed practice.

When to apply: multi-credential failover over idempotent or safely
retryable calls.
When NOT to apply: exactly one credential (retry is same-credential
retry with backoff, different semantics); non-idempotent side-effecting
calls without an idempotency check; cooldown-on-failure is not wanted
for the call kind.

### PR-6. Conversion tables: constructible registry plus a package default, registered in init

For conversion between two formats, use a registry keyed by format pair
with typed format constants. Provide both a constructible `Registry`
type and a package-level default registry; register conversions in
`init()` of the conversion package, keyed by explicit format
constants — only where the PR-3 decision test holds (pure
constant-keyed entries, constructible registry present, tests on
the constructible form). A conversion needing per-pair
configuration, an endpoint, or a credential fails the test: wire
it explicitly (PR-3), never in `init()`.

Reason: the pair matrix is declarative data, not service wiring, so
self-registration keeps each conversion beside its code; the
constructible form keeps tests isolated.

Check: `Register`/`RegisterRequestEnvelope` methods on the registry;
package functions delegating to the default; `init()` functions in the
conversion packages; format keys are constants, not bare strings.

When to apply: a format-pair conversion matrix where conversions are
declarative data and an injectable registry exists alongside the
default.
When NOT to apply: test isolation matters more than call-site brevity
(use only the constructible `Registry`, injected explicitly); service
wiring of any kind — this rule never licenses a global service
locator.

Conflict note (scoped by one decision test, not by label):
`golang-dependency-injection`
rule 4 says never use global registries or package-level service
locators, and `golang-design-patterns` says avoid `init()` and mutable
globals. This rule's package default contradicts both, and the
contradiction is resolved only by the PR-3 decision test applied to
the entries themselves (pure, constant-keyed, constructible
alternative present) — relabelling a registry "declarative data"
does not pass it. Where the test fails, the existing skills win. Do not extend the global-default form
to executors, stores, or any service.

## Priority vs existing skills

- `golang-structs-interfaces`: interface placement, small interfaces,
  discovery over premature design. This skill adds only the executor
  contract shape, key discipline, and capability-probing form.
- `golang-dependency-injection`: constructor injection, composition
  root, no global registries, no `init()` service setup. This skill
  extends it by reference for PR-2/PR-3 and scopes PR-6 against it.
- `golang-design-patterns`: decorator/strategy, `init()` avoidance,
  shutdown and retry shapes. This skill adds only the selection-vs-
  execution split and the switch-vs-init split by extension kind.
- `codebase-design`: seam/adapter vocabulary. This skill's interface
  is the seam; do not introduce it with one adapter and no second consumer.
- `golang-concurrency` / `error-handling` / `golang-error-handling`:
  retry, backoff, error classification. This skill owns only the
  tried-set plus single result sink; retry/backoff rules stay there.
