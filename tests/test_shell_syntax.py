from pathlib import Path
import subprocess
import unittest


class ShellSyntaxTests(unittest.TestCase):
    def test_all_service_entry_points_parse_as_bash(self):
        root = Path(__file__).resolve().parents[1] / "xiao_otbr_patch/rootfs/etc/s6-overlay"
        scripts = [path for path in root.rglob("*") if path.is_file() and path.read_bytes().startswith(b"#!")]
        self.assertGreater(len(scripts), 5)
        for path in scripts:
            with self.subTest(script=str(path.relative_to(root))):
                subprocess.run(["bash", "-n", str(path)], check=True, capture_output=True)
