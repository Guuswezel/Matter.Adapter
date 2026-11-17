# Reuse upstream binaries: compiling OpenThread exhausts a 2 GB Pi.
FROM ghcr.io/home-assistant/app-openthread-border-router:3.4.0@sha256:d2fd3bd186c51a967e9222a6a903308b6b93455c5e093f5a0adfb76c01b94b23
RUN test "$(dpkg --print-architecture)" = arm64 \
    && apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates curl bzip2 libatomic1 \
    && curl --fail --location --retry 3 \
        https://downloads.arduino.cc/tools/openocd-0.12.0-arduino1-static-aarch64-linux-gnu.tar.bz2 \
        --output /tmp/openocd.tar.bz2 \
    && echo 'd6d78fb9f422647a7606213925f037593e5dbd6ad4d6670c3a54ab9ec1cc0cd1  /tmp/openocd.tar.bz2' | sha256sum -c - \
    && mkdir -p /opt/openocd \
    && tar -xjf /tmp/openocd.tar.bz2 -C /opt/openocd --strip-components=1 \
    && rm /tmp/openocd.tar.bz2 \
    && rm -rf /var/lib/apt/lists/*
COPY rootfs /
COPY LICENSE OPENOCD-LICENSE NOTICE /usr/share/doc/xiao-otbr/
