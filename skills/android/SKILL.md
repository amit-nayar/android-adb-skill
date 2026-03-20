---
name: android
description: General-purpose Android automation. Use for multi-step Android tasks that should be executed through the local ./tools/android command layer instead of raw adb.
allowed-tools: Bash(./tools/android:*), Bash(adb:*), Glob
argument-hint: what you want to do on the Android device
---

Use `./tools/android` as the default execution layer. Read `docs/command-contract.md` if you need the exact command surface.

Workflow:

1. Start with `./tools/android device list --json`.
2. If multiple devices are attached and the user did not choose one, stop and ask.
3. Break the request into steps and route each step to the right command family:
   - screenshots: `screenshot`
   - UI inspection: `ui dump`, `ui find`
   - interaction: `input ...`
   - waits: `wait element`
   - scrolling: `scroll find`
   - app lifecycle: `app ...`
   - logs: `debug ...`
4. Prefer `--json` and reason from structured output.
5. After every interaction, verify with `ui dump`, `wait element`, or `screenshot`.

Fallback to raw `adb` only if the command layer cannot do the required operation.
