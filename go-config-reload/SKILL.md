---
name: go-config-reload
description: "Observed conventions for one hand-rolled single-file config loader with validate-then-sanitize loading, caller-resolved source precedence, fsnotify hot reload behind a hash gate, and a two-phase commit/apply reload. Use when a Go server loads one config document without a config library and must reload it live. Do not use when a layered config library is chosen, for multi-source precedence, or for startup-only config — see golang-spf13-viper and golang-cli instead. Priority: when Viper is chosen, golang-spf13-viper governs precedence and watching; this skill's validate/sanitize ordering still applies inside the unmarshal step. The strict-reject variant in CR-1 applies only under a documented project-wide strict-reject policy, never from a single strict field."
---

# Go config reload: single loader, hash-gated watcher, two-phase apply

Observed practice only, at the pinned commit in `references/PROVENANCE.md`.
This skill covers the hand-rolled single-file loader only. It does not
claim every field reloads: the listener is built once, and only one
field carries a restart-only marker (see PROVENANCE.md).

## Rules

### CR-1. One loader: defaults, then unmarshal, then validate, then sanitize

Load through one loader function for one document. Set defaults on the
struct before unmarshal so absent keys keep defaults, unmarshal, then
validate sub-configs, then run per-section sanitizers that drop invalid
entries. Fail the whole load only for hard validation errors; a bad
single entry is dropped by its sanitizer, never silently kept. The
surveyed drop is silent: no log, metric, or returned record names the
dropped entry. A loader adopting sanitizer-drop must make the drop
observable in review — either a log line naming the dropped entry, or
a loader doc comment listing which entries can drop and that drops
are silent. A sanitizer that drops with neither fails this rule.
Record the source bytes' hash on the loaded config. Decide the unknown-key
policy explicitly and state it: the surveyed main loader uses plain
unmarshal and ignores unknown keys, with strict checking only in one
legacy path — do not claim strict rejection unless the main load path
enforces it.

Strict variant: when project policy is documented strict-reject
(unknown keys and bad entries fail the whole load, exit non-zero,
never a silent fallback), sanitizer-drop does NOT apply — the whole
load fails on any bad entry instead, before any sanitizer drop takes
effect; a sanitizer that drops in strict mode fails this rule. The defaults ordering and the
hash-on-config requirement still apply under the strict variant.

Reason: one ordering makes every load behave the same; defaults-first
prevents absent keys from zeroing configured behaviour; sanitizers
keep one bad entry from killing the whole document.

Check: one loader entry point; defaults assigned before the unmarshal
call; validate calls after unmarshal; sanitizer calls after validate
(14 sanitizer methods in the surveyed loader); every sanitizer drop
is covered by a log line or a loader doc comment naming the
droppable entries; the hash is stored on
the loaded value; `grep -rn KnownFields` shows where, if anywhere,
strict checking runs (1 non-test site, legacy path only).

When to apply: one config document, one loader, no config library;
projects with a documented strict-reject load policy use the strict
variant above.
When NOT to apply: multi-source precedence (flags, env, file, remote)
— use an explicit layered loader instead of growing one file; a
security-relevant entry (secret, access list) must fail loudly instead
of being dropped silently; forward-compatible configs read by older
binaries — then warn-and-ignore plus a validate command reporting
unknown keys is the correct policy, stated as such; do not apply the
strict variant unless the strict-reject policy is documented
project-wide — a single strict field does not make the loader strict.

### CR-2. Hot reload is watcher plus debounce plus hash gate plus serialized apply

