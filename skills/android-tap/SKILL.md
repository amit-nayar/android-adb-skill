---
name: android-tap
description: Tap Android elements or coordinates through ./tools/android input commands.
allowed-tools: Bash(./tools/android:*), Bash(adb:*)
argument-hint: element or coordinates to tap
---

Default to semantic tapping:

1. If the target is described by text, resource-id, or content description, run `./tools/android input tap-element ... --json`.
2. If the user gave coordinates, run `./tools/android input tap --x ... --y ... --json`.
3. After tapping, verify the result with `./tools/android ui dump --json` or `./tools/android wait element ... --json`.

If the target is not visible, switch to `android-scroll` before falling back to raw coordinates.
