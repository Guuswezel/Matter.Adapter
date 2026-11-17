# Firmware preservation and recovery

The release and hashes are recorded in [manifest.json](../firmware/manifest.json).
This is the community image used successfully with the antenna workaround,
not the latest official Arduino image. The repo references upstream artifacts;
it does not contain a maintained RCP firmware source tree or Arduino sketch.
Upstream board build work is documented in
[silabs-firmware-builder PR 193](https://github.com/darkxst/silabs-firmware-builder/pull/193).

Firmware updates interrupt this border router. Back up Home Assistant including
OTBR and Matter Server, stop the OTBR app, and connect the intended board to
the flashing computer. Close Arduino IDE/debugger sessions. Do not mass-erase
the board or replace the existing bootloader during an ordinary application
reflash. Do not reset a working Thread network or recommission devices.

## Obtain and verify the application

With Python 3.11+:

```sh
python3 tools/fetch_firmware.py
```

It downloads only the application by default, verifies SHA-256 and writes to
ignored `.cache/firmware/`. It never accesses hardware. `--bootloader` also
downloads the optional bootloader for recovery planning, not routine flashing.

Use Silicon Labs Simplicity Commander to extract the application without
touching hardware. The original extraction used Commander 1.16.4:

```sh
commander gbl parse .cache/firmware/xiao_mg24_openthread_rcp_2.5.3.0_GitHub-1fceb225b_gsdk_2024.6.3_no_flow_460800.gbl \
  --app .cache/firmware/application.hex
shasum -a 256 .cache/firmware/application.hex
```

The original extraction hash is
`77d873271758f242a67302bbf73a43ad6ab4de359970e66b5eefb11239144c88`.
Newer Commander versions may name this command `gbl3 parse`; see the
[official GBL parsing documentation](https://docs.silabs.com/simplicity-commander/latest/simplicity-commander-commands/gbl-commands).
If output differs, investigate format/content before flashing; do not bypass
verification. The application must start at `0x08006000` and must not contain
bootloader or device-storage writes.

## Preserve the board before programming

Install a board-compatible OpenOCD for the flashing computer. The app downloads
Arduino's pinned **Linux ARM64** tool; it cannot execute natively on macOS.
The Silicon Labs Arduino installation provides host-specific tools with
`interface/cmsis-dap.cfg` and `target/efm32s2_g23.cfg`.

Run commands from the repository root. Set these to your actual tool and board:

```sh
OPENOCD=/absolute/path/to/bin/openocd
OPENOCD_SCRIPTS=/absolute/path/to/share/openocd/scripts
XIAO_SERIAL=YOUR_BOARDS_CMSIS_DAP_SERIAL
mkdir -p private/recovery
chmod 700 private/recovery
```

First identify the target. Do not proceed unless it is the intended MG24B220
with 1536 KiB flash and the debugger connection succeeds:

```sh
"$OPENOCD" -s "$OPENOCD_SCRIPTS" \
  -f interface/cmsis-dap.cfg -f target/efm32s2_g23.cfg \
  -c "adapter serial $XIAO_SERIAL" \
  -c 'init; reset halt; targets; reset run; shutdown'
```

Save a complete readback to a **new dated filename**, plus the USB identity and
probe output. The following address/length apply only to the confirmed target:

```sh
"$OPENOCD" -s "$OPENOCD_SCRIPTS" \
  -f interface/cmsis-dap.cfg -f target/efm32s2_g23.cfg \
  -c "adapter serial $XIAO_SERIAL" \
  -c 'init; reset halt; dump_image private/recovery/preflash.bin 0x08000000 0x00180000; reset run; shutdown'
chmod 600 private/recovery/preflash.bin
shasum -a 256 private/recovery/preflash.bin
```

Check the dump is exactly 1,572,864 bytes and store an additional private copy
outside this checkout. It includes device storage. If a readback is locked or
fails, stop and investigate; do not use an erase-first flasher to bypass it.

## Program only the verified application

After the backup and image checks above, this command writes application flash:

```sh
"$OPENOCD" -s "$OPENOCD_SCRIPTS" \
  -f interface/cmsis-dap.cfg -f target/efm32s2_g23.cfg \
  -c "adapter serial $XIAO_SERIAL" \
  -c 'program .cache/firmware/application.hex verify reset exit'
```

Read back the bootloader and compare its first `0x6000` bytes to the pre-flash
dump. This proves an application reflash did not change it:

```sh
"$OPENOCD" -s "$OPENOCD_SCRIPTS" \
  -f interface/cmsis-dap.cfg -f target/efm32s2_g23.cfg \
  -c "adapter serial $XIAO_SERIAL" \
  -c 'init; reset halt; dump_image private/recovery/bootloader-after.bin 0x08000000 0x6000; reset run; shutdown'
python3 - <<'PY'
from pathlib import Path
before = Path('private/recovery/preflash.bin').read_bytes()[:0x6000]
after = Path('private/recovery/bootloader-after.bin').read_bytes()
assert len(after) == 0x6000 and before == after, 'Bootloader changed; investigate before starting OTBR'
print('Original bootloader preserved')
PY
```

Reconnect the XIAO to the HA host. Use 460800 baud, flow control false, and start
the custom app to initialize the antenna. Verify the same adapter hardware
address, Thread network and Matter devices, then perform the
[release checks](maintenance.md). Application verification alone does not prove
wireless operation. For rollback, use the same board's saved image and its
original transport settings; do not restore another board's device storage.
