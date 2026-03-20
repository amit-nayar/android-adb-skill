# Android Command Contract

This repo now centers on one executable interface:

```bash
./tools/android ...
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
./tools/android device list --json
./tools/android device info --device emulator-5554 --json
./tools/android device avds --json
./tools/android device start-emulator --avd-name Pixel_9 --json
```

### Screenshots

```bash
./tools/android screenshot --out /tmp/screen.png --json
```

### UI

```bash
./tools/android ui dump --json
./tools/android ui find --by text --value "Login" --json
./tools/android ui find --by resource-id --value btn_login --json
```

### Input

```bash
./tools/android input tap --x 540 --y 1600 --json
./tools/android input tap-element --by text --value "Login" --json
./tools/android input text --text "user@example.com" --json
./tools/android input key --key back --json
./tools/android input swipe --x1 540 --y1 1800 --x2 540 --y2 600 --duration 300 --json
```

### Wait / Scroll

```bash
./tools/android wait element --by text --value "Home" --timeout 10000 --json
./tools/android scroll find --by text --value "Privacy" --max-scrolls 10 --json
```

### App

```bash
./tools/android app install --apk ./app/build/outputs/apk/debug/app-debug.apk --json
./tools/android app launch --package com.example.app --json
./tools/android app current --json
```

### Debug

```bash
./tools/android debug clear-logs --json
./tools/android debug logs --package com.example.app --level E --lines 300 --json
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
- App/debug commands should preserve enough raw output to troubleshoot failures.
