# Cross-Platform Gigabyte Monitor Configuration In Python

## Introduction

A script to configure Gigabyte monitor attributes (brightness, contrast, kvm switch, etc...) without bloatware.

## Usage
```text
usage: monitor.py [-h] [-b [0-100]] [-c [0-100]] [-s [0-10]] [-lb [0-10]] [-kvm [0-1]] [-cm [0-3]] [--rgb-red [0-100]] [--rgb-green [0-100]]
                  [--rgb-blue [0-100]]

Set properties of gigabyte monitors.

options:
  -h, --help            show this help message and exit
  -b [0-100], --brightness [0-100]
  -c [0-100], --contrast [0-100]
  -s [0-10], --sharpness [0-10]
  -lb [0-10], --low-blue-light [0-10]
  -kvm [0-1], --kvm-switch [0-1]
  -cm [0-3], --color-mode [0-3]
  --rgb-red [0-100]
  --rgb-green [0-100]
  --rgb-blue [0-100]
```

## Dependencies
* [pyhidapi](https://github.com/apmorton/pyhidapi) (Make sure to install the hidapi shared library)

## Caveats
- Was only tested under macOS, with a M34WQ monitor.
- The supplied script supports only writing attributes and not reading them.
- Only works from the currently active KVM input device.

## Credits
The script is based on the following works:
- @kelvie at https://github.com/kelvie/gbmonctl
- @P403n1x87 at https://github.com/P403n1x87/m27q
- @MarekPrzydanek at https://github.com/MarekPrzydanek/GigabyteMonitorController
- @WildFireFlum at https://github.com/WildFireFlum/gbmonitor