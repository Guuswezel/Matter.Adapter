# Third-party provenance and licenses

Original project code/documentation is Apache-2.0; see [LICENSE](LICENSE).
That license does not relicense independently distributed firmware or tools.

| Component | Pinned input and source | License / handling |
| --- | --- | --- |
| HA OTBR app overlay | [home-assistant/addons at ceb80015bed5531ff15b969457804f6cf91eef47](https://github.com/home-assistant/addons/tree/ceb80015bed5531ff15b969457804f6cf91eef47/openthread_border_router) | Apache-2.0; adapted service/migration files retained in `xiao_otbr_patch` |
| OTBR runtime image | [Home Assistant OTBR app](https://github.com/home-assistant/app-openthread-border-router), tag 3.4.0 | Upstream image and its dependencies retain their licenses; immutable image index digest below |
| OpenThread / OTBR | [openthread/ot-br-posix](https://github.com/openthread/ot-br-posix) | BSD-3-Clause for OTBR; inspect upstream image for dependency notices |
| Arduino OpenOCD | Official [Arduino package index](https://downloads.arduino.cc/packages/package_index.json), `0.12.0-arduino1-static`, ARM64 | GPL-2.0-or-later; downloaded during build, not committed as a binary |
| Community XIAO firmware | [darkxst/silabs-firmware-builder release 20250627](https://github.com/darkxst/silabs-firmware-builder/releases/tag/20250627) | Upstream firmware/SDK terms apply; download by manifest hash, no binary redistribution here |

Home Assistant runtime image index SHA-256:
`d2fd3bd186c51a967e9222a6a903308b6b93455c5e093f5a0adfb76c01b94b23`.

Official Arduino OpenOCD archive:
`https://downloads.arduino.cc/tools/openocd-0.12.0-arduino1-static-aarch64-linux-gnu.tar.bz2`

Archive SHA-256:
`d6d78fb9f422647a7606213925f037593e5dbd6ad4d6670c3a54ab9ec1cc0cd1`.

The firmware's full filenames and GBL/extracted-HEX hashes are in
[firmware/manifest.json](firmware/manifest.json). Downloading an upstream artifact
does not make it an original work of this project. Follow its publisher's
license terms when using or distributing it.

The image includes OpenOCD, so redistributors of built images must satisfy its
GPL notice/source obligations in addition to the upstream runtime's notices.
Its reported Git revision resolves to
[Arduino OpenOCD 21fa2de702699ff647a5fc118718884b5d9f28fd](https://github.com/arduino/OpenOCD/tree/21fa2de702699ff647a5fc118718884b5d9f28fd).
The image carries the project license, OpenOCD license and provenance NOTICE
under `/usr/share/doc/xiao-otbr/`.
Retain the original license files and provide the matching corresponding
source/build information from the Arduino OpenOCD distribution. This repository
does not automatically publish binary images or claim their licenses are all
Apache-2.0.
