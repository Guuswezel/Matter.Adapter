"""Exercise file preservation with serial dependencies mocked; no radio needed."""
import asyncio
import importlib.util
import os
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("migration", ROOT / "xiao_otbr_patch/rootfs/usr/local/bin/migrate_otbr_settings.py")
migration = importlib.util.module_from_spec(spec)
# Unit tests need only Python's standard library. Container smoke tests separately
# import the real dependencies shipped by the pinned upstream runtime.
with patch.dict(sys.modules, {name: MagicMock() for name in ["zigpy", "zigpy.serial", "serialx", "universal_silabs_flasher", "universal_silabs_flasher.spinel"]}):
    spec.loader.exec_module(migration)


class MigrationTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.data = Path(self.directory.name)
        self.settings = [(migration.OtbrSettingsKey.ACTIVE_DATASET, b"private-test-dataset"),
                         (migration.OtbrSettingsKey.PENDING_DATASET, b"pending"),
                         (migration.OtbrSettingsKey.NETWORK_INFO, b"old-device-state")]
        self.probe = AsyncMock(return_value="0102030405060708")
        self.probe_patch = patch.object(migration, "get_adapter_hardware_addr", self.probe)
        self.probe_patch.start()
        self.addCleanup(self.probe_patch.stop)

    async def run_main(self):
        args = ["migrate", "--data-dir", str(self.data), "--adapter", "/dev/test"]
        with patch.object(sys, "argv", args), patch.object(migration, "AFTER_DISCONNECT_DELAY", 0):
            await migration.main()

    def write_settings(self, name, settings=None):
        path = self.data / name
        path.write_bytes(migration.serialize_otbr_settings(self.settings if settings is None else settings))
        return path

    async def test_fresh_install_never_opens_radio(self):
        await self.run_main()
        self.probe.assert_not_awaited()
        self.assertEqual(list(self.data.iterdir()), [])

    async def test_unrelated_files_and_invalid_dataset_do_not_open_radio(self):
        (self.data / "notes.data").write_text("unrelated")
        self.write_settings("0_dead.data", [(migration.OtbrSettingsKey.NETWORK_INFO, b"state")])
        await self.run_main()
        self.probe.assert_not_awaited()

    async def test_current_adapter_settings_remain_byte_identical(self):
        path = self.write_settings("0_102030405060708.data")
        before = path.read_bytes()
        await self.run_main()
        self.assertEqual(path.read_bytes(), before)
        self.assertEqual(list(self.data.iterdir()), [path])

    async def test_migration_keeps_dataset_and_archives_old_destination(self):
        old_destination = self.write_settings("0_102030405060708.data")
        os.utime(old_destination, (1, 1))
        original = self.write_settings("0_dead.data")
        before = original.read_bytes()
        await self.run_main()
        self.assertEqual(original.read_bytes(), before)
        self.assertEqual(migration.parse_otbr_settings(old_destination.read_bytes()), self.settings[:2])
        archived = list(self.data.glob("*.backup-*"))
        self.assertEqual(len(archived), 1)
        self.assertEqual(archived[0].read_bytes(), before)

    async def test_corrupt_settings_fail_without_rewriting_or_probing(self):
        path = self.data / "0_dead.data"
        path.write_bytes(b"\x01")
        with self.assertRaises(AssertionError):
            await self.run_main()
        self.assertEqual(path.read_bytes(), b"\x01")
        self.probe.assert_not_awaited()


class ModemLineTests(unittest.IsolatedAsyncioTestCase):
    async def test_modem_lines_asserted_with_and_without_hardware_flow_control(self):
        protocol = types.SimpleNamespace(wait_until_connected=AsyncMock(), reset=AsyncMock(),
                                         send_command=AsyncMock(return_value=types.SimpleNamespace(data=b"response")),
                                         disconnect=AsyncMock())
        connection = AsyncMock(return_value=(None, protocol))
        migration.PropertyID.deserialize.return_value = (migration.PropertyID.HWADDR, bytes.fromhex("0102030405060708"))
        for flow in [None, "hardware"]:
            with patch.object(migration.zigpy.serial, "create_serial_connection", connection):
                address = await migration.get_adapter_hardware_addr("/dev/test", flow_control=flow)
            self.assertEqual(address, "0102030405060708")
            self.assertEqual(connection.call_args.kwargs["flow_control"], flow)
            self.assertEqual(connection.call_args.kwargs["rtsdtr_on_open"], migration.PinState.HIGH)
            self.assertEqual(connection.call_args.kwargs["rtsdtr_on_close"], migration.PinState.LOW)
        self.assertEqual(protocol.disconnect.await_count, 2)
