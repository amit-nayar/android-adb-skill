# android-adb-skill

Android device automation via ADB for AI coding agents — screenshots, UI inspection, gestures, app management, and debugging. No MCP server, no dependencies, just ADB.

## What is this?

A collection of skills and instruction files that give AI coding agents full control over Android devices and emulators through ADB. Instead of running a separate MCP server, the agent calls `adb` directly and reasons about the results in real-time.

Works with multiple agents:

| Agent | How it loads | Invocation |
|-------|-------------|------------|
| **Claude Code** | Plugin or copy `skills/` | `/android-adb-skill:android <task>` (plugin) or `/android <task>` (local) |
| **Codex** | Reads `AGENTS.md` automatically | Natural language — references `skills/` for details |
| **Cursor** | Reads `.cursor/rules/android-adb.mdc` | Activates when relevant via description match |
| **GitHub Copilot** | Reads `.github/copilot-instructions.md` | Available in Copilot Chat context |
| **Other agents** | Point them at `skills/*/SKILL.md` | Any agent that can read markdown and run shell commands |

### Why skills over MCP?

| | MCP approach | Skill approach |
|---|---|---|
| **Multi-step flows** | One tool call per action, many round-trips | Single skill runs tap → wait → verify → retry |
| **Error recovery** | AI sees failure, picks next tool | Agent adapts in real-time, retries with alternatives |
| **Dependencies** | Node.js, npm packages, MCP SDK | Just `adb` on PATH |
| **Setup** | Configure MCP client + server process | Copy files or install plugin |
| **Composition** | Fixed tool schemas | Agent chains commands naturally |

## Prerequisites

- An AI coding agent (Claude Code, Codex, Cursor, etc.)
- Android SDK with `adb` on your PATH (or `ANDROID_HOME` set)
- A connected Android device or running emulator

Verify ADB is working:

```bash
adb devices
```

## Installation

### Claude Code (plugin — recommended)

Install as a plugin so skills stay up to date and are available across all projects:

```bash
# Inside Claude Code, run:
/plugin marketplace add <your-github-username>/android-adb-skill
```

Skills become available as `/android-adb-skill:android`, `/android-adb-skill:android-tap`, etc.

For local development, load the plugin from disk:

```bash
claude --plugin-dir /path/to/android-adb-skill
```

### Claude Code (local copy)

If you prefer not to use the plugin system, copy the skill files directly:

```bash
# Global (available in all projects)
cp -r skills/* ~/.claude/skills/
cp CLAUDE.md ~/.claude/CLAUDE.md

# Or project-scoped
mkdir -p .claude/skills
cp -r skills/* .claude/skills/
cp CLAUDE.md .   # optional: ADB reference loaded into every conversation
```

Skills become `/android`, `/android-tap`, etc. (no namespace prefix).

### OpenAI Codex

Copy `AGENTS.md` and `skills/` into your project root:

```bash
cp AGENTS.md /path/to/your/project/
cp -r skills/ /path/to/your/project/skills/
```

Codex automatically reads `AGENTS.md` on startup. The file references `skills/*/SKILL.md` for detailed step-by-step instructions, which Codex can read on demand.

### Cursor

Copy the rules file and skills into your project:

```bash
mkdir -p /path/to/your/project/.cursor/rules
cp .cursor/rules/android-adb.mdc /path/to/your/project/.cursor/rules/
cp -r skills/ /path/to/your/project/skills/
```

Cursor loads `.cursor/rules/android-adb.mdc` automatically when its description matches the conversation context. The rule references `skills/` for detailed instructions.

### GitHub Copilot

Copy the instructions file and skills into your project:

```bash
mkdir -p /path/to/your/project/.github
cp .github/copilot-instructions.md /path/to/your/project/.github/
cp -r skills/ /path/to/your/project/skills/
```

Copilot reads `.github/copilot-instructions.md` automatically in Copilot Chat. The file references `skills/` for detailed instructions.

### Windsurf

Windsurf uses a single `.windsurfrules` file. Copy the ADB reference into your project:

```bash
cp AGENTS.md /path/to/your/project/.windsurfrules
cp -r skills/ /path/to/your/project/skills/
```

### Cline / Roo Code

Copy the instructions and skills into your project:

```bash
cp AGENTS.md /path/to/your/project/.clinerules
cp -r skills/ /path/to/your/project/skills/
```

Cline reads `.clinerules` automatically. The file references `skills/` for detailed instructions.

### Other agents

Any agent that can read markdown files and run shell commands can use the skills directly. Point the agent at the relevant `skills/*/SKILL.md` file for the task at hand. Each skill is self-contained with step-by-step ADB instructions.

## Available Skills

| Skill | Description |
|-------|-------------|
| **android** | General-purpose Android automation — routes to the right approach |
| **android-screenshot** | Capture and analyze a screenshot |
| **android-ui** | Inspect UI hierarchy and find elements |
| **android-tap** | Tap an element by text, resource-id, or description |
| **android-navigate** | Navigate to a specific screen with verification |
| **android-scroll** | Scroll to find an element not currently visible |
| **android-gesture** | Swipe, long press, double tap, drag and drop |
| **android-test** | Run a multi-step test flow with pass/fail reporting |
| **android-debug** | Collect and analyze logcat, crash logs, ANRs |
| **android-install** | Install APK, launch, and verify |
| **android-device** | List devices, start emulators, get device info |

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

## Repo Structure

```
android-adb-skill/
├── skills/                          # Core skill files (universal markdown)
│   ├── android/SKILL.md
│   ├── android-screenshot/SKILL.md
│   ├── android-ui/SKILL.md
│   ├── android-tap/SKILL.md
│   ├── android-navigate/SKILL.md
│   ├── android-scroll/SKILL.md
│   ├── android-gesture/SKILL.md
│   ├── android-test/SKILL.md
│   ├── android-debug/SKILL.md
│   ├── android-install/SKILL.md
│   └── android-device/SKILL.md
├── .claude-plugin/plugin.json       # Claude Code plugin manifest
├── CLAUDE.md                        # ADB knowledge base for Claude Code
├── AGENTS.md                        # Instructions for Codex
├── .cursor/rules/android-adb.mdc   # Rules for Cursor
├── .github/copilot-instructions.md # Instructions for GitHub Copilot
├── .gitignore
├── LICENSE
└── README.md
```

## License

MIT
