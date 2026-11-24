# Android Automation

Use the `android-adb` command for Android device work:

```bash
android-adb ...
```

If `android-adb` is not on `PATH`, run `bin/android-adb` from the android-adb-skill checkout.

Run `android-adb guide contract` for the supported commands and output conventions. Run `android-adb guide <skill>` for a task-specific workflow, for example `android-adb guide android-test`.

## Default Behavior

- Prefer `android-adb ... --json` over raw `adb`.
- If multiple devices are connected, pass `--device <id>` or stop and ask the user to choose.
- Verify state after each interaction with `ui dump`, `wait element`, or `screenshot`.
- Use raw `adb` only when the command layer does not support the required operation.

## Skill Guides

- `android` — General orchestration
- `android-screenshot` — Screenshots
- `android-ui` — UI inspection
- `android-tap` — Element tapping
- `android-navigate` — Navigation
- `android-scroll` — Scrolling
- `android-gesture` — Gestures
- `android-test` — Test flows
- `android-debug` — Debugging
- `android-install` — APK installation and app reset
- `android-device` — Device management
