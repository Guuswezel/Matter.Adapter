# Troubleshooting and rollback

First record the app, RCP, Core, Supervisor and OS versions and the selected
serial path. Preserve Thread/Matter data. A failed new firmware or app build is
not a reason to delete a network or factory-reset commissioned devices.

| Symptom | Check and next action |
| --- | --- |
| App absent from store | Repository root has `repository.yaml`; copied app includes `config.yaml` and Dockerfile. Reload the store and inspect Supervisor logs. |
| Install stays at 0% | Read Supervisor build logs. This app downloads binaries; if logs show OpenThread compilation, the wrong Dockerfile is being built. Check free storage and outbound network access. |
| CMSIS-DAP open fails | Confirm USB data cable, correct host/passthrough, app USB access and selected serial. Close Arduino IDE/debug sessions and other processes using the debugger. |
| Adapter serial disagreement | Choose the stable by-id path or correct `adapter_serial`; do not bypass the guard to reset another board. |
| Antenna verification fails | Stop. Inspect the configured non-secure aliases and OpenOCD output. Never substitute secure `0x4003...` aliases. |
| Spinel timeout / `Init()` failure | Confirm pinned RCP image, 460800 baud, flow control false and asserted modem lines. Stop competing OTBR apps. Power-cycle only the radio, then restart this app. |
| Firewall chain already exists | Two OTBR apps may be active, or a previous crash left rules behind. Stop both cleanly and start only the intended app. Avoid broad firewall flushing. |
| Weak signal / transmit timeouts | Confirm antenna initialization first. Move radio away from Pi/USB 3 on an extension cable; compare fresh Matter reads and control latency. |
| REST API cannot connect | Ensure app is running. Use its discovered internal base URL on port 8081, not the HA web address. Keep unauthenticated REST off the LAN unless needed temporarily. |
| Devices disappeared after changing install source | Repository prefix changes full app identity and data directory. Restore the existing local app and backup; do not commission devices into a new dataset. |
| Only a battery sensor is unavailable | Wake it without resetting, inspect battery/display and test again. Diagnose the sensor separately if fresh bulb controls are reliable. |

## Useful commands

Run these inside Terminal & SSH; replace `APP_SLUG` with the full installed ID
(the original local deployment is `local_xiao_otbr_patch`):

```sh
ha apps info APP_SLUG
ha apps logs APP_SLUG
ha apps logs core_matter_server
ha supervisor logs
curl --fail http://APP_INTERNAL_IP:8081/node/state
```

The REST state should be a working Thread role (`router` or `leader`), not
persistently `disabled` or `detached`. A running process alone does not prove
radio health. Check fresh Matter attribute reads and actual device controls;
cached HA state is insufficient.

## Rollback

Before upgrading, save the app's source and a downloaded HA backup that includes
both OTBR and Matter Server. If an app-only change fails, stop the candidate,
restore the prior source/version and app backup as needed, rebuild, and start
only that app. Confirm the original Thread network is still preferred and devices
are reachable. Keep the stock OTBR app disabled throughout this rollback.

If firmware was changed, follow [firmware recovery](firmware.md), using the
private pre-flash readback and matching serial settings. A full chip restore
also restores device storage from the backup; use it deliberately on the same
board. Keep the baseline app and original bootloader until recovery is proven.

When reporting a problem, use the repository's bug template and redact datasets,
Wi-Fi credentials, Matter setup codes, access tokens, precise location and HA
backup contents. Share fresh relevant logs with timestamps and versions.
