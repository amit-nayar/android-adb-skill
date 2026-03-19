# Android ADB Automation

You can control Android devices and emulators via ADB. Read the relevant skill files in `skills/` for detailed instructions on each capability.

## Quick Reference

- **Screenshots:** `adb exec-out screencap -p > /tmp/screen.png`
- **UI tree:** `adb shell uiautomator dump /dev/tty`
- **Tap:** `adb shell input tap X Y`
- **Swipe:** `adb shell input swipe X1 Y1 X2 Y2 DURATION_MS`
- **Long press:** `adb shell input swipe X Y X Y 1000`
- **Type text:** `adb shell input text 'text'` (spaces → `%s`, escape special chars with `\`)
- **Key press:** `adb shell input keyevent CODE` (back=4, home=3, enter=66)
- **Launch app:** `adb shell am start -n PACKAGE/ACTIVITY`
- **Install APK:** `adb install -r path.apk`
- **Logs:** `adb logcat -d -t 200`
- **Current activity:** `adb shell dumpsys activity activities | grep mResumedActivity`

## Skills Available

For detailed step-by-step instructions, read these files:

- `skills/android/SKILL.md` — General-purpose Android automation
- `skills/android-screenshot/SKILL.md` — Capture and analyze screenshots
- `skills/android-ui/SKILL.md` — Inspect UI hierarchy, find elements
- `skills/android-tap/SKILL.md` — Tap elements by text, resource-id, or content-desc
- `skills/android-navigate/SKILL.md` — Navigate through screens
- `skills/android-scroll/SKILL.md` — Scroll to find off-screen elements
- `skills/android-gesture/SKILL.md` — Swipe, long press, double tap, drag
- `skills/android-test/SKILL.md` — Run multi-step test flows
- `skills/android-debug/SKILL.md` — Logcat analysis and diagnostics
- `skills/android-install/SKILL.md` — Install and launch APKs
- `skills/android-device/SKILL.md` — Device and emulator management

## Element Targeting Priority

1. **resource-id** — Most stable, language-independent
2. **text** — Human-readable, breaks with i18n
3. **content-desc** — Good for icons
4. **coordinates** — Last resort

## Bounds → Tap Coordinates

```
bounds="[left,top][right,bottom]"
centerX = (left + right) / 2
centerY = (top + bottom) / 2
```

## Text Escaping for ADB

- Spaces → `%s`
- Escape with `\`: `$ & | ; ' " ( ) < > \` \`

## Common Keycodes

back=4, home=3, enter=66, tab=61, delete=67, menu=82, recent_apps=187, volume_up=24, volume_down=25, power=26, dpad_up=19, dpad_down=20, dpad_left=21, dpad_right=22, dpad_center=23
