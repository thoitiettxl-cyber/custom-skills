---
name: go-credential-stores
description: "Observed conventions for credential persistence, file modes, atomic replacement, refresh scheduling, and hashed operator secrets in a Go server. Use when a Go service persists renewable credentials to disk, refreshes them, or stores an operator secret in config. Do not use for in-memory-only credentials, single-process tools with one credential file and no refresh loop, or general secret handling — see golang-security instead. Priority: golang-security owns hashing, constant-time comparison, and secret handling generally; this skill adds only the store contract, file-mode/atomic-write checks, and refresh policy evidenced here. CS-5's stored hash is bcrypt in the surveyed code; a plaintext value supplied at runtime (environment, local password) is a fallback that is never persisted — see CS-5."
---

# Go credential stores: persistence, file safety, refresh, hashed secrets

Observed practice only, at the pinned commit in `references/PROVENANCE.md`.
No rule here claims encryption at rest: credential files in the
surveyed repo are plaintext JSON protected only by file modes. Secret
handling is described by mechanism only; no secret values appear in
this skill or its provenance.

## Rules

### CS-1. One narrow store interface; the manager owns login-then-persist

Put credential persistence behind one interface with list, save, and
delete operations. A manager owns login-then-persist and merges
pre-existing metadata from the store. The store contract forbids the
store from synchronously mutating the manager or re-entering load
during save; the manager merges store-enriched fields even on
non-fatal save errors, replacing metadata values, pointers, and
nested storage objects rather than mutating shared nested values in
place. Save must not retain the record or mutate shared nested values
in place. The no-reentrancy contract is comment-only in the surveyed
code: no grep proves a store never re-enters load — review must read
the `Save` implementations. A record returned without a store is
distinguished by its empty persisted-path return: callers must check
that return, not the record alone, before treating a credential as
durable.

Reason: one persistence contract keeps file, database, and remote
backends interchangeable; the no-reentrancy contract keeps save from
deadlocking the reload barrier it runs under.

Check: one store interface in the consumer-facing package; the
manager's login calls the authenticator, then persists through the
store, returning the record unpersisted (empty persisted path) when
no store is set; no second persistence interface exists in the same
package; `Save` implementations are read in review for reentrancy
and in-place mutation.

When to apply: credentials persist across restarts with reload or
refresh loops and more than one backend.
When NOT to apply: a single-process tool with one credential file and
no reload/refresh loop; in-memory-only credentials with no restart
persistence; one credential file, one writer function, and no second
backend planned — no store interface is required there, but the
single-writer invariant must be documented: every write site calls
the one writer function, and no second writer exists.

### CS-2. Set credential file and directory modes explicitly; audit writers that do not

Credential directories are created with mode `0700`; credential files
are written with mode `0600`, set on the created file itself, not
inherited from the umask. Note that a mode passed to a create/write
call applies only when the file is created: an existing
group-readable file keeps its old mode. Audit every credential writer:
in the surveyed repo, 4 of the 7 real token-file writers use plain
create calls and rely on the umask, while the store's own file writer
sets the modes — treat an unaudited writer as a gap, not as covered.

Reason: the umask is process-wide and mutable; a credential file must
carry its own restriction regardless of the caller's umask.

Check: `grep -rn 'MkdirAll.*0o700'` (38 non-test hits in the surveyed
repo) and `0600` create/write calls at the store paths; every
token-file writer found by grepping write call sites
(`Create`/`WriteFile`/`OpenFile`/`Chmod`) across the module, listed
and classified create-vs-explicit-mode; no writer left unclassified
(the classified list covers every grep hit).

When to apply: credential or secret files on a POSIX filesystem.
When NOT to apply: files that must be readable by another user or
group (shared directory, multi-user cache); Windows-only paths where
POSIX modes are not enforced — then document the platform gap instead
of claiming the mode.

### CS-3. Replace credential files atomically; serialize multi-process writers

Replace a credential file by writing a temp file in the same
directory, setting its mode, then renaming over the destination; clean
the temp file up on failure. If several processes may write the same
file — stated as a deployment fact in review, not assumed — serialize
writers with an inter-process lock file using `flock(2)` semantics:
the lock is held on an open file descriptor and released when the
holder process dies. An existence lock (create-and-remove a lock
file) fails this rule: a killed holder leaves it behind forever.
This is a partial pattern in the surveyed repo: 3 of the 7 real token-file
writers replace atomically (two via temp-plus-rename helpers, one via
a shared atomic-write helper), the other 4 write directly — scope any
claim to the writers actually checked.

Reason: a direct write leaves a torn file if the process dies
mid-write; rename within one directory is the atomic step.

Check: temp file created in the destination directory; mode set before
rename; rename is the last step; deferred temp removal on failure;
`flock`-semantics lock-file acquisition where multi-process writes exist (one writer in
the surveyed repo holds both an in-process mutex and an inter-process
lock file); 0 existence locks.

