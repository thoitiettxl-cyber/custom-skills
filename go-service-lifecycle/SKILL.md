---
name: go-service-lifecycle
description: "Observed conventions for a long-running Go service: signal-derived run context, fresh-timeout shutdown, a fixed worker pool with a coalescing wake channel, singleflight dedup per operation family, channel semaphores, and idempotent ordered shutdown. Use when a Go daemon or embeddable service owns background work and must stop cleanly, or for a long-running command in a CLI dispatch model (per-command pair, see SL-1). Do not use for one-shot commands, libraries with no background work, or general goroutine and context design — see golang-concurrency, golang-context, and golang-design-patterns instead. Priority: those skills govern goroutine, channel, and shutdown mechanics generally; this skill adds only the wiring shapes evidenced here. Shutdown context is entrypoint-scoped Background+timeout (SL-1); WithoutCancel is the request-scoped form for work outliving one request — see the Priority note."
---

# Go service lifecycle: run, workers, dedup, semaphores, shutdown

Observed practice only, at the pinned commit in `references/PROVENANCE.md`.
Shutdown here means "stop promptly": the surveyed HTTP stop closes
listeners immediately without draining active connections. Do not
promise draining from this evidence.

## Rules

### SL-1. One Run/Shutdown pair; signals derive the run context; shutdown runs on a fresh timeout context and is idempotent

One long-running service owns all background work behind a single
`Run(ctx)` / `Shutdown(ctx)` pair. The entrypoint derives the run
context from OS signals (SIGINT/SIGTERM). `Run` blocks on context
done or a server-error channel. A run is one-shot when it has no
serve loop and is never re-entered after it returns: a `Run()` that
is called once and ends on a signal/timer without restarting
satisfies this, and re-entering it — calling it again from a
restart loop or retry wrapper — fails the one-shot test, whatever
its name. Shutdown runs under a fresh timeout
context derived from `context.Background()` — never under the
cancelled run context — and is idempotent. Do not fake readiness
with a sleep before reporting "started": the surveyed code sleeps
100 ms before printing started, with no readiness channel — flag
that shape, do not copy it. In a CLI dispatch model with no single
owning service, the pair requirement is per long-running command:
each such command must derive its run context from signals and shut
down on a fresh timeout context; no cross-command pair is required.

Reason: one pair makes ownership of background work auditable; a
fresh shutdown context is the only context still alive after
cancellation; idempotence makes double shutdown safe.

Check: one signal-derived context at the entrypoint; `Run` blocks on
done/error; the deferred shutdown builds a fresh timeout context
(30 s in the surveyed code); shutdown is guarded so repeat calls are
safe.

When to apply: long-running servers, daemons, embeddable service
types with background work; long-running commands in a CLI dispatch
model (per-command pair, see above).
When NOT to apply: one-shot commands (a single `Run()` that returns,
no serve loop, no restart), however long one run lasts; libraries
with no background work; shutdown that must be instantaneous — then
close semantics, documented as such, are the honest choice, and no
draining is promised.

### SL-2. Background refresh runs as a fixed pool with a coalescing wake channel

Background refresh or polling work runs as a fixed pool of workers
consuming a buffered jobs channel. Pool size comes from configuration
with a sane default and is clamped (never 0, never more than the
work). Every worker loop selects on context done. A non-blocking
wake channel (capacity 1) reschedules without queueing duplicates.
Record the dirty work in the dirty set BEFORE sending the wake: a
dropped wake is safe only because the dirty set persists and the
loop re-reads it on the next wake — a wake sent before the dirty
set is recorded can be dropped with the work unrecorded. Spawn workers once per loop lifetime; the loop, not the caller, owns
them. Workers owned solely by context cancellation are never joined;
state that ownership explicitly rather than implying a join. Cancel
first on shutdown: do not close a shared resource synchronously on
the shutdown path while unjoined workers may still be using it —
that window is a recorded gap, bounded only by the shutdown
timeout. One-off
parallelism is a different shape (a `WaitGroup` fan-out), not a
standing pool.

