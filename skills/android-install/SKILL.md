---
name: android-install
description: Install and launch an Android APK through ./tools/android app commands.
allowed-tools: Bash(./tools/android:*), Bash(adb:*), Glob
argument-hint: path or name of the APK to install
---

Install flow:

1. Resolve the APK path with `Glob` if needed.
2. Run `./tools/android app install --apk <path> --json`.
3. If the command returns a package name, launch it with `./tools/android app launch --package <package> --json`.
4. If the package name is unknown, stop and ask for it instead of guessing.
5. Verify launch with `./tools/android app current --json` and `./tools/android screenshot --json`.

Do not infer the package from unrelated shell output such as a recent package list.
