Status: approved as-is by Boss 2026-10-24; PR #3 merged with only the 12 keeps below (298 other ECC skills removed from the branch).

# ECC Curation — proposed keep/drop for PR #3

Status: PROPOSED, awaiting Boss review. Nothing in this doc merges anything.
PR #3 (thoitiettxl-cyber/custom-skills) stays OPEN and unmerged until Boss approves a keep set.
Scope: the 310 ECC skills on branch `feat/ecc-skills` (source affaan-m/ECC, MIT).
Method: each skill's H1 was scored against the profile below; for every keep candidate and
every ambiguous H1, the SKILL.md body was read to check for macOS-only tooling and required keys/tools.
Rule applied: strict, no 'just in case'. If unsure, DROP. A keep must cite a specific profile repo or workflow.
Note: two kept skills (automation-audit-ops, terminal-ops) name other ECC skills in their
'Skill Stack' sections (workspace-surface-audit, github-ops, verification-loop, tdd-workflow,
security-review, knowledge-ops). Those referenced skills are themselves DROPPED here; the keep is for
the core workflow of the kept skill only, not for its ECC stack.

## Profile (facts with repo evidence)

- Agent infra, pushed 2026-10-24 (thoitiettxl-cyber): muse-heal — self-healing VM toolkit
  (heal check/fix, heal-agents orphaned-work detector, jlog journal, hourly heal cron; Shell).
- Agent infra, pushed 2026-10-24: custom-skills — Muse playbooks (31 live skills).
- Agent infra, pushed 2026-10-24: muse-mcp — MCP client CLI (Node, registry in servers.json, OAuth PKCE).
- Agent infra, pushed 2026-10-24: lemo-opuscar (fork) — 59 code-only film styles plus the local
  hybrid/ workflow (ffmpeg normalize/make_card/assemble/mix_voice/colormatch, 1920x1080, 24 fps).
- muse-cli (fork, pushed 2026-10-23): terminal client for the Muse agent, gateway protocol, JSON
  output, scriptable/cron-friendly; plus pi-muse (Pi provider for Muse).
- Sales apps, pushed 2026-10-24: shopthaothao — React 19 + TypeScript + Vite, GitHub Pages,
  Cloudflare Worker API on KV (cloned from KSHT); giaban — KSHT original (TypeScript, AI Studio app);
  khosihuythao-landingpage (TypeScript).
- Android, still active: SpoofX (pushed 2026-10-22; LSPosed module, Kotlin/Java/C++, libxposed API 102);
  E-muse (pushed 2026-10-06; Android phone as MCP server via Cloudflare Tunnel); plus Zygisk/Xposed/
  KernelSU/Android app repos.
- From-scratch benchmarks via a paired Pi device: mini-sql-db (TS: SQL parser, B-tree, MVCC, WAL),
  mini-git (Python, complete, 37 tests), caro-game, collab-sheet (realtime spreadsheet), plus raft-kv,
  gameboy-emu, tiny-lang, crdt-editor in progress. Rules: English README, honest pass/fail, frequent
  pushes, tests per component, no ready-made core libraries.
- Recurring work with Mea: muse-cli ops, heal install/check/cron, git/PR/merge work (gh), film
  rendering (lemo-opuscar + hybrid), native media generation, web search + MCP tools.
- Keys present on this VM (only): CONTEXT7, EXA, FIRECRAWL, REDIS, TYPESAFE. Absent, among others:
  FAL_KEY, VIDEO_DB_API_KEY, NUTRIENT_API_KEY, GEMINI_API_KEY, OPENAI_API_KEY, ANTHROPIC_API_KEY,
  ELEVENLABS_API_KEY, STRIPE_API_KEY, NCBI_API_KEY, USPTO_API_KEY.
- Already covered, never duplicated: existing custom skills (api-design, apk-reverse, cli-creator,
  code-review, codebase-design, codemode, commit, diagnosing-bugs, domain-modeling, ghidra, github,
  grill-with-docs, grilling, heal, improve-codebase-architecture, lemo-opuscar, librarian,
  linkage-checks, mcp-builder, mcp-client, native-web-search, search-playbook, security-audit,
  subagent-orchestration, summarize, tdd, technical-scoping-workflow, tmux, update-changelog, uv,
  verify-before-claiming) and built-in skills (documents, email-management, scheduling, shopping,
  groceries, flight/hotel/trip, messaging, music-discovery, social-publishing, and the rest of
  /opt/muse/skills).

## Proposed KEEP list (12 skills)

