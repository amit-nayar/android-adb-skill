# Android Automation

Prefer the local command layer:

```bash
./tools/android ...
```

Read `docs/command-contract.md` for the command surface and `skills/*/SKILL.md` for task-specific workflow guidance.

Default behavior:

- Prefer `./tools/android ... --json` over raw `adb`.
- Pass `--device <id>` when the target device is known or multiple devices are connected.
- Verify state after each interaction with `ui dump`, `wait element`, or `screenshot`.