Watch the config file with an OS file watcher. Debounce events
(150 ms for config reload in the surveyed watcher — a surveyed
value, not a norm: tune it to document size and filesystem),
ignore empty writes, and reload only when the content hash differs
from the last applied hash. Serialize the read-hash-reload sequence
behind one mutex; ordering is the mutex plus the hash gate together,
not the mutex alone (the sequence gate for concurrent writers is
CR-4's). On load failure, keep serving the old config and log: a
failed load leaves the last-applied hash unchanged, so the next
write event retries — with no further event there is no retry, and
no self-healing is claimed. An empty read is ignored as transient
during editor writes; an intentionally empty document is not valid
config and must fail validation if it reaches the loader. Record the
hash of the bytes actually parsed, not the bytes that triggered
the event.

Reason: editors emit bursts of events; without debounce and a hash gate
every keystroke reloads; without serialization, concurrent writers
apply out of order; without keep-old-on-failure, one bad save takes
the server down.

Check: debounce constants (150 ms for config reload in the surveyed
watcher); empty-file ignore before hashing; hash comparison against
the last applied hash; the applied hash taken from the parsed config's
stored hash, updated only on a successful reload; load error returns without swapping the config. One
counterexample inside the surveyed watcher: a blocking sleep sits in
the event handler for remove/rename disambiguation — require any such
sleep to be justified or moved to a timer; do not copy it unexamined.

When to apply: config that can be applied incrementally while serving.
When NOT to apply: fields that cannot be applied incrementally
(listener bind address/port, TLS identity — those need restart or a
listener-rebuild path); polling when an OS watcher is available;
reloading on every event without debounce and a hash gate.

### CR-3. Resolve the config source in the entrypoint, never inside the loader

The entrypoint (caller) decides which path loads: an explicitly
configured store path, a flag value, or a working-directory default,
in one documented order. A `.env` file, if used, is loaded once at
startup for process environment only. The loader takes one explicit
path and performs no environment-variable lookup. Document the
precedence order wherever it is non-obvious: in the surveyed entrypoint
a configured store path overrides the flag, which surprises readers
who expect the flag to always win — never present "flag always wins"
as universal.

Reason: a loader that reads the environment hides its inputs and cannot
be tested with a path alone; caller-resolved precedence is reviewable
in one place.

Check: 0 environment lookups in the parse/load function itself; shared
helpers the loader calls are in scope only where they read the
environment for the load — list them, or state that none do; the
caller-side resolution function is named explicitly and is not
counted as a loader callee; the
precedence chain lives in the entrypoint; the `.env` load is
entrypoint-only and tolerates a missing file; no config library is in
the module file.

When to apply: the single-file loader of CR-1, with at most one
store-backed override.
When NOT to apply: services requiring env override of file values —
then implement one explicit precedence function (flag, env, file,
default) in a single place and test the ordering; do not scatter
environment reads; never load `.env` implicitly from the working
directory inside a library.

Conflict note: `golang-spf13-viper` fixes precedence as flag, env,
file, remote, default, and `cli-creator` uses env, file, flag. This
skill does not reconcile those orders. It states only that precedence
is caller-defined, documented, and tested; when Viper is used, Viper's
fixed order governs. The surveyed order (store, flag, default) is
evidence that orders differ, not a recommended order.

### CR-4. Reload in two phases: commit, then apply, gated on sequence currency

Phase 1, commit: validate, deep-clone, swap the pointer under a write
lock, bump a monotonic sequence; reject invalid updates before the
swap. Phase 2, apply: re-derive runtime state (selectors, executors,
clients) under a second lock, checking sequence currency first so a
stale commit's apply is dropped and the drop is logged. A dropped
stale apply leaves readers on the newer commit with runtime state
derived from the older apply — do not claim commit+apply atomicity.
Check cancellation between apply steps.

Reason: the swap must be atomic and rejectable, while re-deriving
runtime state is slow and must not block readers; the sequence gate
keeps a slow apply from overwriting a newer commit.

Check: a commit function holding the update lock, cloning, swapping,
and incrementing the sequence; an apply function holding the runtime
lock, dropping stale commits, and logging the drop; cancellation checks between steps.
The clone discipline is CR-5's: the commit clone and the handoff
clones are the same clone function, not two copy mechanisms.

When to apply: config applied live by more than one writer (watcher,
management API, control plane).
When NOT to apply: config read once at startup (a single swap under
one lock is enough); applies already serialized by a single goroutine
(the sequence gate is for concurrent writers).

Gap note: the surveyed repo marks only one field as restart-only and
leaves bind host/port and TLS unannotated. This skill does not turn
that into a marking convention; see PROVENANCE.md, Observed gaps.
State reloadable vs restart-only per field group in the field's own
documentation as a project decision, and verify the listener is not
assumed reloadable.

### CR-5. Publish immutable snapshots; clone on every handoff

Never share a mutable config value across goroutines. Publish
immutable snapshots: every handoff (watcher, server, handler, manager)
deep-clones before storing; reads go through an `RWMutex` accessor
returning the current snapshot pointer. Require a test that mutating
a published snapshot's exported fields cannot affect the stored
config (mutate the snapshot, read the stored value back). Note the
surveyed clone's limit: it is reflection-based and shares fields it
cannot set, so unexported state is shared, not cloned — the
snapshot-mutation test must not be written against unexported
state (it fails by construction there); probe the unexported-sharing
limit in a separate test that documents the sharing, and flag it
in review.

Reason: a shared mutable config makes every reader a potential writer;
clone-on-handoff confines mutation to the commit path.

Check: a clone function; clone call sites at every handoff (11 call
sites plus the definition in the surveyed repo); an `RWMutex` accessor
for reads; a snapshot-mutation test over exported fields exists, plus
a separate documented-sharing test for unexported state.

When to apply: config read concurrently while reloads happen.
"Reload" here means replacing a stored in-process snapshot.
When NOT to apply: a small config read on a hot path — clone cost
here is paid only on commit/handoff, not per request, so excluding
a hot path requires measurement, not assumption (reads use the
snapshot pointer); a provably immutable value (all
fields unexported with only getters, or frozen after load);
re-parse-per-request and explicit re-read with no stored snapshot —
with nothing stored, there is no snapshot to protect.

## Priority vs existing skills

- `golang-spf13-viper`: layered precedence, `WatchConfig`, test
  isolation with per-test instances. This skill is the no-Viper
  counterpart; when Viper is chosen it governs, and this skill's
  CR-1 ordering applies inside Viper's unmarshal step.
- `golang-cli`: flag binding and config layering. This skill adds only
  the entrypoint-resolved source chain and the no-env-in-loader rule.
- `management-center-webui`: one-document config and minimal-patch
  save from the client side. This skill owns the server-side loader
  and reload mechanics; save semantics stay there.
- `golang-concurrency`: mutex discipline. This skill adds only the
  commit/apply split and the snapshot accessor as concrete instances.
- `golang-context`: cancellation between apply steps. Mechanics stay
  there; this skill requires the checks at apply boundaries.
- `golang-safety`: defensive copies across boundaries. This skill adds
  only the config-snapshot instance of that rule.
