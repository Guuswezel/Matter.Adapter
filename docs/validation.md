# Consolidation validation — 2026-11-17

Candidate: **3.2.16**, experimental. The deployed Raspberry Pi was not changed.

| Check | Result |
| --- | --- |
| ARM64 Docker build | Passed using pinned OTBR 3.4.0 digest and verified Arduino OpenOCD archive |
| Container smoke checks | Passed: native OpenOCD runs, MG24 target file exists, real migration dependencies import, licenses/notices present |
| Python regression tests | 15 passed; mocked USB/network, no physical device access |
| Antenna Tcl tests | Passed: correct debugger serial, allowed non-secure registers, preservation of unrelated pins, repeat initialization, readback failure, missing/invalid serial rejection |
| Optional automation examples | 16 schedule boundary/restart scenarios passed, including 2400 K normal state |
| Repository checks | YAML/metadata, relative documentation links and private/generated artifact exclusions passed |
| Shell checks | All service entry points pass Bash syntax; ShellCheck passes maintained helper/test entry points |
| Firmware downloads | Both upstream application and optional bootloader GBL downloaded afresh; hashes match manifest |

Locally built image ID (not a published registry digest):
`sha256:523349491f51b0f6e4c98e1e2fd340a867a36000dc87b6fb85cf46dbbf5e7f8f`.

The Mac's default Python is older than the required version. Full `make test`
used Python from the built runtime while Ruby/Tcl checks ran on the host:

```sh
make test PYTHON='docker run --rm --entrypoint python3 -v "$(CURDIR):/repo:ro" -w /repo xiao-otbr:3.2.16'
make image container-test
```

Not performed: live app update, physical flash, cold boot, sustained Thread/Matter
traffic on the candidate, a full 24-hour run, hosted-repository migration, or
execution on GitHub Actions. Those remain explicit release tasks in the
[maintainer guide](maintenance.md). Earlier 3.2.15 hardware evidence is recorded
separately in [compatibility](compatibility.md).
