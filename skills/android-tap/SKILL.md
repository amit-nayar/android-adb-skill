---
name: android-tap
description: Tap Android elements or coordinates through android-adb input commands.
allowed-tools: Bash(android-adb:*), Bash(adb:*)
argument-hint: element or coordinates to tap
---

Default to semantic tapping:

1. If the target is described by text, resource-id, or content description, run `android-adb input tap-element ... --json`. Add `--exact` when the label is short or a prefix of other labels ("Log" vs "Logout").
2. If the user gave coordinates, run `android-adb input tap --x ... --y ... --json`.
3. After tapping, verify the result with `android-adb ui dump --json` or `android-adb wait element ... --json`.

If the target is not visible, switch to `android-scroll` before falling back to raw coordinates.
