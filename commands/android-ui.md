---
description: Inspect the Android UI hierarchy and find elements
allowed-tools: Bash(adb:*), Read
argument-hint: "[optional] element to search for (e.g., 'Login button', 'text input fields')"
---

Inspect the UI hierarchy of the connected Android device.

**User request:** $ARGUMENTS

## Steps

### 1. Dump the UI tree

Try the fast path first:
```bash
adb shell uiautomator dump /dev/tty
```

If that fails or returns empty, use the file-based fallback:
```bash
adb shell uiautomator dump /sdcard/window_dump.xml
adb shell cat /sdcard/window_dump.xml
```

### 2. Parse the output

Extract `<node>` elements from the XML. For each relevant node, identify:
- **resource-id** — e.g., `com.app:id/button_login`
- **text** — visible text on the element
- **content-desc** — accessibility description
- **bounds** — `[left,top][right,bottom]` format
- **class** — Android view class (Button, EditText, TextView, etc.)
- **clickable** — whether the element accepts taps
- **enabled** — whether the element is active
- **scrollable** — whether the element can scroll

### 3. Present results

If the user asked for a specific element:
- Search by resource-id (exact or suffix match), text (case-insensitive substring), or content-desc
- Report: element found/not found, its bounds, center coordinates, and state
- If not found, suggest scrolling or checking a different screen

If the user asked for a general overview:
- List the key interactive elements (buttons, inputs, links)
- Group by screen region (top bar, content area, bottom nav)
- Note which elements are clickable vs. display-only

### 4. Calculate tap coordinates

For any element the user might want to interact with, calculate and report the center:
```
bounds="[left,top][right,bottom]"
centerX = (left + right) / 2
centerY = (top + bottom) / 2
```

## Filtering tips

Skip elements that are:
- Not clickable AND have no text, resource-id, or content-desc (layout containers)
- Off-screen (bounds with negative coordinates or larger than screen size)

Focus on elements that are:
- Clickable (buttons, links, inputs)
- Have meaningful text or descriptions
- EditText fields (form inputs)
- Scrollable containers