Reason: a fixed pool bounds refresh concurrency; a capacity-1 wake
channel coalesces bursts of reschedule requests into one wake;
context ownership gives workers a single exit signal.

Check: pool size from config, clamped to the work count (16 default,
config-overridable in the surveyed refresh loop); workers select on
context done; wake channel capacity 1 with a non-blocking send
after the dirty set is recorded; workers spawned once in the loop's run method; shutdown cancels before closing shared resources.

When to apply: periodic background refresh or polling in a daemon.
When NOT to apply: one-off parallelism (use a `WaitGroup` fan-out, or
errgroup per `golang-concurrency`); work items that must not be
coalesced or dropped (the cap-1 wake channel deliberately drops
duplicate wakes).

Conflict note: `golang-concurrency` prefers errgroup where error
propagation is needed and `errgroup.SetLimit` over hand-rolled pools.
The surveyed repo uses no errgroup anywhere (0 hits); fan-out errors
surface via result slots or logging. This rule does not override the
errgroup preference in general; it records the standing-pool shape
for refresh loops and requires the error-surfacing mechanism to be
stated. For one-off fan-out with errors, errgroup still governs.

### SL-3. Deduplicate identical concurrent refreshes with one singleflight group per operation family

Deduplicate concurrent identical refresh or fetch operations with one
`singleflight.Group` per operation family, keyed by the identity being
refreshed. One group per family (package-level or per-manager), never
one global group for unlike operations; the in-flight call's result,
including its error, is shared with all waiters. A package-level
group is allowed only when the family is the package's single
operation family; a package serving two families needs two groups
(or per-manager groups). Do not claim
singleflight alone implements backoff or blocking: the surveyed code
pairs it with a separate mutex-guarded block map for negative caching,
whose entries carry an expiry (`until`) and are cleared on success.

Reason: without dedup, N concurrent callers trigger N identical
refreshes; one group per family keeps unlike operations from
colliding on a key. Not to be confused with cross-process
single-flight guards (owner files/flocks): the two mechanisms are
unrelated and may coexist under distinct names.

Check: one group declaration per family (15 `singleflight.Group`
references, 17 files mentioning singleflight in the surveyed repo);
the key is the refreshed identity; a paired block map exists where
negative caching is needed.

When to apply: concurrent refresh of credentials, catalogs, or remote
metadata.
When NOT to apply: callers needing independent cancellation
(singleflight shares one call; a waiter's context cannot cancel the
leader); cheap, idempotent operations already serialized; keys that
could collide across unlike operations (separate groups, or key
namespacing, is mandatory); request-scoped fan-out (see SL-2);
cross-process single-flight guards (owner files/flocks) — a
different mechanism, not this rule's subject.

### SL-4. Bound a scarce resource with a named-capacity channel semaphore, acquired under context

Bound concurrent access to a scarce resource with a buffered
`chan struct{}` used as a semaphore: capacity is a named constant,
acquisition selects on context done, and the permit is released
exactly once, on the branch that acquired it — the context-done
branch releases nothing, because it never acquired. A weighted
semaphore is a different tool
for a reader/writer-style exclusion gate, not an interchangeable
general pattern: the surveyed weighted gate excludes the whole
store (mutations acquire 1, a full load acquires all), and must be
named as whole-store exclusion, not as a permit budget. Do not use a fixed-capacity channel where the budget
must change at runtime, where acquisition must be fair/FIFO, or for
ordinary mutual exclusion — use a mutex there. A stop-signal channel
(send-to-stop, no acquire/release) is not a semaphore.

Reason: a named capacity makes the budget reviewable; context-aware
acquisition keeps a cancelled waiter from consuming a permit;
release-on-all-paths keeps the budget from leaking.

