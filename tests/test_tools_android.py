import json
import os
import pathlib
import subprocess
import sys
import tempfile
import unittest
import importlib.util
from unittest import mock
from importlib.machinery import SourceFileLoader


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
TOOLS_ANDROID = REPO_ROOT / "tools" / "android"


def write_executable(path: pathlib.Path, contents: str) -> None:
    path.write_text(contents)
    path.chmod(0o755)


def png_bytes(width: int = 1080, height: int = 2400) -> bytes:
    import binascii
    import struct
    import zlib

    def chunk(chunk_type: bytes, data: bytes) -> bytes:
        return (
            struct.pack(">I", len(data))
            + chunk_type
            + data
            + struct.pack(">I", binascii.crc32(chunk_type + data) & 0xFFFFFFFF)
        )

    raw = b"".join(b"\x00" + b"\x00\x00\x00" * width for _ in range(height))
    compressed = zlib.compress(raw, 9)
    return b"".join(
        [
            b"\x89PNG\r\n\x1a\n",
            chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)),
            chunk(b"IDAT", compressed),
            chunk(b"IEND", b""),
        ]
    )


FAKE_ADB = r"""#!/usr/bin/env python3
import os
import pathlib
import sys


def load_arg(name, default=""):
    return os.environ.get(name, default)


args = sys.argv[1:]
device_id = None
if args[:2] == ["-s", args[1] if len(args) > 1 else ""]:
    device_id = args[1]
    args = args[2:]

if args == ["devices", "-l"]:
    sys.stdout.write(load_arg("FAKE_ADB_DEVICES", "List of devices attached\n"))
    sys.exit(0)

if args == ["exec-out", "screencap", "-p"]:
    path = load_arg("FAKE_ADB_PNG_PATH")
    sys.stdout.buffer.write(pathlib.Path(path).read_bytes())
    sys.exit(0)

if args[:3] == ["shell", "uiautomator", "dump"]:
    xml = load_arg("FAKE_ADB_UI_XML")
    if args[3] == "/dev/tty":
        if load_arg("FAKE_ADB_UI_TTY_FAIL") == "1":
            sys.stderr.write("ERROR: dump failed\n")
            sys.exit(1)
        sys.stdout.write("UI hierchary dumped to: /dev/tty\n")
        sys.stdout.write(xml)
        sys.exit(0)
    if args[3] == "/sdcard/window_dump.xml":
        sys.stdout.write("UI hierchary dumped to: /sdcard/window_dump.xml\n")
        sys.exit(0)

if args == ["shell", "cat", "/sdcard/window_dump.xml"]:
    sys.stdout.write(load_arg("FAKE_ADB_UI_XML"))
    sys.exit(0)

if args == ["shell", "wm", "size"]:
    sys.stdout.write(load_arg("FAKE_ADB_WM_SIZE", "Physical size: 1080x2400\n"))
    sys.exit(0)

if args == ["shell", "wm", "density"]:
    sys.stdout.write(load_arg("FAKE_ADB_WM_DENSITY", "Physical density: 440\n"))
    sys.exit(0)

if args == ["shell", "getprop", "ro.product.model"]:
    sys.stdout.write(load_arg("FAKE_ADB_MODEL", "sdk_gphone64_arm64\n"))
    sys.exit(0)

if args == ["shell", "getprop", "ro.product.manufacturer"]:
    sys.stdout.write(load_arg("FAKE_ADB_MANUFACTURER", "Google\n"))
    sys.exit(0)

if args == ["shell", "getprop", "ro.build.version.release"]:
    sys.stdout.write(load_arg("FAKE_ADB_ANDROID_VERSION", "15\n"))
    sys.exit(0)

if args == ["shell", "getprop", "ro.build.version.sdk"]:
    sys.stdout.write(load_arg("FAKE_ADB_API_LEVEL", "35\n"))
    sys.exit(0)

if args == ["shell", "getprop", "ro.serialno"]:
    sys.stdout.write(load_arg("FAKE_ADB_SERIAL", (device_id or "emulator-5554") + "\n"))
    sys.exit(0)

if args == ["shell", "getprop", "ro.build.display.id"]:
    sys.stdout.write(load_arg("FAKE_ADB_BUILD", "test-build\n"))
    sys.exit(0)

if args == ["shell", "getprop", "sys.boot_completed"]:
    sys.stdout.write(load_arg("FAKE_ADB_BOOT_COMPLETED", "1\n"))
    sys.exit(0)

if args == ["shell", "dumpsys", "activity", "activities"]:
    sys.stdout.write(load_arg("FAKE_ADB_CURRENT_ACTIVITY", "mResumedActivity: ActivityRecord{ test com.example/.MainActivity}\n"))
    sys.exit(0)

if args[:3] == ["shell", "input", "text"]:
    sys.stdout.write("\n")
    sys.exit(0)

if args[:3] == ["shell", "input", "tap"]:
    sys.stdout.write("\n")
    sys.exit(0)

if args[:3] == ["shell", "input", "keyevent"]:
    sys.stdout.write("\n")
    sys.exit(0)

if args[:3] == ["shell", "input", "swipe"]:
    sys.stdout.write("\n")
    sys.exit(0)

if args[:2] == ["logcat", "-c"]:
    sys.stdout.write("\n")
    sys.exit(0)

if args[:2] == ["logcat", "-d"]:
    sys.stdout.write(load_arg("FAKE_ADB_LOGCAT", "03-20 12:00:00.000  1234  1234 E Example: boom\n"))
    sys.exit(0)

if args[:2] == ["shell", "pidof"]:
    sys.stdout.write(load_arg("FAKE_ADB_PIDOF", "1234\n"))
    sys.exit(0)

if args[:2] == ["install", "-r"]:
    sys.stdout.write(load_arg("FAKE_ADB_INSTALL_OUTPUT", "Success\n"))
    sys.exit(0)

if args[:3] == ["shell", "monkey", "-p"]:
    sys.stdout.write("Events injected: 1\n")
    sys.exit(0)

if args[:3] == ["shell", "am", "start"]:
    sys.stdout.write("Starting: Intent\n")
    sys.exit(0)

# ADBKeyboard detection
if args[2:4] == ["list", "packages"] and "com.android.adbkeyboard" in args:
    if load_arg("FAKE_ADB_ADBKEYBOARD_INSTALLED", "0") == "1":
        sys.stdout.write("package:com.android.adbkeyboard\n")
    sys.exit(0)

# IME get
if args[:3] == ["shell", "settings", "get"] and len(args) >= 5 and args[-1] == "default_input_method":
    sys.stdout.write(load_arg("FAKE_ADB_CURRENT_IME", "com.google.android.inputmethod.latin/.LatinIME\n"))
    sys.exit(0)

# IME set
if args[:3] == ["shell", "ime", "set"]:
    sys.stdout.write("")
    sys.exit(0)

# Broadcast text (ADBKeyboard) — validates correct intent action + base64 payload
if args[:3] == ["shell", "am", "broadcast"]:
    # Record full invocation so tests can assert on exact arguments
    record_path = os.environ.get("FAKE_ADB_BROADCAST_LOG")
    if record_path:
        with open(record_path, "a") as f:
            f.write(" ".join(args) + "\n")
    # Validate the intent action
    if "-a" not in args or "ADB_INPUT_B64" not in args:
        sys.stderr.write(f"ERROR: expected -a ADB_INPUT_B64, got: {' '.join(args)}\n")
        sys.exit(1)
    # Reject the wrong action name (the bug we're guarding against)
    if "ADB_INPUT_TEXT" in args:
        sys.stderr.write("ERROR: ADB_INPUT_TEXT is not supported, use ADB_INPUT_B64\n")
        sys.exit(1)
    # Validate --es msg contains something base64-like
    msg_idx = None
    for i, a in enumerate(args):
        if a == "--es" and i + 2 < len(args) and args[i + 1] == "msg":
            msg_idx = i + 2
            break
    if msg_idx is None:
        sys.stderr.write("ERROR: missing --es msg <payload>\n")
        sys.exit(1)
    sys.stdout.write("Broadcasting: Intent\n")
    sys.exit(0)

sys.stderr.write("Unhandled fake adb args: " + " ".join(args) + "\n")
sys.exit(1)
"""


