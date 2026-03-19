# Android ADB Automation

You can control Android devices and emulators via ADB. Read the relevant skill files in `skills/` for detailed instructions.

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

## Detailed Instructions

For step-by-step guides, read the corresponding file in `skills/`:

- `skills/android/SKILL.md` — General-purpose automation
- `skills/android-screenshot/SKILL.md` — Screenshots
- `skills/android-ui/SKILL.md` — UI inspection
- `skills/android-tap/SKILL.md` — Tapping elements
- `skills/android-navigate/SKILL.md` — Navigation
- `skills/android-scroll/SKILL.md` — Scrolling
- `skills/android-gesture/SKILL.md` — Gestures
- `skills/android-test/SKILL.md` — Test flows
- `skills/android-debug/SKILL.md` — Debugging
- `skills/android-install/SKILL.md` — APK installation
- `skills/android-device/SKILL.md` — Device management

## Element Targeting Priority

1. **resource-id** — Most stable, language-independent
2. **text** — Human-readable, breaks with i18n
3. **content-desc** — Good for icons
4. **coordinates** — Last resort

## Bounds to Tap Coordinates

```
bounds="[left,top][right,bottom]"
centerX = (left + right) / 2
centerY = (top + bottom) / 2
```

## Text Escaping for ADB

- Spaces → `%s`
- Escape with `\`: `$ & | ; ' " ( ) < > \` \`

## Common Keycodes

back=4, home=3, enter=66, tab=61, delete=67, menu=82, recent_apps=187, volume_up=24, volume_down=25, power=26
