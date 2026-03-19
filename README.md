# android-adb-skill

Claude Code skills for Android device automation via ADB — screenshots, UI inspection, gestures, app management, and debugging. No MCP server, no dependencies, just ADB.

## What is this?

A collection of [Claude Code custom slash commands](https://docs.anthropic.com/en/docs/claude-code/tutorials/custom-slash-commands) that give Claude full control over Android devices and emulators through ADB. Instead of running a separate MCP server, Claude calls `adb` directly and reasons about the results in real-time.

### Why skills over MCP?

| | MCP approach | Skill approach |
|---|---|---|
| **Multi-step flows** | One tool call per action, many round-trips | Single skill runs tap → wait → verify → retry |
| **Error recovery** | AI sees failure, picks next tool | Claude adapts in real-time, retries with alternatives |
| **Dependencies** | Node.js, npm packages, MCP SDK | Just `adb` on PATH |
| **Setup** | Configure MCP client + server process | Copy files, done |
| **Composition** | Fixed tool schemas | Claude chains commands naturally |
| **Image handling** | In-process compression | Claude reads screenshots directly |

## Prerequisites

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) CLI installed
- Android SDK with `adb` on your PATH (or `ANDROID_HOME` set)
- A connected Android device or running emulator

Verify ADB is working:

```bash
adb devices
```

## Installation

### Global (available in all projects)

```bash
cp commands/* ~/.claude/commands/
```

### Project-scoped

```bash
cp -r commands/ /path/to/your/project/.claude/commands/
```

### CLAUDE.md (recommended)

Copy `CLAUDE.md` to your project root or `~/.claude/CLAUDE.md` for global ADB knowledge in every conversation.

## Available Skills

| Skill | Command | Description |
|-------|---------|-------------|
| **android** | `/android <task>` | General-purpose Android automation — routes to the right approach |
| **android-screenshot** | `/android-screenshot [description]` | Capture and analyze a screenshot |
| **android-ui** | `/android-ui [query]` | Inspect UI hierarchy and find elements |
| **android-tap** | `/android-tap <element>` | Tap an element by text, resource-id, or description |
| **android-navigate** | `/android-navigate <destination>` | Navigate to a specific screen with verification |
| **android-scroll** | `/android-scroll <element>` | Scroll to find an element not currently visible |
| **android-test** | `/android-test <flow>` | Run a multi-step test flow with pass/fail reporting |
| **android-debug** | `/android-debug <issue>` | Collect and analyze logcat, crash logs, ANRs |
| **android-install** | `/android-install <apk>` | Install APK, launch, and verify |
| **android-device** | `/android-device [action]` | List devices, start emulators, get device info |

## Usage Examples

### Take a screenshot and describe what's on screen

```
/android-screenshot what's currently showing?
```

### Tap a button

```
/android-tap Login button
/android-tap resource-id:com.myapp/btn_submit
```

### Run a test flow

```
/android-test login with user@test.com and password123, then verify the home screen loads
```

### Debug a crash

```
/android-debug crashes in com.myapp after tapping Settings
```

### Navigate somewhere

```
/android-navigate Settings > Account > Privacy
```

### General automation

```
/android open Chrome and search for "Claude Code"
/android fill in the registration form with test data
```

## How It Works

Each skill is a markdown file with:
1. **Frontmatter** — description, allowed tools, argument hints
2. **Instructions** — step-by-step guide for Claude on how to accomplish the task
3. **ADB commands** — the actual shell commands Claude will execute
4. **Verification** — how to confirm the action worked

Claude reads the skill, executes ADB commands via Bash, reads screenshots/UI trees to understand device state, and adapts its approach based on what it sees.

## ADB Quick Reference

```bash
# Device management
adb devices -l                              # List connected devices
adb -s <device_id> shell ...                # Target specific device

# Screenshots
adb exec-out screencap -p > /tmp/screen.png # Capture screenshot

# UI inspection
adb shell uiautomator dump /dev/tty         # Dump UI hierarchy

# Input
adb shell input tap X Y                     # Tap at coordinates
adb shell input swipe X1 Y1 X2 Y2 MS       # Swipe gesture
adb shell input text 'hello'                # Type text
adb shell input keyevent 66                 # Press key (66=Enter)

# App management
adb shell am start -n pkg/.Activity         # Launch app
adb install -r app.apk                      # Install APK
adb shell dumpsys activity activities       # Current activity

# Logs
adb logcat -d -t 200                        # Recent 200 log lines
adb logcat -c                               # Clear log buffer
```

## License

MIT
