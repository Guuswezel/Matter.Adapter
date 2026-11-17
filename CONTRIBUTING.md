# Contributing

Open an issue describing the device, versions, observed behaviour and a
reproduction. Distinguish fresh device responses from cached Home Assistant
state. Report security-sensitive details privately where the hosting platform
supports it; see [SECURITY.md](SECURITY.md).

Keep the project focused on the XIAO MG24 RCP and its HAOS OTBR app. Make small
changes, preserve deployment data and add a regression test for changed radio,
startup, migration or download logic. Run:

```sh
make test
make image container-test
```

Python 3.11+ is required. No Python package installation is needed for the unit
tests. Container tests check the actual Python dependencies from the base image.
Tests never open a physical radio, flash firmware or contact Home Assistant.

Changes to the RCP image, serial settings, antenna sequence, app identity or
upstream runtime need the [hardware release checklist](docs/maintenance.md),
including recovery evidence. A successful build is not a hardware test.

Use the existing Apache-2.0 license for original contributions and retain
upstream attribution. Do not add private flash dumps, HA backups, network
datasets, signed firmware keys or vendored binary tools to Git.
