---
name: management-center-webui
description: Build or maintain a single-file management-center web UI for a command-line API proxy — protected management API plus a bundled SPA for editing config, managing accounts/auth, logs, usage, plugins and updates. Use when adding or changing such a UI, its management API client, its navigation/pages, or its single-file packaging. Do not use for the proxy core itself, for proxy request forwarding, for a general marketing site, or for small syntax questions already covered by a framework skill.
---

# Build a single-file management-center UI for a CLI API proxy — protected management API, bundled SPA, mobile-first navigation

Source: `router-for-me/Cli-Proxy-API-Management-Center`, pinned commit `64b4f5aed19b8f791eb21eb9e785ea379ea05b44` (2026-10-26), MIT. Evidence in `references/PROVENANCE.md`; endpoints in `references/api-contract.md`; UI/UX style in `references/ui-style.md`. The backend is CLIProxyAPI v8; the UI never forwards proxy traffic. Re-express, do not copy verbatim.

## 1. Shape of the system

1. The UI is a frontend only. It does not proxy traffic and must not add a proxy path; upstream data goes through the management API or a backend-declared plugin path, never around it.
2. One SPA, one HTML file in production, served by the core binary at a management path (source: `management.html` under the API port). No separate frontend deployment for the standard setup.
3. Keep three layers separate: feature pages/components, one API-client layer, and stores. Feature code stays in its feature folder; shared UI, hooks and utilities stay shared. Do not promote a feature helper early.
4. Treat the backend contract as source of truth. Before changing an endpoint name, payload, provider key, OAuth callback parameter, auth-file semantic or plugin/config contract, inspect the backend checkout; if it is unavailable, report the missing evidence instead of guessing.
5. Pin one backend major version per UI release (source: v8 only, no v0 fallback). The single sanctioned legacy touchpoint is a read-only probe that only improves the error message after a v8 login 404; it must never supply application data or act as a login fallback.

## 2. Management API contract

1. One base URL, one prefix. Detect the base from the page URL, let the user override it, strip a trailing `/v8/management` the user pasted, default the scheme to `http://`, then append the prefix for every request.
2. Every management request carries `Authorization: Bearer <management key>`. The management key is not a client/proxy API key and the two are never interchangeable; say so in UI copy where both appear.
3. Route all management calls through a single client that centralises the base URL, bearer header, timeout, error normalisation and response headers. No ad-hoc requests from components.
4. Normalise on read, serialise on write, inside the API layer. Components never handle raw backend field names; a `transformers` module owns the backend-shape to UI-shape mapping.
5. Parse errors into one envelope: a stable machine-readable code plus a human message. Newer endpoints put the code in `error` and the detail in `message`; older ones put the only useful text in `error` — keep both fallbacks, and keep the raw body on the error object for download paths.
6. A 401 from any management call logs the user out (one global `unauthorized` event). Do not retry a 401 with the same key.
7. Read server capability from response headers on every response, not from a separate capability call: version, build date, and whether the backend supports plugins. Gate plugin routes/UI on that flag; without plugin support, plugin routes redirect home.
8. Guard stale responses across connection changes. Pin a connection revision when a read starts and re-check it before a dependent write; a captured client pins one connection so a dialog started before a switch cannot write to the new session. Old async responses must never overwrite new-session state.
9. Config is one full document, not sections. Fetch the whole config with a short TTL cache (source: 30 s) plus in-flight deduplication, and invalidate the cache after any mutation. Optimistic UI updates keep the last server document intact until the invalidated cache is refetched.

## 3. Auth: the management key

1. Login is a connection test, not a token exchange. On login, set the client config and fetch the full config; success means authenticated. A 404 on that fetch only triggers the legacy-backend probe.
2. The login form has exactly three inputs: server URL (prefilled from the page URL, editable), management key, and remember-password. Do not add a username, and do not invent a session-cookie flow.
3. Remember-password controls persistence only. When off, the key lives in memory and the session is not restored; when on, persist it in browser storage and restore it on load. Clearing local login data is a System-page action.
4. Persisted keys are obfuscated, not encrypted. The source uses reversible XOR with a host/user-agent-derived key and says so in code and docs; never describe it as encryption or a security boundary.
5. Never commit a real management key, provider credential or auth file, and redact them from logs, screenshots and fixtures. A refresh response may contain tokens: never return it to callers or render it.
6. Remote access is a server-side decision. The UI accepts remote addresses, but remote management may require a server flag (source: `management.allow-remote`); surface the backend's behaviour in troubleshooting copy instead of adding a client-side bypass.

