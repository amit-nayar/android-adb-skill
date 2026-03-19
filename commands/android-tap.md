---
description: Tap an Android UI element by text, resource-id, or description
allowed-tools: Bash(adb:*), Read
argument-hint: element to tap (e.g., "Login button", "resource-id:com.app/btn_login", "content-desc:Navigate up")
---

Tap an element on the connected Android device.

**Target:** $ARGUMENTS

## Steps

### 1. Get the UI tree

```bash
adb shell uiautomator dump /dev/tty
```

### 2. Find the target element

Parse the argument to determine the targeting method:

- **`resource-id:VALUE`** — Match by resource-id (exact or suffix match, e.g., `btn_login` matches `com.app:id/btn_login`)
- **`content-desc:VALUE`** — Match by content-desc (case-insensitive substring)
- **Plain text** — Match by visible text first (case-insensitive substring), then fall back to content-desc, then resource-id

Search through the `<node>` elements in the UI dump for a match.

### 3. Calculate tap coordinates

Extract the bounds attribute and calculate center:
```
bounds="[left,top][right,bottom]"
centerX = (left + right) / 2
centerY = (top + bottom) / 2
```

### 4. Tap

```bash
adb shell input tap <centerX> <centerY>
```

### 5. Verify

Wait briefly, then check the result:
```bash
sleep 0.5
adb shell uiautomator dump /dev/tty
```

Report what changed on screen after the tap. If the user's intent implies a follow-up (e.g., tapping a text field suggests they want to type), mention what they might do next.

## If element not found

1. Take a screenshot to see the current screen state:
   ```bash
   adb exec-out screencap -p > /tmp/screen.png
   ```
   Read the screenshot to understand what's visible.

2. Try scrolling down to find it:
   ```bash
   adb shell input swipe 540 1500 540 500 300
   ```

3. Re-dump the UI tree and search again. Retry up to 3 times.

4. If still not found, report what elements ARE available that might match the user's intent.

## Multiple matches

If multiple elements match, prefer:
1. The one that is `clickable="true"` and `enabled="true"`
2. The one with the most specific match (exact text over substring)
3. Ask the user to clarify if ambiguous
