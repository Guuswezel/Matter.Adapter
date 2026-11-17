import hashlib
import importlib.util
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("fetch_firmware", Path(__file__).resolve().parents[1] / "tools/fetch_firmware.py")
firmware = importlib.util.module_from_spec(spec)
spec.loader.exec_module(firmware)


class FirmwareDownloadTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.target = Path(self.directory.name) / "app.gbl"
        self.content = b"verified firmware"
        self.digest = hashlib.sha256(self.content).hexdigest()

    def test_download_is_verified_before_replacing_existing_file(self):
        self.target.write_bytes(b"old firmware")
        with patch.object(firmware.urllib.request, "urlopen", return_value=io.BytesIO(self.content)):
            firmware.fetch("https://example.invalid/app", self.target, self.digest)
        self.assertEqual(self.target.read_bytes(), self.content)

    def test_checksum_failure_preserves_previous_file_and_removes_partial(self):
        self.target.write_bytes(b"old firmware")
        with patch.object(firmware.urllib.request, "urlopen", return_value=io.BytesIO(b"corrupted")):
            with self.assertRaisesRegex(ValueError, "SHA-256 mismatch"):
                firmware.fetch("https://example.invalid/app", self.target, self.digest)
        self.assertEqual(self.target.read_bytes(), b"old firmware")
        self.assertFalse(self.target.with_suffix(".gbl.part").exists())

    def test_verified_cached_file_needs_no_network(self):
        self.target.write_bytes(self.content)
        with patch.object(firmware.urllib.request, "urlopen", side_effect=AssertionError("Network accessed")):
            firmware.fetch("https://example.invalid/app", self.target, self.digest)
