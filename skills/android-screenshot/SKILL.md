---
name: android-screenshot
description: Capture and analyze an Android device screenshot
allowed-tools: Bash(adb:*), Read
argument-hint: "[optional] what to look for or where to save"
---

Capture a screenshot from the connected Android device and analyze it.

**User request:** $ARGUMENTS

## Steps

### 1. Capture the screenshot

```bash
adb exec-out screencap -p > /tmp/android-screenshot.png
```

If a specific save path was requested, also copy it there.

### 2. View the screenshot

Use the Read tool to view `/tmp/android-screenshot.png`. You can see images directly.

### 3. Analyze

If the user asked about something specific, describe what you see in relation to their question. Otherwise, provide:
- What app/screen is currently shown
- Key UI elements visible (buttons, text fields, labels)
- Any notable state (errors, loading indicators, dialogs)

### 4. Optional: Get UI tree for details

If you need more precise information about elements (resource-ids, exact text, clickable state):

```bash
adb shell uiautomator dump /dev/tty
```

## Multi-device

If multiple devices are connected, check first with `adb devices -l` and use `adb -s <device_id>` for the target device.

## If screencap fails

Try the file-based approach:
```bash
adb shell screencap -p /sdcard/screenshot.png
adb pull /sdcard/screenshot.png /tmp/android-screenshot.png
adb shell rm /sdcard/screenshot.png
```
