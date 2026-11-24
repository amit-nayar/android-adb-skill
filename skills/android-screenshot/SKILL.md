---
name: android-screenshot
description: Capture an Android screenshot through android-adb and analyze the result.
allowed-tools: Bash(android-adb:*), Bash(adb:*)
argument-hint: what to inspect on the current screen
---

Preferred flow:

1. Run `android-adb screenshot --json`.
2. If the user asked for visual analysis, inspect the saved image with the agent's local image-view capability if available.
3. If you need precise element data, also run `android-adb ui dump --json`.
4. Report what is visible and answer the user's question.

If the command layer fails for screenshot capture, fall back to raw `adb` only as a last resort.
