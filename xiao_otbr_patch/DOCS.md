# XIAO MG24 app configuration

Requires Home Assistant OS on ARM64 and a locally attached Seeed XIAO MG24
(Sense) running the pinned OpenThread RCP image. This app does not flash the
board. Read the repository's firmware recovery guide before replacing firmware.

Stop the stock OTBR app and disable its watchdog/start-on-boot before using this
app. Back up existing OTBR and Matter Server data. Keep the existing Thread
network and commissioned devices when updating this app.

## Options

| Option | Setting |
| --- | --- |
| `device` | Select the XIAO's stable `/dev/serial/by-id/...CMSIS-DAP_...-if02` serial device |
| `adapter_serial` | Leave empty for a recognized XIAO by-id path; otherwise specify the same board's CMSIS-DAP USB serial |
| `baudrate` | `460800` for the pinned alternative RCP firmware |
| `flow_control` | `false`; DTR/RTS remain asserted independently |
| `backbone_interface` | Optional; defaults to the primary host interface |
| `otbr_log_level` | `notice` normally; temporarily use `info`/`debug` for diagnosis |
| `firewall` | `true` |
| `nat64` | `false` for the recorded local Matter-over-Thread setup |
| `beta` | Keep `false`; inherited upstream beta mode is unvalidated |
| `network_device` | Leave unset; network-attached radios are rejected |

At startup the app resets only the selected debugger, enables the onboard
antenna, verifies its registers, then starts OTBR. It does not erase flash or
factory-reset the Thread network. A failed antenna step deliberately prevents
radio startup. USB access is required in addition to the serial device.

## Home Assistant discovery

Start the app and accept the discovered **Open Thread Border Router** integration.
Use **Thread** to select/synchronize the network credentials and **Matter** with
the official Matter Server app to commission devices through the Companion app.
No custom Home Assistant integration is required.

The app advertises its internal REST URL. If manual setup is necessary, use its
actual base URL `http://APP_INTERNAL_IP:8081`; `/node/state` is a useful diagnostic
endpoint, not part of the base URL. Do not use the Home Assistant frontend port.

Keep web/REST port mappings disabled by default. Exposing them grants network
management access without a Home Assistant login. The web interface is optional
and should not be used to form a replacement network in an existing home.

## Updates and recovery

The existing local app identity is `local_xiao_otbr_patch`. Keep its directory,
slug and persistent data when updating. Installing from a hosted repository
creates a different repository-prefixed ID and needs deliberate data migration.

If startup fails, inspect this app's and Supervisor's logs. Confirm the selected
device, matching firmware/baudrate and that only one OTBR app is running. Restore
the previous app backup/source if needed; do not delete the Thread integration
or reset end devices as an app-update workaround.
