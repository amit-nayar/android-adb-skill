---
name: android-scroll
description: Scroll to find an element on an Android device
allowed-tools: Bash(adb:*), Read
argument-hint: "element to find (e.g., 'Privacy Policy link', 'Sign Out button')"
---

Scroll the Android device screen to find a specific element.

**Target element:** $ARGUMENTS

## Steps

### 1. Check if the element is already visible

```bash
adb shell uiautomator dump /dev/tty
```

Search the UI tree for the target by text, resource-id, or content-desc. If found, report its location and stop.

### 2. Get screen dimensions

```bash
adb shell wm size
```

Use the screen dimensions to calculate swipe coordinates. For a typical 1080x2400 screen:
- Swipe area: avoid top 200px (status bar) and bottom 200px (nav bar)
- Start Y: ~75% of screen height
- End Y: ~25% of screen height

### 3. Scroll and search loop

Repeat up to 10 times:

**a. Scroll down:**
```bash
adb shell input swipe 540 1800 540 600 300
```
(Adjust coordinates based on actual screen size)

**b. Wait for content to settle:**
```bash
sleep 0.5
```

**c. Dump UI tree:**
```bash
adb shell uiautomator dump /dev/tty
```

**d. Search for the element.**

If found, report its bounds and center coordinates.

**e. Check for end of scrollable content:**
Compare the current UI tree with the previous one. If they're identical, we've reached the bottom — the element doesn't exist on this screen.

### 4. Try scrolling up

If not found after scrolling down, try scrolling back up (the element might have been above the starting position):

```bash
adb shell input swipe 540 600 540 1800 300
```

Repeat up to 5 times with the same search pattern.

### 5. If not found

- Take a screenshot to show the current state
- Report that the element was not found after scrolling in both directions
- Suggest alternative approaches:
  - Check if the element uses a different label
  - Navigate to a different section of the app
  - Use `adb shell uiautomator dump /dev/tty` to see what IS available

## Horizontal scrolling

If the user indicates horizontal scrolling or if the content appears to be a horizontal list:
```bash
# Scroll right
adb shell input swipe 900 1000 200 1000 300
# Scroll left
adb shell input swipe 200 1000 900 1000 300
```
