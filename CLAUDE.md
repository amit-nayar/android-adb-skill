# Android Skills

Use the shared command layer instead of raw `adb` when possible:

```bash
./tools/android ...
```

Read [`docs/command-contract.md`](docs/command-contract.md) for the supported command surface. Read the relevant `skills/*/SKILL.md` file for task-specific orchestration.

## Rules

- Prefer `./tools/android ... --json` for anything that returns structured data.
- Use `--device <id>` when the user named a target device or when multiple devices are attached.
- Verify state after interactions with `./tools/android ui dump`, `./tools/android wait element`, or `./tools/android screenshot`.
- Fall back to raw `adb` only when `./tools/android` lacks the needed operation.