When to apply: credential or state files replaced in place.
When NOT to apply: append-only logs; files where torn writes are
harmless and cheaply re-derived; stores (database, object store) that
already provide atomic replace — do not add temp-plus-rename on top
of a transactional store.

### CS-4. Refresh before expiry with a per-credential lead time; refresh once on 401; classify terminal rejection

Refresh renewable credentials before expiry, with a per-credential
lead time declared by each authenticator as a `*time.Duration`: a
nil lead time means no proactive refresh, and is a legitimate
opt-out for non-expiring credentials; a zero-duration lead time
means refresh exactly at expiry and is distinct from nil. On an
upstream 401, refresh once before falling back or suspending.
Classify a terminal grant rejection as "requires sign-in"
instead of retrying forever. Terminal classification checks the
status code and error code first; substring matching of status
messages is only a fallback after those checks, so a wording change
upstream can misclassify — keep the classification rules beside
the status-code checks and review them when an upstream changes
wording.

Reason: lead-time refresh avoids expiry mid-request; one 401 refresh
recovers from a stale token without masking a revoked grant; terminal
classification stops an infinite refresh loop.

Check: a refresh-lead declaration per authenticator (9 registered in
the surveyed repo, 2 returning nil), typed `*time.Duration` so nil
and zero stay distinct; a refresh loop with a bounded
timer; a single refresh attempt after a 401 before fallback; a
terminal branch setting requires-sign-in, with status/code checks
before any substring fallback.

When to apply: renewable credentials with an expiry and a refresh
endpoint.
When NOT to apply: non-renewable static keys; credentials whose
refresh endpoint would itself leak or rate-limit — then refresh
lazily on 401 only, and say so; session keepers that re-authenticate
(for example browser re-export) rather than refresh tokens — they
are out of scope; do not force a refresh-endpoint shape onto them.

### CS-5. Store an operator secret only as a hash; hash plaintext on load and reject residual copies

A management or operator secret is stored only as a hash. The hash
is a slow password hash — bcrypt in the surveyed code; Argon2id is
the other accepted form per `golang-security`. A fast unsalted hash
(SHA-256 of the secret, compared with any comparator) fails this
rule. A plaintext value supplied in config is hashed on load and
the file rewritten through the CS-3 atomic replace; the surveyed
direct-write rewrite is the counterexample, not the pattern.
Any second plaintext copy elsewhere in the file is rejected. Verify
with the hash comparator, never by comparing hashes with `==`.
"Stored only as a hash" governs the config file. Plaintext-in-memory
fallbacks (environment value, local password) supplied at runtime
and never persisted are the exception, not the pattern, and are
compared in constant time; constant-time comparison does not hide
length, and a fallback must never be written to the file. Rotation
must cover all accepted sources. The plaintext value is
accepted at the input boundary and hashed on load — "never plaintext"
is false at that boundary; state the boundary honestly. With one
accepted source and no fallbacks, the rotation clause is trivially
satisfied by listing that one source; a fallback that exists but is
unlisted fails the rotation clause; residual-copy rejection applies
only when the file format admits a second copy location.

Reason: a stored hash survives a config-file leak without giving away
the secret; rejecting residual copies stops a second copy from
silently becoming the effective secret.

Check: hash-if-plaintext plus atomic file rewrite on load; residual-plaintext
rejection where the format admits a second copy location; bcrypt or
Argon2id hash, 0 fast-hash stores; hash
comparison at verification; constant-time comparison for the
in-memory fallbacks, 0 persisted plaintext fallbacks; all accepted sources listed in the
rotation procedure (one source, listed, when there is only one).

When to apply: an operator secret stored in a config file for a
network-listening service.
When NOT to apply: single-user local tools with no network listener
and no stored secret; systems using an external secret manager or
mutual TLS where a stored hash adds no boundary.

## Priority vs existing skills

- `golang-security`: hashing, constant-time comparison, file
  permissions, secrets in logs, brute-force defence. This skill
  extends it by reference and adds only the store contract, the
  mode/atomic-write audit checks, the refresh policy, and the
  load-time hash-and-rewrite mechanics. Do not restate its general
  secret-handling rules from here.
- `golang-structs-interfaces`: interfaces at the consumption site.
  This skill owns only the credential-store contract shape.
- `golang-dependency-injection`: constructor injection. The manager
  receives its store; this skill does not re-own injection.
- `golang-concurrency` / `golang-context`: timer and cancellation
  mechanics for the refresh loop. This skill owns only the lead-time
  registry and the 401-then-terminal policy.
- `management-center-webui`: management key distinct from client keys,
  from the client side. This skill owns the server-side storage and
  verification of that key.
