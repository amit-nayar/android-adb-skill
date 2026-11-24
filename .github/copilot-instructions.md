# Android Automation

Use the `android-adb` command for Android device work (or `bin/android-adb` from the android-adb-skill checkout if it is not on `PATH`).

Run `android-adb guide contract` for the command surface and `android-adb guide <skill>` for task-specific workflows, for example `android-adb guide android-test`.

Default behavior:

- Prefer `android-adb ... --json` over raw `adb`.
- Pass `--device <id>` when the target device is known or multiple devices are connected.
- Verify state after each interaction with `ui dump`, `wait element`, or `screenshot`.
