---
name: android-install
description: Install an APK and launch it on an Android device
allowed-tools: Bash(adb:*), Read, Glob
argument-hint: "path to APK file (e.g., './app/build/outputs/apk/debug/app-debug.apk')"
---

Install an APK on the connected Android device and launch it.

**APK:** $ARGUMENTS

## Steps

### 1. Find the APK

If the user gave a specific path, use it. If they gave a partial path or just a name, search for it:
```bash
# Use Glob to find APK files matching the description
```

Verify the APK exists before proceeding.

### 2. Check device connection

```bash
adb devices -l
```

### 3. Install the APK

```bash
adb install -r <path_to_apk>
```

The `-r` flag replaces the existing installation if present.

If installation fails:
- **INSTALL_FAILED_UPDATE_INCOMPATIBLE** — Uninstall first, then retry:
  ```bash
  adb uninstall <package_name>
  adb install <path_to_apk>
  ```
- **INSTALL_FAILED_INSUFFICIENT_STORAGE** — Report to user
- **INSTALL_FAILED_INVALID_APK** — Check APK path, report to user

### 4. Identify the package name

Extract from the APK:
```bash
adb shell pm list packages -3 | tail -5
```
Or if aapt is available:
```bash
aapt dump badging <path_to_apk> 2>/dev/null | grep package:
```

### 5. Launch the app

```bash
adb shell monkey -p <package_name> -c android.intent.category.LAUNCHER 1
```

Or with a specific activity:
```bash
adb shell am start -n <package_name>/<activity_name>
```

### 6. Verify launch

Wait for the app to start, then check:
```bash
sleep 2
adb shell dumpsys activity activities | grep mResumedActivity
adb exec-out screencap -p > /tmp/app-launched.png
```

Read the screenshot to confirm the app launched successfully.

### 7. Report

- Installation result (success/failure)
- Package name
- App launched and what screen is showing