| Skill | One-line reason (profile-tied) |
|---|---|
| `agent-runtime-gateway-smoke-test` | muse-cli gateway protocol and E-muse (Android as MCP server via Cloudflare Tunnel): verify a local agent API + gateway tunnel + remote callback end to end, then restore the app connection. |
| `android-clean-architecture` | SpoofX (LSPosed module, Kotlin/Java/C++, pushed 2026-10-22): module boundaries, UseCase/Repository layers, data-layer design. |
| `automation-audit-ops` | muse-heal work: audit live jobs, hooks, connectors, MCP servers, and wrappers for breakage/redundancy before fixing anything. |
| `documentation-lookup` | Recurring search/MCP work with CONTEXT7 key present: current library/framework docs via Context7 instead of training data. |
| `error-handling` | TypeScript bench projects (mini-sql-db, tiny-lang) and TypeScript sales apps: error types, retries, circuit breakers, user-facing messages. |
| `kotlin-patterns` | SpoofX (Kotlin, LSPosed module): idiomatic Kotlin, null safety, sealed hierarchies, coroutines/Flow, Gradle Kotlin DSL. |
| `mcp-server-patterns` | muse-mcp (Node MCP client CLI, registry/OAuth PKCE) and E-muse (Android phone as MCP server via Cloudflare Tunnel): building/debugging MCP servers, tools, resources, transports. |
| `python-patterns` | mini-git (Python 3 stdlib only, complete, 37 tests) and bench Python work: idiomatic Python structure, typing, PEP 8. |
| `react-patterns` | shopthaothao (React 19 + TypeScript + Vite): idiomatic function components, hooks, state shape, TSX review. |
| `safety-guard` | muse-heal production VM changes and the paired-Pi two-writer rule: restrict edit scope during autonomous work, deploys, and migrations. |
| `terminal-ops` | Daily heal/gh/muse-cli ops: run a command, check a repo, debug CI, push a narrow fix with exact proof of what was executed and verified. |
| `vite-patterns` | shopthaothao (React 19 + TypeScript + Vite, GitHub Pages): Vite config, plugins, HMR, env variables, proxy, build optimization. |

## Drop summary (298 dropped)

| Drop reason category | Count |
|---|---|
| Duplicate of an existing custom or built-in skill (overlap named in the reason) | 82 |
| Domain or stack Boss does not work in | 121 |
| No clear use in the profile (generic skill, no evidenced work item) | 36 |
| Generic process/meta skill already covered by an existing playbook or workflow | 27 |
| Wrong platform (macOS/iOS/Windows/Claude Code-only) | 12 |
| ECC self-management (curation is this one-off task, not an ongoing ECC install) | 11 |
| Needs a key/tool Boss lacks | 9 |
| **Total dropped** | **298** |

## Genuinely torn (dropped, but Boss may disagree)

- `canary-watch` — For: shopthaothao is deployed (GitHub Pages + Cloudflare Worker), so post-release
  URL checks fit. Against: no deployed-URL monitoring is evidenced, and the heal cron already covers
  scheduled checks.
- `cpp-coding-standards` — For: SpoofX has C++ native parts. Against: no C++ authoring work is
  evidenced, and apk-reverse/ghidra already cover Android native work.
- `mcp-dependency-review` — For: muse-mcp registry work. Against: Boss's registry is servers.json,
  not per-repo .mcp.json, and mcp-client + kept mcp-server-patterns already cover MCP work.

## Full table — all 310 skills (12 keep, 298 drop)

