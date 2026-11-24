---
name: android-gesture
description: Perform Android gestures through android-adb input commands.
allowed-tools: Bash(android-adb:*), Bash(adb:*)
argument-hint: gesture to perform
---

Map requests to command-layer actions:

- tap: `input tap`
- double tap: `input double-tap` (one command, so the taps land close enough together)
- long press: `input swipe` from a point to itself with a long duration, for example `--duration 800`
- swipe / drag: `input swipe`

If the user names an element instead of coordinates, resolve it first with `ui find` or `input tap-element`.

After the gesture, verify with `ui dump` or `screenshot`.
