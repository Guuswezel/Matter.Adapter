PYTHON ?= python3
IMAGE ?= xiao-otbr:3.2.16

.PHONY: test test-python image container-test firmware
test:
	ruby tools/check_repository.rb
	tclsh tools/test_xiao_antenna.tcl
	ruby tools/test_homeassistant_schedules.rb
	$(MAKE) test-python
	bash -n xiao_otbr_patch/rootfs/usr/local/bin/xiao-antenna-init tools/test_container.sh

test-python:
	$(PYTHON) -m unittest discover -s tests -v

image:
	docker build --platform linux/arm64 -t $(IMAGE) xiao_otbr_patch

container-test:
	docker run --rm --platform linux/arm64 --entrypoint /bin/bash -v "$(CURDIR):/repo:ro" $(IMAGE) /repo/tools/test_container.sh

firmware:
	$(PYTHON) tools/fetch_firmware.py
