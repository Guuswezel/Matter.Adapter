import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "xiao_otbr_patch/rootfs/usr/local/bin/xiao-antenna-init"
DEVICE = "/dev/serial/by-id/usb-Seeed_Studio_Seeed_Studio_XIAO_MG24__Sense__CMSIS-DAP_TEST1234-if02"


class AntennaSelectionTests(unittest.TestCase):
    def run_init(self, device=DEVICE, serial="", status=0):
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            stub = directory / "timeout"
            stub.write_text('#!/bin/sh\nprintf "%s\\n" "$XIAO_ADAPTER_SERIAL" "$@" > "$RESULT"\nexit "$MOCK_STATUS"\n')
            stub.chmod(0o755)
            result = directory / "result"
            env = dict(os.environ, PATH=f"{directory}:{os.environ['PATH']}", RESULT=str(result), MOCK_STATUS=str(status))
            process = subprocess.run(["bash", str(SCRIPT), device, serial], env=env, capture_output=True, text=True)
            return process, result.read_text().splitlines() if result.exists() else []

    def test_selected_device_determines_debugger(self):
        process, args = self.run_init()
        self.assertEqual(process.returncode, 0, process.stderr)
        self.assertEqual(args[:3], ["TEST1234", "15", "/opt/openocd/bin/openocd"])
        self.assertEqual(args[-1], "/usr/local/share/xiao-antenna.cfg")

    def test_explicit_serial_for_numbered_device(self):
        process, args = self.run_init("/dev/ttyACM0", "OTHER5678")
        self.assertEqual(process.returncode, 0, process.stderr)
        self.assertEqual(args[0], "OTHER5678")

    def test_different_board_cannot_be_reset(self):
        process, args = self.run_init(serial="OTHER5678")
        self.assertEqual(process.returncode, 2)
        self.assertEqual(args, [])

    def test_unknown_or_malicious_serial_never_reaches_openocd(self):
        for serial in ["", "[exit]", "hello world", "x; shutdown"]:
            with self.subTest(serial=serial):
                process, args = self.run_init("/dev/ttyACM0", serial)
                self.assertEqual(process.returncode, 2)
                self.assertEqual(args, [])

    def test_timeout_or_openocd_failure_is_propagated(self):
        process, _ = self.run_init(status=124)
        self.assertEqual(process.returncode, 124)
