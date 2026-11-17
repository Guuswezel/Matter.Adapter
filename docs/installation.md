# Installation and Home Assistant integration

## Before installing

Use the [supported configuration](compatibility.md). Home Assistant OS must
have working local IPv6 and multicast connectivity. Connect the XIAO to the
host with a USB data cable; a short extension helps move it away from the Pi
and USB 3 interference. A Mac VM requires USB passthrough and bridged networking;
the supported maintenance target is the Raspberry Pi installation.

If this is an existing home, first create and download a Home Assistant backup
including Matter Server, Thread and the current OTBR app. Preserve backup
encryption credentials separately. Stop the stock OpenThread Border Router app
and disable its watchdog and start-on-boot. Run only one OTBR app on this host.
Do not delete the existing integration or form another Thread network.

## Install from this checkout

Until this repository is published, use the local-app workflow:

1. Make the Home Assistant local apps directory available over Samba or SSH.
   It is `/local_apps` on the recorded HAOS installation. Older installations
   may expose `/addons`; use the actual directory shown by your SSH/Samba app.
2. Copy the entire `xiao_otbr_patch` directory there, including `Dockerfile`,
   `.dockerignore`, `rootfs` and service dependency marker files. Preserve
   executable modes. For SSH with legacy SCP support:

   ```sh
   scp -O -r -P YOUR_SSH_PORT xiao_otbr_patch root@YOUR_HA_IP:/local_apps/
   ```

3. In **Settings → Apps → Install app**, check for updates/reload the store.
   Install **XIAO MG24 Thread Border Router** from Local apps.
4. Wait for the image build to finish. It downloads existing binaries and adds
   OpenOCD; it does not compile OpenThread on the Pi. See Supervisor logs if
   the progress dialog stays at 0%.

For the existing `local_xiao_otbr_patch` installation, update its existing source
directory and rebuild/update that app. Retaining the folder/slug and its app
data avoids creating a second empty app. Back up the old source before copying.

After publishing to a Git host, users can instead add the repository's actual
clone URL under **App store → Repositories**. The root `repository.yaml` and
`xiao_otbr_patch/config.yaml` provide repository discovery. No hosted URL is
configured in this local checkout.

**A Git repository install has a different full app ID from a Local apps install.**
It receives a repository prefix instead of `local_`. Treat moving an existing
installation to a hosted repository as an explicit app-data migration, not an
in-place update. Keep using the local app until migration and rollback are tested.

## Configure the radio

Select the actual stable `/dev/serial/by-id/usb-Seeed_Studio_...CMSIS-DAP_...-if02`
device from the app's configuration. The example below contains placeholders:

```yaml
device: /dev/serial/by-id/YOUR_XIAO_DEVICE
adapter_serial: ""
baudrate: "460800"
flow_control: false
otbr_log_level: notice
firewall: true
nat64: false
beta: false
```

With a recognized XIAO by-id path, leave `adapter_serial` empty: the app derives
the debugger serial from that device. For a numbered `/dev/ttyACM*` path, enter
the same board's CMSIS-DAP USB serial explicitly. A disagreement with the by-id
path is rejected. Do not paste a serial from another board.

The backbone interface defaults to the host's primary interface. If necessary,
set `backbone_interface` to the real Ethernet interface, such as `end0`. Leave
`network_device` unset and `beta` false; these inherited options are not part of
the supported XIAO configuration. Keep the REST and web ports disabled initially.

Start the app. Logs must show the onboard antenna verification succeeded, the
migration step completed/skipped, and `otbr-agent` started without Spinel failures.
Enable start-on-boot and watchdog only after this works.

## Connect Home Assistant

1. Under **Settings → Devices & services**, accept the discovered **Open Thread
   Border Router** integration. The app sends its internal REST URL to Supervisor
   discovery; prefer this over guessing an IP address.
2. If a manual URL is requested, inspect the app logs/discovery information.
   From the SSH app you can test the app's current address using
   `curl http://APP_INTERNAL_IP:8081/node/state`. Use the base URL
   `http://APP_INTERNAL_IP:8081` in the integration. Internal addresses can differ
   between installations. Port 8081 is a REST API, not the HA web port.
3. Open the **Thread** integration. For an existing installation, verify the
   existing network is still preferred and credentials are present. For a first
   installation, configure the Home Assistant Thread network there.
4. Install/start the official **Matter Server** app and configure the **Matter**
   integration if they are not present already.
5. In the Home Assistant Companion app on your phone, synchronize the preferred
   Thread credentials using its Thread configuration flow, then use
   **Add Matter device** to commission a new device. The phone needs local
   connectivity and Bluetooth permissions. Existing devices do not need resetting.

For Alexa, share a commissioned device through Home Assistant's Matter device
page to obtain a temporary pairing code, then add that existing Matter device
in Alexa. Codes expire. Alexa sharing does not turn this XIAO into an independent
border router; the host must continue running unless another border router
actually joins the same Thread network.

Official references: [app repositories](https://contributors.home-assistant.io/apps/guides/repository/),
[Thread integration](https://www.home-assistant.io/integrations/thread/),
[Matter integration](https://www.home-assistant.io/integrations/matter/).