Check: named capacity constants (2, 4, and per-category caps in the
surveyed code); acquire inside a select with context done; exactly
one release on the acquired branch and 0 releases on the
context-done branch; the weighted-semaphore
gate, where present, is exactly one gate with whole-store exclusion
semantics.

When to apply: bounding upstream calls, decodes, or connection
validation to a small fixed budget (2–16 permits) in a long-running
service, where a channel semaphore is the chosen mechanism.
When NOT to apply: runtime-resizable budgets; fairness requirements;
ordinary critical sections (mutex, per `golang-concurrency`); a fixed
worker fan-out sized once at startup (`WaitGroup`, one goroutine per
slot) — that shape is SL-2's; do not retrofit a semaphore onto it;
stop-signal channels (send-to-stop, no acquire/release).

### SL-5. Shutdown is idempotent, ordered, and error-tolerant, keeping the first error

Guard the shutdown body with `sync.Once` (or equivalent), nil-guard
every stored cancel function before calling it, cancel background
loops before stopping the components they feed, and accumulate errors
keeping only the first, while still attempting every stop step and
logging the rest. Never let a failing stop step skip the remaining
steps. Require an explicit, documented stop order per service: the
surveyed shutdown order is not uniform across its two shutdown paths,
and the deferred `Run` shutdown logs its error only. Do not apply
`sync.Once` shutdown to restartable components (Once never runs
again; use explicit state plus a mutex for start/stop cycles), and do
not use first-error-only accumulation where every error must be
reported (use `errors.Join` per `golang-error-handling` instead). For
closables that are reconfigured after close, mutex-guarded flag
idempotence satisfies this rule; `sync.Once` is required only for
terminal shutdown.

Reason: shutdown must complete even when parts fail; keeping the first
error preserves the root cause without hiding later failures in logs;
an explicit order prevents feed-before-consumer stops.

Check: a `Once` guard on terminal shutdown, or a mutex-guarded flag
for closables reconfigured after close — keyed by kind: terminal
shutdown uses `Once`, reconfigurable closables use the flag, and
neither form is accepted for the other kind; nil-guarded cancels; loop cancel
before component stop; first-error accumulation with all steps
attempted; a documented stop order for the service naming the
feed-before-consumer order (cancel loops before stopping the
components they feed); the deferred-`Run` shutdown's error-only
logging is stated as a limit, not presented as full reporting.

When to apply: services with multiple stoppable subsystems.
When NOT to apply: restartable components; every-error-must-report
shutdown reporting; closables reconfigured after close (flag
idempotence, not `Once`, satisfies the idempotence clause).

## Priority vs existing skills

- `golang-concurrency`: goroutine lifecycle, channels, `sync`
  primitives, errgroup, singleflight, worker pools, pipelines. This
  skill extends it by reference and adds only the signal-to-Run
  wiring, the config-clamped pool plus cap-1 wake, the
  one-group-per-family dedup shape, the channel-semaphore form, and
  the idempotent ordered shutdown. Channel vs mutex vs atomic
  selection, errgroup preference, and leak rules stay there.
- `golang-context`: cancellation ownership, never storing a context,
  `WithoutCancel` for outliving work. This skill requires the
  fresh-timeout shutdown context and context-done selects; mechanics
  stay there. Reconciliation: the shutdown context is
  `context.WithTimeout(context.Background(), …)` at the service
  entrypoint — a top-level entry point, where Background is the
  correct base — while `WithoutCancel` is the form for work that
  must outlive a single request. The two forms answer different
  questions (entrypoint lifetime vs request continuation) and
  neither replaces the other.
- `golang-design-patterns`: graceful shutdown and retry shapes. This
  skill adds only the concrete wiring; pattern selection stays there.
- `golang-uber-fx` / `golang-samber-do`: framework lifecycles. This
  skill is the no-framework wiring; when a framework owns lifecycle,
  that skill governs.
- `golang-error-handling`: error accumulation and `errors.Join`. This
  skill's first-error rule is scoped to shutdown; full-error reporting
  stays there.
