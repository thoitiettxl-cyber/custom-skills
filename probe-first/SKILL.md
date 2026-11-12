---
name: probe-first
description: Use whenever you are about to report that something cannot be done, is impossible, is unavailable, is not supported, or does not work — especially when the only evidence is reasoning, a document, an error from a different path, or another agent's report, and no direct test of the claimed thing has run. Write the smallest probe first, measure, and report from the measurement. Do not repeat an untested limit as a fact. Also use whenever you are about to write new code, UI, config, docs or a helper — check what already exists (repo, the fork/template, dependencies, docs) and reuse it before building anything.
---

# Probe first: write the smallest probe before declaring impossible, unavailable, or broken — use when about to report something cannot be done, when the only evidence is reasoning, or when repeating a limit nobody tested (chưa viết đã lo báo là không được)

## The rule

Boss's words, verbatim: "chưa viết đã lo báo là không được" — reporting "it can't be done" before anything has been written and tried is the wrong way to work. An impossibility claim is a claim about reality, and reality is checked by running something, not by reasoning about it.

No sentence of the form "X cannot / does not / is impossible" leaves this session unless one of these is true:

- a probe of X itself ran in this session and failed, with the command and output on record; or
- the sentence is explicitly marked as untested reasoning ("chưa kiểm chứng"), with the exact probe that would settle it named.

A failed attempt down a *different* path is not a probe of X. A document that does not mention X is not a probe of X. Another agent's report that X failed is not a probe of X — it is a lead for your own probe.

## Reuse first (the build-side twin)

The rule above stops untested "can't be done". This section stops untested "doesn't exist". Before writing anything — code, UI, config, docs, or a helper — check what already exists and reuse it before building anything.

1. **Search first, in this order:** the repo; the forked upstream or template the work derives from; the current dependencies and their docs; the project's own docs and patterns. Record where you looked and what you found, in the report or the plan — "checked, nothing exists" is a claim that needs the same evidence standard as any other.
2. **If it exists, use it as-is.** A component, function, config, or pattern that does the job is the job done. Restyling it, re-implementing it, or wrapping it in a parallel version is not using it.
3. **If it falls short, extend that thing.** Add the missing case, prop, or branch to the existing component/function/config — never write a parallel version alongside it. A parallel version is two things to maintain and a standing invitation for them to drift.
4. **Writing your own is allowed only after a probe shows the existing one cannot do the job, with evidence.** Same standard as impossibility claims: the probe is a direct test of the existing thing against the requirement (render it, call it, load the config), with the command and output on record — not reasoning, not a doc that does not mention the requirement, not another agent's report.
5. **Self-review check before reporting:** did I re-style, re-implement, or duplicate anything that already existed? Name each reused thing in the report, and each place where you extended rather than duplicated. If the answer is "I built a parallel version because it was faster", that is the failure this section exists to catch — say so and fix it before reporting.

## When this triggers

Use this skill when any of these is true:

- You are about to write "cannot", "impossible", "not supported", "does not work", "unavailable", or "no way to" about a tool, a config, a mechanism, or a system behaviour.
- Your evidence is a doc, a template, an error message from a different operation (for example a scaffold tool failing), or a chain of reasoning — but nothing that directly exercised the claimed thing.
- You are about to repeat a limit stated in a prior report, plan, or memory note without re-measuring it.
- The fix would be small *if* the mechanism works (a few lines of config, one descriptor file, one flag). Small fixes deserve small probes, not long arguments.

## The probe recipe

1. **State the claim precisely, plus its falsifier.** One sentence for the claim ("the catalog cannot list a connector without a registered connection"), one sentence for the observation that would disprove it ("a hand-written descriptor with no credential appears in search results").
2. **Build the smallest probe that could falsify it.** Write it against the documented surface — see `search-playbook` for finding the right docs first. Scratch-only, reversible, no edits to live files, no fake credentials, registrations, hosts, or secrets. If the probe only runs with an invented value, stop: that by itself proves the mechanism needs something real — report that, do not invent the value.
3. **Record the baseline first.** Run the failing behaviour before the probe and keep the command and output (the exact error, the exact search result).
4. **Run the probe and capture evidence correctly** (see Measurement hygiene). Keep the probe's exact input and the exact output.
5. **Restore the baseline.** Delete every scratch artifact, re-run the baseline check, and confirm the result is identical to step 3. A probe that leaves residue behind is not a probe, it is an unapproved change.
6. **Restate the claim from the measurement only.** If the probe worked, the *fix* still needs its own approval before any live file changes — a successful probe authorises nothing except the report. Applying the fix is a separate, approved change.

