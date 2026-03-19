# Android ADB Skills

When working with Android devices via ADB, follow these guidelines.

## ADB Command Reference

```bash
# Device
adb devices -l                                    # List devices with details
adb -s <id> shell ...                             # Target specific device

# Screenshot
adb exec-out screencap -p > /tmp/screen.png       # Capture PNG screenshot

# UI Hierarchy
adb shell uiautomator dump /dev/tty               # Fast: dump to stdout
adb shell uiautomator dump /sdcard/window_dump.xml # Fallback: dump to file
adb shell cat /sdcard/window_dump.xml              # Then read the file

# Touch Input
adb shell input tap X Y                           # Tap at coordinates
adb shell input swipe X Y X Y 1000                # Long press (swipe to same point)
adb shell input swipe X1 Y1 X2 Y2 300             # Swipe gesture
adb shell input text 'escaped_text'               # Type text
adb shell input keyevent CODE                     # Press key

# App Management
adb shell am start -n PACKAGE/ACTIVITY             # Launch activity
adb shell am start -a android.intent.action.MAIN -c android.intent.category.LAUNCHER PACKAGE  # Launch default
adb shell pm list packages                         # List installed packages
adb install -r /path/to/app.apk                   # Install/replace APK
adb shell am force-stop PACKAGE                    # Force stop app

# Diagnostics
adb logcat -d -t 200                               # Last 200 log lines
adb logcat -d *:E                                  # Errors only
adb logcat -c                                      # Clear log buffer
adb shell dumpsys activity activities | grep mResumedActivity  # Current activity
adb shell getprop ro.build.version.release          # Android version
adb shell wm size                                   # Screen resolution
```

## UI Element Targeting Priority

1. **resource-id** — Most stable, language-independent. Match by exact or suffix (e.g., `btn_login` matches `com.app:id/btn_login`)
2. **text** — Human-readable, but breaks with localization. Case-insensitive substring match
3. **content-desc** — Good for icons/images. Case-insensitive substring match
4. **coordinates** — Last resort. Fragile across screen sizes and devices

## UI Tree Parsing

The `uiautomator dump` output is XML with `<node>` elements. Key attributes:
- `resource-id` — e.g., `com.app:id/button_login`
- `text` — Visible text on the element
- `content-desc` — Accessibility description
- `bounds` — Format: `[left,top][right,bottom]`
- `clickable`, `enabled`, `focused`, `scrollable` — Boolean states
- `class` — Android view class (e.g., `android.widget.Button`)

**Calculate tap coordinates from bounds:**
```
bounds="[100,200][300,400]"
centerX = (100 + 300) / 2 = 200
centerY = (200 + 400) / 2 = 300
→ adb shell input tap 200 300
```

## Text Escaping for ADB Input

When using `adb shell input text`:
- Spaces → `%s`
- Escape these characters with `\`: `$ & | ; ' " ( ) < > \` \`
- Example: `Hello World!` → `adb shell input text 'Hello%sWorld\!'`

## Common Keycodes

| Key | Code | Key | Code |
|-----|------|-----|------|
| Back | 4 | Home | 3 |
| Enter | 66 | Tab | 61 |
| Delete | 67 | Menu | 82 |
| Recent Apps | 187 | Search | 84 |
| Volume Up | 24 | Volume Down | 25 |
| Power | 26 | | |
| D-pad Up | 19 | D-pad Down | 20 |
| D-pad Left | 21 | D-pad Right | 22 |
| D-pad Center | 23 | | |

## Best Practices

- Always verify device connection with `adb devices` before starting
- After any interaction (tap, type, swipe), verify the result with a screenshot or UI tree
- Prefer `uiautomator dump /dev/tty` for speed; fall back to file-based dump if it fails
- When an element isn't found, try scrolling before giving up
- Clear logcat before reproducing bugs to get clean logs
- Use screenshots to understand visual layout; use UI tree for precise element targeting
