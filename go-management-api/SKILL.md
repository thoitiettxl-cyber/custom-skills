---
name: go-management-api
description: "Observed conventions for a separate management/control-plane route group in a Go server: its own auth, availability gating, per-IP failure bans, one stable error shape, config ETags, and a tri-state incoming-auth chain. Use when a Go server exposes an operator surface on the same process as its data plane. Do not use for CLI-only tools, for a management surface on a separate loopback-only listener, or for general REST design — see api-design and management-center-webui instead. Priority: api-design owns versioning, naming, and pagination; management-center-webui owns the client-side contract (single API client, bearer header, 401 logs out, one-document config, minimal-patch save); this skill owns only the backend separation, gating, and auth mechanics evidenced here, including the backend ETag/If-Match contract in MA-3, which is surveyed-repo backend evidence, not a client behaviour from management-center-webui. MA-3's envelope/ETag halves apply independently when a prior contract ships only one half — see MA-3."
---

# Go management API: separate group, gated auth, stable errors

Observed practice only, at the pinned commit in `references/PROVENANCE.md`.
"Management" means operator/control-plane routes. "Data plane" means
the routes that serve client traffic. Both run in the same process and
on the same port in the surveyed repo, separated by route group,
middleware, and registration gate — not by listener.

## Rules

### MA-1. Separate the management group with its own auth; hide it when unavailable

Register management routes in their own route group with their own
auth middleware, separate from the data-plane group. Register the
group only when a management secret exists. When the group is not
available, its routes answer 404 (hiding existence) rather than 401.
A management-only server that does not start at all when the secret
is absent satisfies the hiding requirement; on a combined server
(management + data plane in one process) the not-starting variant
does not apply — refusing to start over the management secret takes
down the data plane too, so the 404 variant is the only compliant
one there. Keep callbacks that must live
outside the group behind the same availability check, except
liveness/health callbacks for the data plane, which stay ungated:
gating a health callback behind the management-secret check makes
an orchestrator report a healthy data plane as dead.

Reason: a separate group keeps operator auth from leaking into client
auth decisions; 404-hiding avoids confirming the surface exists to
unauthenticated callers.

Check: distinct group registration for management vs data plane;
registration gated on a secret being present; an availability
middleware answering 404 when disabled; unauthenticated exceptions
(health endpoint, management page) listed explicitly, not assumed.

When to apply: a management surface sharing a process/port with a
data plane.
When NOT to apply: no management surface at all; management exposed
only over a separate loopback-only listener — then 404-hiding is
unnecessary, but the separate-auth rule still applies.

### MA-2. One shared management-key check: bearer or dedicated header, per-IP bans, remote off by default

Authenticate management requests with one shared check used by HTTP
and non-HTTP callers alike. Accept `Authorization: Bearer <key>` or a
dedicated header. Accepting only `Authorization: Bearer <key>` is a
compliant stricter variant of the two-form clause. A non-`Bearer`
Authorization value must not be accepted verbatim as the key: every
Authorization value is scheme-checked (Bearer scheme, or the
dedicated header alone). The ban response must not include the
remaining ban time. Both shapes exist in the surveyed code and are
recorded flaws, not patterns: a verbatim-acceptance path or a
ban response carrying remaining time fails this rule. Count failures per
client IP and ban the IP after a small fixed threshold for a fixed duration (5 failures / 30 minutes
in the surveyed code, hardcoded constants, not configuration).
Remote management is off by default; loopback alone does not bypass
the key, and loopback-only reachability does not lift the ban
requirement.

Reason: one check keeps HTTP and non-HTTP entry points consistent;
per-IP bans bound credential guessing; remote-off-by-default keeps
the operator surface local until explicitly opened.

Check: one authentication function shared by callers; Authorization
values accepted only with the Bearer scheme, or Bearer-only as the
stricter variant; 0 verbatim-acceptance paths; 0 ban responses
carrying remaining ban time; failure counting and ban per IP; remote requires an
explicit allow flag; loopback is exactly the loopback addresses.

When to apply: a management surface reachable over a network, even
only loopback.
When NOT to apply: behind an authenticating reverse proxy or mutual
TLS where IP-based banning would punish a shared egress IP; public
read-only status endpoints that intentionally need no key (mark them
explicitly unauthenticated).

### MA-3. One stable management error shape; config reads carry an ETag and honour If-Match

