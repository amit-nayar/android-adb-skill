---
name: android-scroll
description: Scroll until an Android element is visible by using android-adb scroll find.
allowed-tools: Bash(android-adb:*), Bash(adb:*)
argument-hint: element to find while scrolling
---

Use `android-adb scroll find --by ... --value ... --json`.

Options:

- `--direction down|up|left|right` sets which way to reveal content (default `down`). Use `left`/`right` for carousels and tabs.
- `--container-by ... --container-value ...` scrolls inside one element (a list, a carousel) instead of the whole screen. Find the container's `resource-id` with `ui dump` first; scrollable elements have `"scrollable": true`.
- `--exact` requires the whole text to match, so "Log" does not find "Logout".

Guidelines:

1. Choose the selector that best matches the request.
2. Report how many scrolls were needed and what element was found.
3. If the element is still missing, say so explicitly and summarize what you observed instead.
4. If the user likely wants to interact with the found element, follow with `input tap-element`.
