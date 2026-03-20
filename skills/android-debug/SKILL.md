---
name: android-debug
description: Debug Android issues using ./tools/android device, screenshot, app, and debug commands.
allowed-tools: Bash(./tools/android:*), Bash(adb:*)
argument-hint: issue to investigate
---

Debugging workflow:

1. Collect context with `./tools/android device info --json`, `./tools/android app current --json`, and `./tools/android screenshot --json`.
2. If reproducing a bug, clear logs first with `./tools/android debug clear-logs --json`.
3. Collect logs with `./tools/android debug logs --json`, adding `--package` and `--level` when relevant.
4. Correlate the logs with the current screen and the user's report.
5. Report:
   - what happened
   - the strongest evidence
   - likely root cause
   - the next debugging step

Use raw `adb` only for diagnostics not yet covered by the command layer.