## Diagnosing a failure: separator first, then one layer at a time

When something fails, do not debug each failing case separately. First find the separator: one experiment that decides which side is at fault.

**Read the current version, never memory or an old summary.** Before acting on a doc, a config, or code, open the current file and read it. Memory notes and summaries — including your own earlier reports — lag edits and drop details. When they disagree with the live file, the live file wins; re-read it before deciding or editing.

1. **Same symptom on different systems → the shared side is suspect.** If two different systems (different servers, different protocols) fail in exactly the same place, the cause is almost certainly in the component they share — the client, the helper, the proxy path — not in either system. Debugging the systems first wastes the session.
2. **A theory must explain every case.** A theory that explains one failing case but contradicts another is wrong or incomplete, however well documented. Discard it and keep looking; do not keep patching it case by case.
3. **Test one layer at a time, smallest probe first.** Decompose the path into layers (client → helper → proxy → network → server) and test the lowest layer directly, with no other layer involved: a raw socket, a timestamped byte log. Only when a layer is proven good move up to the next suspect.
4. **Trust bytes on the wire, not "sent" in a log.** A log line saying a message was "sent" means the program wrote it to its own pipe or buffer — not that the bytes reached the peer. Record what actually arrived, with timestamps and byte counts, before concluding anything about either direction.
5. **Read the suspect component's code.** When the probe narrows the fault to one component, open that component and read it. The bug is often a single call whose semantics differ from what the author assumed (see the buffering entry in Measurement hygiene).
6. **Prove the fix by re-running the same failing probe.** A fix is proven only when the exact probe that failed now passes. An argument that the fix "should" work is not proof.

## Measurement hygiene (real mistakes, kept)

- **Exit codes through a pipe lie.** `cmd | head; echo $?` reports `head`'s exit code, not the command's. A tab-close probe measured this way read exit 0; re-measured with a redirect it was exit 1 in both addressing forms. Capture exits without pipes: `cmd > out 2>&1; echo "exit=$?"`, then read the file.
- **Indexes lag writes.** A search index can show the previous version of a file after an edit. When a search snippet and a direct read disagree, the direct read wins. Re-read a file before editing it; never edit from a search snippet alone.
- **PIDs, ports, and process state are ephemeral.** Never hardcode a PID, a port occupant, or a "services are up" claim from an earlier report. Resolve them live every time (listener → PID → `/proc/<pid>/cmdline` verification before signalling anything).
- **Buffered reads block for the full request.** `BufferedReader.read(n)` waits until `n` bytes arrive or EOF — it does not return the bytes already available. Never use it in a streaming relay: small packets (an SSH version string, a KEXINIT) sit in the buffer forever while the peer waits. Use `os.read` (one syscall, returns what is available) and `os.write` in a loop for partial writes. Measured 2026-11-02: a CONNECT helper using `read(65536)` produced banner-only SSH stalls to two different servers; switching to `os.read`/`os.write` made KEX complete in 2.6 s.

## Worked example: the connector.yaml discovery gap (2026-10-27)

The claim, repeated through a whole build: `muse.connector_search` cannot find a local no-credential connector, because discovery needs a registered connection plus a `connector.yaml`, and no registration exists for a local binary. The evidence offered: the scaffold tool failed for the codemode precedent with "no connector named custom.codemode is registered", and creating a descriptor unilaterally would be a fake registration. The Floor check for discovery failed, honestly, on that reasoning — and the reasoning was wrong.

What nobody had done: read the descriptor template and try a truthful one. The template (`/opt/muse/skills/custom-connector-setup/templates/connector/connector.yaml`) has five fields, no hosts, no credential fields — and its own comment says of `require_auth`: "Use false for a public API that needs no credential." A no-credential descriptor was an expressible, designed form, not a fake.

