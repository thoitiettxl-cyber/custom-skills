---
name: apk-reverse
description: Reverse Android APKs from the CLI — unpack, decompile, patch smali, rebuild, and hook with Frida.
---

# Analyzing Android APKs on the CLI: unpacking, patching smali, rebuilding, and hooking with Frida — use when you need to reverse an APK, patch logic, or observe an app at runtime

> **Source & adaptation.** Adapted from `skills/apk-reverse` in
> [zhaoxuya520/reverse-skill](https://github.com/zhaoxuya520/reverse-skill)
> (MIT License, Copyright (c) 2026 zhaoxuya520).
> This deployment is English-only and Linux-focused:
> - Upstream docs were bilingual (EN/ZH); everything here is English
>   (H1 in Vietnamese per local convention — skill search indexes the H1).
> - Only the Linux scripts (`scripts/*.sh`) are included. The upstream
>   Windows `.ps1` variants depend on that repo's `scripts/lib/` infrastructure
>   (`ToolDiscovery.ps1`, `bootstrap-reverse.ps1`) and cannot run standalone —
>   see upstream for Windows.
> - The upstream auto-bootstrap hook is replaced by detection-only tool checks
>   with manual install hints. Scripts never download or install anything.
> - Upstream `references/` docs were not imported (Chinese-language).
> - Behavior described below follows the actual script code (surveyed 2026-10-15),
>   not upstream marketing copy — where docs and code disagreed, code won.

## When to use

- Inspect an APK's Java business logic (login, signing, cert pinning, root detection)
- Read or modify `AndroidManifest.xml` and smali
- Repack, align, sign and reinstall a modified APK
- Dynamically hook Java/native methods with Frida
- Hand off to native analysis when the APK ships important `.so` files

## Scripts

All scripts are `bash` (`set -euo pipefail`). They **detect** required tools
and print install hints when missing — they never install anything themselves.

| Script | Purpose |
| ------ | ------- |
| `scripts/decode.sh` | Run `jadx` + `apktool` on an APK; print package / java / smali / so summary |
| `scripts/frida-run.sh` | Unified Frida entry: list devices/processes, spawn or attach with a JS hook |
| `scripts/rebuild-sign-install.sh` | `apktool b` → `zipalign` → `apksigner` → optional `adb install`; auto-generates a debug keystore if missing |

### `decode.sh`

```bash
bash scripts/decode.sh app.apk
bash scripts/decode.sh app.apk --name demo --out /tmp/work --skip-jadx
bash scripts/decode.sh app.apk --clean   # wipe previous output first
```

Output lands in `<apk-dir>/<name>/{jadx,apktool}` plus a summary
(package, exit codes, file counts). Tolerates partial jadx failures —
a non-zero jadx exit still leaves usable artifacts.

### `frida-run.sh`

```bash
bash scripts/frida-run.sh --list-devices
bash scripts/frida-run.sh --usb --list-processes
bash scripts/frida-run.sh --usb --spawn --package com.example.app --script hook.js
bash scripts/frida-run.sh --package com.example.app --script hook.js   # attach over TCP 127.0.0.1:27042
```

### `rebuild-sign-install.sh`

```bash
bash scripts/rebuild-sign-install.sh apktool_out
bash scripts/rebuild-sign-install.sh apktool_out --install --reinstall --device 127.0.0.1:7555
bash scripts/rebuild-sign-install.sh apktool_out --out /tmp/signed --name patched
```

Generates `~/.android/debug.keystore` on first use (override with `--keystore`).
Produces `<name>-unsigned.apk`, `<name>-aligned.apk`, `<name>-signed.apk`.

## Toolchain

| Tool | Used for | Install |
| ---- | -------- | ------- |
| `jadx` | Java decompile | https://github.com/skylot/jadx/releases |
| `apktool` | Unpack / repack, smali | https://apktool.org/docs/install/ |
| `frida`, `frida-ps` | Dynamic hooking | `pip3 install frida-tools` |
| `adb` | Install, logcat, pull | `sudo apt install adb` |
| `zipalign`, `apksigner` | Align + sign | `sudo apt install android-sdk-build-tools` or `sdkmanager "build-tools;35.0.0"` |
| `keytool`, `java` | Debug keystore | `sudo apt install default-jdk` |

**Login shell:** on Muse the full toolchain (`~/.local/bin`, `~/.local/jdk-21/bin`) is only on PATH in a login shell — run commands via `bash --login -c '...'` if `which <tool>` comes up empty.

## Recommended workflow

1. **Triage** — `decode.sh`: check the manifest, main package, components,
   and whether `lib/` contains `.so` files. Don't rush to patch or hook.
2. **Java** — read the jadx output first (`MainActivity`, `Application`,
   login/crypto/network classes, third-party SDK init).
3. **Smali** — drop to `apktool_out/smali*/` when jadx output is incomplete,
   heavily obfuscated, or an actual patch is needed (`res/values/strings.xml`,
   `AndroidManifest.xml`).
4. **Rebuild** — `rebuild-sign-install.sh` for the full
   repack → align → sign → install loop.
5. **Hook** — `frida-run.sh`: hook the Java layer first
   (login, OkHttp/Retrofit, `javax.crypto`, root/SSL checks);
   go native only if needed. Print args/return values before modifying them.
6. **Native** — if `.so` carries the core logic (Java is just a JNI wrapper),
   switch to the `ghidra` / IDA / radare2 skills.

Rules of thumb: don't patch smali blind before reading the manifest and entry
points; don't write hooks before knowing the target class/method; don't keep
digging in Java when the real logic lives in `.so`.

## Notes

- During the 2026-10-15 survey, upstream docs and code disagreed in places
  (doc version numbers vs manifest pins; doc described Frida setup as
  manual-only while the Linux script does detection). This file follows the code.
- Dynamic analysis only on devices you own or are explicitly authorized to test.
