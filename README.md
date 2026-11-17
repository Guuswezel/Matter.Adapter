# XIAO MG24 Thread Border Router for Home Assistant

Run a Seeed Studio XIAO MG24 (Sense) as the USB Thread radio for Home Assistant.
This repository brings together the tested firmware version, the Home Assistant
OTBR app, antenna initialization, recovery instructions and regression tests.

The XIAO is an **OpenThread radio co-processor (RCP)**. The host runs the border
router and Matter Server; powering the XIAO from a USB charger alone does not
provide a border router. The host must stay on for this border router to work.

```text
Matter-over-Thread devices
         |  Thread / 802.15.4
    XIAO MG24 RCP
         |  USB serial + onboard CMSIS-DAP
    XIAO OTBR app ── IPv6 LAN ── Home Assistant Matter integration / Matter Server
```

## Start here

1. Check the [supported hardware and versions](docs/compatibility.md).
2. Follow [installation and Home Assistant integration](docs/installation.md).
3. If the board was overwritten, follow [firmware preservation and recovery](docs/firmware.md).
4. For failures, use [troubleshooting](docs/troubleshooting.md).

The working baseline is app **3.2.15**, validated on a Raspberry Pi 4 with HAOS.
The consolidated app **3.2.16 is an experimental candidate**: container and
regression checks do not replace the hardware release checks. No device is
automatically flashed, reset to factory defaults, or commissioned by this repo.
See [the consolidation validation record](docs/validation.md) for completed
checks and the remaining hardware work.

## Repository layout

| Path | Purpose |
| --- | --- |
| [xiao_otbr_patch/](xiao_otbr_patch/) | Installable Home Assistant app; existing slug retained |
| [firmware/manifest.json](firmware/manifest.json) | Pinned upstream firmware, transport settings and hashes |
| [tools/](tools/) | Verified firmware downloads and hardware-free checks |
| [tests/](tests/) | Board selection, migration and download regression tests |
| [docs/](docs/) | Setup, architecture, recovery and maintenance |
| [examples/homeassistant/](examples/homeassistant/) | Optional household automation examples, not installed by the app |

VMs, upstream checkouts, tool installations, flash dumps, credentials and local
history stay outside Git. Firmware binaries are downloaded from their publisher
instead of being redistributed here. See [third-party provenance](THIRD_PARTY.md).

## Development

Requires Python 3.11+, Ruby, Tcl, Bash and Git. Docker is required for the ARM64
image checks; x86 Docker hosts need ARM64 emulation configured separately.

```sh
make test
make image container-test
python3 tools/fetch_firmware.py
```

GitHub Actions runs source checks and a native ARM64 build without USB access.
For contribution and release rules, see [CONTRIBUTING.md](CONTRIBUTING.md) and
[the maintainer guide](docs/maintenance.md). Project code is Apache-2.0;
upstream tools and firmware retain their own licenses.