Management errors use one stable machine-readable shape
(`{"error": "<code>"}` plus HTTP status, no free-form detail by
default). Config reads carry an `ETag` that is the hash of the
on-disk bytes plus `Cache-Control: no-store`; writes honour an
optional `If-Match` (mismatch answers 412 with no write). This shape
is partial in the surveyed repo: the `{"error": …}` form dominates
management handlers, but bare-numeric error responses and at least
one free-form error string exist — audit the handler set and fix
stragglers rather than claiming uniformity. The ETag/`If-Match`
contract covers the config document only; the data plane uses a
different error body (see `go-http-errors`). This rule applies when
no error-envelope / concurrency contract exists yet. When a project
already ships a contract, each half is decided independently: a
shipped nested envelope exempts only the envelope half (record the
divergence, do not retrofit the flat shape), and a shipped
body-hash concurrency contract exempts only the concurrency half.
A project shipping one half adopts the other half under this rule.

Reason: a stable code lets clients branch without parsing prose;
ETag plus `If-Match` turns a concurrent edit into a visible conflict
instead of a silent overwrite.

Check: bare-numeric responses are enumerated with a disposition per
handler, and the flat form covers the handlers in scope; ETag equals the on-disk hash;
a mismatched `If-Match` returns 412 and writes nothing; absent
`If-Match` stays unconditional; or, for a prior shipped contract, the
divergence is recorded per half and the shipped halves are unchanged.

When to apply: a management API with concurrent editors or clients
that branch on error codes, and no prior envelope/concurrency
contract (or a prior contract covering only one half, for the
other half).
When NOT to apply: wire-compatible proxies that must preserve an
upstream error body verbatim; single-writer config with no concurrent
editors (the ETag is still cheap, but `If-Match` enforcement may be
dropped — say so); a project that already ships both a nested
envelope and a body-hash concurrency contract (record the divergence
per half; do not retrofit).

### MA-4. Incoming-request auth is an ordered tri-state chain; call out a zero-provider fail-open

Authenticate incoming requests through an ordered chain of providers,
each returning handled, no-credentials, or invalid. Try providers
until one succeeds; "not handled" never becomes an error; missing and
invalid stay distinct so the final error is accurate (invalid wins
over missing for the error code; the final status is 401 in both
cases in the surveyed code). Zero providers configured means
unauthenticated access in the surveyed code — a legacy fail-open
labelled as such in the surveyed comment. Do not copy the
zero-provider branch, and do not copy a nil-manager pass-through:
a chain with no providers gates nothing, and its endpoints must be
marked explicitly unauthenticated instead (see WHEN-NOT). A
zero-provider or nil-manager branch returning unauthenticated fails
this rule; a comment or docs line does not cure it.

Reason: tri-state outcomes keep a provider that does not recognise a
request from vetoing providers that do; distinguishing missing from
invalid keeps the final error honest.

Check: a provider interface with the three outcomes; a chain loop
remembering missing vs invalid, returning 401 for both with the
invalid code winning; 0 zero-provider or nil-manager branches
returning unauthenticated; per-route variants share one chain function rather than duplicating the shape (the surveyed
code duplicates it — flag that drift in review).

When to apply: more than one credential kind can authenticate a
request, with at least one provider configured.
When NOT to apply: exactly one fixed credential (a single check is
clearer than a chain); public endpoints with no auth at all (mark
them explicitly unauthenticated).

## Priority vs existing skills

- `api-design`: resource naming, status codes, pagination, error
  envelope `{error:{code,message}}`, versioning, token auth patterns.
  This skill adds only the backend group separation, availability
  gating, ban mechanics, and the tri-state chain; versioning and
  naming stay there. Note the envelope tension: `api-design` uses
  `{error:{code,message}}`, the surveyed management surface uses the
  flatter `{"error": "<code>"}` — the flatter form is scoped to this
  management surface only; do not present it as the general API shape.
- `management-center-webui`: the client-side management contract
  (single API client, bearer header, 401 logs out, one-document
  config, minimal-patch save). This skill owns the backend side
  of the same contract, including the backend ETag/`If-Match`
  contract in MA-3, which rests on surveyed-repo backend evidence
  alone — `management-center-webui` contains no ETag/`If-Match`
  content and owns no part of it; do not restate
  its client behaviour here.
- `golang-security`: authentication, brute-force defence, timing
  attacks. This skill adds only the management-key plus ban plus
  remote-off combination; generic brute-force guidance stays there.
- `golang-swagger`: OpenAPI documentation. Unaffected; document the
  management surface there when it applies.
