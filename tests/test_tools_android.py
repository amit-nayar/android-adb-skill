import json
import os
import pathlib
import subprocess
import sys
import tempfile
import unittest
import importlib.util
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

    def test_parse_ui_xml_filters_relevant_nodes(self):
        elements = self.module.parse_ui_xml(SAMPLE_UI_XML)
        self.assertEqual(len(elements), 2)
        self.assertEqual(elements[0]["text"], "Login")
        self.assertTrue(elements[1]["clickable"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
