# Provenance — management-center-webui skill

## Source

- Repo: `https://github.com/router-for-me/Cli-Proxy-API-Management-Center`
- Pinned commit read: `64b4f5aed19b8f791eb21eb9e785ea379ea05b44`
  ("docs(readme): remove APIMart sponsor sections and assets", 2026-10-26).
- Surveyed: 2026-11-01, from a full clone checked out detached at the pinned
  commit (`~/workspace/tmp/mgmt-center-distill/`). The working tree at that
  commit was byte-identical (`diff -r --exclude=.git`, exit 0) to the earlier
  shallow clone at the same commit. No source file was edited; no build, test
  or install script of the repo was run. The full clone was scratch and was
  removed after the survey; re-clone to refresh.
- License: MIT, Copyright (c) 2026 Router-For.ME (`LICENSE`). Rules below are
  re-expressed; no verbatim copy beyond short identifiers (endpoint paths,
  header names, config keys) needed for interoperability.
- Scale at the pinned commit [STATIC]: 1,297 commits, 55 distinct authors
  (`git log --format=%an | sort -u`), 472 files under `src/`, 167 test files
  under `tests/`.

## Sources used, by trust tier

### T1 — Explicit guidance (repo's own instructions)

- `AGENTS.md` — whole file: scope (React frontend, v8 only, no v0 fallback),
  feature layout, single-file deployment constraint, API-client and store
  rules, style/i18n/a11y conventions, testing, security (obfuscation is not
  encryption), Conventional Commits.
- `README.md` / `README_CN.md` — quick start, management-key vs client-key
  distinction, connection settings, remote-access flag, feature table,
  deployment and security notes. Note: README says four UI languages; the
  code at the pinned commit ships six locales — code (T2) wins, see below.

### T2 — Machine-enforced (CI, config, tests)

- `.github/workflows/ci.yml` — Node 24, Bun 1.4.3, `bun install
  --frozen-lockfile`, `bun run verify`.
- `.github/workflows/release.yml` — tags `v*`, `VERSION` from tag,
  `dist/index.html` renamed to `management.html`, release notes from git log.
- `package.json` — Bun 1.4.3, scripts (`dev`/`build`/`test`/`lint`/
  `type-check`/`verify`/`format`), React 19 / TypeScript 6 / Vite 8 /
  Zustand / Axios / React Router 7 / i18next / CodeMirror 6.
- `vite.config.ts` — `vite-plugin-singlefile`, no code splitting, CSS not
  split, `assetsInlineLimit: 100000000`, target `es2020`, `@` alias,
  version injection order (`VERSION` → git tag → package version → `dev`).
- `tsconfig.json` — `strict: true`, `noUnusedLocals`,
  `noUnusedParameters`, `include: ["src"]`.
- `eslint.config.js` — recommended + typescript-eslint, `any` and unused
  vars are warnings; `react-hooks/set-state-in-effect` off by design.
- `tests/` (167 files, `bun:test`) — pure-logic, static-markup and
  source/contract checks; no DOM harness (per `AGENTS.md`).

### T3 — History

- Commit history was available in the full clone (1,297 commits) but was
  NOT mined commit-by-commit for this distillation; no T3 rule in the
  skill rests on a single commit message. The pinned commit's own message
  and the release/CI history above are the only history claims used.
- The CLIProxyAPI backend repo (`../CLIProxyAPI`) was NOT available during
  this survey. Per the source `AGENTS.md`, backend contracts are the source
  of truth; every endpoint in `references/api-contract.md` is therefore
  labelled as "observed in the UI's API layer", not as verified backend
  behaviour.

### T4 — Inferred from code (patterns repeated in code; [NEEDS-MEASUREMENT] where noted)

- Feature layout (`src/features/{dashboard,providers,authFiles,oauth,quota,
  config,logs,plugins}`), shared `src/components|hooks|utils`,
  `src/services/api` domain modules, `src/stores` (Zustand),
  `src/i18n/locales` (6 locales), `src/router` (hash router).
