---
name: android-install
description: Install and launch an Android APK through android-adb app commands.
allowed-tools: Bash(android-adb:*), Bash(adb:*), Glob
argument-hint: path or name of the APK to install
---

Install flow:

1. Resolve the APK path with `Glob` if needed.
2. Run `android-adb app install --apk <path> --json`.
3. If the command returns a package name, launch it with `android-adb app launch --package <package> --json`.
4. If the package name is unknown, stop and ask for it instead of guessing.
5. Verify launch with `android-adb app current --json` and `android-adb screenshot --json`.

Do not infer the package from unrelated shell output such as a recent package list.

To reset state between runs, use `android-adb app stop --package <package> --json` (force-stop) or `android-adb app clear-data --package <package> --json` (also wipes data). Remove the app with `android-adb app uninstall --package <package> --json`.
