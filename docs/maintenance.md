# Maintainer guide

## Scope and current state

Maintain one focused app repository: pinned XIAO RCP artifacts, an OTBR overlay
and HA integration/recovery documentation. Home Assistant supplies Matter Server
and the Thread/Matter integrations. Avoid maintaining a parallel HA integration
or an untracked fork of the firmware SDK.

Hardware-tested baseline: custom app 3.2.15, 2026-11-15. Consolidated candidate:
3.2.16, experimental. The repository records reproducible inputs, not a guarantee
of byte-identical images: Debian package indexes/security updates remain live.
Record the resulting image digest and installed packages when releasing.

## Local checks

```sh
make test
make image container-test
```

Requires Python 3.11+, Ruby, Tcl, Bash, Git and Docker. Python unit tests use only
the standard library. If the Mac's `python3` is older, use a current interpreter
through `make test PYTHON=/path/to/python3.13`, or run source checks individually
and `make container-test` for Python checks in the actual runtime.

Checks cover board selection/mismatches, antenna register writes and unrelated
pin preservation, fresh-install probe avoidance, existing settings preservation,
migration backup, modem-line assertion, verified-download replacement, app YAML
and relative links. The image check imports real migration dependencies and
executes the shipped OpenOCD without USB access. None of these proves Thread
radio reliability.

GitHub Actions repeats source checks and builds/tests the ARM64 image natively.
Workflows have read-only permissions and do not publish images, access devices
or deploy to a home. Dependency updates arrive as reviewable pull requests.

## Dependency updates

- Compare the copied app overlay against Home Assistant upstream, starting at
  the revision recorded in [THIRD_PARTY.md](../THIRD_PARTY.md). Review service
  ordering, discovery, firewall cleanup and migration behaviour together.
- Update the OTBR tag **and** immutable digest in Dockerfile. Review changes to
  Python APIs and OTBR UART options; run image checks before hardware tests.
- Update OpenOCD URL/hash only from the official Arduino package index. Keep
  the target config and ARM64 executable check. Add architecture support only
  with the matching native debugger and hardware validation.
- Firmware changes update `firmware/manifest.json`, including the release,
  application hash and transport settings. Obtain the artifact from its
  publisher, compare board build configuration, preserve a readback, then test.
- Keep inherited `beta` false and network radios unsupported in the release
  baseline. Removing inherited options requires a configuration migration.

## Hardware release gate

Before publishing or recommending a runtime/firmware candidate:

- [ ] Save/download a HA backup including OTBR and Matter Server; retain prior source/image.
- [ ] Verify only one OTBR app runs and its full ID/data directory are unchanged.
- [ ] Confirm firmware/USB identity, baudrate and DTR/RTS settings.
- [ ] Cold-start: disconnect/reconnect radio power, start app, verify antenna readback.
- [ ] Confirm the original Thread dataset/network and Matter devices remain intact.
- [ ] Test actual bulb on/off and colour controls with fresh state verification; restore prior state.
- [ ] Run sustained fresh reads, record duration, sample count, failures and latency distribution.
- [ ] Restart app and host separately; repeat radio and Matter availability checks.
- [ ] Test a battery device after waking it; separate sensor issues from router health.
- [ ] Check logs for Spinel timeouts, TX recovery, partition changes and SMU faults.
- [ ] Leave the candidate running for at least 24 hours; inspect recovery after a transient USB interruption.
- [ ] Demonstrate rollback to the prior app/firmware without recommissioning devices.
- [ ] Record the exact hardware, versions, image digest, results and remaining limitations.

3.2.15 passed a short sustained-read/control test and app restart, not this entire
expanded gate. Keep 3.2.16 experimental until its own results are recorded. Do
not infer long-term stability from the older short test.

## Versioning and publishing

Keep the app slug `xiao_otbr_patch`. Increment the three-part version in
`config.yaml`, Makefile's default image tag and the app changelog together.
Use `breaking_versions` for changes requiring user intervention. Document any
firmware/serial/data migration and its rollback before releasing it.

When the owner chooses a Git host/repository, add its real URL to `repository.yaml`
and the app homepage, enable branch protection and private vulnerability reports,
and require the CI jobs before merging. Add CODEOWNERS only with actual account
handles. Do not use placeholder remotes, contacts or fake install badges.

After the hardware gate, create an annotated version tag matching the app
version and publish release notes with checksums, compatibility, migration and
rollback. Keep third-party notices and corresponding source available if
publishing container images. No automated workflow publishes releases today.

Moving Local apps users to a Git-hosted repository changes the repository prefix
of the full app ID. Validate a separate backed-up data migration before asking
existing users to switch. A matching short slug does not solve that change.

## Next work

1. Run the consolidated 3.2.16 candidate through the hardware gate on a planned maintenance window.
2. Build RCP firmware with PB4/PB5 initialization in firmware and validate cold-start/recovery, to remove the debugger workaround.
3. Test backup/restore migration from Local apps to a hosted repository.
4. Add a second physical XIAO/host to broaden evidence before supporting more architectures.
