# wifi_qrcode
Generate WiFi Access QR Codes

# Installation

```bash
pip install -U wifi_qrcode
```

# Usage example

```bash
wifi_qrcode --ssid MYWIRELESSNETWORK --auth WPA --password SECRET
```

or as python module

```bash
python -m wifi_qrcode wifi --ssid MYWIRELESSNETWORK --auth WPA --password SECRET
python -m wifi_qrcode mailto --to user@mail.org --subject "Mail from QR"
```

# Arguments

## Required

* `--ssid` Network SSID

## Optional

* `--auth` Authentication type; can be WEP or WPA, or 'nopass' for no password;
* `--password` Password, ignored if `--auth` is "nopass";
* `--hidden` True if the network SSID is hidden;
* `--output` QR-code file. Can be with PNG or SVG extension.
