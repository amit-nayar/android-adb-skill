---
name: android-navigate
description: Navigate to a specific screen on an Android device
allowed-tools: Bash(adb:*), Read
argument-hint: "destination (e.g., 'Settings > Account > Privacy', 'home screen', 'com.myapp login page')"
---

Navigate to a specific screen or location on the connected Android device.

**Destination:** $ARGUMENTS

## Approach

This is a composite skill — it combines screenshots, UI inspection, tapping, and verification to navigate through multiple screens.

### 1. Understand the starting point

Take a screenshot and get the UI tree to understand where we are:
```bash
adb exec-out screencap -p > /tmp/screen.png
adb shell uiautomator dump /dev/tty
```
Read the screenshot to understand the current screen.

### 2. Plan the navigation path

Break the destination into discrete steps. For example:
- `Settings > Account > Privacy` → tap Settings, then Account, then Privacy
- `home screen` → press Home key
- `com.myapp login page` → launch the app, wait for login screen

### 3. Execute each step

For each navigation step:

**a. Find the target element**
- Dump the UI tree
- Search by text, resource-id, or content-desc
- If the target is a menu item, look for matching text in the UI tree

**b. Tap it**
```bash
adb shell input tap <centerX> <centerY>
```

**c. Wait for the screen to settle**
```bash
sleep 0.8
```

**d. Verify we arrived at the next screen**
```bash
adb shell uiautomator dump /dev/tty
```
Check that the expected content for this step is now visible.

### 4. Handle special cases

**Launch an app:**
```bash
adb shell am start -a android.intent.action.MAIN -c android.intent.category.LAUNCHER <package>
```
Or with a specific activity:
```bash
adb shell am start -n <package>/<activity>
```

**Go home:**
```bash
adb shell input keyevent 3
```

**Go back:**
```bash
adb shell input keyevent 4
```

**Open recent apps:**
```bash
adb shell input keyevent 187
```

**Open notification shade:**
```bash
adb shell input swipe 540 0 540 1000 300
```

### 5. If a step fails

- The target element may be off-screen — try scrolling down:
  ```bash
  adb shell input swipe 540 1500 540 500 300
  ```
- The app may be loading — wait and retry:
  ```bash
  sleep 1
  adb shell uiautomator dump /dev/tty
  ```
- The target may use a different label — take a screenshot to see what's actually on screen and adapt

### 6. Confirm arrival

Take a final screenshot and report:
- Which screen we arrived at
- Key elements visible
- Whether it matches the requested destination
