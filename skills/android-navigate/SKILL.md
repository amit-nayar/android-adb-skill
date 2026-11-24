---
name: android-navigate
description: Navigate to a target Android screen by chaining android-adb UI, input, wait, and screenshot commands.
allowed-tools: Bash(android-adb:*), Bash(adb:*)
argument-hint: destination to reach on the device
---

Navigation workflow:

1. Establish current state with `android-adb ui dump --json` and optionally `android-adb screenshot --json`.
2. Break the destination into discrete steps.
3. For each step:
   - find the target with `ui find`
   - interact with `input tap-element` or another `input` command
   - verify with `wait element` or `ui dump`
4. If a target is off-screen, use `scroll find`.
5. Finish with a final verification screenshot or UI dump and report where you landed.
