---
name: android-device
description: Manage Android devices and emulators through android-adb device commands.
allowed-tools: Bash(android-adb:*), Bash(adb:*), Bash(emulator:*)
argument-hint: device or emulator action to perform
---

Use:

- `android-adb device list --json`
- `android-adb device info --json`
- `android-adb device avds --json`
- `android-adb device start-emulator --avd-name ... --json`

Guidelines:

1. Report connected devices first when the request is ambiguous.
2. Use explicit device IDs when multiple devices are attached.
3. After starting an emulator, wait for boot completion before handing control back.
