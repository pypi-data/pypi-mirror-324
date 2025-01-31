#!/bin/bash
# runtime, skd, and base has to be installed, see net.boxyfoxy.net.OptimaLab35.json
# uses [flatpak-pip-generator](https://github.com/flatpak/flatpak-builder-tools/tree/master/pip) to download and build all dependency from pip
python flatpak-pip-generator --runtime='org.kde.Sdk//6.8' piexif pillow optima35 PyYAML hatchling
flatpak-builder --user --install flatpak-build-dir net.boxyfoxy.OptimaLab35.json --force-clean