## 4. Mobile-first layout and navigation

Check any new UI at phone width first; desktop is the widened form. This pattern is the one Boss approved from phone screenshots (127.0.0.1:8317) and matches the pinned source.

1. Breakpoints: mobile `<=768px`, tablet `769-1024px`. Below mobile the sidebar becomes an overlay drawer with a backdrop, rail tooltips disappear, and header actions float.
2. Floating top bar, always reachable: refresh-all, language switch, theme switch, logout — icon-only. Refresh-all clears the config cache and refetches config, plugin resources and the auth-file count together; any rejection shows one failure notification, never a silent pass.
3. Sidebar: 216px open, 60px collapsed rail, 280px max on mobile. Collapsed state shows icons with hover/focus tooltips (label + meta); the collapse toggle is keyboard-shortcut accessible. Labels return when the drawer opens on mobile.
4. Group navigation by job, in this order, with a group label per group. Do not flatten it into one long list.

   | Group | Items (route) |
   | --- | --- |
   | Operate | Dashboard (`/`), Quick Start (`/quick-start`) |
   | Gateway | AI Providers (`/ai-providers`), Auth Files (`/auth-files`, count badge), OAuth Login (`/oauth`) |
   | Observe | Quota Management (`/quota`), Logs Viewer (`/logs`) |
   | Control | Config Panel (`/config`), Plugins (`/plugins`), Plugin Store (`/plugin-store`), Management Center Info (`/system`) |
   | Plugins (only when backend advertises support) | One entry per plugin resource page, grouped per plugin; multi-page plugins become a collapsible drawer |

5. Quick Start moves: under Operate normally, under Gateway when its sponsor provider is configured. Keep that conditional placement; do not duplicate the entry in both groups.
6. Auth Files carries a live count badge (files from `GET /credentials`), with a screen-reader label. A failed count load shows no badge, never a stale number.
7. Every nav item has a label and a one-clause meta description used in the collapsed-rail tooltip (e.g. "Auth files & credentials", "Request tracing").
8. Hash routing. The single-file deployment has no server-side routing, so routes are hash routes and unknown routes redirect to Dashboard. Keep legacy redirects (`/settings`, `/api-keys` to `/config`).
9. No standalone Routing page at the pinned commit: routing strategy is a config concern (Dashboard shows it, Config edits it). Do not add a top-level Routing nav item from the word "routing" in a label.

## 5. Page patterns

### Dashboard

1. Lead with a computed verdict, not a slogan: connection state drives the headline (steady / turbulence / needs attention / quiet / offline).
2. Show in one glance: connection status, server version + build date, model availability/counts, and traffic over a rolling window (10-minute buckets) with success rate. Numbers above six digits compress so tiles never break layout.
3. Dashboard data is assembled from config, auth files, models and recent-request usage — there is no dedicated dashboard endpoint. If a source is empty, show a dash, never a zero that implies measurement.

### Config Panel

1. Two editors, one document: a visual editor for common settings and client keys, and a YAML editor (CodeMirror, search + highlight) with a diff preview before saving. A YAML parse failure drops the user to source mode with the error; fixing it must allow a retry into visual mode.
2. Save by minimal patch, never blind full overwrite. Diff before/after YAML into patch + deletions + explicit-empty-maps, validate every field path before any mutation, then `PATCH /config`, `PUT {}` for intentional empty maps, and `DELETE` per removed field (a 404 on delete is tolerated; anything else aborts).
3. Refuse ambiguous concurrent list edits: if a list changed server-side to neither the old nor the desired value, throw a conflict instead of replacing it positionally. After a partial save, rebase the draft onto the latest document by replaying wire-level intent, not editor positions, pruning empty ancestors as the backend does.
4. Field paths must be safely representable in a URL: reject empty, `.`, `..`, slash/backslash and control characters before building `/config/<path>`; encode each segment separately.
5. Keep a draft-recovery path: an unsaved draft survives reload and can be restored or discarded explicitly. Never silently overwrite a recovered draft with a fresh fetch.
6. Whole-file escape hatch: `GET /config.yaml` as text, `PUT /config.yaml` as `application/yaml`. Raw mode only, not the normal save path.

