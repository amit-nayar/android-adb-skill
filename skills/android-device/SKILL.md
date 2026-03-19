---
name: android-device
description: Manage Android devices and emulators
allowed-tools: Bash(adb:*), Bash(emulator:*), Read
argument-hint: "[optional] action (e.g., 'list', 'start Pixel_7_API_34', 'info')"
---

Manage Android devices and emulators.

**Action:** $ARGUMENTS

## Available actions

### List connected devices
```bash
adb devices -l
```
Shows device ID, state (device/offline/unauthorized), and transport info.

### List available AVDs (emulators)
```bash
emulator -list-avds
```

### Start an emulator
```bash
emulator -avd <avd_name> -no-snapshot-load &
```
Wait for it to come online:
```bash
adb wait-for-device
sleep 5
adb shell getprop sys.boot_completed
```
Poll `sys.boot_completed` until it returns `1` (up to 60 seconds).

### Get device info
```bash
echo "Model: $(adb shell getprop ro.product.model)"
echo "Manufacturer: $(adb shell getprop ro.product.manufacturer)"
echo "Android: $(adb shell getprop ro.build.version.release)"
echo "API Level: $(adb shell getprop ro.build.version.sdk)"
echo "Screen: $(adb shell wm size)"
echo "Density: $(adb shell wm density)"
echo "Serial: $(adb shell getprop ro.serialno)"
echo "Build: $(adb shell getprop ro.build.display.id)"
```

### Check ADB setup
Verify ADB is installed and accessible:
```bash
which adb
adb version
adb devices
```

If ADB is not found, check common locations:
- `$ANDROID_HOME/platform-tools/adb`
- `~/Library/Android/sdk/platform-tools/adb` (macOS)
- `~/Android/Sdk/platform-tools/adb` (Linux)

## Default action

If no specific action is requested, list connected devices and show basic info for each.
