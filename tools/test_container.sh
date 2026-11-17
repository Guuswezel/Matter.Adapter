#!/usr/bin/env bash
# Run inside the built image; never starts OTBR or accesses USB.
set -euo pipefail
test "$(dpkg --print-architecture)" = arm64
/opt/openocd/bin/openocd --version
test -f /opt/openocd/share/openocd/scripts/target/efm32s2_g23.cfg
test -x /usr/local/bin/xiao-antenna-init
test -s /usr/share/doc/xiao-otbr/LICENSE
test -s /usr/share/doc/xiao-otbr/OPENOCD-LICENSE
test -s /usr/share/doc/xiao-otbr/NOTICE
python3 - <<'PY'
import runpy
module = runpy.run_path('/usr/local/bin/migrate_otbr_settings.py', run_name='smoke_test')
assert module['PinState'].HIGH is not None
print('Migration imports resolved against real container dependencies')
PY
python3 -m unittest discover -s /repo/tests -v