The probe (Boss: "tại sao không tìm cách connector.yaml"): a scratch directory `custom.__yaml_probe__` holding only a five-field `connector.yaml` (`require_auth: false`, `include_in_prompt: false`, no hosts, no credential, nothing invented). Search found it immediately — "YAML Probe" with the probe's description — with only a documentation error for the absent `CONNECTOR.md`. The scratch directory was deleted and the baseline re-verified (probe gone, the two original catalog errors back). The mechanism was proven; the fix — truthful `connector.yaml` files in the two live connector directories, `custom.patchright-cli` and `custom.codemode` — was then applied under a separate Boss approval, and search finds both with zero catalog errors.

The lesson is not "yaml fixes everything". It is: the gap between "the scaffold needs registration" and "a descriptor needs registration" was never tested, and one five-line probe closed it.

## Worked example: web UI fork (2026-10-29)

The fork of the Management Center shipped upstream's Button, Card, and header/topbar components plus its theme and styles — the CSS was present and the global stylesheet was imported. Yet the header actions (language, theme, log out) were written as bare `<button>` elements with no `className`, so no upstream rule applied to them: the page looked unstyled — raw browser-default buttons, default-looking text — while the styled components sat unused one import away. Other pages had already used the upstream components; the header had not. The fix was not new CSS and not a new component: use upstream's components and theme only — `Button variant="ghost"` triggers, the upstream theme-menu swatch popover, the toggle moved into `<header>` where its rule lives.

The failure is the same shape as the connector.yaml example above: a template existed and was not used. There, a descriptor form existed and the build worked around it; here, components existed and the markup worked around them. In both cases the search that would have found the existing thing — read the template, read the upstream markup — was never run before building. Reuse first: the existing thing is found by reading it, not by reasoning that it must not fit.

## Worked example: the SSH KEX stall (2026-11-02)

Two SSH targets failed identically: a phone Debian box (plain OpenSSH) and a VM (Tailscale SSH). Both returned a banner, then nothing — KEX never completed. The theories in play each explained only one case: Tailscale SSH check-mode (documented, real) explains the VM but not the phone; a missing tunnel approval explains the first failures but not the stall after approval. Both were discarded as incomplete.

The separator: from a third machine on the same tailnet, SSH to the VM worked, including the browser check step. The targets were fine; the fault was on the Muse VM side.

The layer probe: a raw socket through the same tunnel proxy, no SSH client, no helper — send a client version string, log every received chunk with a timestamp. The server's KEXINIT arrived within 0.5 s of sending the version. Tunnel and server proven good; the suspect was the helper or the client.

The code read: the helper relayed its stdin with `sys.stdin.buffer.read(65536)`, which blocks until 64 KiB or EOF — the client's small version and KEXINIT packets were never forwarded, so each server sent its banner and waited forever. One direction worked (banner out), the other never did, exactly matching the symptom.

The proof: fix the helper to `os.read`/`os.write`, re-run the same failing probe. KEX completed in 2.6 s, the host-key fingerprint matched the expected value exactly, and the login succeeded. The lesson is the section above: separator first, one layer at a time, bytes on the wire, read the suspect, re-run the same probe.

## What a probe must never do

- Write into a live directory "temporarily". Scratch first, always; live only after approval.
- Create a registration, credential, account, host entry, or any claim about a remote system to make the probe run.
- Use a real secret, token, or proxy value as probe input.
- Report a probe result as the fix. The probe proves the mechanism; the fix is applied, verified, and reported separately.
- Relabel a failed probe as "probably works", or a probe that was never run as "expected to fail".

## Related skills

- `verify-before-claiming`: read it when the claim is about a tool, library, or repo's documented behaviour — check the primary source before asserting anything about current state. This skill covers the other half: claims about what can be done here, on this VM, which only a run can settle.
- `tdd`: read it when the probe is code at an agreed seam (red → green). This skill is the umbrella over every domain, not just code: config, discovery, tool behaviour, system limits.
- `search-playbook`: read it before writing the probe — a probe needs the real API surface (docs, flags, schemas, current behaviour) to be a fitting test. It routes need → lookup channel across web search, docs MCPs, Exa, Firecrawl, Context7, vendor docs, and local repo search. A probe written without the docs is a guess, not a test.
