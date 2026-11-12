# Management API contract (observed in the UI layer, pinned commit 64b4f5a)

Base: `<scheme>://<host>:<port>` + `/v8/management`. All calls below are
relative to that prefix, through the single Axios client in
`src/services/api/client.ts`, with `Authorization: Bearer <management key>`
and `Content-Type: application/json` unless stated. Timeouts: 30 s default,
60 s for log downloads, 15 s for client-key usage, 300 s for refresh-all.

Server capability arrives in response headers, not a capability endpoint:
`x-cpa-version`, `x-cpa-build-date`, `x-cpa-support-plugin`
(fallbacks `x-server-version`, `x-server-build-date`).

Error envelope: `{ "error": "<code>", "message": "<detail>" }` on newer
endpoints; older endpoints may put the only text in `error`. A 401 logs
out globally. A config-value read that returns 404 with apiCode
`not_found` means "absent field", not "missing route"
(`src/services/api/configValue.ts`).

## Config

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/config` | Full config document (normalised on read) |
| PATCH | `/config` | Minimal patch object (diff plan) |
| DELETE | `/config/<segment>/…` | Delete one field path (404 tolerated) |
| PUT | `/config/<segment>/…` | Set one field path; `{}` for an intentional empty map |
| GET | `/config.yaml` | Whole config as YAML text (`Accept: application/yaml`) |
| PUT | `/config.yaml` | Whole config as YAML (`Content-Type: application/yaml`) |
| PUT | `/config/access/api-keys` | Replace client (proxy) API keys |
| GET/PUT | `/config/api-keys/<group>` | Upstream provider groups (via group helpers in `providers.ts`) |
| PUT | `/config/observability/logs/request-log` | Request-log on/off (boolean body) |
| GET/PUT | `/config/oauth/excluded-models`, `/config/oauth/model-alias` | OAuth excluded models / model aliases (queued, per-provider map writes) |
| GET/PUT | `/config/plugins/configs/<id>`, `…/<id>/enabled` | Per-plugin config; enable/disable (boolean body) |

Field paths are built segment-by-segment with `encodeURIComponent` per
segment; keys containing `/`, `\`, `.`, `..`, empty or control characters
are rejected client-side before any request.

## Credentials / auth files

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/credentials?name=&auth_index=` | List auth files (optional single lookup) |
| POST (multipart) | `/credentials` | Batch upload auth files (`file` fields) |
| DELETE | `/credentials` | Batch delete (`{ names: […] }` body) or all (`?all=true`) |
| PATCH | `/credentials/status` | Enable/disable (`{ name, disabled, auth_index? }`) |
| PATCH | `/credentials/fields` | Edit fields (`{ name, …fields }`) |
| POST | `/credentials/refresh` | Manual refresh, one file or `{ all: true }`; response may contain tokens and is never returned to callers |
| POST | `/routing/cooldown/reset` | Reset cooldown (`{ auth_index }`) |
| GET (blob) | `/credentials/download?name=` | Download one auth file |
| GET | `/credentials/models?name=` | Models supported by one credential |
| GET | `/routing/model-definitions/<channel>` | Model definitions for a channel |

## OAuth / login flows (management API)

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/oauth/auth-url?provider=&is_webui=` | Start flow; returns `url`, optional `user_code`, `state`, `flow`, `expires_in` |
| GET | `/oauth/status?state=` | Poll: `ok` / `wait` / `error` |
| DELETE | `/oauth/session?state=` | Cancel a flow |
| POST | `/oauth/callback` | Submit manual callback (`{ provider, redirect_url }`) |
| POST | `/oauth/siwc/bind` | Start a SIWC binding for a named credential; returns `url`, `state`, `flow: "siwc_bind"`, `expires_in` |

Provider keys in management paths are normalised (`anthropic` → `claude`
for the path). Which providers a given backend offers, and which flows
each supports, is backend-declared; the UI must not hard-code a provider
list as a contract.

## Observability / usage

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/observability/logs?after=&cursor=&limit=` | Log lines + `latest-timestamp`, `next-cursor`, `cursor-reset` |
| DELETE | `/observability/logs` | Clear logs |
| GET | `/observability/logs/errors` | Error-log file list (`{ files: [{ name, size, modified }] }`) |
| GET (blob) | `/observability/logs/errors/<filename>` | Download one error-log file |
| GET (blob) | `/observability/logs/requests/<id>` | Download one request log |
| GET | `/observability/usage/api-keys` | Client-key usage |

Quota for provider credentials is NOT a single management endpoint in this
UI: it is assembled per credential from credential metadata plus
provider-specific parsers/observations in `src/features/quota/` and
`src/utils/quota/`. Do not invent a `/quota` management endpoint from the
page name.

## Plugins / store / system

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/plugins` | Installed plugins (`plugins_enabled`, `plugins_dir`, `plugins[]` with metadata, menus, config fields, OAuth/quota capability flags) |
| DELETE | `/plugins/<id>` | Delete plugin (result carries `restart_required`) |
| GET | `/plugins/store` | Store catalogue + per-source errors |
| POST | `/plugins/store/<id>/install?source=&version=` | Install (version also in body when given; result carries `restart_required`) |
| GET | `/server/latest-version` | Latest backend version (`latest-version` / `latest_version` / `latest` field — read all three) |

Plugin resource pages themselves are iframes to backend-declared `path`
values from plugin `menus`, resolved against the API base — not management
API calls. Only plugin routes are gated by the `x-cpa-support-plugin`
header.

## Not management API

- `GET /v1/models` — the proxy's OpenAI-compatible endpoint, called
  directly (Axios, not the management client) with a proxy API key, for
  the System page model list. It needs at least one proxy API key.
- Provider upstream quota/usage URLs (Anthropic, Gemini, Kimi, Meta,
  Devin, …) — parsed by provider modules from credential data; they are
  upstream APIs, not the management API, and their shapes are outside
  this contract.

## Legacy probe (only sanctioned v0 touchpoint)

After a v8 login fetch returns 404, the UI probes
`GET /v0/management/config` with the same bearer key, solely to decide
whether to show the "outdated backend" error. It must never supply
application data or act as a login fallback
(`src/services/api/legacyBackendProbe.ts`).
