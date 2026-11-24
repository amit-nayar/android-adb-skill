# Android Command Contract

This repo centers on one executable interface, `bin/android-adb` (it runs `tools/android`):

```bash
android-adb ...
```

Skills and agent adapters should prefer this command surface over raw `adb` calls. Fall back to raw `adb` only when a needed operation is not implemented yet.

## Design Rules

- Prefer `--json` for machine-readable output.
- Prefer `--device <id>` when the user named a device.
- If multiple devices are attached and no `--device` is provided, the command exits non-zero and lists candidates.
- Commands should fail with non-zero exit codes and a clear error message instead of returning ambiguous prose.

## Core Commands

### Device

```bash
android-adb device list --json
android-adb device info --device emulator-5554 --json
android-adb device avds --json
android-adb device start-emulator --avd-name Pixel_9 --json
```

### Screenshots

```bash
android-adb screenshot --out /tmp/screen.png --json
```

### UI

```bash
android-adb ui dump --json
android-adb ui find --by text --value "Login" --json
android-adb ui find --by resource-id --value btn_login --json
android-adb ui find --by text --value "Log in" --exact --json
```

`--by text` and `--by content-desc` match a case-insensitive substring by default. `--exact` requires the whole value to match. `ui find`, `input tap-element`, `wait element` and `scroll find` all accept `--exact`. Exact matches always rank above partial ones.

### Input

```bash
android-adb input tap --x 540 --y 1600 --json
android-adb input double-tap --x 540 --y 1600 --json
android-adb input tap-element --by text --value "Login" --json
android-adb input text --text "user@example.com" --json
android-adb input key --key back --json
android-adb input swipe --x1 540 --y1 1800 --x2 540 --y2 600 --duration 300 --json
```

### Wait / Scroll

```bash
android-adb wait element --by text --value "Home" --timeout 10000 --json
android-adb scroll find --by text --value "Privacy" --max-scrolls 10 --json
android-adb scroll find --by text --value "Item 20" --direction right --container-by resource-id --container-value carousel --json
```

`wait element` keeps retrying failed UI dumps until the timeout, but fails immediately if the device disconnects. The timeout error includes the last dump error.

### App

```bash
android-adb app install --apk ./app/build/outputs/apk/debug/app-debug.apk --json
android-adb app launch --package com.example.app --json
android-adb app current --json
android-adb app stop --package com.example.app --json
android-adb app clear-data --package com.example.app --json
android-adb app uninstall --package com.example.app --json
```

### Debug

```bash
android-adb debug clear-logs --json
android-adb debug logs --package com.example.app --level E --lines 300 --json
```

`--package` keeps only lines from the app's running processes and then applies `--lines`. If the app is not running the command fails instead of returning unfiltered logs; omit `--package` to read logs from an exited process, such as a crash.

### Text input

`input text` types printable ASCII. Newlines and tabs are sent as Enter and Tab key presses. Other characters (emoji, accented letters) are rejected with an error, because `adb shell input text` cannot type them. The JSON output lists the `steps` that were sent.

### Guides

```bash
android-adb guide             # list guides
android-adb guide contract    # this document
android-adb guide android-tap # a skill workflow
```

## Skill Guidance

- `android`: route to the right command family and keep verifying after each step.
- `android-ui`: use `ui dump` / `ui find` and summarize the result.
- `android-tap`: use `input tap-element` first; only fall back to coordinate tap when needed.
- `android-navigate`: chain `ui find`, `input tap-element`, `wait element`, and screenshots.
- `android-test`: use command outputs as evidence, not inferred prose.
- `android-install`: install first, then launch explicitly; do not guess the package from unrelated shell output.

## Output Conventions

- Screenshots should return the saved path plus dimensions when available.
- UI commands should return `bestMatch` and `matches` in JSON mode.
- Wait/scroll commands should report elapsed time or scroll count.
- `device start-emulator` writes the emulator's output to a log file and returns its `logPath`. If the emulator exits before booting, the command fails immediately with the end of that log.
- App/debug commands should preserve enough raw output to troubleshoot failures.
