---
name: go-http-errors
description: "Observed conventions for HTTP error mapping, typed errors with redaction, status-leveled request logging, server timeout policy for streaming servers, and a shared stream-forwarding loop. Use when a Go HTTP server maps errors to statuses, logs requests, or forwards streaming responses. Do not use for non-streaming JSON APIs that need none of this, for structured slog/OTel pipelines, or for general error idioms — see golang-error-handling, golang-observability, and golang-samber-slog instead. Priority: golang-observability and golang-samber-slog govern slog/JSON logging; this skill's text-formatter request line is scoped to servers that already use that logger. HE-3's no-process-killing-log-call clause applies in server code whatever the logger is — see HE-3."
---

# Go HTTP errors: status mapping, typed errors, request logging, streaming

Observed practice only, at the pinned commit in `references/PROVENANCE.md`.
Two error layers coexist in the surveyed repo: a typed local status
mapping (HE-1) and a separate string/body-sniffing layer for upstream
failures. This skill keeps them labelled apart; do not merge them.

## Rules

### HE-1. Map errors to HTTP status through a StatusCode interface inspected with errors.As

Map an error to a status through an interface (`StatusCode() int`)
inspected with `errors.As`, with a documented fallback chain: explicit
status, then body-too-large 413, then client-cancelled 499, then
deadline 504, then unknown. "Unknown" maps to no status in the
surveyed mapper (it returns 0); the caller supplies the fallback
status — never invent one inside the mapper. 499 is a non-standard
nginx-style code for client cancellation, flagged as such wherever
it is returned. Detection is typed, never string matching in the
local layer: body-too-large is recognised via the typed
`http.MaxBytesError`, client cancellation via `errors.Is` on
`context.Canceled`, deadline via `errors.Is` on
`context.DeadlineExceeded`. Do not decide status by matching error
strings in the local mapping layer. One status source only: a type
carrying status in a field without `StatusCode()` must be
constructed only through the centralized constructors that set it;
the mapper's `errors.As` result is the status — never read the
field directly outside the mapper or the constructors, or the two
sources diverge. Typed-error constructors that
centralize status + code at the construction sites satisfy the
mapping-function check; the `StatusCode()` form is required only
where the status must travel in the error value across the handler
boundary. The sniffing layer for upstream
bodies (status/body code maps, substring matches) is a separate
classification for upstream failures, not local status mapping —
label it as such wherever it appears.

Reason: an interface keeps status with the error type, so wrapping
preserves it; string matching breaks when wording changes.

Check: one status-mapping function using `errors.As` for the
interface, then the fallback chain in order, returning 0 for
unknown with the caller supplying the fallback; 499 flagged
non-standard wherever returned; handlers call one
mapping function or construct through the centralized constructors
rather than mapping inline, with 0 direct reads of a status field
outside the mapper/constructors; upstream sniffing lives in its own function and
is never presented as the status mapper.