### AI Providers / Auth Files / OAuth Login

1. Providers are edited as groups (keys, headers, proxies, model mappings), mapped to a shared resource model through descriptors/adapters. Extend those abstractions instead of scattering provider conditionals across pages.
2. A credential's identity is not its key alone: the same key with a different proxy is a different entry. Keep a source index per form entry; a missing or reused index on save is a conflict, not a merge.
3. Auth Files (`/credentials`): list, upload (multipart, 10 MB cap), download, delete (single, batch, all), enable/disable, edit fields, manual refresh, cooldown reset, per-file supported models. Use the raw-response client for upload/download; never log file contents.
4. OAuth Login is one attempt per provider: start, show the backend-returned URL and, when returned, the device/user code with a copy button, poll status every 3 s, allow cancel, and allow manual callback submission for remote flows. Attempts are independent; a stale attempt's late response must not write state. Plugin providers that declare OAuth appear after the built-ins.
5. Keep provider-specific quota/usage parsing in per-provider modules behind one quota-page contract. A provider with no usable observation shows "unknown", not zero.

### Quota / Usage

1. Quota is per credential, from credential metadata plus provider observations (plan type, reset grants, windows). Cache per credential identity and isolate sessions: one credential's observation must never fill another's tile.
2. Show reset instants/schedules in the user's timezone with relative labels, rendered from the same instant model as the numbers.
3. Client-key usage comes from `GET /observability/usage/api-keys` (15 s timeout). Keep it separate from provider quota; do not sum them.

### Logs Viewer

1. Poll with cursor pagination (`after` / `next-cursor`, `cursor-reset`), never re-fetch the whole file. A reset cursor clears the previous one.
2. One toolbar: search (deferred), level filter (trace/debug/info/warn/error/fatal), hide-management-traffic toggle, structured filters with clear-all, live follow with pending-lines resume, download of the cached view, clear logs, fullscreen. Fullscreen is a body class + card state, not a new route.
3. Logs require file logging enabled server-side. When off, say so and offer the toggle (`PUT /config/observability/logs/request-log`); do not show an empty list as if there were no logs.
4. Error logs are files: list, download one by name, download a request log by id, all as blobs with a longer timeout (60 s). Decode a download body as text without interpreting a successful log body as an API error; parse a blob error body before replacing the message.
5. Never render secrets in logs. Redact before display, and log search/filter code must not log matched lines to the console.

### Plugins / Plugin Store / System

1. Plugins are backend-gated and trust-gated. List, enable/disable (via `/config/plugins/configs/<id>/enabled`), delete, and per-plugin config: read via the config-value helper, write by merging touched fields into the latest object and `PUT`-replacing only that plugin's config — a backend `PATCH` would retain nulls and merge objects recursively, which is not what a form clear means.
2. Plugin resource pages are iframes to backend-declared paths, resolved against the API base; only `https:`, `data:` and `blob:` absolute URLs pass through unchanged. The iframe uses `referrerPolicy="no-referrer"`.
3. A plugin is "official" only when both its store source id/name and its repository URL normalise to the official org prefix; a registry copying repository metadata alone must not pass. Third-party installs need an explicit confirmation step.
4. Store install is `POST /plugins/store/<id>/install?source=&version=`, version in the body when given. Surface `restart_required`; do not auto-restart.
5. System page: app version (build-injected), server version + build date from response headers, update check via `GET /server/latest-version` (current/latest/unavailable shown distinctly), model list via `/v1/models` (needs at least one proxy API key), request-log toggle, clear-local-login-data. The update check never installs.

## 6. Build, packaging and release

1. Stack: React 19 + TypeScript (strict) + Vite + Zustand + Axios + React Router + i18next + CodeMirror + SCSS Modules. Use Bun with a frozen lockfile; do not introduce a second package manager's lockfile.
2. Single-file build is the contract: `vite-plugin-singlefile`, no code splitting, CSS not split, assets inlined (source limit 100 MB), ES2020 target, hash routing. No change to assets, imports, splitting or build config may introduce a required external artifact; never hand-edit generated `dist/`.
3. Version injection order: `VERSION` env, then git tag, then package version, then `dev`. Release renames `dist/index.html` to `management.html`; tags `vX.Y.Z` trigger it.
4. Gate: `bun run verify` = tests + lint + build (build includes `tsc`). Lint warnings are not failures in the source; do not silently tighten that gate when porting — record the decision instead.
5. Dev server connects to a real backend instance; prefer an HTTP server over `file://` for previews (CORS). The API address is detected from the page URL and is manually editable.

