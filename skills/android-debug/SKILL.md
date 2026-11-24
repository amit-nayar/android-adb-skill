---
name: android-debug
description: Debug Android issues using android-adb device, screenshot, app, and debug commands.
allowed-tools: Bash(android-adb:*), Bash(adb:*)
argument-hint: issue to investigate
---

Debugging workflow:

1. Collect context with `android-adb device info --json`, `android-adb app current --json`, and `android-adb screenshot --json`.
2. If reproducing a bug, clear logs first with `android-adb debug clear-logs --json`.
3. Collect logs with `android-adb debug logs --json`, adding `--package` and `--level` when relevant. `--package` only works while the app is running; after a crash, omit it and use `--level E` to find the `AndroidRuntime` stack trace.
4. Correlate the logs with the current screen and the user's report.
5. Report:
   - what happened
   - the strongest evidence
   - likely root cause
   - the next debugging step

Use raw `adb` only for diagnostics not yet covered by the command layer.