- Single-client discipline, normalise-on-read/serialise-on-write,
  connection-revision guards, full-config TTL cache + in-flight
  deduplication, config-patch diffing, cursor log pagination, plugin
  gating by response header. Each is backed by the file evidence below;
  counts of repetitions were not exhaustively tallied, so T4 items are
  stated as "the pattern in this codebase", not as universal law.

## Evidence map (pinned commit, paths relative to repo root)

| Skill claim | Evidence |
| --- | --- |
| Frontend only, v8 only, no v0 fallback; one legacy probe | `AGENTS.md` scope section; `src/services/api/legacyBackendProbe.ts` (probes `/v0/management/config` only after a v8 404) |
| Feature layout + shared layers | `AGENTS.md` structure section; `src/features/`, `src/pages/`, `src/services/api/`, `src/stores/` listings |
| Prefix `/v8/management`, port 8317, timeout 30 s, header keys | `src/utils/constants.ts` (`MANAGEMENT_API_PREFIX`, `DEFAULT_API_PORT`, `CPA_VERSION_HEADER_KEYS`, `CPA_SUPPORT_PLUGIN_HEADER_KEYS`, `REQUEST_TIMEOUT_MS`, `CACHE_EXPIRY_MS`) |
| Base detection / suffix stripping / scheme default | `src/utils/connection.ts` (`normalizeApiBase`, `computeApiUrl`, `detectApiBaseFromLocation`) |
| Bearer header, 401 logout, version/plugin headers, error normalisation | `src/services/api/client.ts` (request interceptor sets `Authorization: Bearer …`; response interceptor reads version/plugin headers and dispatches `server-version-update` / `server-plugin-support-update`; `handleError` dispatches `unauthorized` on 401) |
| Error envelope (code in `error`, message in `message`, older fallback) | `src/services/api/apiError.ts` (`parseApiErrorResponse`) |
| Connection revision / captured client | `src/services/api/client.ts` (`getConnectionRevision`, `captureConnection`); `src/services/api/configValue.ts` (`guardConfigConnection`) |
| Login = config fetch; remember-password persistence; obfuscated storage | `src/stores/useAuthStore.ts` (`login`, `restoreSession`, `persist`/`partialize`); `src/services/storage/secureStorage.ts`; `src/utils/encryption.ts` (XOR, `enc::v1::`, "not a security boundary") |
| Login form fields | `src/pages/LoginPage.tsx` (server URL, management key, remember-password; detected base prefill) |
| Hash router, ProtectedRoute, route table, plugin gating, legacy redirects | `src/App.tsx` (`createHashRouter`, `ProtectedRoute`, `MainLayout`); `src/router/MainRoutes.tsx`; `src/router/ProtectedRoute.tsx` |
| Nav groups, badges, collapsed rail, floating header actions | `src/components/layout/MainLayout.tsx` (`navGroups`: operate/gateway/observe/control/plugin-pages; Auth Files badge from `authFilesApi.list()`; `sidebarCollapsed`, rail tooltips, `handleRefreshAll`); `src/i18n/locales/en.json` (`nav`, `nav_groups`, `nav_meta`) |
| Breakpoints 768 / 1024, mobile drawer, floating header | `src/styles/variables.scss` (`$breakpoint-mobile: 768px`, `$breakpoint-tablet: 1024px`); `src/styles/layout.scss` mobile `@media` block (sidebar panel `min(280px, …)`, tooltips hidden, mobile menu button) |
| Dashboard verdict + rolling window | `src/features/dashboard/DashboardPage.tsx` (verdict, 10-minute buckets, six-digit number compression); `src/features/dashboard/hooks/useDashboardOverview.ts` |
| Visual + YAML config, diff modal, draft recovery | `src/features/config/ConfigPage.tsx`; `src/features/config/` hooks/components |
| Config patch plan, field-path validation, apply order, list-conflict refusal, rebase | `src/services/api/configPatch.ts` (`buildConfigPatch`, `fieldUrl`, `applyConfigPatch`, `assertConfigListsUnchanged`, `rebaseConfigDraft`, `hasConfigPatchChanges`) |
| Whole-file YAML API | `src/services/api/configFile.ts` (`GET`/`PUT /config.yaml`) |
| Config fetch cache (30 s TTL, dedup, invalidation) | `src/stores/useConfigStore.ts` (`fetchConfig`, `inFlightConfigRequest`, `clearCache`, `updateConfigValue`) |
| Providers as groups, source-index identity | `src/services/api/providers.ts` (`readProviderGroups`, `applyProviderChanges`, group/key helpers); `src/features/providers/descriptors.ts`, `adapters.ts` (per `AGENTS.md`) |
| Auth files endpoints, 10 MB cap, refresh never returned | `src/services/api/authFiles.ts` (`authFilesApi`: list/status/fields/refresh/cooldown/upload/delete/download/models); `src/utils/constants.ts` (`MAX_AUTH_FILE_SIZE`) |
| OAuth attempts, 3 s poll, user code, manual callback, plugin providers | `src/features/oauth/hooks/useOAuthFlows.ts` (`POLL_INTERVAL_MS = 3000`, per-provider attempt state); `src/services/api/oauth.ts` (`oauthApi`: auth-url/status/session/callback); `src/features/oauth/providers.ts` |
| Quota per credential, session isolation, reset model | `src/features/quota/` (page, logic, providers, reset schedule); `src/utils/quota/` (identity, parsers, constants) |
| Client-key usage endpoint | `src/services/api/apiKeyUsage.ts` (`GET /observability/usage/api-keys`, 15 s) |
| Logs cursor pagination, filters, fullscreen, downloads, file-logging gate | `src/services/api/logs.ts` (`fetchLogs` with `after`/`cursor`, `next-cursor`/`cursor-reset`, error-log files, blob downloads, 60 s timeout); `src/features/logs/LogsPage.tsx` (search, level filter, follow, fullscreen, clear, download) |
| Plugins list/config/store, trust gate, iframe resources | `src/services/api/plugins.ts` (`pluginsApi`, `pluginStoreApi`); `src/features/plugins/pluginResources.ts` (`isOfficialRepository`, `OFFICIAL_PLUGIN_REPO_PREFIX`, `resolvePluginAssetURL`); `src/features/plugins/PluginResourcePage.tsx` (iframe, `no-referrer`) |
| Update check, models list, System page | `src/pages/SystemPage.tsx` (`versionApi.checkLatest`, `/v1/models` via models store); `src/services/api/version.ts` (`GET /server/latest-version`); `src/services/api/models.ts` (`fetchModels` to `/v1/models`) |
| Six locales, zh-CN fallback | `src/i18n/index.ts` (resources + `fallbackLng: 'zh-CN'`); `src/i18n/locales/` (en, ko, ru, vi, zh-CN, zh-TW); `src/utils/constants.ts` (`LANGUAGE_ORDER`) |
| Themes auto/white/light/dark, motion tokens | `src/components/layout/MainLayout.tsx` (`THEME_CARDS`); `src/styles/themes.scss`; `src/hooks/motion.ts` (per `AGENTS.md`) |
| Single-file build + release | `vite.config.ts`; `.github/workflows/release.yml`; `README.md` deployment section |