## 7. i18n, theme and accessibility

1. All user-facing text lives in locale files. The source ships six locales (`zh-CN`, `zh-TW`, `en`, `ru`, `vi`, `ko`) with `zh-CN` fallback; adding or changing a key means updating all six, including accessible labels. Browser detection picks the initial language; a manual switch overrides.
2. Themes: auto / white / light / dark, with preview cards. Reuse theme and motion timing tokens; never hard-code a colour or duration when a token exists.
3. Preserve keyboard interaction, accessible names, focus behaviour and reduced-motion handling on every interactive change. Collapsed-rail tooltips, drawers and menus must work by keyboard, not only hover.
4. When working inside a fork, keep the source style (2-space indent, semicolons, single quotes, 100-char lines, `@/` alias); when porting elsewhere, state the local style instead of mixing the two.
5. Visual and interaction style lives in `references/ui-style.md`: design tokens (light/white/dark), shell and floating top bar, component and state specs, icon set, motion vocabulary, theme switching, i18n text handling and accessibility — with ready-to-copy CSS variables and framework-agnostic skeletons. Reuse the tokens there; never hard-code a colour or duration when a token exists. Where the guide marks a value NOT FOUND, do not invent it.

## 8. Testing

1. Tests live in one `tests/` folder as `*.test.ts` under `bun:test`, with fixtures/helpers beside them: pure logic, static-markup rendering, source/contract checks. There is no DOM harness in the source; static markup tests do not verify browser interaction — say so when a change needs a real browser check.
2. Prefer extracting testable logic over introducing a new framework. For UI changes, verify the affected route in a browser with screenshots or notes; for code changes, run focused tests while iterating and `bun run verify` before handoff, reporting what actually ran.
3. Contract tests are first-class: pin the management prefix, header keys, error envelope, config-patch plan shape and field-path validation, because silent contract drift breaks every page at once.
4. Never put a real key, credential or auth file in a fixture; use redacted shapes with secret fields replaced by placeholders.

## 9. Do not copy from the source

- Provider-specific quota parsers, OAuth provider lists and plugin trust rules for CLIProxyAPI's providers: port the *pattern*, not the list.
- The sponsor/Quick Start provider and any sponsor card: REPO-ONLY, unless the target project has the same sponsor (see PROVENANCE).
- Chinese code comments are working notes, not user copy; user copy comes from locale files. Do not copy the v0 legacy probe into a project with no v0 backend to detect.

## Appendix A — Mapping to castctl (castctl-specific; the skill above stays generic)

Verify every line against the castctl HEAD in force before implementing; castctl facts here are as stated in the task brief and in castctl's web-UI docs as observed in the `castctl-webui` worktree, not re-verified against castctl main in this session.

1. Reuse the layout, navigation grouping, page patterns, single-file packaging and API-client discipline above. Castctl's UI already forks this Management Center; keep its kept/replaced list and NOTICE attribution current when pages change.
2. Diverge on the config model. Castctl config follows sing-box: one `config.json` of modular top-level blocks referenced by tag, not the v8 YAML document. Do not port the YAML patch plan literally; port the *intent* — minimal diff, validate before mutating, refuse ambiguous concurrent list edits, show a diff before saving — onto the JSON block model, citing the sing-box pattern per field.
3. Diverge on auth scope. Castctl's web UI today is read-only for the running instance's state in the brief's terms, and its credential is a required token on loopback; do not assume the Management Center's full write surface exists in castctl until a castctl gate approves it. Secrets stay write-only in castctl: the UI may set/replace cookies/tokens/keys and never shows or returns them.
4. Diverge on plugin/core pairing. Castctl follows CLIProxyAPI for plugin and core management (in-process trusted plugins, one mechanism per platform) while config follows sing-box. The store/iframe plugin patterns apply only if and when castctl's plugin support advertises them as the source gates on the backend header.
5. Login stays as castctl decided it: screencast login via the session keeper and `auth import` are the login paths. Do not carry any Management Center OAuth/device-code login over to castctl's Muse login; that flow is for a different account type and was explicitly rejected for this use.
6. Keep castctl divergences out of the generic skill text above; they belong in this appendix and in castctl's own docs.