When to apply: errors that cross a handler boundary inside one process.
When NOT to apply: errors crossing a process or plugin boundary that
cannot carry Go types — then use stable string codes, never ad-hoc
substrings; CLI exit-code mappings (`ExitCode()`-style typed mappings
are the CLI analogue, not this rule's subject).

### HE-2. Wrap with %w; carry code, message, status, and retryable flag; redact before truncating

Wrap errors with `%w` and context at each boundary. Carry failures as
a typed error with code, message, optional status, and a retryable
flag; keep the cause reachable via `Unwrap`/`As`/`Is`. Before a
failure reaches a log or a client, redact credential-shaped values
and truncate — redact before the final truncate, so a secret
straddling the final cut cannot leak. The surveyed diagnostic
helper truncates a 600-rune scan prefix first, then redacts, then
truncates to 300: that scan-prefix truncate does not satisfy this
rule — only the `truncate(redact(…))` form on the final rendered
string does. Allowlist-summary errors that never embed body
bytes satisfy the redact-before-truncate intent with no truncate
step; the ordering requirement applies only when untrusted text can
reach the rendered string. This is partial in the surveyed repo: wrapping
dominates (1053 `%w` uses in non-test code under the two main trees),
but chain-breaking `%v` wraps exist in server startup paths — audit
for them; do not claim the chain is unbroken. Redaction is
key-name/regex based, so novel secret shapes can slip through; never
claim redaction is complete. A "trust boundary" here is where data
crosses to a less-trusted party (client, log store): across it,
re-create the error with a code/message instead of wrapping, per
`golang-error-handling` (`%w` internally, `%v` at system
boundaries). A same-trust internal boundary wraps with `%w`.

Reason: the chain preserves inspection; the typed fields let handlers
and clients branch without parsing prose; redact-then-truncate
ordering is what keeps a cut secret from leaking.

Check: `%w` at boundaries; the typed error's `Unwrap`/`As`/`Is`
methods; a redact-before-final-truncate helper on the log/client
path (a scan-prefix truncate before redaction does not satisfy
it); upstream JSON bodies passed through only when already valid
JSON, with every pass-through call site naming the caller that
redacts — an unnamed caller fails, because valid JSON can carry
secrets straight through; wrapping stops at trust boundaries
(re-created errors there, `%w` only inside one trust domain).

When to apply: errors that cross a server handler boundary: logged
by server request logging, returned to HTTP clients, or inspected
by handlers.
When NOT to apply: log-only terminal messages whose chain will never
be inspected; errors crossing a trust boundary — re-create them with
a code/message instead of wrapping (a wrapped cause can carry
secrets); errors rendered only from allowlisted fields, with no
untrusted text able to reach the rendered string.

### HE-3. One request line per request, status-leveled, with a server-generated id and masked values

Log one line per request, leveled by status (5xx error, 4xx warn,
else info), with a server-generated request id stored in both the
request context and the framework context, and sensitive header/query
values masked by key name before logging. Masking is key-name based
and incomplete by construction, like HE-2's redaction: novel secret
shapes slip through; never claim masking is complete. The evidenced
key sets are: headers — key names containing `authorization`,
`api-key`/`apikey`, `token`, or `secret`; query — `key`, `value`,
or names containing `api-key`/`apikey`/`api_key`, `token`, or
`secret`. URL path segments are not masked in the surveyed logger
(the path is logged verbatim; only the query of OAuth callback
paths is blanked) — a secret carried in a path segment reaches the
log; do not put secrets in path segments. Use one global logger with
a fixed text format (timestamp, level, caller, short id, ordered
fields); level is debug iff a debug flag is set, else info. No
process-killing log call in server code. Full request/response
capture is a separate opt-in file logger, never the default console
line. The surveyed logger is a custom text formatter, not JSON, and
uses no structured logger — do not present this rule as a
structured-logging rule, and do not assume machine parsing of the
text lines.

Logger-independent clause: the no-process-killing-log-call
requirement applies in server code whatever the logger is; it is
not bundled inside the text-logger scope of this rule.

Reason: one leveled line per request makes status classes greppable;
a server-generated id avoids trusting client-supplied correlation;
masking by the evidenced key names keeps the common secret shapes out of logs.

Check: 0 process-killing log calls in non-test server code, whatever
the logger (logger-independent clause above); 0
structured-logger imports in the surveyed trees; the request id is
generated server-side for data-plane paths only and stored in both
contexts; masking covers headers and query by the evidenced key
names, with the slip-through caveat stated; no secret-bearing path
segments in logged routes; the file
capture logger is opt-in with size caps; health-probe successes are
suppressed from the line.

When to apply: a server using this text logger, where one line per
request is the contract.
When NOT to apply: JSON/OTel pipelines (use a structured logger
end-to-end instead); CLIs where one global logger would hide
per-command output; services that must honour a client-supplied
request id (here ids are always server-generated; no incoming-id
honouring was found).

### HE-4. No body timeouts on a long-lived streaming server; short timeouts only on short-lived local servers

A long-lived proxy/streaming server sets no read/write timeout on the
main listener — only a header/sniff deadline — and only where that
listener serves streaming routes alone. A listener serving both
streaming routes and short-request routes is not covered by this
rule: the no-body-timeout policy must not be copied onto it, because
a slow body trickle on a short-request route is then unbounded.
Separate the listeners (short-request routes on their own listener
with explicit timeouts, as the surveyed local callback servers
are), or leave the combination unscoped and record it as a gap.
Short timeouts belong
on short-lived local servers (for example, local credential-callback
listeners with 10 s read/write timeouts). State the exceptions
explicitly, listed by listener in the guidance file; an unlisted
exception fails this rule.

Reason: a body timeout cuts a legitimately long stream; a sniff
deadline still bounds connection setup.

Check: the main `http.Server` has only a header/sniff deadline (10 s
in the surveyed code) and serves streaming routes only; read/write/idle timeouts appear only on local
callback servers or separate short-request listeners; exceptions are listed by listener in the guidance file.

When to apply: streaming or long-lived proxy servers on a
streaming-only listener.
When NOT to apply: ordinary short-request APIs where a hung handler
must be cut (set explicit read/write/idle timeouts); mixed
streaming/short-request listeners (separate them, or record the
gap); servers behind a proxy that already enforces timeouts (state
which layer owns the timeout; this rule prescribes no second
listener timeout there).

Conflict note: `golang-design-patterns` says every external call
should have a timeout, and `golang-context` covers timeout
mechanics. This rule scopes the no-body-timeout policy to the
streaming server listener only; it does not override timeout rules
for individual upstream calls. Where the two meet, the listener
policy governs the listener and the call policy governs the call.

### HE-5. Forward a stream through one shared loop: cancel on disconnect, write a terminal error once, flush every write

Forward a stream through one shared loop selecting on client
disconnect, data chunks, terminal errors, and a keep-alive ticker.
On disconnect, cancel the upstream work; write a terminal error at
most once, flush after every write, and end with a single terminal
marker — the one terminal write the loop performs (terminal error
or done marker, shared by all handlers through the same helper).
A flush error cancels upstream work and ends the loop; it is not
retried, and the terminal error is not written a second time.
Keep the keep-alive interval configured with a non-zero default, or
a misconfiguration silently disables keep-alives (the
surveyed default is zero — flag that; do not copy the zero default).
No replacement value is prescribed from the survey: the configured
default, in seconds, must be stated and greater than zero.

Reason: one loop keeps disconnect, error, and keep-alive handling
identical across handlers; writing the terminal error twice corrupts
the stream framing.

Check: one forwarding helper used by all streaming handlers (6 call
sites in the surveyed repo); the loop selects on context done, data,
errors, and the ticker; terminal error written once, then flushed,
then cancelled; a flush error ends the loop without a second
terminal write; keep-alive interval has a stated non-zero default in seconds.

When to apply: server-sent-event or chunked streaming responses over
HTTP.
When NOT to apply: non-streaming JSON responses (buffer, then write
once); protocols with their own framing/flow control (WebSocket,
gRPC streaming) — reuse their primitives instead of this loop.

## Priority vs existing skills

- `golang-error-handling`: `%w` wrapping, `errors.Is`/`As`/`Join`,
  sentinels, single handling rule, slog, HTTP logging middleware.
  This skill adds only the `StatusCode()`-via-`errors.As` fallback
  chain, the code/status/retryable typed error, and the
  redact-before-truncate ordering. Sentinel and wrapping basics stay
  there.
- `error-handling` (language-agnostic): typed errors, sentinel plus
  `%w`, handler unwrap to status, retry only retriable errors. This
  skill is the Go-server instance of those rules; the general rules
  stay there.
- `golang-samber-oops`: structured errors with codes and attributes.
  This skill does not re-own structured-error builders; use that
  skill when the codebase adopts that library.
- `golang-observability`: slog/JSON logging, metrics, tracing,
  migration from legacy loggers. This skill is scoped to the
  surveyed text logger; for any new slog/JSON pipeline, that skill
  governs and this rule does not apply.
- `golang-samber-slog`: slog handler pipelines and framework HTTP
  middleware with status-leveled configs. This skill's request line
  is the text-logger counterpart; do not mix the two in one server.
- `golang-concurrency` / `golang-context`: select/channel patterns
  and cancellation. This skill adds only the forward-loop shape;
  select and channel basics stay there.
