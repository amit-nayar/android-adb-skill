---
name: android-ui
description: Inspect the Android UI hierarchy through android-adb ui dump and ui find.
allowed-tools: Bash(android-adb:*), Bash(adb:*)
argument-hint: optional element or screen details to inspect
---

Use:

- `android-adb ui dump --json` for an overview
- `android-adb ui find --by ... --value ... --json` for a specific element

Guidelines:

1. Prefer `resource-id`, then `text`, then `content-desc`.
2. Report the best match plus any ambiguity if there are multiple matches. Use `--exact` to match the whole text instead of a substring.
3. Include bounds, center coordinates, clickable/enabled state, and class when relevant.
4. If the element is missing, suggest `android-scroll` or a different screen.
