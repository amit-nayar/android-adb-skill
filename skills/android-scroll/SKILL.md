---
name: android-scroll
description: Scroll until an Android element is visible by using ./tools/android scroll find.
allowed-tools: Bash(./tools/android:*), Bash(adb:*)
argument-hint: element to find while scrolling
---

Use `./tools/android scroll find --by ... --value ... --json`.

Guidelines:

1. Choose the selector that best matches the request.
2. Report how many scrolls were needed and what element was found.
3. If the element is still missing, say so explicitly and summarize what you observed instead.
4. If the user likely wants to interact with the found element, follow with `input tap-element`.
