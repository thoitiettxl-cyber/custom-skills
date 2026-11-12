# Provenance — lemo-companion

This file is the evidence record for `../SKILL.md`. It is not a second set of rules. If a rule in `SKILL.md` and this file disagree, stop and check the source file listed here before using the rule.

## Source repo

- Primary repo, local clone: `~/workspace/lemo-opuscar`, origin `https://github.com/thoitiettxl-cyber/lemo-opuscar.git` (a fork of lemomo-ai/lemo-opuscar).
- HEAD at survey time: `3992c7a` (full hash from the PHA 2 check of the history rows is in the distillation record; the HEAD line recorded at PHA 0 was `3992c7af1d55fa8976c6c54e1c9101280e4cc71b`, merge, 2026-10-25).
- First commit in this clone's log: 2026-09-26, starting with 39 styles; 66 commits and 59 styles at survey time; 5 authors in the fork log.
- Licence: MIT, LemoLab 2026, from `LICENSE` in the repo. All lessons in the skill are paraphrased, not copied verbatim.
- Survey dates: PHA 0, PHA 1, PHA 2, and PHA 3 all ran on 2026-10-25, with Boss approval at each gate. PHA 4 wrote this skill on 2026-10-25. PHA 5 verification had not run when this file was written, so the skill status is UNVERIFIED by the distill standard.

## Stack at survey time

- Node 20 or newer, `three` ^0.170.0, `playwright-core` ^1.63.0, from `package.json`; the lockfile pins three 0.170 and playwright-core 1.63 exactly.
- Python core: numpy, scipy, soundfile, soxr, pillow, from `requirements.txt`.
- Pipeline: `window.render(t)` → `core/render/still.mjs` → `core/render/mux.sh`, with `core/render/srt.py`, `core/three/post.js` (102 lines), and `core/lib.js` time helpers.
- Sparse-checkout trap, recorded so a later reader does not misread absence: the working tree at survey time was missing `demo/`, `MAINTAINING.md`, `MY-STYLES.md`, `PIPELINE.md`, `hybrid/`, and `.github/workflows/pages.yml`, even though `git ls-files` lists them. Checks that needed those files used `git show HEAD:<path>` or `git grep HEAD`. No PHA 2 row was left as cannot-verify-from-working-tree after that step.

## Sources used, by tier

T1, explicit guidance (all paraphrased):
- `AGENTS.md` (88 lines), `DIRECTOR.md` (137 lines), `TECHNIQUE.md` (162 lines), `core/README.md`, `styles/*/STYLE.md` (59 styles), `styles/_template/STYLE.md`, and `plugin/skills/lemo-opuscar/SKILL.md` (46 lines, the existing lemo-opuscar skill, used only to set priority and avoid overlap, not edited).

T2, machine-enforced or machine-readable:
- `package.json` and its lockfile (engines, dependencies, exact pins), `requirements.txt`, `.github/workflows/pages.yml` (publishes the gallery only; it is not a lint or test gate), `core/render/mux.sh` (two-pass loudnorm, grain, output protection), `core/render/srt.py` (sort, clip, millisecond rounding), `core/render/still.mjs` and `video.mjs` (seek and sharding), `core/render/page.mjs` (ready wait, 180 s), and `core/three/post.js` (post chain order).

