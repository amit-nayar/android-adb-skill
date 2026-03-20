---
name: android-test
description: Execute a multi-step Android test flow using ./tools/android and report evidence-backed pass/fail results.
allowed-tools: Bash(./tools/android:*), Bash(adb:*), Glob
argument-hint: test flow to run
---

Testing workflow:

1. Clear logs with `./tools/android debug clear-logs --json`.
2. Capture the starting state with `./tools/android screenshot --out /tmp/android-test-start.png --json`.
3. Break the flow into explicit steps.
4. Execute each step through the command layer and verify after each action.
5. Save evidence screenshots at meaningful checkpoints.
6. Collect logs with `./tools/android debug logs --json`.
7. Report pass/fail with concrete evidence from command output, screenshots, and logs.

Do not claim success from intent alone. Every step needs observable confirmation.
