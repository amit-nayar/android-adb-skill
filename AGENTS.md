# Android Automation

Use the local command layer first:

```bash
./tools/android ...
```

Read [`docs/command-contract.md`](docs/command-contract.md) for the supported commands and output conventions. Read the relevant `skills/*/SKILL.md` file for task-specific workflow guidance.

## Default Behavior

- Prefer `./tools/android ... --json` over raw `adb`.
- If multiple devices are connected, pass `--device <id>` or stop and ask the user to choose.
- Verify state after each interaction with `ui dump`, `wait element`, or `screenshot`.
- Use raw `adb` only when the command layer does not support the required operation.

## Skill Entry Points

- `skills/android/SKILL.md` — General orchestration
- `skills/android-screenshot/SKILL.md` — Screenshots
- `skills/android-ui/SKILL.md` — UI inspection
- `skills/android-tap/SKILL.md` — Element tapping
- `skills/android-navigate/SKILL.md` — Navigation
- `skills/android-scroll/SKILL.md` — Scrolling
- `skills/android-gesture/SKILL.md` — Gestures
- `skills/android-test/SKILL.md` — Test flows
- `skills/android-debug/SKILL.md` — Debugging
- `skills/android-install/SKILL.md` — APK installation
- `skills/android-device/SKILL.md` — Device management