| Skill | Keep/Drop | Reason |
|---|---|---|
| `accessibility` | DROP | No accessibility-audit work evidenced in any repo or workflow; not a current work item. |
| `agent-architecture-audit` | DROP | Overlaps custom diagnosing-bugs (diagnosing a failing agent layer). |
| `agent-eval` | DROP | Choosing between coding agents by measured pass rate; no agent-comparison work evidenced. |
| `agent-harness-construction` | DROP | Agent tool-set/action-space design meta-work; no harness-definition project in profile. |
| `agent-introspection-debugging` | DROP | Overlaps custom diagnosing-bugs (reproducible diagnosis of a failed run). |
| `agent-payment-x402` | DROP | Agent self-payment with wallets/budgets; no agent-payment work in profile. |
| `agent-runtime-gateway-smoke-test` | KEEP | muse-cli gateway protocol and E-muse (Android as MCP server via Cloudflare Tunnel): verify a local agent API + gateway tunnel + remote callback end to end, then restore the app connection. |
| `agent-security-hardening` | DROP | Multi-tenant agent deployments; Boss runs a single VM and a paired device, not a fleet. |
| `agent-self-evaluation` | DROP | Post-task self-evaluation ritual; verify-before-claiming already gates completion claims. |
| `agent-sort` | DROP | ECC trimming skill; this one-off curation replaces it, not an ongoing ECC install. |
| `agentic-engineering` | DROP | Agent-led engineering process; subagent-orchestration already covers delegation. |
| `agentic-os` | DROP | Persistent multi-agent system on Claude Code (wrong platform) with its own memory/scheduling. |
| `ai-first-engineering` | DROP | Team process for agent-written codebases; Boss works solo with Mea, no team process. |
| `ai-regression-testing` | DROP | Model-wrote-and-reviewed regression coverage; bench tests are component tests, not agent eval. |
| `android-clean-architecture` | KEEP | SpoofX (LSPosed module, Kotlin/Java/C++, pushed 2026-10-22): module boundaries, UseCase/Repository layers, data-layer design. |
| `angular-developer` | DROP | Angular is not used in any profile repo. |
| `api-connector-builder` | DROP | Overlaps built-in custom-connector-setup (building a connector/CLI from API docs). |
| `architecture-decision-records` | DROP | Overlaps custom domain-modeling (recording ADRs). |
| `article-writing` | DROP | Long-form polished writing; no article-writing work in profile. |
| `automation-audit-ops` | KEEP | muse-heal work: audit live jobs, hooks, connectors, MCP servers, and wrappers for breakage/redundancy before fixing anything. |
| `autonomous-agent-harness` | DROP | Autonomous agent harness meta-work; subagent-orchestration already covers delegation. |
| `autonomous-loops` | DROP | Claude Code autonomous-loop architectures; subagent-orchestration covers Boss's loops. |
| `backend-patterns` | DROP | Express/Next.js API routes; sales API is a Cloudflare Worker and bench backends are from-scratch, not Express/Next. |
| `benchmark` | DROP | Page-speed benchmarking; Boss's benchmarks are from-scratch implementations, not page speed. |
| `benchmark-methodology` | DROP | Competitor benchmarking matrices; not Boss's implementation-benchmark work. |
| `benchmark-optimization-loop` | DROP | Overlaps custom diagnosing-bugs (measured speed-up by repeated tests). |
| `bengali-nlp` | DROP | Bengali NLP; language/domain not worked in. |
| `blender-motion-state-inspection` | DROP | Blender character/rig inspection; lemo films are code-rendered, not Blender. |
| `blueprint` | DROP | Multi-PR roadmap planning meta-work; plan files + subagent-orchestration already cover it. |
| `brand-discovery` | DROP | Brand repositioning; no branding work in profile. |
| `brand-voice` | DROP | Brand voice consistency; no branding work in profile. |
| `brownfield-retrospective` | DROP | ECC mid-project retrospective; one-off meta, not a recurring workflow. |
| `browser-qa` | DROP | Staging/preview frontend QA; no staging QA workflow evidenced for shopthaothao. |
| `bun-runtime` | DROP | Bun runtime; Boss's runtimes are Node (muse-mcp, lemo) and Python, not Bun. |
| `canary-watch` | DROP | Post-release deployed-URL monitoring; no deployed-URL monitoring evidenced (heal cron covers scheduled checks). See Torn list. |
| `carrier-relationship-management` | DROP | Freight carrier RFPs/rates; freight is not worked in. |
| `change-impact` | DROP | Overlaps custom code-review + linkage-checks (evidence-backed impact analysis). |
| `cisco-ios-patterns` | DROP | Cisco IOS configuration; network-device work not in profile. |
| `ck` | DROP | Overlaps muse-heal jlog journal (session state, next steps, resume). |
| `claude-devfleet` | DROP | Overlaps custom subagent-orchestration (parallel agents across worktrees). |
| `click-path-audit` | DROP | Broken-button debugging after clean systematic debugging; no such case evidenced. |
| `clickhouse-io` | DROP | ClickHouse schemas/queries; ClickHouse not used. |
| `code-tour` | DROP | Overlaps custom domain-modeling + grill-with-docs (explaining a subsystem). |
| `codebase-onboarding` | DROP | Overlaps custom domain-modeling + grill-with-docs (project onboarding). |
| `codehealth-mcp` | DROP | Overlaps custom code-review (code-quality review before commit/PR). |
| `coding-standards` | DROP | Overlaps custom code-review + codebase-design (naming/quality review). |
| `competitive-platform-analysis` | DROP | Competitor landscape scoping; market/competitor analysis not worked in. |
| `competitive-report-structure` | DROP | Competitive reports for leadership; not worked in. |
| `compose-multiplatform-patterns` | DROP | Compose/KMP UI; SpoofX is native Android, no KMP evidenced. |
| `config-gc` | DROP | Overlaps custom heal skill (config audit, bloat review). |
| `configure-ecc` | DROP | ECC install/update/repair management; one-off curation, not an ongoing ECC install. |
| `connections-optimizer` | DROP | Social-graph following-list cleanup; no social-graph work. |
| `content-engine` | DROP | Social posts/threads/content calendars; no social content work. |
| `content-hash-cache-pattern` | DROP | Content-hash caching pattern; no repeated-processing bottleneck evidenced. |
| `context-and-decisions` | DROP | Overlaps custom domain-modeling (domain terms vs architecture decisions). |
| `context-budget` | DROP | Routes to Codex/Claude Code context meters; wrong platform for Muse. |
| `continuous-agent-loop` | DROP | Self-checking agent loop meta-work; subagent-orchestration covers loops. |
| `continuous-learning` | DROP | Deprecated v1 lesson extractor; MEMORY.md workflow already captures lessons. |
| `continuous-learning-v2` | DROP | Hook-based lesson capture for Claude Code; MEMORY.md workflow covers lessons on Muse. |
| `contract-first` | DROP | Overlaps custom api-design (API/event schema evolution without drift). |
| `conventional-commit-review` | DROP | Overlaps custom commit skill (Conventional Commits message drafting). |
| `cost-aware-llm-pipeline` | DROP | LLM spend routing across model tiers; no LLM-spend management work evidenced. |
| `cost-tracking` | DROP | Overlaps built-in subscription-status (plan/usage/cost questions). |
| `council` | DROP | Overlaps custom grilling (structured disagreement before choosing). |
| `council-multi-model` | DROP | Overlaps custom grilling (second-model challenge to a synthesis). |
| `counterparty-channel-discipline` | DROP | Agent speech rules in group chats with outsiders; no group-chat agent work. |
| `cpp-coding-standards` | DROP | C++ authoring standards; SpoofX has C++ parts but no C++ authoring work evidenced (apk-reverse/ghidra cover native Android). See Torn list. |
| `cpp-testing` | DROP | GoogleTest/CTest work; no C++ test work evidenced (bench tests are TS/Python). |
| `crosspost` | DROP | Overlaps built-in social-publishing (cross-platform distribution). |
| `csharp-testing` | DROP | C#/.NET xUnit tests; .NET not used. |
| `customer-billing-ops` | DROP | Customer billing/subscription operations; no billing-ops work evidenced. |
| `customs-trade-compliance` | DROP | Customs classification/audits; trade compliance not worked in. |
| `dart-flutter-patterns` | DROP | Dart/Flutter; mobile work is native Android (Kotlin), not Flutter. |
| `dashboard-builder` | DROP | Metrics dashboards; no dashboard-building work evidenced. |
| `data-scraper-agent` | DROP | Overlaps custom search-playbook (public-data research); no scraper work. |
| `data-throughput-accelerator` | DROP | Pipeline/backfill speed-up; no data-pipeline work evidenced. |
| `database-migrations` | DROP | Schema migrations with rollback/zero-downtime; bench DB is a from-scratch B-tree, not migrations. |
| `deep-research` | DROP | Overlaps custom search-playbook + native-web-search (deep research). |
| `deepseek-harness-setup` | DROP | ECC on DeepSeek Harness; wrong platform, ECC self-management. |
| `defi-amm-security` | DROP | Solidity AMM/liquidity auditing; DeFi not worked in. |
| `delivery-gate` | DROP | Mechanical done-gate; AGENTS.md workflow gates already block premature done claims. |
| `deployment-patterns` | DROP | Generic CI/CD/containerization; deploys are gh pushes + GitHub Pages/Worker, no CI/CD pipeline work. |
| `design-system` | DROP | Design-system creation/audit; no design-system work evidenced. |
| `dev-team` | DROP | Overlaps custom grilling (multi-role perspective). |
| `django-celery` | DROP | Django background jobs; Django not used. |
| `django-patterns` | DROP | Django/DRF; Django not used. |
| `django-security` | DROP | Django auth/input review; Django not used. |
| `django-tdd` | DROP | Overlaps custom tdd (Django test-first; Django not used). |
| `django-verification` | DROP | Overlaps custom verify-before-claiming (Django PR readiness; Django not used). |
| `dmux-workflows` | DROP | Overlaps custom subagent-orchestration (parallel agent sessions). |
| `docker-patterns` | DROP | Dockerfiles/Compose; Docker not used in profile repos. |
| `docs-governance` | DROP | Overlaps custom domain-modeling (documentation governance/integrity). |
| `documentation-lookup` | KEEP | Recurring search/MCP work with CONTEXT7 key present: current library/framework docs via Context7 instead of training data. |
| `dotnet-patterns` | DROP | C#/.NET conventions; .NET not used. |
| `dynamic-workflow-mode` | DROP | Task-local harness/eval-gate extraction meta-work. |
| `e2e-testing` | DROP | Playwright E2E tests; no Playwright work evidenced. |
| `ecc-guide` | DROP | ECC documentation/install guide; ECC self-management. |
| `ecc-recipes` | DROP | ECC command-sequence recipes; ECC self-management. |
| `ecc-tools-cost-audit` | DROP | Cost spikes in the ECC Tools repo; not Boss's repo. |
| `email-ops` | DROP | Overlaps built-in email-management (organize/draft/send/prove delivery). |
| `energy-procurement` | DROP | Energy tariffs/PPAs/budgets; energy not worked in. |
| `enterprise-agent-ops` | DROP | Production agent fleets on PM2/systemd/containers; Boss runs a single-VM heal cron, not a fleet. |
| `error-handling` | KEEP | TypeScript bench projects (mini-sql-db, tiny-lang) and TypeScript sales apps: error types, retries, circuit breakers, user-facing messages. |
| `esign-field-placement` | DROP | E-signature envelope field placement; legal-doc automation not worked in. |
| `eval-harness` | DROP | Agent-task pass/fail criteria; bench tests are component tests, not agent eval. |
| `evm-token-decimals` | DROP | EVM token decimals; crypto not worked in. |
| `exa-search` | DROP | Overlaps custom search-playbook + native-web-search, which already route to Exa via MCP (EXA key present but workflow covered). |
| `fal-ai-media` | DROP | Needs FAL_KEY for live media generation; key absent, and native media generation already covers this. |
| `fastapi-patterns` | DROP | FastAPI; FastAPI not used. |
| `finance-billing-ops` | DROP | Sales/billing snapshots; no billing-analysis work evidenced. |
| `flox-environments` | DROP | Flox toolchains; heal pins tools, flox not used. |
| `flutter-dart-code-review` | DROP | Flutter/Dart review; Flutter not used. |
| `foundation-models-on-device` | DROP | Apple FoundationModels on iOS 26; Boss is Android/Linux. |
| `frontend-a11y` | DROP | Form/modal a11y fixes; no accessibility-fix work evidenced. |
| `frontend-design-direction` | DROP | Product-specific web design judgment; no design-direction work evidenced (films use lemo styles). |
| `frontend-patterns` | DROP | Overlaps kept react-patterns for React components; Next.js parts not used (shopthaothao is Vite, not Next). |
| `frontend-slides` | DROP | Overlaps built-in documents (presentation building); no slide work evidenced. |
| `fsharp-testing` | DROP | F# tests; F# not used. |
| `gan-style-harness` | DROP | Generator/evaluator autonomous loop; subagent-orchestration covers iteration. |
| `gateguard` | DROP | GateGuard hook for Claude Code; hook tooling, not Muse. |
| `generating-python-installer` | DROP | Minimal Windows installer shipping; Boss is Linux VM/Android, not Windows. |
| `git-workflow` | DROP | Overlaps custom commit + github skills (branching, merge vs rebase, conflicts). |
| `github-ops` | DROP | Overlaps custom github skill (issues/PRs/CI/releases via gh). |
| `golang-patterns` | DROP | Go idioms; no active Go code (raft-kv not started, listed as TS/Go option only). |
| `golang-testing` | DROP | Go tests; no active Go code. |
| `google-workspace-ops` | DROP | Overlaps built-in Google connectors (Workspace asset find/edit/migrate). |
| `growth-log` | DROP | Overlaps MEMORY.md lessons workflow (post-task learning capture). |
| `healthcare-cdss-patterns` | DROP | Clinical decision support; healthcare not worked in. |
| `healthcare-emr-patterns` | DROP | EMR/EHR features; healthcare not worked in. |
| `healthcare-eval-harness` | DROP | Healthcare patient-safety gating; healthcare not worked in. |
| `healthcare-phi-compliance` | DROP | HIPAA/GDPR PHI controls; healthcare not worked in. |
| `hermes-imports` | DROP | Preparing Hermes workflows for public ECC reuse; ECC self-management. |
| `hexagonal-architecture` | DROP | Overlaps custom codebase-design (Ports/Adapters module design). |
| `hipaa-compliance` | DROP | HIPAA compliance framing; healthcare not worked in. |
| `homelab-network-readiness` | DROP | Home-network VLAN/DHCP/VPN planning; Pi is a dev device, not homelab network work. |
| `homelab-network-setup` | DROP | Home/homelab gateway/switch/AP setup; not Boss's work. |
| `homelab-pihole-dns` | DROP | Pi-hole DNS; Pi-hole not used. |
| `homelab-vlan-segmentation` | DROP | UniFi/pfSense VLAN segmentation; not Boss's work. |
| `homelab-wireguard-vpn` | DROP | WireGuard home VPN; remote access is the paired-device bridge + Cloudflare Tunnel, not WireGuard. |
| `hookify-rules` | DROP | Hookify rules for Claude Code; hook tooling, not Muse. |
| `i18n-sync` | DROP | Translation key sync; no i18n work evidenced. |
| `inherit-legacy-style` | DROP | Legacy codebase onboarding; bench work is greenfield from-scratch, not legacy. |
| `intent-driven-development` | DROP | Overlaps custom grilling (clarify feature, acceptance criteria, de-risking). |
| `inventory-demand-planning` | DROP | Demand forecasting/safety stock; manufacturing/inventory not worked in. |
| `investor-materials` | DROP | Investor documents/projections; fundraising not worked in. |
| `investor-outreach` | DROP | Angel/VC outreach messaging; fundraising not worked in. |
| `ios-icon-gen` | DROP | macOS-only sips conversion for iOS icons; Boss is Android/Linux. |
| `iterative-retrieval` | DROP | Overlaps custom subagent-orchestration (subagent context refinement). |
| `ito-baskets` | DROP | Itô prediction-market baskets; no prediction-market work. |
| `ito-compute` | DROP | Itô GPU compute bookings; no Itô bookings. |
| `ito-inference` | DROP | Itô model serving on a compute booking; no Itô bookings. |
| `ito-training` | DROP | Itô ML training on a compute booking; no Itô bookings. |
| `java-coding-standards` | DROP | Overlaps kept kotlin-patterns for Android language work; Java is secondary in SpoofX with no Java-authoring evidence. |
| `jira-integration` | DROP | Jira tickets; Jira not used. |
| `jpa-patterns` | DROP | JPA/Hibernate entities; JPA not used. |
| `knowledge-ops` | DROP | Overlaps built-in knowledge-organization + MEMORY.md (save/organize/search knowledge). |
| `kotlin-coroutines-flows` | DROP | Coroutines/Flow debugging; no coroutines-specific work evidenced (kotlin-patterns kept covers Kotlin generally). |
| `kotlin-exposed-patterns` | DROP | Exposed ORM; Exposed not used. |
| `kotlin-ktor-patterns` | DROP | Ktor server; Kotlin work is Android (SpoofX), not Ktor servers. |
| `kotlin-patterns` | KEEP | SpoofX (Kotlin, LSPosed module): idiomatic Kotlin, null safety, sealed hierarchies, coroutines/Flow, Gradle Kotlin DSL. |
| `kotlin-testing` | DROP | Kotest/MockK tests; no Kotlin test work evidenced (bench test rule is covered by custom tdd). |
| `kubernetes-patterns` | DROP | Kubernetes manifests/RBAC/autoscaling; Kubernetes not used. |
| `laravel-patterns` | DROP | Laravel; Laravel not used. |
| `laravel-plugin-discovery` | DROP | Laravel plugin health; Laravel not used. |
| `laravel-security` | DROP | Laravel auth/safety review; Laravel not used. |
| `laravel-tdd` | DROP | Overlaps custom tdd (Laravel test-first; Laravel not used). |
| `laravel-verification` | DROP | Overlaps custom verify-before-claiming (Laravel pre-merge checks; Laravel not used). |
| `latency-critical-systems` | DROP | Overlaps custom diagnosing-bugs (p95/latency performance work). |
| `lead-intelligence` | DROP | High-value contact outreach; sales outreach not worked in. |
| `liquid-glass-design` | DROP | iOS 26 Liquid Glass UI; Boss is Android. |
| `living-docs-governance` | DROP | Overlaps custom domain-modeling (long-lived docs governance). |
| `llm-trading-agent-security` | DROP | Trading-agent wallet/transaction authority; trading not worked in. |
| `logistics-exception-management` | DROP | Shipping exceptions/freight claims; logistics not worked in. |
| `loop-design-check` | DROP | Agent-loop design checking; subagent-orchestration covers loops. |
| `mailtrap-email-integration` | DROP | Email-sending feature work with Mailtrap; no such work evidenced. |
| `make-interfaces-feel-better` | DROP | Generic UI spacing/typography polish; no UI-polish work item evidenced. |
| `manim-video` | DROP | Overlaps custom lemo-opuscar (code-rendered films); Manim not used. |
| `market-research` | DROP | Market sizing/competitor research; market research not worked in. |
| `marketing-campaign` | DROP | Multi-channel product launches/ad copy; marketing not worked in. |
| `master-agreement-generator` | DROP | Legal agreement drafting; legal work not worked in. |
| `mcp-dependency-review` | DROP | Overlaps custom mcp-client + kept mcp-server-patterns; Boss's registry is servers.json, not per-repo .mcp.json. See Torn list. |
| `mcp-server-patterns` | KEEP | muse-mcp (Node MCP client CLI, registry/OAuth PKCE) and E-muse (Android phone as MCP server via Cloudflare Tunnel): building/debugging MCP servers, tools, resources, transports. |
| `messages-ops` | DROP | Overlaps built-in messaging (read texts/DMs, recover codes, inspect threads). |
| `ml-adoption-playbook` | DROP | Adding ML to a codebase; ML adoption not worked in. |
| `mle-workflow` | DROP | ML systems hardening; ML not worked in. |
| `module-regression` | DROP | Cross-module REGRESSION.md ledger; no large-repo regression governance evidenced. |
| `motion-advanced` | DROP | React drag/drop/gesture/SVG animation; no animation work evidenced for shopthaothao. |
| `motion-foundations` | DROP | React motion tokens/springs; no animation work evidenced. |
| `motion-patterns` | DROP | React element animation; no animation work evidenced. |
| `mybatis-patterns` | DROP | MyBatis persistence; MyBatis not used. |
| `mysql-patterns` | DROP | MySQL/MariaDB schemas; MySQL not used (bench DB is from-scratch). |
| `nanoclaw-repl` | DROP | NanoClaw sessions; NanoClaw not used. |
| `nasiko-control-plane` | DROP | Nasiko CLI; Nasiko not used. |
| `nestjs-patterns` | DROP | NestJS backends; NestJS not used. |
| `netmiko-ssh-automation` | DROP | Netmiko network-device automation; network-device work not in profile. |
| `network-bgp-diagnostics` | DROP | BGP diagnostics; network operations not worked in. |
| `network-config-validation` | DROP | Router/switch config review; network operations not worked in. |
| `network-interface-health` | DROP | Interface error/drop diagnostics; network operations not worked in. |
| `nextjs-turbopack` | DROP | Next.js 16/Turbopack; shopthaothao is Vite, not Next.js. |
| `nodejs-keccak256` | DROP | Ethereum keccak hashing; crypto not worked in. |
| `nutrient-document-processing` | DROP | Needs NUTRIENT_API_KEY (and NUTRIENT_DWS_API_KEY); both absent. |
| `nuxt4-patterns` | DROP | Nuxt 4; Nuxt not used. |
| `openclaw-persona-forge` | DROP | OpenClaw personas; Boss's persona is Mea via SOUL.md/IDENTITY.md, not OpenClaw. |
| `opensource-pipeline` | DROP | Private-to-public repo packaging; Boss's repos start public and secrets are guarded by heal checks. |
| `operator-approval-loop` | DROP | Overlaps platform approval cards, which already gate external sends. |
| `orch-add-feature` | DROP | Overlaps custom subagent-orchestration + tdd + commit (gated feature pipeline). |
| `orch-build-mvp` | DROP | Overlaps custom subagent-orchestration (spec-to-MVP slices). |
| `orch-change-feature` | DROP | Overlaps custom subagent-orchestration (behavior change pipeline). |
| `orch-fix-defect` | DROP | Overlaps custom subagent-orchestration + diagnosing-bugs (defect pipeline). |
| `orch-pipeline` | DROP | Overlaps custom subagent-orchestration (the gated Research-Plan-TDD-Review-Commit engine itself). |
| `orch-refine-code` | DROP | Overlaps custom subagent-orchestration + code-review (behavior-preserving refactor pipeline). |
| `osint-investigation` | DROP | OSINT investigations; OSINT not worked in. |
| `parallel-execution-optimizer` | DROP | Overlaps custom subagent-orchestration (parallel work/verification lanes). |
| `perl-patterns` | DROP | Perl 5.36+; Perl not used. |
| `perl-security` | DROP | Perl input/process review; Perl not used. |
| `perl-testing` | DROP | Perl Test2/Test::More; Perl not used. |
| `plan-canvas` | DROP | Plan presentation surface; plans are Markdown files, no canvas tool. |
| `plan-orchestrate` | DROP | Overlaps custom subagent-orchestration (picking the right command per plan step). |
| `plankton-code-quality` | DROP | Overlaps custom code-review (write-time lint/format hooks). |
| `postgres-patterns` | DROP | PostgreSQL schemas/RLS; Postgres not used (bench DB is from-scratch). |
| `prediction-market-oracle-research` | DROP | Prediction markets as oracle signals; no prediction-market work. |
| `prediction-market-risk-review` | DROP | Prediction-market compliance/risk review; no prediction-market work. |
| `prisma-patterns` | DROP | Prisma schemas/queries; Prisma not used. |
| `product-capability` | DROP | PRD-to-SRS lane; no PRD/SRS work in profile. |
| `product-lens` | DROP | Product-direction pressure-testing; no product-management work. |
| `production-audit` | DROP | Generic production-readiness audit; heal check + verify-before-claiming already cover it. |
| `production-scheduling` | DROP | Manufacturing line scheduling; manufacturing not worked in. |
| `project-flow-ops` | DROP | Overlaps custom github skill (PR triage); no Linear. |
| `prompt-caching-strategy` | DROP | LLM prompt-cache optimization; no prompt-cache work evidenced. |
| `prompt-optimizer` | DROP | Prompt rewriting; no prompt-optimization work evidenced. |
| `python-patterns` | KEEP | mini-git (Python 3 stdlib only, complete, 37 tests) and bench Python work: idiomatic Python structure, typing, PEP 8. |
| `python-testing` | DROP | Overlaps custom tdd (test-first workflow); pytest is not installed on this VM and mini-git tests already run without it. |
| `pytorch-patterns` | DROP | PyTorch training loops; PyTorch not used. |
| `quality-nonconformance` | DROP | Manufacturing non-conformance/CAPA; manufacturing not worked in. |
| `quarkus-patterns` | DROP | Quarkus services; Quarkus not used. |
| `quarkus-security` | DROP | Quarkus auth/secrets hardening; Quarkus not used. |
| `quarkus-tdd` | DROP | Overlaps custom tdd (Quarkus test-first; Quarkus not used). |
| `quarkus-verification` | DROP | Overlaps custom verify-before-claiming (Quarkus pre-deploy checks; Quarkus not used). |
| `rails-patterns` | DROP | Rails apps; Rails not used. |
| `ralphinho-rfc-pipeline` | DROP | Overlaps custom subagent-orchestration (RFC-driven multi-agent execution). |
| `react-native-patterns` | DROP | React Native/Expo; mobile work is native Android, not React Native. |
| `react-patterns` | KEEP | shopthaothao (React 19 + TypeScript + Vite): idiomatic function components, hooks, state shape, TSX review. |
| `react-performance` | DROP | React/Next.js performance refactoring; no React perf work evidenced (react-patterns kept covers components). |
| `react-testing` | DROP | React component/hook tests; no React test work evidenced for shopthaothao. |
| `recsys-pipeline-architect` | DROP | Recommendation/ranking pipelines; recsys not worked in. |
| `recursive-decision-ledger` | DROP | Recursive reasoning evidence trails; meta-work, no profile need. |
| `redis-patterns` | DROP | Redis caching/locks/pub-sub; REDIS key present but no Redis use in any profile repo (key presence alone is not use). |
| `regex-vs-llm-structured-text` | DROP | Regex-vs-LLM extraction choice; no extraction work evidenced. |
| `remotion-video-creation` | DROP | Overlaps custom lemo-opuscar (code video); Remotion not used. |
| `repo-scan` | DROP | ECC pointer to a repo-scan install; performs no audit itself, ECC self-management. |
| `research-ops` | DROP | Overlaps custom search-playbook + native-web-search (fresh-facts research). |
| `returns-reverse-logistics` | DROP | Returns/reverse logistics; logistics not worked in. |
| `rules-distill` | DROP | Overlaps AGENTS.md/MEMORY.md workflow (recurring principles become rules). |
| `rust-patterns` | DROP | Rust ownership/traits/concurrency; Rust not used. |
| `rust-testing` | DROP | Rust tests; Rust not used. |
| `safety-guard` | KEEP | muse-heal production VM changes and the paired-Pi two-writer rule: restrict edit scope during autonomous work, deploys, and migrations. |
| `santa-method` | DROP | Publishing/deploy gating ritual; AGENTS.md workflow gates already cover it. |
| `scientific-db-pubmed-database` | DROP | Needs NCBI_API_KEY; absent, and biomedical literature is not Boss's work. |
| `scientific-db-uspto-database` | DROP | Needs USPTO_API_KEY; absent, and patent records are not Boss's work. |
| `scientific-pkg-gget` | DROP | Needs gget/bioinformatics tooling; genomics not worked in. |
| `scientific-thinking-literature-review` | DROP | Academic literature synthesis; academic review not worked in. |
| `scientific-thinking-scholar-evaluation` | DROP | Academic work evaluation rubrics; academic review not worked in. |
| `search-first` | DROP | Overlaps custom search-playbook + verify-before-claiming (check-before-building). |
| `security-bounty-hunter` | DROP | Bug-bounty vulnerability hunting; not worked in (security-audit covers review). |
| `security-review` | DROP | Overlaps custom security-audit (auth/input/secrets/API/payment review). |
| `security-scan` | DROP | Overlaps custom security-audit + heal check (auditing .claude/MCP/hooks config). |
| `seo` | DROP | Search-visibility/SEO remediation; no SEO work evidenced for the landing page. |
| `skill-comply` | DROP | Overlaps custom verify-before-claiming (checking agents follow given skills/rules). |
| `skill-host-compat` | DROP | Linting ECC skills for Codex/Cursor; not Muse, ECC self-management. |
| `skill-scout` | DROP | Finding/creating skills for ECC; this curation is the one-off. |
| `skill-stocktake` | DROP | Auditing Claude skills/commands; ECC self-management. |
| `social-graph-ranker` | DROP | Social graph ranking engines; social-graph work not in profile. |
| `social-publisher` | DROP | Overlaps built-in social-publishing (multi-platform publishing). |
| `springboot-patterns` | DROP | Spring Boot backends; Spring Boot not used. |
| `springboot-security` | DROP | Spring Security review; Spring Boot not used. |
| `springboot-tdd` | DROP | Overlaps custom tdd (Spring Boot test-first; Spring Boot not used). |
| `springboot-verification` | DROP | Overlaps custom verify-before-claiming (Spring Boot pre-deploy checks; Spring Boot not used). |
| `story-lifecycle` | DROP | Feature delivery tracking without Jira/Linear; plan files already track delivery. |
| `strategic-compact` | DROP | Session compaction timing; compaction is runtime behavior, not a skill workflow. |
| `swift-actor-persistence` | DROP | Swift actor persistence; iOS/Swift not worked in. |
| `swift-concurrency-6-2` | DROP | Swift 6.2 concurrency; iOS/Swift not worked in. |
| `swift-protocol-di-testing` | DROP | Swift DI testing; iOS/Swift not worked in. |
| `swiftui-patterns` | DROP | SwiftUI views/state; iOS/Swift not worked in. |
| `taste` | DROP | Music-video/fancam visual direction; Boss's films are lemo code styles, not fancams. |
| `taste-application` | DROP | Needs FAL_KEY for live style application; absent (dry-run only without it). |
| `taste-distillation` | DROP | Needs FAL_KEY for live style capture; absent (dry-run only without it). |
| `tasteforge-video` | DROP | Needs provider generation keys for image/video/3D discovery and generation; absent. |
| `tdd-workflow` | DROP | Overlaps custom tdd skill (failing-tests-first workflow) by name and function. |
| `team-agent-orchestration` | DROP | Overlaps custom subagent-orchestration (multi-agent fan-out/Kanban). |
| `team-builder` | DROP | Overlaps custom subagent-orchestration (composing agent teams). |
| `terminal-opener` | DROP | Overlaps custom tmux skill (interactive CLIs/terminals, including new-terminal plans). |
| `terminal-ops` | KEEP | Daily heal/gh/muse-cli ops: run a command, check a repo, debug CI, push a narrow fix with exact proof of what was executed and verified. |
| `test-collaboration` | DROP | Overlaps custom tdd (test-asset inventory/governance). |
| `tinystruct-patterns` | DROP | tinystruct framework; not Boss's tiny-lang (a from-scratch language, not tinystruct). |
| `token-budget-advisor` | DROP | Response-length/token-budget control; the ECC context concern is skill-list size, not response length. |
| `token-card` | DROP | Coding-agent usage cards; no usage-card reporting work. |
| `ui-demo` | DROP | Web-app demo/screen-record videos; films are lemo code renders, not screen demos. |
| `ui-to-vue` | DROP | UI-to-Vue 3 conversion; Vue not used. |
| `uncloud` | DROP | Uncloud clusters with uc CLI; Uncloud not used. |
| `unified-memory` | DROP | Overlaps muse-heal jlog journal (save/transfer/resume work state). |
| `unified-notifications-ops` | DROP | Alert routing/dedup/escalation; heal cron reports failures directly, no routing work. |
| `verification-loop` | DROP | Overlaps custom verify-before-claiming (verify before PR/merge). |
| `video-editing` | DROP | Overlaps custom lemo-opuscar + hybrid/ scripts (video assembly with ffmpeg). |
| `videodb` | DROP | Needs VIDEO_DB_API_KEY; absent. |
| `visa-doc-translate` | DROP | Visa document translation/OCR; immigration paperwork not worked in. |
| `vite-patterns` | KEEP | shopthaothao (React 19 + TypeScript + Vite, GitHub Pages): Vite config, plugins, HMR, env variables, proxy, build optimization. |
| `vue-patterns` | DROP | Vue 3/Nuxt/Pinia; Vue not used. |
| `windows-desktop-e2e` | DROP | Windows native desktop E2E with pywinauto; Boss is Linux VM/Android. |
| `workspace-surface-audit` | DROP | Overlaps custom heal skill (environment/capability inventory). |
| `x-api` | DROP | Overlaps built-in social-publishing (X automation); no X automation work. |
