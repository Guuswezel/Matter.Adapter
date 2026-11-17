# Architecture and invariants

The firmware is a Spinel RCP, not a standalone OTBR or an Arduino Matter lamp
sketch. Home Assistant's official Matter integration and Matter Server remain
responsible for Matter fabrics, subscriptions and device commands. The app
supplies the USB Thread radio and border routing; no custom HA integration is
needed.

At app startup:

1. Resolve the primary backbone interface and the selected USB device.
2. Select only that board's CMSIS-DAP debugger. Reset the RCP, enable its onboard
   antenna switch and read back the pin configuration. Failure stops startup.
3. Configure upstream OTBR firewall rules and persistent `/data/thread` storage.
4. Migrate settings only when existing valid dataset files need examination.
   A fresh install returns without opening the serial port. Existing adapter
   settings are retained; migration to another adapter keeps Thread datasets
   while backing up an old destination file.
5. Start the pinned upstream OTBR runtime with 460800 baud, no CTS/RTS hardware
   flow control, and modem lines asserted. Advertise the REST service to HA.

## Antenna workaround

[Seeed's board documentation](https://wiki.seeedstudio.com/xiao_mg24_bluetooth/)
requires PB5 high to power the RF switch and PB4 low for the onboard antenna.
The pinned RCP firmware did not initialize these pins in the observed deployment.

Use only the **non-secure** GPIO aliases below. Secure aliases faulted the
firmware's SMU handler during diagnosis.

| Register | Address | Operation |
| --- | --- | --- |
| GPIO B MODEL | `0x5003c064` | Preserve other bits; PB4/PB5 push-pull: mask `0x00ff0000`, value `0x00440000` |
| GPIO B DOUT CLR | `0x5003e070` | Clear PB4 with `0x10` |
| GPIO B DOUT SET | `0x5003d070` | Set PB5 with `0x20` |
| GPIO B DOUT | `0x5003c070` | Verify `value & 0x30 == 0x20` |

The workaround writes RAM-mapped registers, not flash. The debugger server ports
are disabled. It requires USB access in the app container and is repeated on
app startup. An independent RCP reset while the app remains running can clear
the pins; restart the app to reinitialize them. A future board-specific firmware
build should initialize the pins itself, then retire this workaround only after
cold-start and recovery tests.

## Changes that require explicit migration planning

- The app slug `xiao_otbr_patch` and app data identity.
- Thread dataset files under `/data/thread`, the preferred network and Matter
  Server's fabric storage. These are private deployment data, never source files.
- Firmware application base `0x08006000` and the existing bootloader.
- Modem-line assertion: disabling hardware flow control must not deassert DTR/RTS.
- The antenna register addresses, masks, sequencing and readback checks.
- The base image and OpenOCD versions: review changes against the compatibility
  baseline and the hardware release gate.