## Boss screenshot evidence (2026-11-01, not in the repo)

Boss ran the Management Center on a phone at `127.0.0.1:8317` (mobile view)
and described: login page (server URL + management key + remember); collapsible
sidebar grouped OPERATE / GATEWAY / OBSERVE / CONTROL; floating top bar
(refresh / language / theme / logout); Logs Viewer with search, level filter,
live follow, download, clear, fullscreen. Every item in that description was
checked against the pinned source and matches it, with one exception: the
screenshots' "Routing" entry under GATEWAY has no standalone route at the
pinned commit — routing strategy is a config concern. The skill records the
pinned-commit state and flags the discrepancy here rather than inventing a
Routing page. No screenshot image file was supplied in the chat; no pixel
detail beyond Boss's description is claimed.

## REPO-ONLY — excluded from the generic skill (kept as examples at most)

- Provider list and per-provider quota/OAuth parsers for CLIProxyAPI's
  providers (Gemini, Codex, Claude, Vertex, OpenAI-compatible, Kimi, xAI,
  Antigravity, Devin, Meta, plugin providers). Pattern ported; list not.
- Sponsor/Quick Start special-casing (`apikeyFun`, sponsor cards,
  `src/features/providers/sponsor*`, `src/features/config/sponsors.ts`).
- The `management.allow-remote` flag name and v7→v8 migration notes: backend
  specifics, restated only where the UI must surface them.
