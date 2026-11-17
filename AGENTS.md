# Repository maintenance

- Read README.md, docs/architecture.md and docs/maintenance.md before changing runtime behaviour.
- The live Home Assistant host is outside this repository. Do not deploy, reboot,
  flash or control physical devices merely to prepare/review source changes.
  Hardware operations require a task that authorizes them.
- Preserve `xiao_otbr_patch` and existing deployment data. A repository-prefix
  change is an app-data migration; changing a folder name is not a safe migration.
- Never add private flash dumps, Thread datasets, Matter fabric storage, pairing
  codes, HA backups, local IP inventories, credentials or tool binaries to Git.
- Use non-secure GPIO aliases only. Preserve unrelated pins and antenna readback
  checks. Keep DTR/RTS assertion independent of hardware flow control.
- Pin firmware/download hashes and the OTBR base image digest. Do not substitute
  a new upstream version and call it tested without the hardware release checks.
- Run `make test` and `make image container-test` for runtime/build changes.
  Use Python 3.11+. Keep optional household examples outside the app.
- Record what was tested, what was not, and the rollback path. Do not publish
  images or Git releases as a side effect of local validation.
