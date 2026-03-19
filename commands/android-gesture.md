---
description: Perform gestures on an Android device (swipe, long press, double tap)
allowed-tools: Bash(adb:*), Read
argument-hint: "gesture to perform (e.g., 'swipe left', 'long press the icon', 'double tap at 500 800')"
---

Perform a gesture on the connected Android device.

**Gesture:** $ARGUMENTS

## Gesture types

### Tap
```bash
adb shell input tap X Y
```

### Long press
Implemented as a swipe to the same point with a duration:
```bash
adb shell input swipe X Y X Y <duration_ms>
```
Default duration: 1000ms (1 second). Adjust based on context.

### Double tap
Two taps with a short interval:
```bash
adb shell input tap X Y && sleep 0.1 && adb shell input tap X Y
```

### Multi-tap
Repeated taps at the same location:
```bash
for i in $(seq 1 N); do adb shell input tap X Y; sleep 0.1; done
```

### Swipe
```bash
adb shell input swipe X1 Y1 X2 Y2 <duration_ms>
```

Common swipe patterns (assuming 1080x2400 screen):
- **Swipe up** (scroll down): `adb shell input swipe 540 1800 540 600 300`
- **Swipe down** (scroll up): `adb shell input swipe 540 600 540 1800 300`
- **Swipe left** (next page): `adb shell input swipe 900 1200 200 1200 300`
- **Swipe right** (prev page): `adb shell input swipe 200 1200 900 1200 300`

### Drag and drop
Slow swipe from source to destination:
```bash
adb shell input swipe X1 Y1 X2 Y2 1500
```
Use a longer duration (1500ms+) to ensure the system registers it as a drag, not a fling.

## Finding coordinates

If the user specifies an element name instead of coordinates:

1. Dump the UI tree:
   ```bash
   adb shell uiautomator dump /dev/tty
   ```

2. Find the element by text, resource-id, or content-desc

3. Calculate center from bounds:
   ```
   bounds="[left,top][right,bottom]"
   centerX = (left + right) / 2
   centerY = (top + bottom) / 2
   ```

## Screen-relative gestures

If the user says things like "swipe from the middle of the screen":

1. Get screen dimensions:
   ```bash
   adb shell wm size
   ```

2. Calculate coordinates relative to screen size:
   - "center" → width/2, height/2
   - "top" → width/2, height*0.1
   - "bottom" → width/2, height*0.9

## Verification

After performing the gesture, take a screenshot or dump the UI tree to verify the result:
```bash
sleep 0.5
adb exec-out screencap -p > /tmp/screen.png
```
Read the screenshot and describe what changed.