- Chinese working comments in code: not user copy.
- `logo.jpg` / inline logo asset and the exact theme palette: branding, not
  pattern. (Theme *mechanism* — tokens, preview cards — is ported; token
  *values* are additionally documented in `references/ui-style.md` per the
  2026-11-01 style-guide extension below, for reproduction of the look.)

## Unverified / [NEEDS-MEASUREMENT]

- Backend behaviour behind every management endpoint (the CLIProxyAPI
  checkout was unavailable). Endpoint shapes are UI-layer observations only.
- Whether the live instance Boss screenshotted is newer than the pinned
  commit (its HEAD in the full clone was ahead of the pin). The "Routing"
  discrepancy above may be a newer-build difference; re-pin before
  implementing against a newer UI.
- No build, test or browser run was performed in this session (read-only
  distillation; running the repo's scripts was out of scope). `bun run
  verify` passing at the pinned commit is a T2 claim from CI config, not
  a measurement made here.
- Full A/B verification of the skill (per `distill-repo-skill` PHA 5) was
  NOT run: this skill is descriptive/architectural, and no held-out tasks
  were executed. Status: **UNVERIFIED** for A/B purposes. Static checks
  (line budget, frontmatter, secret scan, citation spot-check) were run
  and are reported in the session summary.
- Castctl mapping in Appendix A of `SKILL.md` was not re-verified against
  castctl main in this session; it is labelled as such in the skill.
- The Muse (Meta) device-code login visible in the Management Center was
  explicitly excluded from this skill by Boss correction (2026-11-01):
  it is for paid API / Muse Code accounts, not the personal Muse agent
  castctl drives. No research note on it was written, and no claim about
  its flow is made here.

## UI/UX style-guide extension (2026-11-01)

Boss follow-up: the skill under-covered UI/UX. `references/ui-style.md`
was added as a dedicated style guide, extracted from the same pinned
commit (`64b4f5aed19b8f791eb21eb9e785ea379ea05b44`), covering design
tokens (light + dark + white), typography as actually found (no invented
scale), spacing/radii/shadows/borders/z-index, layout grid and
breakpoints, sidebar drawer and floating top bar, cards/lists/badges/
buttons/inputs/toggles/modals/toasts/empty and loading/error states, the
icon set, motion and transitions, the header background as actually
implemented (gradient + blur overlay, no literal pixel pattern), mobile
touch targets as actually stated (no global rule), theme switching,
i18n text handling and accessibility — with ready-to-copy CSS variables
and framework-agnostic HTML+CSS skeletons using only traced values.

Method: four parallel read-only research scouts (tokens/themes,
layout/shell, components/states, motion/icons/a11y/i18n), each
re-verifying `git rev-parse HEAD` in the shallow clone at the pinned
commit before reading, each writing a separate evidence file with
`[STATIC]` file:line citations or `[NEEDS-MEASUREMENT]` flags under
`~/workspace/tmp/mgmt-ui-style/`; one writer (the coordinator) composed
`ui-style.md` from those four files; an independent verifier step follows
(see Unverified below). No source file was edited; no build/test/install script was run;
no secrets were printed. The shallow clone
`~/workspace/tmp/mgmt-center-research/` was re-verified at the same HEAD,
clean, on 2026-11-01.

Budget: the original ≤600-line total budget for the skill is superseded
for this explicitly requested dedicated guide. The binding limits are
`SKILL.md` ≤300 lines (146 at creation, plus a lean pointer in §7) and a
self-contained `references/ui-style.md`. MIT attribution: the guide
re-expresses the style; short identifiers/values are quoted for
interoperability, with the upstream copyright noted in the guide header.

Style evidence (pinned commit, paths relative to repo root), in addition
to the evidence map above:

| Style claim | Evidence |
| --- | --- |
| Theme blocks, glass + motion tokens, light-vs-white diff, auto→white, unused tokens | `src/styles/themes.scss`; `src/styles/variables.scss`; `src/stores/useThemeStore.ts`; `src/utils/constants.ts:33` (`STORAGE_KEY_THEME`); `src/types/common.ts:5` |
| Shell grid, sidebar widths, floating pills, drawer, backdrop, rail tooltips, gradient header | `src/styles/layout.scss` (1,018 lines); `src/styles/mixins.scss`; `src/components/layout/MainLayout.tsx`; `src/components/common/PageTransition.tsx` + `.scss` |
| Buttons, cards, lists, badges, inputs, Select, toggles, checkboxes, modals, sheets, tables, skeletons, collapsibles, toasts, empty/loading/error | `src/styles/components.scss`; `src/components/ui/Button.tsx`, `Card.tsx`, `Input.tsx`, `Select.tsx` + `Select.module.scss`, `ToggleSwitch.tsx` + `ToggleSwitch.module.scss`, `SelectionCheckbox.tsx` + `SelectionCheckbox.module.scss`, `Modal.tsx`, `src/components/ui/Sheet/Sheet.tsx` + `Sheet.module.scss`, `src/components/ui/Table/Table.tsx` + `Table.module.scss`, `Skeleton.tsx` + `Skeleton.module.scss`, `src/components/ui/Collapsible/Collapsible.tsx` + `Collapsible.module.scss`; `src/components/common/{ConfirmationModal,NotificationContainer}.tsx` + modules; `src/features/logs/LogsPage.module.scss` (toolbar only) |
| Motion tokens, reveal/count-up, page transitions, reduced motion | `src/styles/themes.scss:88-92`; `src/hooks/motion.ts`; `src/components/common/PageTransition.tsx` |
| Icon convention + 52-export inventory | `src/components/ui/icons.tsx` |
| Focus/keyboard/ARIA/live regions, no skip link | `src/styles/layout.scss` (focus rings); `src/styles/components.scss`; `src/components/ui/{Modal,Sheet,Select,ToggleSwitch,SelectionCheckbox,Collapsible}.tsx`; `src/components/ui/scrollLock.ts`; `src/components/common/NotificationContainer.tsx` |
| i18n setup, fallback, formatting helpers | `src/i18n/index.ts`; `src/i18n/locales/`; `src/utils/{constants,language,format}.ts`; `src/stores/useLanguageStore.ts`; `src/App.tsx:51-54` |

Unverified for the style guide (carried from the scouts; see
`ui-style.md` §14): no browser run — rendered `--header-height`, the
`#0d0c0a` gradient stop in light/white themes, modal/spinner reduced-
motion behaviour, and Select-vs-Sheet-vs-Modal stacking are unmeasured;
no A/B verification per `distill-repo-skill` PHA 5 was run for the guide
either. Verifier loop 1 (2026-11-01): **FAIL** — 2 blocking findings
(B1 focus-ring mapping in §13.1, B2 modal shadow token in §§3.3/7.6);
both fixed in the writer pass of loop 1, plus nits N1–N8. Delta
re-review loop 2 (2026-11-01): **PASS** — no blocking findings remain;
2 new non-blocking nits (D1 nav-icon citation range, D2 scrollLock
citation) were fixed directly by the coordinator against source and are
noted here, not re-verified by a third loop.

## Refresh

To refresh: re-clone (full, no `--depth`), check out the new pinned commit,
re-run the evidence map above, and update the pinned hash, the locale count
and the endpoint table. If the backend major version changes, treat the
skill as stale until the new contract is re-read.
