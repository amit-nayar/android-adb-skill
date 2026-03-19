---
name: android-test
description: Run an automated test flow on an Android app
allowed-tools: Bash(adb:*), Read
argument-hint: "test flow description (e.g., 'login with user@test.com / pass123, verify home screen')"
---

Execute a test flow on the connected Android device and report pass/fail results.

**Test flow:** $ARGUMENTS

## Approach

### 1. Prepare

Clear logs so we capture only what happens during the test:
```bash
adb logcat -c
```

Take an initial screenshot to record the starting state:
```bash
adb exec-out screencap -p > /tmp/test-start.png
```

### 2. Plan the steps

Break the test flow description into discrete, verifiable steps. For example:
- "login with user@test.com and pass123, verify home screen" becomes:
  1. Find and tap the email field
  2. Type `user@test.com`
  3. Find and tap the password field
  4. Type `pass123`
  5. Tap the Login button
  6. Verify the home screen appears

### 3. Execute each step

For every step:

**a. Get current state:**
```bash
adb shell uiautomator dump /dev/tty
```

**b. Find the target element** by text, resource-id, or content-desc. Calculate center from bounds.

**c. Perform the action:**
```bash
# Tap
adb shell input tap <centerX> <centerY>

# Type text (escape spaces as %s, escape special chars with \)
adb shell input text '<escaped_text>'

# Press key
adb shell input keyevent <keycode>

# Swipe
adb shell input swipe X1 Y1 X2 Y2 300
```

**d. Wait for UI to settle:**
```bash
sleep 0.8
```

**e. Verify the step succeeded:**
```bash
adb shell uiautomator dump /dev/tty
```
Check that the expected change occurred (field populated, new screen appeared, etc.).

**f. Take evidence screenshot:**
```bash
adb exec-out screencap -p > /tmp/test-step-N.png
```

### 4. If a step fails

- **Element not found:** Scroll down, try alternative selectors, take a screenshot to see what's visible
- **Tap didn't register:** Retry the tap once
- **Wrong screen appeared:** Press Back and retry the step
- **App crashed:** Collect logs and report immediately

Do NOT retry more than once per step. Mark the step as failed and continue.

### 5. Collect results

After all steps complete:

**a. Get logs:**
```bash
adb logcat -d -t 500
```
Filter for errors and warnings.

**b. Take final screenshot:**
```bash
adb exec-out screencap -p > /tmp/test-final.png
```

### 6. Report

Present a clear pass/fail report:

```
## Test Results

**Flow:** <test description>
**Result:** PASS / FAIL

### Steps
1. ✅ Find email field — found via resource-id:email_input
2. ✅ Type user@test.com — text entered
3. ✅ Find password field — found via resource-id:password_input
4. ✅ Type password — text entered
5. ✅ Tap Login — button tapped
6. ✅ Verify home screen — "Welcome" text found

### Errors in logcat
None / <list any errors>
```

## Text escaping reminder

When using `adb shell input text`:
- Spaces → `%s`
- Escape: `$ & | ; ' " ( ) < > \` \` with preceding `\`
- Example: `user@test.com` → `adb shell input text 'user@test.com'`
- Example: `Hello World` → `adb shell input text 'Hello%sWorld'`