T3, history (used for context and for the history lessons that were examined, not as standalone skill rules):
- Full hashes verified in PHA 2: `02dce5b6ff6210622788c15319c082e9cb9e7217` (STYLE/DEMO split, 2026-09-29), `a401d6c26d4b3846b699257af25a85d2d45b438e` (library audit, 2026-10-22; the message's count of 54 unreferenced files was not separately confirmed, total deleted files were 67), `f3c590dffab39419e2f3018416706e046986fe11` (mux loudness warning, 2026-09-30), `0ab27f9d15c014557bd00880471910497defff50` (end-to-end skill test fixes, 2026-10-22; no test or harness file was found in its diff, so that lesson rests on the commit message alone), `375de139c7acfb96175dd772438fdae19df56b7e` (readcheck end-of-film cap, 2026-10-13, with a new 54-line test file).

T4, patterns inferred from code (each still needs the PHA 2 occurrence count and counterexample check recorded in the PHA 2 table before it is treated as more than a pattern):
- Time functions in `core/lib.js` (`seg`, easing, `monotone`, `track`, `env`, `mulberry`, `hash`), render-by-time in `core/render/*`, SRT handling in `core/render/srt.py`, post-processing in `core/three/post.js`, and mux handling in `core/render/mux.sh`.

Secondary sources, borrowed models only, no runtime installed:
- threejs-animation, hyperframes-animation, hyperframes/gsap, gsap-timeline, and remotion-captions, as found through the public skills index. Only short public summaries were retrieved for each (36–52 lines per source); no full skill text was retrieved in PHA 1 or PHA 2. That is why section F of `SKILL.md` labels every borrowed model unverified, and why the not-implemented models are listed below as excluded, not as rules.

## Sources and rules excluded at PHA 3

REPO-ONLY pipeline rows, kept only as short prerequisites in SKILL.md where noted, not as a full pipeline tutorial:
- Treatment with three candidate structures before opening a demo; keeping every style invariant fixed as an absolute rule; video sharding in full detail; page fail-fast in full detail; target-frame sizing in full detail; audio-event versus subtitle separation beyond the short rule in section C; camera-type depth-of-field detail beyond the warning in section D; and the pinned stack beyond the short check in section D.

Style-specific techniques, excluded as standalone rules:
- Whiteboard pen stroke fitting, satellite double-precision sphere math, impasto fixed-seed repaint (except the unseeded-random caution, which is folded into the determinism rule), and news-document PDF rebuild with `pdftotext` (no tool in the repo calls `pdftotext`, and demo coordinates are literal hardcode).

Contradicted or style-specific guidance, excluded as standalone rules at PHA 3 item 3 (soft 3D light and 2.5D shoulder drawing are not rules in SKILL.md; a rendered frame is judged on its own, and the shoulder technique belongs to the styles that use it, not to this companion):
- Soft 3D light with a soft area light plus low-intensity environment light, and 2.5D shoulder rotation with no outline on an overlapping arm. Both are guidance in TECHNIQUE.md, both are contradicted by library demos, and neither is enforced by code.

General directing rules, excluded to keep this skill inside motion, caption, 3D, and asset preparation:
- Evaluation order (sound, rhythm, camera, performance), one subject, one goal, and a 3-second hook as a standalone rule, three-layer sound and ducking, two silences and scene bridges, numbers honesty as a standalone rule, the one-round review loop and post-delivery scope rule, a total delivery checklist as a standalone rule, and synthesised-music frequency-band balancing (single source, wording around -3 dB, no measuring tool).

Foreign runtime rows, excluded outright:
- HyperFrames paused-timeline contract (`window.__timelines`, `data-composition-id`), `quickTo` and `matchMedia`, scroll-driven and React timelines, Remotion Studio and React Sequence caption rendering, and WebGPU and TSL rendering with a newer three target. None of these is implemented in lemo, and none was installed.

External models excluded as rules (see SKILL.md section F8):
- Skeletal animation and glTF clips, morph targets, clip blending by weight, label seeking, caption JSON with millisecond timestamp fields, and a caption page-break flag. All are not implemented in lemo, their examples target a newer three version, and their full source text was not retrieved.

Other exclusions, by the approved parameters:
- Vietnamese voice prosody rules: no approved source supported them, so none are in this skill.
- OpenMontage: not reinstalled, not recommended; a HyperFrames skill is not an OpenMontage install.
- Remotion, GSAP, and HyperFrames runtimes: not installed, not imported, not copied into a lemo project by this skill.

## Unverified list — do not present these as verified

- Full text of all five secondary skills (summaries only, as above).
- Compatibility of threejs-animation examples written for three r186 with lemo's pinned three 0.170.
- `mixer.setTime(t)` versus delta-update behaviour inside lemo's deterministic `render(t)` model.
- Whether `timestampMs` in the caption model is a midpoint, and what display-page window values should be.
- Satellite double-precision threshold described as a few tens of kilometres: no test in the repo measures it.
- Measurements that can only be made on a specific film, not from static code: picture-to-music accent offset, tempo and breathing on a real film, 0.2 s review and expression at final size on a real film, subject size, contrast, and brightness on a real film, and the total delivery checklist on a real film.
- Every rule in SKILL.md that PHA 5 has not yet touched: until PHA 5 runs, the whole skill is UNVERIFIED by the distill standard, even where PHA 2 classified a rule as enforced in lemo code. PHA 2 enforcement is about lemo, not about this skill helping an agent.

## Revision round 2 — after PHA 5 round 1 (2026-10-25, Boss-approved)

PHA 5 round 1 ended NO-BENEFIT-DETECTED, not PASS (HELD-OUT B 9.5 vs A 8.3, B-A 1.2 below Delta 2; trigger should-match 5/10 below the 8/10 threshold), and the skill was not edited during that round. Boss then approved revising the skill from the red-team findings and the trigger failure, then re-verifying. This section records that revision; it does not claim the revised skill is verified, and PHA 5 round 2 is the round that must judge it.

Applied, all 29 red-team findings in substance, with no rule cut (ablation proposed no cut):
- Priority contradictions resolved: C1 hold outranks B7 grid and C4 clipping, with a re-time/merge/shorten/report rule instead of silent clipping; D2 outranks D1 for orthographic scenes, with D1's order kept; E1 true peak corrected to at or below -1.2 dB, LRA reported against target 11 with no invented pass threshold, and the silent-audio skip recorded as the documented exception; B7 grid fixed to beat step 60/BPM and half-beat step 30/BPM, so 120 BPM gives 0.5 s beat and 0.25 s half-beat.
- Mislabels corrected: A2 and C5 changed from Enforced to Aspiration, because no tool forces them; F8 changed from Unverified model to Prohibition, because it bans rather than models; Do-not-do and Checklist sections now state they add no enforcement claim.
- Silent-harm paths strengthened: A1 grep expanded to performance.now, new Date, crypto random, and module-level carried state; C4 equivalence now requires a sample test against srt.py; E2 naming does not exempt mux grain; E3 external-font search expanded beyond fonts.googleapis and CJK subsetting now requires a subsetting tool plus a character-set comparison; E4 failure path now requires a deliberate missing-input test in a temp directory.
- Definitions added where the red-team found undefined terms: spoken duration source in C1, preset set as the chosen STYLE.md's transitions in C2, signature shot with type/duration/start/end in B3, breathing beat as at least 1 s with no new information in B4, one-frame-event check alongside the 0.2 s review in B5, subject share and lightness difference reported in B6, near-zero offset explained at one frame or more in A4, and scene-default versus use-site override in F6.
- Other contradictions resolved: B1 stepped styles follow B2, with the comic pop as a single named frame; B3 locked-off styles exempt from the four-move count when named; C1 versus B7 resolved in favour of C1; F8 ban clarified not to cover A3 timeline JSON or C4 millisecond rounding; D1 scene-local copies must list differences in the scene plan; D3 exact pins clarified; E5 static scenes no longer fail on identical JPEGs.
- Where a threshold did not exist in the library, none was invented: B6 and A4 report numbers and require explanation, rather than claiming a library threshold.

Not changed in the skill, by design: no rule was cut, no new rule was added beyond the priority section and the clarifications above, and the 8 section F models stay labelled unverified. The two PHA 5 round 1 scorer quirks (H2 grain bound at most 0.1 contradicting mux.sh default 2, and the NOTES.md font-domain check) are scorer fixes for round 2, not skill edits, and must be fixed in the round 2 scorer before any run, not after seeing round 2 results.

Trigger fixes in this revision: frontmatter description and H1 now name motion timing, caption hold, camera moves, deterministic render, 3D post, loudnorm mux, and font credits explicitly, and the WHEN-NOT now states that choosing a style or writing a treatment is lemo-opuscar territory even when motion, captions, or cameras are mentioned.

Status after this revision, before round 2: still not PASS. Round 1's NO-BENEFIT-DETECTED stands for the pre-revision skill; the revised skill has no verification result until round 2 reports one.

## Revision round 3 — after PHA 5 round 2 (2026-10-25, Boss-approved)

PHA 5 round 2 ended UNVERIFIED, not a judgement on the skill: HELD-OUT was never run because all HELD-OUT spawns failed with a runtime authorisation error, while DEV passed Floor (B 9.4 vs A 7.5). Boss then approved fixing the skill from round 2 red-team (20 findings) before running HELD-OUT. This section records that revision; it does not claim the revised skill is verified, and PHA 5 round 3 is the round that must judge it. Because the skill changed again, round 2's Floor and baseline cannot be reused for round 3: round 3 must re-baseline and fix Floor after baseline, with fresh tasks, before HELD-OUT.

Applied, all 20 round 2 red-team findings in substance, with no rule cut:
- Blocking contradictions resolved by sequencing and definition, not by claiming a tool does what it does not: C1 is now checked on the cue list before export and on the exported file after export, with the fix in the cue list, because `srt.py` only clips and cannot re-time, merge, or refuse; shortening text is available only with re-recorded or re-synthesised audio and a re-measured spoken duration, never by re-estimating from shortened text.
- STYLE.md priority narrowed: style invariants, defined testably as rules for all films in that style stated with always, must, or never under a style-rule heading, outrank companion Aspiration and style-grammar rules, but do not override companion tool-contract rules (C4 export steps, D3 exact pins, E1 loudnorm targets, E4 output protection) by a mere mention; a conflict with a tool-contract rule must be reported as unresolvable within lemo tools, and an ambiguous style line is treated as not an invariant.
- D1/D2 label inversion fixed: D1 is a perspective-scene rule only, D2 is now labelled Narrowed, and an orthographic scene is recorded as D2, not as D1, with a rendered depth comparison (depth on versus off at the same time, near and far blur differing) and with GTAO or supersampling drops recorded as deviations with reasons, not merely listed.
- A3/F8/C5 timeline tension fixed by definition: A3 planning timeline, C5 driving timeline (the file the subtitle renderer actually reads), and banned caption JSON with timestamp fields are three distinct things; if a planning timeline becomes the file the renderer reads, it is the driving timeline, its cue times are checked in C1, and it uses t0 and t1 in seconds like `srt.py`.
- Silent-harm fixes: E1 truly silent now uses `mux.sh`'s own operational definition (first-pass loudnorm inf or nan, or measured loudness below -70 LUFS, with no decoder errors), plus a separate voice-presence check, so a missing or muted voice track cannot be recorded as silent; E1 peak wording corrected to match `mux.sh` code itself (loudnorm target -1.2 dB, script warning threshold peak above -1 dB, both numbers reported); E2 now states the default grain 2 for non-pixel and non-vector styles, so passing zero for every style fails; E3 search expanded to @font-face src, script-injected links, and any non-self-hosted font URL, with exactly defined as equal character sets, no missing and no extras, and text actually used defined as project code plus SRT plus on-screen text files; C4 equivalence now requires identical times to the millisecond and identical text on a sample covering overlap, rounding boundary, and sort order, with re-testing on exporter change; D3, E4, and E5 checks now state their limits honestly (lockfile versus installed version, early-failure test versus mid-encode code behaviour, two-point sampling with an expected-state diff criterion).
- Other fixes: A1 picture-code boundary defined with a conservative fallback, A2/F1 boundary defined as keys plus interpolation versus a per-frame literal table, A4 report alone does not pass an unexplained deviation of one frame or more, B2 covers any stepped style, B1 comic pop requires a full-size pop frame with before and after frames, B5 short events enumerated from the plan, B7 C1-moved cuts recorded as C1 exceptions, B4 cue times not used as cut times unless mapped, B6/C3 reporting alone does not pass a clipped, dark, or covering subject, and the checklist now carries the qualifiers it claims to inherit (C1 fallback, C4 equivalence, STYLE.md resolution, D2 recording, silent-audio confirmation, LRA report, grain default).
- Trigger: frontmatter description now adds three.js post-processing chain and orthographic camera depth of field; round 3 trigger test must still use fresh queries.

Not applied in this revision, by scope: the round 2 ablation GB CUT proposal (motion/camera rules) was not a red-team finding and was confounded by brief-prescribed formats, so GB is kept unchanged and the cut proposal remains undecided for a separate Boss decision; it is not silently accepted or rejected here.

Status after this revision, before round 3: still not PASS. Round 2's UNVERIFIED stands for the pre-revision skill; the revised skill has no verification result until round 3 reports one.

## Revision round 4 — 17-repo update (PHA 4, 2026-10-25, Boss-approved)

PHA 3 was approved in full by Boss, including all 7 Boss-decides recommendations,
and PHA 4 wrote this `.next` copy from it. The original skill is untouched by this
round. PHA 5 has NOT run on this copy: the skill status is UNVERIFIED by the
distill standard, round 3's NO-BENEFIT-DETECTED stands only for the pre-update
skill, and the round 3 HELD-OUT numbers must not be reused, because the skill
changed. PHA 5 must re-baseline and fix Floor/Delta after baseline, with fresh
tasks. Replay source is still unresolved (no clean replay commit found in any
round; none invented) — PHA 5 must use a second greenfield HELD-OUT task as in
round 1, or Boss must accept lowered certainty.

### The 17 repos (PHA 1/2 scope, items 04-20; surveyed 2026-10-25, API/raw reads only, no full clone per Boss's PHA 0 decision)

- 04 SVGO `svg/svgo`, MIT. 05 Satori `vercel/satori`, MPL-2.0. 06 GSAP
  `greensock/gsap`, NO LICENCE FOUND (no SPDX, no LICENSE file at root) —
  paraphrase only, nothing copied. 07 Anime.js `juliangarnier/anime`, MIT.
  08 Motion `motiondivision/motion`, MIT. 09 Rive, CORRECTED: no `rive-app/rive`
  exists; the real repos are `rive-app/rive-wasm` and `rive-app/rive-react`,
  both MIT. 10 dotLottie, CORRECTED: `LottieFiles/dotlottie-web`, MIT, Rust+WASM
  player. 11 Remotion `remotion-dev/remotion`, NOASSERTION — paraphrase only.
  12 Motion Canvas `motion-canvas/motion-canvas`, MIT. 13 Three.js
  `mrdoob/three.js`, MIT — surveyed HEAD is 0.186.0, 16 minors above lemo's
  pinned 0.170, so HEAD docs are NOT evidence of 0.170 behaviour; only the
  r170 spot-checks count for pinned behaviour. 14 React Three Fiber
  `pmndrs/react-three-fiber`, MIT. 15 Drei `pmndrs/drei`, MIT. 16 React Three
  Rapier `pmndrs/react-three-rapier`, MIT. 17 React Postprocessing
  `pmndrs/react-postprocessing`, MIT. 18 Howler.js `goldfire/howler.js`, MIT.
  19 Mediabunny, CORRECTED: no `mediabunny/mediabunny` exists; the real repo is
  `Vanilagy/mediabunny`, MPL-2.0. 20 FFmpeg `FFmpeg/FFmpeg`, NOASSERTION, and a
  mirror of git.ffmpeg.org, not a JS library — paraphrase only.
- Items 01-03 (the video's "skill" section) were verified separately on
  2026-10-25 and are NOT part of the PHA 1/2 lots: Remotion Skills
  `remotion-dev/skills`, GSAP Skills `greensock/gsap-skills` (MIT), Motion AI Kit
  `motiondivision/ai-kit` (the `/motion` skill at
  `plugins/motion/skills/motion/SKILL.md`; Performance Doctor, MotionScore, and
  CSS spring generation are Motion+ paid, not free). None of the three is
  installed locally, and this update imports no runtime from any of them.
- Paraphrase check for this round: all new SKILL.md wording was written from the
  PHA 3 synthesis (itself a paraphrase), in the skill's own English style; no
  foreign repo was cloned in this cycle, so no foreign source text exists on
  disk here to copy from, and no new rule quotes a no-licence or NOASSERTION
  source. Numeric values (loudnorm targets, ffmpeg defaults) are facts about
  tool behaviour, not copied prose.

### What PHA 4 did (Keep) and did not do (Cut)

- Keep, 35 items from PHA 3, implemented as: 10 amended rules (A1, A2, A4, C4,
  D2, D3, E1, E3, E4, E5), 15 new rules (A6, A7, B8, B9, B10, C6, D4, D5, D6, D7,
  D8, D9, E6, E7, E8), 2 new Do-not-do bullets (no CSS animation for film
  motion; no visibility-driven pause/resume), and 4 new checklist bullets. The
  B6 perceptual-scale recommendation is implemented as a caution note inside A2
  only (check scale motion in still review, never by linear numbers alone) —
  no compensation curve is prescribed, because none was measured on lemo.
- Cut, nothing from these lists entered the skill: the 24 already-implemented
  rows (duplicates of existing rules); the 34 REPO-ONLY rows (foreign runtimes,
  hooks, pass merging, BVH, browser audio unlock, mediabunny packet-count
  precondition, FFmpeg C internals, contribution routes, foreign CI workflow
  files); contradictory mechanisms (ms/confidence/page-break caption fields,
  FPS-adaptive quality, tight near/far as a rule, WebGPU/TSL, pmndrs MSAA-4
  default, scroll, skeletal/morph/clip — F8 stands, and brick `clean()`
  stripping non-position/normal/uv attributes is why it stands); and
  no-attach-point items (physics fixed-step, component isolation, SRT parser as
  a rule, CI gates, encoder fallback branches, sample-exact pad against E4's
  0.02 s tolerance, demand/invalidation cache, shader warmup as a
  correctness rule, camera-type state-key invalidation, SVGO pipeline for
  code-drawn line-art, remap helper as a separate rule, four combinators as an
  API). Full row lists are in `~/workspace/tmp/lemo-companion-pha0-17/pha3.md`.
- Boss-decides resolutions applied: mux holes are warnings/checks in the skill
  only — fixing `mux.sh` itself (trap, dropping `-y`, isFinite, LRA/TP checks
  before linear, separate stats file) is a separate lemo-repo task needing its
  own approval, and was NOT done here; the GB motion/camera CUT proposal from
  rounds 2-3 remains undecided and GB was NOT cut; no disposal rule was added
  (disposal stays a film-code choice without a verifying tool); LOD was cut
  entirely; D27/D28 appear only in the open-measurement notes below, not as
  rules.

### Open-measurement notes (NOT rules — do not present as verified)

- D27 mono loudness handling: PHA 1 rests on a single code branch, below the
  T4 bar of 5 occurrences, and lemo has no mono-specific loudness handling in
  `mux.sh` — no rule until measured.
- D28 silence detection: needs both a threshold and a minimum duration; PHA 1
  rests on code options only because `doc/filters.texi` (976,324 bytes) was not
  retrieved in full, and lemo has no silencedetect tool — no rule until measured.
- C16 orthographic half, C28 three 0.170-vs-0.186 API parity, C31 LOD thresholds
  under ortho, B27 foreign usage count, and the B12/B22 foreign diffs (commit
  titles only, diffs unread): labels carried forward, not upgraded. The lemo
  side of B12/B22 was verified independently in PHA 2; the foreign side was not.

## Loop round — after class-(i) rescore and class-(ii) re-runs (2026-10-25, Boss-approved)

This section records step (e) of the approved loop: the skill fix after the
scorer/brief fixes. It does NOT claim the skill is verified: the
verification round (step (g)) has not run, HELD-OUT is still sealed and
never run, and the re-runs below are reference-only, not generalizing
evidence. D2n is reference-only after the fixes.

### Evidence used

- Blind rescore, step (c) (`loop-rescore.md`): class-(i) items 3, 5, 8 only,
  all 15 blinded D2n runs, ZERO deviations from the change-list predictions
  — 23 cells flip fail→pass (item 3: 003/010/015; item 5: 10 mesh-form runs;
  item 8: 10 paraphrase runs), monotonicity holds (no pass→fail), rescored
  D2n means by blinded group 8.0/6.0/5.4, overall ≈6.47, exactly as
  predicted. Items 4 and 9 were correctly not rescored (class (ii)).
- Class-(ii) re-runs, step (d) (`loop-reruns/`, parent-verified): all 15 runs
  (A/B/N × 5) score 10/10 under the new scorer in field mode, including
  items 4 and 9 everywhere. Sampled run outputs show caches declared as
  identifiers (`containerGeo`, `containerMat`, `containers`) that are real
  bindings with use sites in `scene.js`, and ready checks carrying an
  explicit severity classification for the required-asset 404.
- What the rescore proves: items 3, 5, and 8 on the old runs were
  measurement failures (scorer literalism), not skill gaps — the practices
  were already in the skill (D4 per-material opacity, D7 needsUpdate flag,
  B8/B9/B10 plan declarations). What the re-runs prove: items 4 and 9 pass
  under the new brief for every branch, including no-skill runs — the brief
  change, not skill content, supplied the identifier discipline and the
  severity field. Neither result, on its own, justifies a skill change; a
  change needs a gap the skill itself leaves open.

### The one change: D6 identifier discipline (general rule, not scorer wording)

- Old D6: "Share geometry and material through caches, instead of creating
  new ones per mesh in a loop", checked by reuse in scene code and by a
  loop-creation defect. It did not say what counts as a cache claim.
- New D6 (same paragraph, two sentences added): "A cache is a code binding,
  not a label: declare each shared geometry or material under an identifier
  in the scene code, and reference that identifier at every use site; a
  name that appears only in the plan, in prose, in a comment, or in a
  string table is not a cache, and a declared binding that is never
  referenced is dead code, not sharing." Check extended: every cache
  identifier named in the plan must appear in the scene code as a declared
  binding and at a use site.
- Evidence for the gap: old runs satisfied "share through caches" in prose
  while the code told a different story — prose cache names with no matching
  code identifier, a string table mapping names to names, comment claims
  over null placeholders, and skill-guided runs that shared through a single
  InstancedMesh but named their caches only in prose or a comment, so a
  reviewer could not verify the claim from the plan alone. The old D6 check
  ("reuses cached geometry and material") could not separate real sharing
  from a sharing claim, because it never defined the claim's burden of
  proof.
- Generality justification: the rule holds for any lemo film, not just D2n.
  It forces no specific word, token, field, or identifier — any identifier
  the film itself chooses qualifies, as long as it is a real binding with a
  use site. It is the same discipline as dead-code review: a claimed helper,
  cache, or asset that no code references is not a thing the film has, it
  is a thing the plan asserts. A reviewer checking "does this scene reuse
  cached geometry?" needs exactly this test in every film.
- What was NOT added to D6, deliberately: no `scene.json` field name, no
  `caches` array requirement, no identifier format — those belong to the
  task brief and the scorer, not to film practice.

### Explicitly rejected changes (with evidence)

- E5 severity-classification rule: REJECTED. E5 already states the
  substance — "treat a missing required asset (font, image, or fetch 404)
  as a defect rather than the tool's optional-file warning." The old
  item-9 failures were scorer literalism (negation-scope strip, helper-name
  tokens), not a missing skill rule: skill-guided old runs already wrote
  defect verdicts under E5 and still failed the old scorer. The
  `severity: defect|warning` field that fixed item 9 is a brief measurement
  device; writing that field name into the skill would be scorer-passing
  wording. Adding a generic "classify every failure" sentence would
  duplicate E5's required→defect direction, and there is no observed
  failure evidence for the optional→warning direction (no old run
  mishandled an optional asset; the optional-file warning path was never
  the failure mode).
- Items 2 and 6 (focus value, loudnorm numbers): NO CHANGE. The old-run
  failures were genuine exact-value errors, and every branch passes them
  under the new brief — evidence AGAINST a skill gap, not for one. D2
  already states that a focus target overrides a distance value, and E1
  already states the loudnorm targets (-14 LUFS, TP -1.2 dB, LRA 11).
- Items 3, 5, 8: NO CHANGE. The rescore proved these were measurement
  artifacts (23 flips, zero deviations); the practices were already in
  D4, D7, and B8/B9/B10, which require the behaviour, not specific words.
  Amending them to match the new scorer's wording would be scorer-passing,
  not film practice.
- No new rule, no checklist change, no frontmatter change: the D6 amendment
  is covered by the existing checklist line ("shared geometry and
  material"), and the amendment adds no new enforcement claim (D6 stays
  [Aspiration]).

### Status after this round

- `.next` SKILL.md is 119 lines (the D6 amendment stays inside one existing
  paragraph line); total with this file is within the 600-line budget (see
  the step (e) change note for exact counts). Original skill untouched;
  lemo-opuscar untouched; scorer, briefs, fixtures, and sealed HELD-OUT
  tasks untouched by this step.
- The skill remains UNVERIFIED by the distill standard until step (g)
  reports. This round's results must not be presented as skill
  verification: the rescore measured the instrument, and the re-runs are
  reference-only calibration under a changed brief.

## Refreshing this skill later

- Re-run the PHA 0 checks first: HEAD, licence, stack pins, and whether the sparse-checkout set has changed.
- Re-check the PHA 2 counts before reusing any rule whose classification was aspiration or contradictory; do not carry a classification forward without re-counting.
- Retrieve the full text of any secondary skill before upgrading a section F model from unverified to a rule, and test it on three 0.170 before claiming compatibility.
- Keep the budget: `SKILL.md` at most 300 lines, total skill at most 600 lines, counting this file and any future references files.

## .next2 changes (2026-10-26, step 2, Boss-approved fix list; base = copy of .next, original untouched)

- Base: `.next` SKILL.md `f76017ee…` (119 lines) + PROVENANCE `99ae7234…`
  (308 lines), copied byte-identical to `.next2`; all edits below are in
  `.next2` only. The original skill (`6a41a83e…`) and `.next` are untouched.
- Blocker 1 (A3/C5): A3's check now requires the SRT to match the C5
  driving timeline, not the planning timeline; divergent-case branch
  added (SRT follows driving, difference recorded, not a failure);
  priority line: C5 source rule outranks the A3 match check.
- Blocker 2 (A1): determinism verdict is now the order-independence
  render test (same t rendered twice with other times between must give
  identical frames); grep demoted to a review hint; carve-out added for
  re-derivation from t vs carried state; D6 cache binding declared not
  itself a violation.
- Blocker 3 (C1): delivery states added — pass, recorded C1 exception
  accepted by the owner (violating cues listed), or blocked return to
  the voice stage; least-harm ordering (Boss-approved): short hold over
  moved cue over merged distinct-speaker cues, with the reason recorded.
- Blocker 4 (E3): criterion is now exact equality against the DISPLAYED
  character set (SRT + on-screen text as rendered, including generated
  text); code strings never displayed are excluded. Tool verified on
  this VM 2026-10-26: fontTools 4.46.0 in system python,
  `python3 -m fontTools.subset` runs (`pyftsubset` CLI is not on PATH);
  functional test on NotoSans-700 with 23 Vietnamese characters
  (including diacritics) → subset 23 chars, 0 missing, 0 extras.
- Blocker 5 (D2): single-depth-plane scenes use the focus-sweep test
  (two focus distances, blur must change); the unverified
  target-overrides-distance assertion is deleted; focus is set by
  distance and recorded on orthographic scenes.
- Blocker 6 (A7/E5/E1): A7 distinguishes required vs defaulted
  parameters (defaulted-removed must not fail); E5 required-404 is
  judged against the plan's required-asset list, and READY-early needs
  a named font-load signal or is recorded as unchecked; E1 voice
  presence is measured per voice-cue window with ffmpeg volumedetect
  mean_volume above -20 dBFS (peak alone rejected as
  non-discriminating). Calibration measured 2026-10-26 on the delivered
  news film (Trúc Ly voice + 120 BPM bed): 8 voice windows -15.3 to
  -16.4 dB mean; bed-only gaps -24.6 to -38.7 dB, tail -21.9 dB; if the
  same film's bed-only windows measure above -24 dBFS, both numbers are
  reported and the absolute floor alone is not claimed.
- Silent-harm #7 (self-certification): general principle added — an
  explanation, reason, or plan acceptance never by itself passes a
  check; a deviation is recorded and delivery with it requires owner
  acceptance, except where a rule names an independent deciding check
  (D2's rendered comparison is the model). Targeted fixes: A4 deviation
  ≥1 frame fails the grid-alignment check; E1 LRA deviation is recorded,
  not a pass; BPM-mismatch recording passes no music-cut alignment
  check; an E2 grain reason does not pass the mux-call check.
- Silent-harm #12 (plan-only): D6's code-binding discipline generalized
  to B9 (fit/anchor must be values used in scene code), B10 (origin must
  be a declared code binding at every use site), and B4 (tempo change
  must be implemented in scene code); plan-only names do not pass.
- Checklist updated consistently: C1 exception state, code-implemented
  tempo/breathing, code bindings for stagger origin and fit/anchor,
  volumedetect voice measurement. No other rule text changed.
- Counts after this draft: SKILL.md 119 lines, PROVENANCE 368 lines,
  total 487/600 — within budget. SKILL.md line count is unchanged at 119
  because all rule fixes are substring replacements inside existing long
  lines; the growth is entirely this PROVENANCE section (+60 lines).

## .next3 draft (completion program, 2026-10-26; single writer = coordinator)

Base: `.next2` copied verbatim (SKILL `a27f8044…`, PROVENANCE
`bf89c111…`, 119 + 368 = 487/600), then 5 rule fixes, all substring
replacements inside existing long lines. Evidence for the fixes: the
.next2 round's combined verdict NO-BENEFIT-DETECTED (mean gap 2.75 <
Delta 4; SRT tasks saturated at baseline A 9.00) and its red-team
report (27 findings, 3 blocking). No other rule text changed in this
draft.

- F1 (E3, red-team blocking R1): exact subset equality was
  unprovable for render-time-generated text (canvas/WebGL text
  exists only as pixels post-render; subset precedes render).
  New check: subset charset must equal exactly the DECLARED set
  = SRT text ∪ plan-declared literal on-screen strings ∪
  plan-declared generated-text classes (each with its charset,
  declared before render). Rendered text outside the declared
  set = recorded deviation, not a pass; still review must catch
  it. Never-displayed code strings still excluded; fallback
  order declaration kept.
- F2 (C2, red-team blocking R2): preset-set check vs
  chart-operation check gave opposite verdicts when the preset
  list contains only a fade, with no priority inside C2. New
  priority: for chart transitions the chart-operation
  requirement ALWAYS governs (a fade is never a chart
  operation, even if listed); preset-set membership governs
  non-chart transitions only; with a fade-only preset list the
  preset-set check is not applicable to chart transitions.
- F3 (B7, red-team blocking R3): grid multiples were anchored
  implicitly at t=0 with no origin/phase, so an intro offset
  made honest beat-aligned cuts systematically fail. New check:
  plan declares the grid origin (music start / first downbeat
  time); cuts satisfy (cut − origin) % step == 0 to ms
  rounding; an undeclared offset makes t=0-aligned cuts FAIL.
  C1-wins exception kept.
- F4 (E1, red-team silent-harm): the pass check used the mux
  script's warning thresholds (−14 ± 1 LU, peak ≤ −1 dB), not
  the stated targets, so a mix could pass while missing both
  targets. New check: pass = |I+14| ≤ 1 LU AND true peak ≤
  −1.2 dB (the target); the −1 dB script warning is reported
  alongside but does not pass a peak above target. LRA rule
  unchanged (deviation = recorded deviation + owner
  acceptance).
- F5 (A1, red-team silent-harm): order-independence passed
  unseeded-random-cached-on-first-render, and grep-as-hint let
  a direct prohibition violation pass. New check: A1 =
  order-independence test AND zero banned calls in
  comment-and-string-stripped picture code; a banned call fails
  even if re-render comparison passes. Sole exception: calls
  inside seeded helpers (mulberry, hash). D6 cache binding
  still not a violation. This also aligns the skill with the
  .next2 canonical item 1(c), which already treated banned
  calls as fail (prior reviewer noted the skill/item tension).
- SKIPPED with reason (recorded, not hidden): E5 static-label
  self-certification (cannot be made checkable without
  render-order evidence — needs a test-design proposal);
  C5/A3 hand-provenance relabeling risk (needs renderer
  instrumentation — manual provenance remains the check);
  remaining silent-harm/minor items (coverage budget: each fix
  needs task coverage; the 5 above are checkable and
  high-leverage).

Counts after this draft: SKILL.md 119 lines (unchanged — all
fixes are substring replacements), PROVENANCE 368 + this section,
total within the 600 budget (verified by line count at draft
time; see the round floor record).
