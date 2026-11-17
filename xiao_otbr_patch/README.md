# XIAO MG24 Thread Border Router

Home Assistant app for a locally attached Seeed XIAO MG24 (Sense) RCP on an
ARM64 host. Based on the Home Assistant OpenThread Border Router app, with:

- Verified onboard antenna initialization over the XIAO's CMSIS-DAP interface.
- 460800 baud, no hardware flow control, DTR/RTS asserted independently.
- A fresh-install migration fix that avoids an unnecessary serial probe.
- A pinned prebuilt OTBR runtime, avoiding OpenThread compilation on the Pi.

Read [the app instructions](DOCS.md) before starting. This app requires a
board-specific RCP image; it does not flash firmware or provide a standalone
Matter controller. Only `aarch64` and direct USB radios are supported.

Version 3.2.16 is an experimental consolidation of the hardware-tested 3.2.15
deployment. Review the [release procedure](../docs/maintenance.md) before upgrading
an existing network. Retain its app data and Home Assistant backup.
