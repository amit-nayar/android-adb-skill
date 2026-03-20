---
name: android-gesture
description: Perform Android gestures through ./tools/android input commands.
allowed-tools: Bash(./tools/android:*), Bash(adb:*)
argument-hint: gesture to perform
---

Map requests to command-layer actions:

- tap: `input tap`
- long press: `input swipe` from a point to itself with a long duration
- swipe / drag: `input swipe`
- double tap: run two `input tap` commands in sequence and then verify

If the user names an element instead of coordinates, resolve it first with `ui find` or `input tap-element`.

After the gesture, verify with `ui dump` or `screenshot`.
