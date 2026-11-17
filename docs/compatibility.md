# Supported configuration

| Component | Recorded working baseline, 2026-11-15 |
| --- | --- |
| Radio board | Seeed Studio XIAO MG24 (Sense), EFR32MG24B220F1536IM48, onboard CMSIS-DAP |
| Host | Raspberry Pi 4, 2 GB, 64-bit Home Assistant OS 18.5 |
| Home Assistant Core / Supervisor | 2026.11.1 / 2026.11.0 |
| Deployed custom app | 3.2.15, local slug `local_xiao_otbr_patch` |
| Repository candidate | 3.2.16, experimental; not yet deployed to that host |
| OTBR base image | Home Assistant OTBR 3.4.0; immutable index digest in Dockerfile |
| RCP firmware | Community release 20250627, `2.5.3.0_GitHub-1fceb225b` |
| Serial | 460800 baud, hardware flow control disabled, modem lines asserted |
| Antenna | PB5 high powers RF switch; PB4 low selects onboard antenna |

The configured Core minimum is inherited from the upstream app; it is not a
claim that every version from that minimum has been tested. Start with the
recorded baseline. Other XIAO models, ESP32 boards, generic MG24 boards, TCP
radios and amd64 hosts are outside this support boundary. The bundled OpenOCD
download is ARM64-only, so the app does not advertise amd64 compatibility.

The vendor Arduino RCP 2.6.1.0 at 115200 baud was used earlier but had repeated
transmit failures in this deployment. The working alternative is older; it is
not advertised as the latest vendor firmware. Host-side antenna initialization
is still required for the pinned alternative.

After enabling the antenna on app 3.2.15, 72 sustained fresh bulb reads passed
with zero failures, median 77–78 ms and maximum 183 ms, across a controlled app
restart. Six verified off/on commands passed in 186–284 ms. Two KAJPLATS bulbs
were reachable. Later commissioning also added GRILLPLATS plugs and a third
KAJPLATS bulb. The original TIMMERFLOTTE pairing was unavailable during the
radio repair; its recovery is not covered by that validation result.

This is evidence for one installation over a short observation window, not a
multi-day reliability claim or a certified commercial border router.