FAKE_EMULATOR = r"""#!/usr/bin/env python3
import os
import sys

args = sys.argv[1:]
if args == ["-list-avds"]:
    sys.stdout.write(os.environ.get("FAKE_EMULATOR_AVDS", "Pixel_9\nPixel_Fold\n"))
    sys.exit(0)

if args[:1] == ["-avd"]:
    sys.exit(0)

sys.stderr.write("Unhandled fake emulator args\n")
sys.exit(1)
"""


SAMPLE_UI_XML = """<?xml version="1.0" encoding="UTF-8"?>
<hierarchy rotation="0">
  <node index="0" text="Login" resource-id="com.example:id/btn_login" class="android.widget.Button" content-desc="" clickable="true" enabled="true" focused="false" checked="false" scrollable="false" bounds="[100,200][300,260]" />
  <node index="1" text="" resource-id="" class="android.view.View" content-desc="Navigate up" clickable="true" enabled="true" focused="false" checked="false" scrollable="false" bounds="[0,0][80,80]" />
</hierarchy>
"""


class AndroidToolTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._tempdir = tempfile.TemporaryDirectory()
        base = pathlib.Path(cls._tempdir.name)
        sdk = base / "sdk"
        platform_tools = sdk / "platform-tools"
        emulator_dir = sdk / "emulator"
        platform_tools.mkdir(parents=True)
        emulator_dir.mkdir(parents=True)

        cls.png_path = base / "screen.png"
        cls.png_path.write_bytes(png_bytes(320, 640))
        cls.apk_path = base / "app-debug.apk"
        cls.apk_path.write_bytes(b"fake-apk")

        write_executable(platform_tools / "adb", FAKE_ADB)
        write_executable(emulator_dir / "emulator", FAKE_EMULATOR)

        cls.sdk = sdk
        cls.base = base

    @classmethod
    def tearDownClass(cls):
        cls._tempdir.cleanup()

    def base_env(self):
        env = os.environ.copy()
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        env["ANDROID_HOME"] = str(self.sdk)
        env["FAKE_ADB_DEVICES"] = (
            "List of devices attached\n"
            "emulator-5554          device product:sdk_gphone64_arm64 model:sdk_gphone64_arm64 device:emu64a transport_id:1\n"
        )
        env["FAKE_ADB_UI_XML"] = SAMPLE_UI_XML
        env["FAKE_ADB_PNG_PATH"] = str(self.png_path)
        env["FAKE_EMULATOR_AVDS"] = "Pixel_9\nPixel_Fold\n"
        return env

    def run_cli(self, *args, env=None):
        proc = subprocess.run(
            [sys.executable, str(TOOLS_ANDROID), *args],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            env=env or self.base_env(),
        )
        return proc

    def test_device_list_json(self):
        proc = self.run_cli("device", "list", "--json")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        payload = json.loads(proc.stdout)
        self.assertEqual(payload["count"], 1)
        self.assertEqual(payload["devices"][0]["id"], "emulator-5554")

    def test_device_avds_json(self):
        proc = self.run_cli("device", "avds", "--json")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        payload = json.loads(proc.stdout)
        self.assertEqual(payload["avds"], ["Pixel_9", "Pixel_Fold"])

    def test_ui_find_returns_center_coordinates(self):
        proc = self.run_cli("ui", "find", "--by", "text", "--value", "Login", "--json")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        payload = json.loads(proc.stdout)
        self.assertEqual(payload["bestMatch"]["resourceId"], "com.example:id/btn_login")
        self.assertEqual(payload["bestMatch"]["center"], {"x": 200, "y": 230})

    def test_input_text_reports_escaped_value(self):
        proc = self.run_cli("input", "text", "--text", "Hello World!", "--json")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        payload = json.loads(proc.stdout)
        self.assertEqual(payload["escaped"], "Hello%sWorld\\!")
        self.assertEqual(payload["method"], "default")

    def test_input_text_falls_back_when_ime_missing(self):
        proc = self.run_cli("input", "text", "--text", "hello world", "--json")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        payload = json.loads(proc.stdout)
        self.assertEqual(payload["method"], "default")
        self.assertEqual(payload["text"], "hello world")
        self.assertIn("escaped", payload)

    def test_input_text_uses_ime_when_available(self):
        env = self.base_env()
        env["FAKE_ADB_ADBKEYBOARD_INSTALLED"] = "1"
        proc = self.run_cli("input", "text", "--text", "hello world", "--json", env=env)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        payload = json.loads(proc.stdout)
        self.assertEqual(payload["method"], "ime")
        self.assertEqual(payload["text"], "hello world")

    def test_input_text_handles_unicode_via_ime(self):
        env = self.base_env()
        env["FAKE_ADB_ADBKEYBOARD_INSTALLED"] = "1"
        proc = self.run_cli("input", "text", "--text", "Hello 🌍 émoji!", "--json", env=env)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        payload = json.loads(proc.stdout)
        self.assertEqual(payload["method"], "ime")
        self.assertEqual(payload["text"], "Hello 🌍 émoji!")

    def test_input_text_broadcasts_with_correct_action_and_base64(self):
        import base64
        log_file = str(self.base / "broadcast_log.txt")
        env = self.base_env()
        env["FAKE_ADB_ADBKEYBOARD_INSTALLED"] = "1"
        env["FAKE_ADB_BROADCAST_LOG"] = log_file
        text = "test payload"
        proc = self.run_cli("input", "text", "--text", text, "--json", env=env)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        # Inspect what the fake adb actually received
        lines = pathlib.Path(log_file).read_text().strip().splitlines()
        self.assertEqual(len(lines), 1)  # exactly one broadcast call
        invocation = lines[0]
        # Must use ADB_INPUT_B64 (not ADB_INPUT_TEXT — that was the bug)
        self.assertIn("-a", invocation)
        self.assertIn("ADB_INPUT_B64", invocation)
        self.assertNotIn("ADB_INPUT_TEXT", invocation)
        self.assertNotIn("is_base64", invocation)
        # Must carry a valid base64-encoded --es msg
        self.assertIn("--es", invocation)
        self.assertIn("msg", invocation)
        expected_b64 = base64.b64encode(text.encode("utf-8")).decode("ascii")
        self.assertIn(expected_b64, invocation)

    def test_input_text_restores_ime_after_typing(self):
        env = self.base_env()
        env["FAKE_ADB_ADBKEYBOARD_INSTALLED"] = "1"
        env["FAKE_ADB_CURRENT_IME"] = "com.example/.CustomIME\n"
        proc = self.run_cli("input", "text", "--text", "restored", "--json", env=env)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        payload = json.loads(proc.stdout)
        self.assertEqual(payload["method"], "ime")

    def test_app_install_uses_explicit_package_name(self):
        proc = self.run_cli("app", "install", "--apk", str(self.apk_path), "--package", "com.example", "--json")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        payload = json.loads(proc.stdout)
        self.assertEqual(payload["packageName"], "com.example")
        self.assertEqual(payload["output"], "Success")

    def test_multiple_devices_require_explicit_selection(self):
        env = self.base_env()
        env["FAKE_ADB_DEVICES"] = (
            "List of devices attached\n"
            "emulator-5554 device model:first\n"
            "emulator-5556 device model:second\n"
        )
        proc = self.run_cli("device", "info", "--json", env=env)
        self.assertEqual(proc.returncode, 1)
        payload = json.loads(proc.stderr)
        self.assertIn("Multiple devices detected", payload["error"])

    def test_debug_logs_filters_package_and_returns_lines(self):
        env = self.base_env()
        env["FAKE_ADB_LOGCAT"] = (
            "03-20 12:00:00.000  1234  1234 E Example: boom\n"
            "03-20 12:00:00.000  9999  9999 E Other: skip\n"
        )
        proc = self.run_cli("debug", "logs", "--package", "com.example", "--json", env=env)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        payload = json.loads(proc.stdout)
        self.assertEqual(payload["lineCount"], 1)
        self.assertIn("Example: boom", payload["lines"][0])


class AndroidToolUnitTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        loader = SourceFileLoader("android_tool", str(TOOLS_ANDROID))
        spec = importlib.util.spec_from_loader("android_tool", loader)
        module = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(module)
        cls.module = module

    def test_parse_bounds(self):
        self.assertEqual(
            self.module.parse_bounds("[10,20][110,220]"),
            {"x": 10, "y": 20, "width": 100, "height": 200},
        )

    def test_parse_bounds_rejects_non_positive_dimensions(self):
        self.assertIsNone(self.module.parse_bounds("[10,20][10,220]"))
        self.assertIsNone(self.module.parse_bounds("[10,20][110,20]"))

    def test_parse_ui_xml_filters_relevant_nodes(self):
        elements = self.module.parse_ui_xml(SAMPLE_UI_XML)
        self.assertEqual(len(elements), 2)
        self.assertEqual(elements[0]["text"], "Login")
        self.assertTrue(elements[1]["clickable"])

    def test_get_ui_xml_retries_until_xml_is_available(self):
        responses = iter(
            [
                subprocess.CompletedProcess(args=[], returncode=137, stdout="", stderr="Killed"),
                subprocess.CompletedProcess(args=[], returncode=1, stdout="", stderr="dump failed"),
                subprocess.CompletedProcess(args=[], returncode=0, stdout="", stderr=""),
                subprocess.CompletedProcess(args=[], returncode=0, stdout="UI hierchary dumped to: /dev/tty\n" + SAMPLE_UI_XML, stderr=""),
            ]
        )

        with mock.patch.object(self.module, "adb_result", side_effect=lambda *args, **kwargs: next(responses)):
            with mock.patch.object(self.module.time, "sleep"):
                xml = self.module.get_ui_xml("emulator-5554")

        self.assertIn("<hierarchy", xml)

    def test_select_started_device_prefers_new_device(self):
        current_devices = [
            {"id": "emulator-5554", "state": "device"},
            {"id": "emulator-5556", "state": "device"},
        ]
        self.assertEqual(
            self.module.select_started_device(current_devices, {"emulator-5554"}),
            "emulator-5556",
        )

    def test_select_started_device_ignores_existing_ready_devices(self):
        current_devices = [{"id": "emulator-5554", "state": "device"}]
        self.assertIsNone(self.module.select_started_device(current_devices, {"emulator-5554"}))

    def test_select_started_device_requires_explicit_choice_for_multiple_new_devices(self):
        current_devices = [
            {"id": "emulator-5554", "state": "device"},
            {"id": "emulator-5556", "state": "device"},
        ]
        with self.assertRaises(self.module.ToolError):
            self.module.select_started_device(current_devices, set())


if __name__ == "__main__":
    unittest.main(verbosity=2)
