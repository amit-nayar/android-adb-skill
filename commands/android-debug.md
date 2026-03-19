---
description: Debug an Android app using logcat and device diagnostics
allowed-tools: Bash(adb:*), Read
argument-hint: "what to debug (e.g., 'crashes in com.myapp', 'ANR after tapping Settings', 'network errors')"
---

Debug an issue on the connected Android device.

**Issue:** $ARGUMENTS

## Steps

### 1. Gather context

Get device info and current state:
```bash
# Device info
adb shell getprop ro.product.model
adb shell getprop ro.build.version.release
adb shell getprop ro.build.version.sdk

# Current foreground activity
adb shell dumpsys activity activities | grep mResumedActivity

# Screenshot of current state
adb exec-out screencap -p > /tmp/debug-screen.png
```

### 2. Collect logs

**Recent logs (general):**
```bash
adb logcat -d -t 300
```

**Errors only:**
```bash
adb logcat -d *:E -t 200
```

**Package-specific logs** (if a package name is mentioned):
```bash
# Get the PID
PID=$(adb shell pidof <package_name>)

# Filter logs by PID
adb logcat -d -t 500 | grep "$PID"
```

**Crash logs:**
```bash
adb logcat -d | grep -i "fatal\|crash\|exception\|ANR\|FATAL EXCEPTION"
```

**ANR traces:**
```bash
adb shell cat /data/anr/traces.txt 2>/dev/null | head -200
```

### 3. Analyze

Look for:
- **FATAL EXCEPTION** — app crash with stack trace
- **ANR** — Application Not Responding
- **NetworkOnMainThreadException** — blocking network call on UI thread
- **OutOfMemoryError** — memory exhaustion
- **SecurityException** — permission denied
- **ClassNotFoundException / NoSuchMethodError** — missing dependency or ProGuard issue
- **SQLiteException** — database errors
- Custom error patterns relevant to the user's description

### 4. Reproduce (if applicable)

If the issue is about a specific action:
1. Clear logcat: `adb logcat -c`
2. Perform the action that triggers the bug
3. Collect fresh logs: `adb logcat -d -t 200`
4. Take a screenshot of the result

### 5. Additional diagnostics

**Memory info:**
```bash
adb shell dumpsys meminfo <package_name>
```

**Running processes:**
```bash
adb shell ps -A | grep <package_name>
```

**Battery and thermal:**
```bash
adb shell dumpsys battery
```

**Network connectivity:**
```bash
adb shell ping -c 3 8.8.8.8
```

### 6. Report findings

Present a structured analysis:
- **What happened:** Summary of the issue based on logs
- **Root cause:** Best assessment from the stack trace / error pattern
- **Evidence:** Key log lines that point to the cause
- **Suggestion:** Possible fix or next debugging step
