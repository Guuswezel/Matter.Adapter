# Home Assistant schedules

These optional household examples are separate from the radio app. They are
not installed automatically; replace the example entity IDs with your own.
The source configuration is in `examples/homeassistant/automations.yaml` and
`examples/homeassistant/scripts.yaml`. Times use Home Assistant's `Europe/Berlin`
timezone; sunrise and sunset use its configured home location.

| Device | Schedule |
| --- | --- |
| Aquarium Luft | On daily at 17:00, off at 17:15 |
| Aquarium Light | On at sunrise, off at sunset |
| Weihnachts Stern | On at sunset, 2400 K at 70% brightness, off at 23:00 |
| Star light show | 20:00–20:30, after sunset; returns to 2400 K at 20:30 |

The show alternates smooth colour sweeps, golden brightness twinkles and
slow colour pops. Switching the star off manually stops the show. In summer,
the show waits for sunset and is skipped if sunset is after 20:30.

The automations reconcile their schedules on Home Assistant startup and when
each device recovers from being unavailable. The air pump uses separate on/off
times so restarting Home Assistant cannot cancel a pending 15-minute delay.

The Pi also has a user-created TIMMERFLOTTE battery notification automation.
Preserve it when merging these three automations into `/config/automations.yaml`;
the local file contains only the three schedules. Likewise, preserve any other
scripts when merging `/config/scripts.yaml`.

Original configuration backup on the Pi:
`/config/manual_backups/2026-11-15-before-schedules-1828/`.

Run local boundary checks with `ruby tools/test_homeassistant_schedules.rb`.
After merging changes on the Pi, run `ha core check --no-progress` before
reloading scripts and automations in Home Assistant, or restarting its Core.

Installed on 2026-11-15. Home Assistant's configuration check passed, Core
restarted successfully, and all three automation entities registered without
being disabled. Fresh Matter reads after startup confirmed the evening states:
star on in colour-temperature mode at 416 mired (approximately 2400 K), aquarium
light off, and air pump off. The complete scheduled show has not yet run.
