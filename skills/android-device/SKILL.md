---
name: android-device
description: Manage Android devices and emulators through ./tools/android device commands.
allowed-tools: Bash(./tools/android:*), Bash(adb:*), Bash(emulator:*)
argument-hint: device or emulator action to perform
---

Use:

- `./tools/android device list --json`
- `./tools/android device info --json`
- `./tools/android device avds --json`
- `./tools/android device start-emulator --avd-name ... --json`

Guidelines:

1. Report connected devices first when the request is ambiguous.
2. Use explicit device IDs when multiple devices are attached.
3. After starting an emulator, wait for boot completion before handing control back.
